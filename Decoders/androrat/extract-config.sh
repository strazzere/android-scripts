#!/bin/sh

get_normal_variable() {
    echo `grep -A 2 "v9, \"ip\"" $1 | tail -1 | cut -d'"' -f2`
}

get_packaged_date() {
    echo `unzip -v -l $1 | grep classes.dex | cut -d"%" -f2 | cut -d" " -f3`
}

for file in `find $1`
do

    if [[ -f "$file" ]] && [[ "$file" == *.apk ]]
        then
        # Extract and decode assests
	java -jar ~/bin/apktool.jar -q d "$file" tmp/

        # Search for files
	PACKAGE_NAME=`grep "package=" tmp/AndroidManifest.xml | sed 's/^.*package="//' | sed 's/".*//'`
	SHA1=`shasum "$file" | cut -c1-40`
	PACKAGED_DATE=`get_packaged_date $file`

	echo "Sha1:                        $SHA1"
	echo "Package Name:                $PACKAGE_NAME"
	echo "Packaged Date:               $PACKAGED_DATE"

	CONFIG="tmp/smali/my/app/client//ProcessCommand.smali"
	if [ ! -f $CONFIG ]
	    then
	    echo "Config not found in normal place!"
	fi

	if [ -f $CONFIG ]
            then
	    #Un-encoded config values
	    C2_URL=`get_normal_variable $CONFIG ">urlPostInfo"`

            # Pipe it all out
	    echo "C2_URL:                      $C2_URL"
	    echo "\n"
	else
	    echo "No config file found!"
	fi
        # Clean up
	rm -rf tmp/
    else
	echo "Skipping '$file'.."
    fi
done