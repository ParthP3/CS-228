#!/bin/bash 

# Use as ./run.sh N T unsat/sat

if [ $# != 3 ]
then 
	echo "Usage: $0 N T unsat/sat"
	exit 0
fi 

python3 generator.py $1 $2 $3 input.txt
time python3 210100106_21b090003_210050074_tile_loop.py input.txt | tee output.txt
