"""android_jni_assist.py: Label enums for Android JNI to aid in reversing."""

__author__ = "Tim 'diff' Strazzere"
__copyright__ = "Copyright 2015, Red Naga"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "strazz@gmail.com"

# Thanks to trojancyborg and TheCjw for posting code/ideas I based most of
# this work on.

#
# Constants
#
DEBUG = True

# TODO : There is an issue with IDA Pro where it grabs the repeatable comment
#        from the wrong enum if on it is performing the enum grab for the ADD
#        (TWO_PATTERNS) based instruction.

# Attempt for the following patterns:
#   ADD     R5, SP, #0x18+var_14
#   ADD     R1, SP, #0x18+var_14
TWO_MNEM = ['ADD']
TWO_PATTERNS = ['#0x', "+var_"]

# Attempt for the following patterns:
#   STR     R1, [SP,#0x18+var_14]
#   LDR     R0, [SP,#0x18+var_14]
THREE_MNEM = ['STR', 'LDR']
THREE_PATTERNS = ['SP'] + TWO_PATTERNS

# JNI Methods to recurse through for setting enums
#   JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm, void* reserved);
#   JNIEXPORT void JNICALL JNI_OnUnload(JavaVM* vm, void* reserved);
# TODO : Need to find these programmatically
JNI_METHODS = [
    'JNI_OnLoad',
    'JNI_OnUnLoad'
]

# JNI enum names and comments pulled from jni.h in the Android NDK
JNIInvokeInterface = [
    ('jni_DestroyJavaVM', 'jint (*DestroyJavaVM)(JavaVM*)'),
    ('jni_AttachCurrentThread', 'jint (*AttachCurrentThread)(JavaVM*, JNIEnv**, void*)'),
    ('jni_DetachCurrentThread', 'jint (*DetachCurrentThread)(JavaVM*)'),
    ('jni_GetEnv', 'jint (*GetEnv)(JavaVM*, void**, jint)'),
    ('jni_AttachCurrentThreadAsDaemon', 'jint (*AttachCurrentThreadAsDaemon)(JavaVM*, JNIEnv**, void*)')
]

JNI_VERSION_MNEM = ['LDR', 'MOV']
JNI_VERSION_VALUES = ['0x10004', '0x10005', '0x10006']

JNIVersion = [
    ('jni_Version_1_4' ,'JNI_VERSION_1_4'),
    ('jni_Version_1_5' ,'JNI_VERSION_1_5'),
    ('jni_Version_1_6' ,'JNI_VERSION_1_6')
]

#
# Utility functions
#
def info(formatted_string):
    print(formatted_string)

def error(formatted_string):
    print('ERROR - %s' % formatted_string)

def debug(formatted_string):
    if DEBUG:
        print('DEBUG - %s' % formatted_string)

#
# Main functionality
#
def create_enum(enum_name, member_infos, offset, increment):
    return_id = idc.add_enum(-1, enum_name, 0x1100000);

    if return_id == BADADDR:
        error('Unable to create enum : %s' % enum_name)
        return return_id

    for member_info in member_infos:
        debug("Attempting to create enum member and comment : %s.%s -> %s" % (enum_name, member_info[0], member_info[1]))

        if idc.add_enum_member(return_id, member_info[0], offset, -1) == 0:
            const_id = idc.get_enum_member(return_id, offset, 0, -1)

            if const_id == -1:
                debug('Unable to get constant id for : %s.%s' % (enum_name, member_info[0]))

            else:
                if ida_enum.set_enum_member_cmt(const_id, member_info[1], 1):
                    debug('Enum value created : %s.%s' % (enum_name, member_info[0]))

                else:
                    error('Enum value failed to have comment set : %s.%s' % (enum_name, member_info[0]))

                offset += increment
        else:
            error('Unable to create enum member : %s.%s' % (enum_name, member_info[0]))
            return -1

    info('Finished creating enum : %s' % enum_name)
    return return_id

def create_or_find_enum(enum_name, member_infos, offset, increment):
    enum_id = create_enum(enum_name, member_infos, offset, increment)

    if enum_id == -1:
        debug('Unable to create enum, attempting to find one')
        enum_id = ida_enum.get_enum(enum_name)
        if enum_id == -1:
            error('Could create or find a enum')
            return False

    return enum_id

def find_function_address(function_name):
    for name in Names():
        if name[1] == function_name:
            return name[0]

    return -1

def is_enum(addr):
    patterns = []
    if idc.print_insn_mnem(addr) in THREE_MNEM:
        patterns = THREE_PATTERNS
    elif idc.print_insn_mnem(addr) in TWO_MNEM:
        patterns = TWO_PATTERNS

    for pattern in patterns:
        # This means we are in TWO_PATTERNS mode
        if(idc.print_operand(addr, 1) == 'SP'):
            if pattern in idc.print_operand(addr, 2):
                return True
        else:
            # THREE_PATTERNS mode
            if pattern in idc.print_operand(addr, 1):
                return True

    return False

def mark_enums(enum_id, method):
    addr = find_function_address(method)
    if addr == -1:
        error('Unable to find %s' % method)
        return False

    debug('Found function starting @ 0x%x' % addr)
    func_end = next(Chunks(addr))[1]
    if(func_end < addr):
        error('Unable to find good function end for %s' % method)
        return False

    debug('Found function ending @ 0x%x' % func_end)

    while(addr < func_end):
        if is_enum(addr):
            debug('Found a enum to mark @ 0x%x' % addr)
            ret = idc.op_enum(addr, 1, enum_id, 0)
            # Try one more time due to IDA Pro bug
            if ret == -1:
                ret = idc.op_enum(addr, 1, enum_id, 0)
                error("Tried twice, result %s" % ret)

        addr = ida_search.find_code(addr, SEARCH_DOWN)

    return True

def jni_jvm_enum_init():
    jvm_enum_id = create_or_find_enum('JNI_JVM_FUNC', JNIInvokeInterface, -0x8, 0x4)

    if jvm_enum_id is not False:
        for method in JNI_METHODS:
            mark_enums(jvm_enum_id, method)

    return True

def is_const(addr):
    # This might be incorrect to do
    if idc.print_insn_mnem(addr) not in JNI_VERSION_MNEM:
        return False

    for value in JNI_VERSION_VALUES:
        if value in idc.print_operand(addr, 1):
            return True

    return False

def jni_constants():
    const_enum_id = create_or_find_enum('JNI_VERSIONS', JNIVersion, 0x10004, 0x1)

    if const_enum_id is not False:
        method = 'JNI_OnLoad'
        addr = find_function_address(method)
        if addr == -1:
            error('Unable to find %s' % method)
            return False

        debug('Found function starting @ 0x%x' % addr)
        func_end = next(Chunks(addr))[1]
        if(func_end < addr):
            error('Unable to find good function end for %s' % method)
            return False

        debug('Found function ending @ 0x%x' % func_end)

        while(addr < func_end):
            if is_const(addr):
                debug('Found a const to mark @ 0x%x' % addr)
                ret = idc.op_enum(addr, 1, const_enum_id, 0)
                # Try one more time due to IDA Pro bug
                if ret == -1:
                    ret = idc.op_enum(addr, 1, const_enum_id, 0)
                    debug("Tried twice, result %s" % ret)

            addr = ida_search.find_code(addr, SEARCH_DOWN)

    return True

def main():
    jni_jvm_enum_init()
    jni_constants()

if __name__ == "__main__":
    main()
