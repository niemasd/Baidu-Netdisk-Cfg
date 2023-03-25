#! /usr/bin/env python3
from base64 import b64decode
from os.path import isdir, isfile
from sys import argv

# helper class to represent Baidu Netdisk CFG files
class BaiduNetdiskCfg:
    # create object from cfg path
    def __init__(self, cfg):
        if isfile(cfg) and cfg.lower().endswith('.cfg'):
            self.data_b64 = open(cfg).read()
        else:
            raise ValueError("Invalid cfg: %s" % cfg)
        self.data = b64decode(self.data_b64)

    # return length of Base64-decoded data
    def __len__(self):
        return len(self.data)

# main function
def main():
    if len(argv) != 2 or '-h' in argv or '--help' in argv:
        print("USAGE: %s <baiduyun.uploading.cfg>" % argv[0]); exit(1)
    cfg = BaiduNetdiskCfg(argv[1])

# run from CLI
if __name__ == "__main__":
    main()
