from subprocess import Popen
import os

br = Popen("ros_build_recipes.bat")
bp = Popen("ros_build_packages.bat")




input("Press any key to continue")
#p = Popen("ros_build_recipes.bat", cwd=r"./")
#stdout, stderr = p.communicate()