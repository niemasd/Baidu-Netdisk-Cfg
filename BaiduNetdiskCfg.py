#! /usr/bin/env python3
from base64 import b64decode, b64encode
from os.path import isdir, isfile
from sys import argv

# helper class to represent Baidu Netdisk CFG files
class BaiduNetdiskCfg:
    # create object from cfg path
    def __init__(self, cfg):
        if isfile(cfg) and cfg.lower().endswith('.cfg'):
            data_b64 = open(cfg).read()
            self.data = b64decode(data_b64)
        else:
            raise ValueError("Invalid cfg: %s" % cfg)

    # return length of Base64-decoded data
    def __len__(self):
        return len(self.data)

    # return Base64 string
    def get_b64(self):
        return b64encode(self.data)

    # return string representation (Base64 string)
    def __str__(self):
        return self.get_b64().decode()

    # return hexdump
    def get_hex(self, bytes_per_block=None, blocks_per_line=None, block_delim=' ', upper=True):
        for s,v in [('bytes_per_block', bytes_per_block), ('blocks_per_line', blocks_per_line)]:
            if v is not None and (not isinstance(v, int) or v < 1):
                raise ValueError("%s must be a positive integer: %s" % (s,v))
        lines = [[[]]]
        for v in self.data:
            if len(lines[-1][-1]) == bytes_per_block:
                if len(lines[-1]) == blocks_per_line:
                    lines.append(list())
                lines[-1].append(list())
            lines[-1][-1].append(hex(v)[2:].zfill(2))
        out = '\n'.join(block_delim.join(''.join(b) for b in l) for l in lines)
        if upper:
            return out.upper()
        else:
            return outa

    # compare this cfg vs. another cfg
    def print_diff(self, o, diff_symbol='|', bytes_per_block=None, blocks_per_line=None, block_delim=' ', upper=True):
        if not isinstance(o, BaiduNetdiskCfg):
            raise TypeError("other object must be BaiduNetdiskCfg: %s" % type(o))
        h = self.get_hex(bytes_per_block=bytes_per_block, blocks_per_line=blocks_per_line, block_delim=block_delim, upper=upper); print(h)
        h2 = o.get_hex(bytes_per_block=bytes_per_block, blocks_per_line=blocks_per_line, block_delim=block_delim, upper=upper); print(h2)
        for i in range(max(len(h),len(h2))):
            x = None; y = None
            if i < len(h):
                x = h[i]
            if i < len(h2):
                y = h2[i]
            if x == y:
                print(' ', end='')
            else:
                print(diff_symbol, end='')
        print()

# main function
def main():
    if len(argv) not in {2,3} or '-h' in argv or '--help' in argv:
        print("USAGE: %s <baiduyun.uploading.cfg> [other.baiduyun.uploading.cfg]" % argv[0]); exit(1)
    cfg = BaiduNetdiskCfg(argv[1])
    if len(argv) == 2:
        print(cfg.get_hex(bytes_per_block=1))
    else:
        cfg2 = BaiduNetdiskCfg(argv[2])
        cfg.print_diff(cfg2, bytes_per_block=1)

# run from CLI
if __name__ == "__main__":
    main()
