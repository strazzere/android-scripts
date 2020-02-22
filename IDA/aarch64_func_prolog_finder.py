# aarch64_func_prolog_finder.py
#
# Find undiscovered aarch64 functions that had been missed by IDA's auto-analysis.
#
# Originally from Fernand Lone Sang @ Quarkslab
# https://blog.quarkslab.com/reverse-engineering-samsung-s6-sboot-part-i.html
#
# I've simply updated the apis for usage with 7.4.191112
# diff -at- protonmail -dot- com
#

import idaapi

def find_sig(segment, sig, callback):
    seg = idaapi.get_segm_by_name(segment)
    if not seg:
        return
    ea, maxea = seg.start_ea, seg.end_ea
    while ea != idaapi.BADADDR:
        ea = idaapi.find_binary(ea, maxea, sig, 16, idaapi.SEARCH_DOWN)
        if ea != idaapi.BADADDR:
            callback(ea)
            ea += 4

def is_prologue_insn(ea):
    insn = ida_ua.insn_t()
    idaapi.decode_insn(insn, ea)
    return ida_ua.insn_t().itype in [idaapi.ARM_stp, idaapi.ARM_mov, idaapi.ARM_sub]

def callback(ea):
    flags = ida_bytes.get_full_flags(ea)
    if ida_bytes.is_unknown(flags):
        while ea != ida_idaapi.BADADDR:
            if is_prologue_insn(ea - 4):
                ea -= 4
            else:
                print("[*] New function discovered at %#lx" % (ea))
                idaapi.add_func(ea, ida_idaapi.BADADDR)
                break
    if ida_bytes.is_data(flags):
        print("[!] %#lx needs manual review" % (ea))

mov_x29_sp = "fd 03 00 91"
find_sig("ROM", mov_x29_sp, callback)
