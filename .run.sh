#!/bin/bash
action=$1
shift 1
gitutils='/home/pi/GIT-REPO/gitUtils'
${gitutils}/ln_lib_zip


pgmz="/home/pi/GIT-REPO/Python/PyMount/bin/PyMount.zip"
pgmy="/home/pi/GIT-REPO/Python/PyMount/__main__.py"


if [[ -z "$action"  ]]; then
	echo "immettere:  zip | compile"
	exit 0

elif [[ "$action" == "zip" ]]; then
        pgm=$pgmz

elif [[ "$action" == "compile" ]]; then
	${gitutils}/ln_zip_project $*
	echo "compiled...."
	echo

	exit 0
else
	pgm=$pgmy # run __main__.py

fi


cd /tmp # lancio il programma da una directory fuori dalla reale per simulare il cron
/usr/bin/python ${pgm} $*
