#!/bin/bash

COUNT=0
for f in [0-9][0-9][0-9]*.png
do
	 convert $f -resize 50% -background transparent -fill white -pointsize 40 -gravity SouthEast label:$COUNT  -composite `printf "%05d-label.png" $COUNT`
	 echo $COUNT
	 let "COUNT=COUNT+1"
done
