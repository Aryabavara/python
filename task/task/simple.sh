#! /bin/bash

echo "enter 3 numbers"
read n1
read n2
read n3

if (( $n1 > $n2 ));
then
 if (( $n1 > $n3 ));
 then
 echo "$n1 is largest"
  else
  echo "$n3 is larger "
 fi
else
echo "$n2 is larger"
fi
