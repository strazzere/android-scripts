# xorish.py
#
# Just playing around with fast and easy commenting for
# IDA Pro, mainly used on some ELF ARM binaries
#
# Tim Strazzere <diff@lookout.com
#

def strxor(a, b):
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

def xor():
    print ' ..'
    ea = ScreenEA()
    string = idc.GetString(idc.GetOperandValue(ea,1))
    key = 'BB2FA36AAA9541F0'
    xored_string = strxor(string, key)
    print ' got %s ' % xored_string
    comment = ''
    if GetCommentEx(ea, 1) is not None:
        comment = idc.GetCommentEx(ea, 1) + '\n'
    MakeRptCmt(ea, comment + string + " xor'ed " + xored_string)

# Create something bindable
idaapi.CompileLine('static xorish() { RunPythonStatement("xor()"); }')
# Bind the hotkey
AddHotkey("/", 'xorish')
