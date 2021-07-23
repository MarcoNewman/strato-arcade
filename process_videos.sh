#!/bin/bash
echo "Converting Videos for Flight: $1"
files=(videos/$1/*.h264)
total=${#files[@]}
i=0
for f in "${files[@]}"; do
  echo "Converting File: ${f}"
  i=$(( i + 1 ))
  MP4Box -add "$f:fps=30" "videos/$1/video${i}.mp4"
done

echo
echo "Concatenating Video Files..."
files=(videos/$1/*.mp4)
for f in ${files[@]}; do 
  echo file \'$f\' >> list.txt; 
done 
ffmpeg -hide_banner -loglevel error -f concat -safe 0 -i list.txt -c copy mp4s/$1.mp4
rm list.txt

echo
echo "Removing Temporary .mp4s:"
for f in videos/$1/*.mp4; do
  echo "-${f}"
  rm $f
done 