#!/usr/bin/env bash
#https://unix.stackexchange.com/questions/102691/get-age-of-given-file
#omc kube cd224 completion
#~/.omc/cache/completion/kube/cd224/completion
prefix=~/.omc/cache/completion
completion_relpath=''
duration_relpath=''
for one in $@; do
    completion_relpath=$completion_relpath/$one
    if [ $one == 'completion' ];then
    	duration_relpath=$duration_relpath/duration
    else
    	duration_relpath=$duration_relpath/$one
	fi
done

filename=$prefix$completion_relpath
duration_filename=$prefix$duration_relpath

cache_duration=60

if [ -f "$duration_filename" ];then
	cache_duration=`cat $duration_filename`

fi

if [ -f "$filename" ]; then
	if [[ $cache_duration == -1 ]];then
		cat $filename
	else
		file_age=$(($(date +%s) - $(stat -t %s -f %m -- $filename)))
		if [[ $file_age -gt $cache_duration ]];then
			# cache in invalid
			omc $@
		else
			cat $filename
		fi
	fi
else
	omc $@
fi
