#!/bin/sh

if [ ! -f "razstealer_decoder.class" ]
then
    javac razstealer_decoder.java
fi

for file in `find $1`
do

    if [ -f "$file" ]
        then
        # Extract and decode assests
	java -jar ~/bin/apktool.jar -q d "$file" tmp/

        # Search for files
	PACKAGE_NAME=`grep "package=" tmp/AndroidManifest.xml | sed 's/^.*package="//' | sed 's/".*//'`
	SHA1=`shasum "$file"`

	echo "Sha1:              $SHA1"
	echo "Package Name:      $PACKAGE_NAME"

	GLOBAL="tmp/smali/com/android/systemSettings/Globals.smali"
	if [ ! -f $GLOBAL ]
	    then
	    echo "Global config not found in normal place, attempt secondary location..."
	    GLOBAL=`find tmp/ -name Globals.smali`
	fi

	DECODE="java razstealer_decoder"
	if [ -f $GLOBAL ]
            then
	    #Un-encoded config values
	    STEAL_CONTACTS=`grep -B 2 ">stealContacts" $GLOBAL | head -1 | cut -d\" -f2`
	    STEAL_SMS=`grep -B 2 ">stealSMS" $GLOBAL | head -1 | cut -d\" -f2`
	    STEAL_INFO=`grep -B 2 ">stealInfo" $GLOBAL | head -1 | cut -d\" -f2`
	    STEAL_PICS=`grep -B 2 ">stealPics" $GLOBAL | head -1 | cut -d\" -f2`
	    STEAL_WHATSAPP=`grep -B 2 ">stealWhatsapp" $GLOBAL | head -1 | cut -d\" -f2`
	    USE_ROOT=`grep -B 2 ">useRoot" $GLOBAL | head -1 | cut -d\" -f2`
	    ZIP_DATA=`grep -B 2 ">zipData" $GLOBAL | head -1 | cut -d\" -f2`
	    DELETE_ZIP=`grep -B 2 ">deleteZip" $GLOBAL | head -1 | cut -d\" -f2`
	    TRIGGER_VIA_SMS=`grep -B 2 ">triggerViaSms" $GLOBAL | head -1 | cut -d\" -f2`
	    RUN_ON_STARTUP=`grep -B 2 ">runOnStartup" $GLOBAL | head -1 | cut -d\" -f2`
	    MINUTE_OFFSET=`grep -B 2 ">minuteOffset" $GLOBAL | head -1 | cut -d\" -f2`
	    USE_DATA=`grep -B 2 ">useData" $GLOBAL | head -1 | cut -d\" -f2`
	    MAIL_PROVIDER=`grep -B 2 ">mailProvider" $GLOBAL | head -1 | sed "s/^.*>//" | cut -d: -f1`
	    if [[ $MAIL_PROVIDER == *const-string* ]]
	        then
		MAIL_PROVIDER=`echo $MAIL_PROVIDER | cut -d\" -f2`
	    fi
	    USE_FTP=`grep -B 2 ">useFTP" $GLOBAL | head -1 | cut -d\" -f2`

	    # Encoded values we must decode
	    TRIGGER_START=`grep -B 2 ">triggerStart" $GLOBAL | head -1 | cut -d\" -f2`
	    TRIGGER_START=`$DECODE $TRIGGER_START`
            MY_MAIL=`grep -B 2 ">myMail" $GLOBAL | head -1 | cut -d\" -f2`
            MY_MAIL=`$DECODE $MY_MAIL`
            MY_PASSWORD=`grep -B 2 ">myPassword" $GLOBAL | head -1 | cut -d\" -f2`
            MY_PASSWORD=`$DECODE $MY_PASSWORD`
            YOUR_MAIL=`grep -B 2 ">yourMail" $GLOBAL | head -1 | cut -d\" -f2`
            YOUR_MAIL=`$DECODE $YOUR_MAIL`
	    FTP_HOST=`grep -B 2 ">ftpHost" $GLOBAL | head -1 | cut -d\" -f2`
	    FTP_HOST=`$DECODE $FTP_HOST`
	    FTP_USER=`grep -B 2 ">ftpUser" $GLOBAL | head -1 | cut -d\" -f2`
            FTP_USER=`$DECODE $FTP_USER`
	    FTP_PW=`grep -B 2 ">ftpPw" $GLOBAL | head -1 | cut -d\" -f2`
            FTP_PW=`$DECODE $FTP_PW`
	    FTP_PORT=`grep -B 2 ">ftpPort" $GLOBAL | head -1 | cut -d\" -f2`
            FTP_PORT=`$DECODE $FTP_PORT`
	    ANDROID_DATA_PATH=`grep -B 2 ">androidDataPath" $GLOBAL | head -1 | cut -d\" -f2`
            ANDROID_DATA_PATH=`$DECODE $ANDROID_DATA_PATH`

            # Pipe it all out
    	    echo "MY_MAIL:           $MY_MAIL"
    	    echo "MY_PASSWORD:       $MY_PASSWORD"
            echo "YOUR_MAIL:         $YOUR_MAIL"
  	    echo "STEAL_CONTACTS:    $STEAL_CONTACTS"
    	    echo "STEAL_SMS:         $STEAL_SMS"
    	    echo "STEAL_INFO:        $STEAL_INFO"
    	    echo "STEAL_PICS:        $STEAL_PICS"
            echo "STEAL_WHATSAPP:    $STEAL_WHATSAPP"
  	    echo "USE_ROOT:          $USE_ROOT"
    	    echo "ZIP_DATA:          $ZIP_DATA"
    	    echo "DELETE_ZIP:        $DELETE_ZIP"
    	    echo "TRIGGER_START:     $TRIGGER_START"
	    if [[ -z "$TRIGGER_VIA_SMS" ]]
	        then
		TRIGGER_VIA_SMS="Not found, likely version where always enabled"
	    fi
	    echo "TRIGGER_VIA_SMS:   $TRIGGER_VIA_SMS"
    	    echo "RUN_ON_STARTUP:    $RUN_ON_STARTUP"
    	    echo "MINUTE_OFFSET:     $MINUTE_OFFSET"
    	    echo "USE_DATA:          $USE_DATA"
    	    echo "MAIL_PROVIDER:     $MAIL_PROVIDER"
    	    echo "USE_FTP:           $USE_FTP"
    	    echo "FTP_HOST:          $FTP_HOST"
    	    echo "FTP_USER:          $FTP_USER"
    	    echo "FTP_PW:            $FTP_PW"
    	    echo "FTP_PORT:          $FTP_PORT"
    	    echo "ANDROID_DATA_PATH: $ANDROID_DATA_PATH"
	    echo "\n"
	else
	    echo "No config file found!"
	fi
        # Clean up
	rm -rf tmp/
    else
	echo "File doesn't appear to be regular file, skipping.."
    fi
done