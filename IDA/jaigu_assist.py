"""jaigu_assist.py: Label function wrappers used by jaigu."""

__author__ = "Tim 'diff' Strazzere"
__copyright__ = "Copyright 2018, Red Naga"
__license__ = "GPL"
__version__ = "1.0"
__email__ = "strazz@gmail.com"

#
# Constants
#
DEBUG = False

# Attempt for the following pattern
#    LOAD:00027DEC sub_27DEC                               ; CODE XREF: sub_CE58+1D4↑p
#    LOAD:00027DEC                                         ; sub_DCAC+1A↑p
#    LOAD:00027DEC                 BX              PC
#    LOAD:00027DEC ; ---------------------------------------------------------------------------
#    LOAD:00027DEE                 ALIGN 0x10
#    LOAD:00027DF0                 CODE32
#    LOAD:00027DF0
#    LOAD:00027DF0 loc_27DF0                               ; CODE XREF: sub_27DEC↑j
#    LOAD:00027DF0                 LDR             R12, =(__fixdfsi - 0x27DFC)
#    LOAD:00027DF4                 ADD             PC, R12, PC ; __fixdfsi
#    LOAD:00027DF4 ; End of function sub_27DEC
#
# Above should be renamed to "fixdfsi_wrapper" (dropping the leading '_'s)


#
# Utility functions
#
def info(formatted_string):
    print formatted_string

def error(formatted_string):
    print 'ERROR - %s' % formatted_string

def debug(formatted_string):
    if DEBUG:
        print 'DEBUG - %s' % formatted_string

#
# Main functionality
#

def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1

def find_space(s):
    return find_str(s, ' ')

def trim_underscore(s):
    if s.startswith('_'):
        return trim_underscore(s[1:])
    return s

def main():
    load_seg = idaapi.get_segm_by_name('LOAD')
    for addr in Functions(load_seg.startEA, load_seg.endEA):
        name = GetFunctionName(addr)
        func = idaapi.get_func(addr)
        if name.startswith('sub_'):
            debug('Looking at %s @ 0x%x' % (name, addr))
            # Starts with 'BX PC' ?
            if GetMnem(addr) == 'BX' and GetOpnd(addr, 0) == 'PC':
                addr = FindCode(addr, SEARCH_DOWN)
                if GetMnem(addr) == 'LDR' and GetOpnd(addr, 0) == 'R12' and GetOpnd(addr, 1).startswith('=('):
                    real_name = GetOpnd(addr, 1)
                    real_name = trim_underscore(real_name[2:find_space(real_name)])
                    debug('%s real name should be %s_wrapper' % (name, real_name))

                    if idc.MakeNameEx(func.startEA, real_name, SN_PUBLIC):
                        info('%s renamed to %s_wrapper' % (name, real_name))
        else:
            debug('Skipping %s' % name)

if __name__ == "__main__":
    main()
