#!/bin/bash
lines=$(wc -l < $1) 
if [ $lines -le 10000 ]
then
	echo "Error: File contains less than 10000 lines!"
	exit 1
else
	echo $lines
	head -n 1 $1
fi
tail -n 10000 $1 | grep -c -i "potus"
sed -n '100,200p' $1 | grep -c -w "fake"
