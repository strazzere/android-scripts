// Dalvik Function Rename Script
// ---
// Attempt to make the function names look better -- avoid the ugly _def_ blah crap
//
// Created during #Hacksgiving 2012 @Lookout
// Updated 2014.2.12 to speed up and block user input to prevent issues
//
// Tim "diff" Strazzere
// <diff@lookout.com>
// <strazz@gmail.com>

#include <idc.idc>

static is_dalvik_function(name)
{
    if(strstr(name, "_def_") != -1 && strstr(name, "@") != -1) {
        return 1;
    }
    return 0;
}

static strip_annoying_characters(name) {
    // Strip out _def_ and @ plus anthing after that
    name = substr(name, strstr(name, "_def_") + 5, strstr(name, "@"));

    // Strip trailing _ chars
    while(substr(name, strlen(name) - 1, -1) == "_") {
        name = substr(name, 0, strlen(name) - 1);
    }

    // Strip the cases of "._" inside the names
    if(strstr(name, "._") != -1) {
        name = substr(name, 0, strstr(name, "._")) + "_" + substr(name, strstr(name, "._") + 2, -1);
    }

    // Strip the cases of "__" inside the names
    if(strstr(name, "__") != -1) {
        name = substr(name, 0, strstr(name, "__")) + "_" + substr(name, strstr(name, "__") + 2, -1);
    }

    return name;
}

// TODO: This should just use a list and iterate through, not two hardcoded ones
static get_location_by_hooks(addr) {
    // Mostly everything has an activity, so this should take care of 90% of the apps
    addr = LocByName("_def_Activity._init_@V");
    if(addr == -1) {
        Message("Unable to find our first hook method!\n");
	// Since it's possible to not have an activity, try to find the BuildConfig, which
	// is bundled in apps automatically by SDK 15+
        addr = LocByName("_def_BuildConfig._init_@V");
        if(addr == -1) {
            Message("Unable to find our second hook method - most likely this is going to fail now...\n");
        }
    }
}

static main() {
    auto addr, name, new_name, new_name_with_appendable, appendable, userName, firstpass, original;
    firstpass = 1;

    addr = get_location_by_hooks(addr);

    SetStatus(IDA_STATUS_WORK);
    while(addr != -1) {
        name = Name(addr);
        userName = NameEx(BADADDR, addr);
        if(name != "") {
            if(name != userName) {
                Message("Detected a user defined name of [ %s ] will no overwrite!\n", userName);
            } else {
	        if(is_dalvik_function(name)) {
		    appendable = 0;
		    new_name = new_name_with_appendable = strip_annoying_characters(name);
		    // Loop through a few tries incase the name already exists
		    while(!MakeNameEx(addr, new_name_with_appendable, 0)) {
			new_name_with_appendable = new_name + sprintf("_%i", appendable);
			appendable++;
		    }
		}
            }
        }
	if(firstpass) {
	    original = addr;
   	    addr = NextAddr(addr);
	    if(addr == -1) {
               firstpass = 0;
     	    }
	} else {
	    original = PrevAddr(original);
            addr = original;
        }
    }
    SetStatus(IDA_STATUS_READY);
}