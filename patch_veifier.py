import os
import re

def check(path):
    file = open(path,"rb")
    try:  # catch OSError in case of a one line file 
        file.seek(-2, os.SEEK_END)
        while file.read(1) != b'\n':
            file.seek(-2, os.SEEK_CUR)
    except OSError:
        file.seek(0)
    last_line = file.readline().decode()
    sampled = re.sub(r'[╵\s]', '', last_line)
    return not bool(len(sampled))


"""
def check(path, target):
    file = open(path,"r",encoding="utf-8").read()
    pattern = re.compile(f'Output: {target}.*', re.DOTALL)
    match = pattern.search(file)
    print(match.group())
"""


if __name__ == "__main__":
    path_1 =  "Patches/boa_log_fail.txt"
    path_2 =  "Patches/boa_build_suc.txt"
    target = "ros-humble-hardware-interface"
    build_success = check(path_1)

    print(build_success)