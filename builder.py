from subprocess import Popen
import argparse
import os


def get_argparser():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-s', '--source', type=str, default="ros-humble", help="Directory of robostack")
    return parser

def main(args):
    br = Popen(f"ros_build_recipes.bat {args.source}")
    #bp = Popen("ros_build_packages.bat")

    input("Press any key to continue")




if __name__ =="__main__":
    parser = get_argparser()
    args = parser.parse_args()
    main(args)