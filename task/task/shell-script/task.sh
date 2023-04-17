#! /bin/bash
#! /bin/bash

filename='test.txt'
truncate -s 0 data.txt
declare -a arr[]
declare -a arr1[]

(cat test.txt | grep -A3 "Test Suites:") >> data.txt #ith with out fileil k kodukkathe koduthal get our actul output
#cat data.txt | grep -Eo '[0-9]{1,4}' data.txt

cat data.txt


#take values from first line
var1=$(cat data.txt |sed -n 1p| grep -Eo '[0-9]{1,4}')
#echo "$var1"
n=0
for i in "$var1"
do 
#echo "$i"
arr[n]="$i"
done
a=(${arr[0]})
for i in "${arr[@]}"
do
    y=${i:0:1}
    ts_passed=$y
  # echo $y 
done

for i in "${arr[@]}"
do
    y=${i:2:2}
    ts_total=$y
   # echo $y 
done
for i in "${arr[@]}"
do
    y=${i:3:3}
    ts_fail=$y
   # echo $y 
done

#take values from second line
var2=$(cat data.txt |sed -n 2p| grep -Eo '[0-9]{1,4}')
#echo "$var2"
for i in "$var2"
do 
#echo "$i"
arr1[n]="$i"
done
a=(${arr[0]})
for i in "${arr1[@]}"
do
    y=${i:0:1}
    t_passed=$y
   # echo $y 
done

for i in "${arr1[@]}"
do
    y=${i:2:2}
    t_total=$y
   # echo $y 
done
for i in "${arr1[@]}"
do
    y=${i:3:3}
    t_fail=$y
   # echo $y 
done
snapshots=$(cat data.txt |sed -n 3p| grep -Eo '[0-9]{1,4}')

Time=$(cat data.txt |sed -n 4p| grep -Eo '[0-9]{1,4}[\.?]+[0-9]{1,4}'
