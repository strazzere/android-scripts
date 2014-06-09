#!/bin/sh

# Check for dependancy of base64 command
command -v base64 >/dev/null 2>&1 || {
    echo >&2 "base64 is not available, aborting!"
    exit 1
}

decode_base64 () {
  echo "$1" | base64 -D ; echo
}

get_normal_variable() {
    echo `grep -B 2 "$2" $1 | head -1 | cut -d\" -f2`
}

get_encoded_variable() {
    decode_base64 `get_normal_variable $1 $2`
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

	CONFIG="tmp/smali/com/connect/MyService.smali"
	if [ ! -f $CONFIG ]
	    then
	    echo "Config not found in normal place!"
	fi

	if [ -f $CONFIG ]
            then
	    #Un-encoded config values
#	    GPLAY_BYPASS=`get_normal_variable $CONFIG ">GPlayBypass"`
	    URL_POSTINFO=`get_normal_variable $CONFIG ">urlPostInfo"`
	    if [ -z "$URL_POSTINFO" ]
	    then
		URL_POSTINFO=`get_normal_variable $CONFIG ">ﹳ"`
	    fi

	    URL_SENDUPDATE=`get_normal_variable $CONFIG ">urlSendUpdate"`
            if [ -z "$URL_SENDUPDATE" ]
            then
		URL_SENDUPDATE=`get_normal_variable $CONFIG ">ﾞ"`
            fi

	    URL_UPLOADFILES=`get_normal_variable $CONFIG ">urlUploadFiles"`
            if [ -z "$URL_UPLOADFILES" ]
            then
		URL_UPLOADFILES=`get_normal_variable $CONFIG ">ʹ"`
            fi

	    URL_UPLOADPICTURES=`get_normal_variable $CONFIG ">urlUploadPictures"`
            if [ -z "$URL_UPLOADPICTURES" ]
            then
		URL_UPLOADPICTURES=`get_normal_variable $CONFIG ">ՙ"`
            fi

	    URL_FUNCTIONS=`get_normal_variable $CONFIG ">urlFunctions"`
            if [ -z "$URL_FUNCTIONS" ]
            then
		URL_FUNCTIONS=`get_normal_variable $CONFIG ">י"`
            fi

	    # Encoded values we must decode
            ENCODED_URL=`get_encoded_variable $CONFIG ">encodedURL"`
	    if [ -z "$ENCODED_URL" ]
	    then
		ENCODED_URL=`get_encoded_variable $CONFIG ">ˎ"`
	    fi
            BACKUP_URL=`get_encoded_variable $CONFIG ">backupURL"`
	    if [ -z "$BACKUP_URL" ]
	    then
		BACKUP_URL=`get_encoded_variable $CONFIG ">ˏ"`
	    fi
            ENCODED_PASSWORD=`get_encoded_variable $CONFIG ">encodedPassword"`
	    if [ -z "$ENCODED_PASSWORD" ]
	    then
		ENCODED_PASSWORD=`get_encoded_variable $CONFIG ">ᐝ"`
	    fi

            # Pipe it all out
#	    echo "GPLAY_BYPASS: $GPLAY_BYPASS"
	    echo "URL_POSTINFO:                $URL_POSTINFO"
	    echo "URL_SENDUPDATE:              $URL_SENDUPDATE"
	    echo "URL_UPLOADFILES:             $URL_UPLOADFILES"
	    echo "URL_UPLOADPICTURES:          $URL_UPLOADPICTURES"
	    echo "URL_FUNCTIONS:               $URL_FUNCTIONS"

	    echo "ENCODED_URL (c2):            $ENCODED_URL"
	    echo "BACKUP_URL:                  $BACKUP_URL"
    	    echo "ENCODED_PASSWORD:            $ENCODED_PASSWORD"
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