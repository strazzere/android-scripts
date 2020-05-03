import ida_funcs
import ida_name
 
def do_rename(line):
    symbol_address, symbol_type, symbol_name = line.strip().split(' ')
    if symbol_type in ('t', 'T'):
        ida_funcs.add_func(int(symbol_address, 16))
        attempts = 0
        while attempts < 10:
            if attempts > 0:
                symbol_name = ('%s_%d' % (symbol_name[:-2], attempts))
            if ida_name.set_name(int(symbol_address, 16), symbol_name):
                break
            else:
                attempts += 1

### do_rename(line):
  
if __name__ == "__main__":
    with open('/home/diff/path/to/the.kallsyms', 'r') as file_handle:
        for line in file_handle:
            do_rename(line)

