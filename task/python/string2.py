# D. verbing
# Given a string, if its length is at least 3, add 'ing' to its end. Unless it already ends in 'ing', in which case add 'ly' instead. If the string length is less than 3, leave it unchanged. Return the resulting string.

def verbing(s):
  if len(s)>=3:
   if(s.endswith("ing")):
     p=s+'ly'
   else:
     p=s+'ing'
  else:
    p=s
  return(p)


# E. not_bad
# Given a string, find the first appearance of the substring 'not' and 'bad'. If the 'bad' follows the 'not', replace the whole 'not'...'bad' substring with 'good'. Return the resulting string. So 'This dinner is not that bad!' : This dinner is good!.

def not_bad(s):
  l=len(s)
  n = s.find('not')
  b = s.find('bad')
  x = 0
  y = 0
  if 'not'in s:
   x = 1
   if 'bad'in s:
    y = 1
   if x == y and b > n:
    s = s.replace(s[n:(b+3)], 'good')
    return(s)
   else:
    return(s)


# F. front_back
# Consider dividing a string into two halves. If the length is even, the front and back halves are the same length. If the length is odd, we'll say that the extra char goes in the front half. e.g. 'abcde', the front half is 'abc', the back half 'de'. Given 2 strings, a and b, return a string of the form a-front + b-front + a-back + b-back.

def front_back(a, b):
  la=len(a)
  lb=len(b)
  if la % 2 == 0:
   aend = la // 2
  else:
   aend = (la // 2) + 1

  if lb % 2 == 0:
   bend = lb // 2
  else:
   bend = (lb // 2) + 1

  afront = a[0:aend]
  aback = a[aend:]  

  bfront = b[0:bend]
  bback = b[bend:]

  return (afront + bfront + aback + bback)



# Simple provided test() function used in main() to print what each function returns vs. what it's supposed to return.

def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print('%s got: %s expected: %s' % (prefix, repr(got), repr(expected)))


# main() calls the above functions with interesting inputs, using the above test() to check if the result is correct or not.

def main():
  print('verbing')
  test(verbing('hail'), 'hailing')
  test(verbing('swiming'), 'swimingly')
  test(verbing('do'), 'do')

  print
  print('not_bad')
  test(not_bad('This movie is not so bad'), 'This movie is good')
  test(not_bad('This dinner is not that bad!'), 'This dinner is good!')
  test(not_bad('This tea is not hot'), 'This tea is not hot')
  test(not_bad("It's bad yet not"), "It's bad yet not")

 
  print ('front_back')
  test(front_back('abcd', 'xy'), 'abxcdy')
  test(front_back('abcde', 'xyz'), 'abcxydez')
  test(front_back('Kitten', 'Donut'), 'KitDontenut')

if __name__ == '__main__':
  main()