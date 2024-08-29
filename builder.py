from subprocess import Popen
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-s', '--source', type=str, default="ros-humble", help="Directory of robostack")

    args = parser.parse_args()

    br = Popen(f"ros_build_recipes.bat {args.source}")
    #bp = Popen("ros_build_packages.bat")
    input("Press any key to continue")
    
#p = Popen("ros_build_recipes.bat", cwd=r"./")
#stdout, stderr = p.communicate()


if __name__ =="__main__":
    main()