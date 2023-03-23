import pandas as pd 
import os
import ast
from sqlalchemy import create_engine
import json
from multiprocessing.pool import ThreadPool as Pool
import time
import os

import logging
from lib.mongo_utils import mongo_conn,mongo_row_count,extract_id
from lib.mysql_utils import mysql_conn,check_table_existence,execute_query,dump_
from dotenv import load_dotenv
load_dotenv()

mongo_db       = os.getenv('MONGO_DB')
mongo_user     = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_host     = os.getenv('MONGO_HOST')

mysql_host     = os.getenv('MYSQL_HOST')
mysql_user     = os.getenv('MYSQL_USER')
mysql_db       = os.getenv('MYSQL_DB')
mysql_password = os.getenv('MYSQL_PASSWORD')


def load_json(file_name):
    '''Function for json load'''
    try:
        with open(file_name) as f:
            read = f.read()
            json_load = json.loads(read)
            return json_load
    except Exception as e:
        # logger.error(str(e))
        raise Exception(str(e))

def generate_df(lines):
    '''Function for generate pandas dataframes'''
    try:
        df = pd.DataFrame(lines)
        types=df.dtypes
        head=df.columns
        return(df,types,head)
    except Exception as e:
        # logger.error(str(e))
        raise Exception(str(e))

def list_to_string(s):
    try:
        str1 = " "
        return (str1.join(s))
    except Exception as e:
        raise Exception(str(e))

def replace_qoutes(df):
    '''Function for replace single qoutes into double qoutes'''
    try:
        for i in df.columns:
            df[i]=df[i].astype('string').str.replace("'",'"',regex=False)
            return df[i]
    except Exception as e:
        # logger.error(str(e))
        raise Exception(str(e))

def change_dtype(types):
    '''Function for change datatypes'''
    try:
        types_list=[]
        for t in types:
            if t == 'O':
                t='char(100)'
            elif t == 'float64':
                t='char(100)'
            elif t == 'int64':
                t='char(100)'
            else:
                t='char(100)'
            types_list.append(t)
        return types_list
    except Exception as e:
        raise Exception(str(e))

def query_formating(head, types_list):
    '''Function for generate query field value'''
    try:
        list_fields_value=[]
        for col, typ in zip(head, types_list):
            field_value=col, typ
            list_fields_value.append(field_value)
        field_value_list=[]
        for i in list_fields_value:
            key=i[0]
            value=i[1]
            field_val="`"+str(key)+"`"+' '+str(value)
            field_value_list.append(field_val+",")
        field_value_list=field_value_list[-1:] + field_value_list[:-1]
        query_list = ' '.join(map(str, field_value_list))
        query_list=query_list[:-1]
        
        return(query_list,field_value_list)
    except Exception as e:
        # logger.error(str(e))
        raise Exception(str(e))

def column_check_list(field_value_list,head_list,logger):
    '''Function for get diffrence of query field of each batch'''
    try:
        copy_list=[] #copy of filed_value_list
        copy_list=field_value_list
        diffrence=set(copy_list).difference(set(head_list))
        diffrence=list(diffrence)
        query_str = 'add column'
        alter_list=[ query_str +" "+ s for s in diffrence]
        alter_list = list_to_string(alter_list)
        alter_list=alter_list[:-1]
        return(alter_list,diffrence,field_value_list,copy_list)
    except Exception as e:
        # logger.error(str(e))
        raise Exception(str(e))

def update_column_check_list(copy_list,logger):
    '''Function for update field value list in each batch'''
    try:
        for i in copy_list:
            if i in column_list:
                pass 
            else:
                column_list.append(i)
    except Exception as e:
        # logger.error(str(e))
        raise Exception(str(e))

def check_count(table_name,cur,logger):
    '''Function for compare table row count'''
    try:
        mongo_count = mongo_row_count(table_name,logger,db)
        cur.execute(f'''SELECT COUNT(*) FROM {table_name};''')
        sql_count = cur.fetchone()[0]
        return(sql_count,mongo_count)
    except Exception as e:
        raise Exception(str(e))

def mongo_to_mysql(table_name,connection,logger):
    '''Main function for mongoDB to MYSQL datamigration '''
    try:
        skip=0
        count = mongo_row_count(table_name,logger,db)
        while skip<count:
            cur = connection.cursor()
            file_name = table_name + "export.json"
            os.system(f"""mongoexport -d={mongo_db} -c={table_name}  --limit=100000 --skip={skip} --out={file_name} --jsonArray""")
            json_load = load_json(file_name)
            lines = ast.literal_eval(str(json_load))
            df,types,head = generate_df(lines)
            df['_id'] = df['_id'].apply(extract_id)
            replace_qoutes(df)
            types_list = change_dtype(types)    
            query_list,field_value_list = query_formating(head, types_list)
            alter_list,diffrence,field_value_list,copy_list = column_check_list(field_value_list,column_list,logger)
            result = check_table_existence(cur,table_name,logger)
            create = '''create table if not exists  `{}` ({},PRIMARY KEY (_id));'''.format(table_name,query_list)
            update = '''ALTER TABLE  `{}` {} ;'''.format(table_name,alter_list)
            try:
                if not result:
                    execute_query(cur,create,logger)
                    dump_(df,table_name,engine,logger)

                else:
                    try:
                        if (len(diffrence)!=0) and (column_list not in [set()]):
                            execute_query(cur,update,logger)
                            dump_(df,table_name,engine,logger)
                        else:
                            dump_(df,table_name,engine,logger)
                    except Exception as e:
                        logger.error(str(e))
            except Exception as e:
                logger.error(str(e))
            update_column_check_list(copy_list,logger)
            mongo_count,sql_count = check_count(table_name,cur,logger)
            try:
                if mongo_count == sql_count:
                    logger.info("row counts are eqal")
                else:
                    logger.info("row counts not eqal")
            except Exception as e:
                logger.error(str(e)) 

            # time.sleep(2)
            cur.close()
            skip += 100000
    except Exception as e:
        logger.error(str(e))

if __name__ == "__main__":
    try:
        column_list=[]  #table field value list for comparing each batch
        logging.basicConfig(filename='mongo_to_mysql_script.log',level=logging.ERROR,filemode='w')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        conn = mongo_conn(logger)
        db = conn[mongo_db]
        thread_pool_size = 3 # Number of python threads
        thread_pool = Pool(thread_pool_size)
        collections = db.list_collection_names()
        # connection,engine = mysql_conn()
        logger.info(collections)
        for collection in collections:
            logger.info(collection)
            time.sleep(2)
            connection,engine = mysql_conn()
            thread_pool.apply_async(mongo_to_mysql,(collection,connection,logger,))
        thread_pool.close()
        thread_pool.join()
    except Exception as e:
        logger.error(str(e))
