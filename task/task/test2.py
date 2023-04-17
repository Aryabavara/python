def donuts(count):
  if count >=10: 
   result='Number of donuts: many'
  else:
    result='Number of donuts: '+str(count)
  return result


# B. both_ends
#Given a string s, return a string made of the first 2  and the last 2 chars of the original string, so 'spring' yields 'spng'. However, if the string length is less than 2, return the empty string instead.


def both_ends(s):
 l=len(s)
 if l>2:
   s1=s[0:2] 
   s=s1 +s[-2:]
 else:
   s=''
 return s
# C. fix_start
# Given a string s, return a string where all occurrences of its first char have been changed to '*', except do not change the first char itself. e.g. 'babble' yields 'ba**le' .Assume that the string is length 1 or more.
# Hint: s.replace(stra, strb) returns a version of string s
# where all instances of stra have been replaced by strb.

def fix_start(s):
 p=s[0]
 q=(s[1:].replace(s[:1],'*'))
 s=p+q
 return (s) # +++your code here+++


# D. MixUp
# Given strings a and b, return a single string with a and b separated by a space '<a> <b>', except swap the first 2 chars of each string.
# e.g.
#   'mix', pod' -> 'pox mid'
#   'dog', 'dinner' -> 'dig donner'
# Assume a and b are length 2 or more.

def mix_up(a, b):
   x=a[0:2]
   p=(a.replace(a[0:2],b[0:2]))
   q=(b.replace(b[0:2],x[0:2]))
   r=p+" "+q
   return(r)# +++your code here+++



# Provided simple test() function used in main() to print what each function returns vs. what it's supposed to return.


def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# Provided main() calls the above functions with interesting inputs, using test() to check if each result is correct or not.


def main():
  print('donuts')
# Each line calls donuts, compares its result to the expected for that call.
  test(donuts(4), 'Number of donuts: 4')
  test(donuts(9), 'Number of donuts: 9')
  test(donuts(10), 'Number of donuts: many')
  test(donuts(99), 'Number of donuts: many')


  print('both_ends')
  test(both_ends('spring'), 'spng')
  test(both_ends('Hello'), 'Helo')
  test(both_ends('a'), '')
  test(both_ends('xyz'), 'xyyz')

 
 
  print('fix_start')
  test(fix_start('babble'), 'ba**le')
  test(fix_start('aardvark'), 'a*rdv*rk')
  test(fix_start('google'), 'goo*le')
  test(fix_start('donut'), 'donut')

 
  print ('mix_up')
  test(mix_up('mix', 'pod'), 'pox mid')
  test(mix_up('dog', 'dinner'), 'dig donner')
  test(mix_up('gnash', 'sport'), 'spash gnort')
  test(mix_up('pezzy', 'firm'), 'fizzy perm')


# Standard boilerplate to call the main() function.
if __name__ == '__main__':
  main()