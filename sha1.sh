#!/bin/bash

START=0000
END=9999

for I in $(seq $START $END)
do
	echo "queenrulez$I"
	echo -n "queenrulez$I" |shasum
done
