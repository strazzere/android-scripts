"""decrypter.py: Automate some reversing of some Dalvik encryption for Raxir surveillance implants."""

__author__ = "Tim 'diff' Strazzere"
__copyright__ = "Copyright 2016, Red Naga"
__license__ = "GPL"
__version__ = "1.0"
__email__ = ["strazz@gmail.com"]

from idautils import *
from idc import *
import idaapi
import sys
import string

#
# Constants
#
DEBUG = False

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

def readShort(addr):
    return (GetOriginalByte(addr + 0x1) << 0x8) + GetOriginalByte(addr)

def readInt(addr):
    return (GetOriginalByte(addr + 0x3) << 0x18) + (GetOriginalByte(addr + 0x2) << 0x10) + (GetOriginalByte(addr + 0x1) << 0x8) + GetOriginalByte(addr)

# Todo this will only accept strings of lenght 0xFF
def getStringFromAddr(addr):
    length = GetOriginalByte(addr)
    string = ''
    for i in range(1, length + 1):
        string = '%s%c' % (string, unichr(GetOriginalByte(addr + i)))

    return string

def getString(addr):
    string_id = readShort(addr + 0x2) # (GetOriginalByte(addr + 0x3) << 0x8) + GetOriginalByte(addr + 0x2)
    string_ids = ida_segment.get_segm_by_name('STR_IDS')
    string_addr = readInt(string_ids.startEA + (string_id * 4))

    return getStringFromAddr(string_addr)

def generic_decrypt(encrypted, mod, static_xor, mod_add_1, mod_add_2):
    if encrypted is None or mod is None:
        return ''

    mod = mod + mod_add_1

    out = ''
    for char in list(encrypted):
        out = '%s%s' % (out, unichr(ord(char) ^ (mod & static_xor)))
        mod = (mod + mod_add_2)

    # MakeComm and MakeRptCmt barf if we don't convert this to non-unicode, unknown if this will cause issues downstream...
    return out.encode('ascii', 'replace')#.encode('UTF-32')

cryptions = [
# v 7.0.0 obf
    [ 'Gson.equals(ref, int)', 0x5F, -0xC, 0x3 ],
    [ 'g9.concat(int, ref)', 0x5F, 0xB, -0xB ],
    [ 'Autostart.regionMatches(int, ref)', 0x5F, 0xE, -0xB ],
    [ 'f.replace(ref, int)', 0x5F, 0xD, 0xB ],
    [ 'h.equals(ref, int)', 0x5F, 0xC, 0x9 ],
    [ 'a.toString(int, ref)', 0x5F, -0xB, -0x1 ],
# Earlier samples - v 4.0 obf
    [ 'Gson.getChars(ref, int)', 0x5F, 0x7, 0xD ],
    [ 'JsonNull.split(int, ref)', 0x5F, 0x8, 0xF ],
# v 4.0 obf
    [ 'JsonNull.concat(int, ref)', 0x5F, -0x7, 0x9 ],
    [ 'Gson.indexOf(ref, int)', 0x5F, 0x3, -0xD ],
# v 6.1.0 obf - tre
    [ 'li.valueOf(int, ref)', 0x5F, 0xF, -0x1 ],
    [ 'Gson.concat(ref, int)', 0x5f, -0x1, 0x1 ],
# Zed detect sample - v 6.1.0 obf - bulk
#    [ 'Gson.indexOf(ref, int)', 0x5F, 0x5, -0x9 ],
    [ 'JsonNull.startsWith(int, ref)', 0x5F, -0x5, -0xB ],
# v 3.2 obf
    [ 'Gson.endsWith(int, ref)', 0x5F, 0x1, -0x9 ],
    [ 'k9.toString(ref, int)', 0x5F, -0xA, 0x9 ],
]

cryptions_3arg = [
    [ 'e.getChars(ref, int, int)', 0x5F, -0xF ],
]

def is_encrypted(addr):
    if GetMnem(addr) == 'const-string':
        addr_2 = FindCode(addr, SEARCH_DOWN)
        if 'const/' in GetMnem(addr_2):
            addr_3 = FindCode(addr_2, SEARCH_DOWN)
            if GetMnem(addr_3) == 'invoke-static':
                for (func, xor, mod1, mod2) in cryptions:
                    if func in GetOpnd(addr_3, 2):
                        debug(' %s in %s ' % (func, GetOpnd(addr_3, 2)))
                        # GetOpnd(addr, 2) will just return the string name, so, we're screwed and need to calculate it by hand
                        # This is done by getting the string_id offset, then looking it up in the STR_ID table...
                        loaded_string = getString(addr)
                        # Should always work, it will guess that it's base16 and chop off the expected '0x' prefix
                        modifier = int(GetOpnd(addr_2, 1), 0)
                        info('0x%x : %s' % (addr, generic_decrypt(loaded_string, modifier, xor, mod1, mod2)))
                        MakeComm(addr, generic_decrypt(loaded_string, modifier, xor, mod1, mod2))
                        return True
            elif 'const/' in GetMnem(addr_3):
                addr_4 = FindCode(addr_3, SEARCH_DOWN)
                if GetMnem(addr_4) == 'invoke-static':
                    for (func, xor, mod1) in cryptions_3arg:
                        if func in GetOpnd(addr_4, 3):
                            debug(' %s in %s ' % (func, GetOpnd(addr_4, 3)))
                            loaded_string = getString(addr)
                            modifier = int(GetOpnd(addr_2, 1), 0)
                            mod2 = int(GetOpnd(addr_3, 1), 0)
                            info('0x%x : %s' % (addr, generic_decrypt(loaded_string, modifier, xor, mod1, mod2)))
                            MakeComm(addr, generic_decrypt(loaded_string, modifier, xor, mod1, mod2))
                            return True
    elif 'const/' in GetMnem(addr):
        addr_2 = FindCode(addr, SEARCH_DOWN)
        if GetMnem(addr_2) == 'const-string':
            addr_3 = FindCode(addr_2, SEARCH_DOWN)
            if GetMnem(addr_3) == 'invoke-static':
                for (func, xor, mod1, mod2) in cryptions:
                    if func in GetOpnd(addr_3, 2):
                        debug(' %s in %s ' % (func, GetOpnd(addr_3, 2)))
                        modifier = int(GetOpnd(addr, 1), 0)
                        loaded_string = getString(addr_2)
                        info('0x%x : %s' % (addr, generic_decrypt(loaded_string, modifier, xor, mod1, mod2)))
                        MakeComm(addr, ('%s' % generic_decrypt(loaded_string, modifier, xor, mod1, mod2)))
                        return True
    return False

def main():
    strings_added = 0
    code_seg = ida_segment.get_segm_by_name('CODE')

    for addr in Functions(code_seg.startEA, code_seg.endEA):
        name = GetFunctionName(addr)

        end_addr = Chunks(addr).next()[1]
        if(end_addr < addr):
            error('Unable to find good end for the function %s' % name)
            pass

        debug('Found function %s starting/ending @ 0x%x 0x%x' %  (name, addr, end_addr))

        while addr <= end_addr:
            if is_encrypted(addr):
                strings_added += 1

                addr = FindCode(FindCode(FindCode(addr, SEARCH_DOWN), SEARCH_DOWN), SEARCH_DOWN)
            else:
                addr = FindCode(addr, SEARCH_DOWN)

    info('%d strings decrypted' % strings_added)

if __name__ == "__main__":
    info('Dalvik Decryptor loaded...')
    main()