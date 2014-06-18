#!/bin/sh

get_c2_address() {
    echo `grep "\"http" $1 | cut -d\" -f2`
}

get_number_of_extort_numbers() {
    echo `grep -ir "\+" tmp/res/values/strings.xml | cut -d"+" -f2 | cut -d" " -f1 | wc -l | tr -d " "`
}

get_extort_number() {
    echo `grep -ir "\+" tmp/res/values/strings.xml | cut -d"+" -f2 | cut -d" " -f1 | sed -n $1p`
}

get_packaged_date() {
    echo `unzip -v -l $1 | grep classes.dex | cut -d"%" -f2 | cut -d" " -f3`
}

get_number_of_countries() {
    echo `grep -ir "getCountry" $1 | wc -l | tr -d " "`
}

get_country() {
    GET_COUNTRY_LINE=`grep -ir -nr "getCountry" $1 | sed -n $2p | cut -d":" -f2`

    echo `sed -n $(expr $GET_COUNTRY_LINE + 4)p $1 | cut -d"\"" -f2`
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

	C2="tmp/smali/my/sharaga/loser/f.smali"
	if [ -f $C2 ]
            then
	    ADDRESS=`get_c2_address $C2`

	    NUM_EXTORT=`get_number_of_extort_numbers`

	    echo "C2 ADDRESS:                  $ADDRESS"
	    echo "NUMBER OF EXTORTION #s:      $NUM_EXTORT"

	    for i in $(seq 1 $NUM_EXTORT)
	    do
		CURRENT_EXTORT=`get_extort_number $i`
		echo "EXTORTION #$i:                +$CURRENT_EXTORT"
	    done
	else
	    echo "No C2 file found!"
	fi

	COUNTRY="tmp/smali/my/sharaga/loser/Main.smali"
	if [ -f $COUNTRY ]
	    then
	    NUM_COUNTRIES=`get_number_of_countries $COUNTRY`
	    echo "# OF COUNTRIES TARGETED:     $NUM_COUNTRIES"

	    for i in $(seq 1 $NUM_COUNTRIES)
	    do
		CURRENT_COUNTRY=`get_country $COUNTRY $i`
		echo "COUNTRY CODE #$i:             $CURRENT_COUNTRY"
	    done
	else
	    echo "No country config file found!"
	fi
        # Clean up
	rm -rf tmp/
    else
	echo "Skipping '$file'.."
    fi
done