ffmpeg -f v4l2 -r 25 -s 1280x720 -i /dev/video0 -c:v h264_omx -b:v 3072k -an -f segment -segment_time 1 -segment_wrap 2 -segment_list_size 1 -segment_list "/var/www/html/hls/stream.m3u8" "/var/www/html/hls/stream%03d.ts"

