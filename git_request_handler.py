from github import Github, Auth
import git
import os
from subprocess import Popen
import shutil
import glob
import builder
from time import sleep

branches_dir = "branches/"


def insert_after_category(file_path, category_name, added_insert):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if category_name in line:
            # Insert the URL on the next line
            lines.insert(i + 1, added_insert + '\n')
            break

    with open(file_path, 'w') as file:
        file.writelines(lines)



skip_existing_flag = "  - /home/ryan/bld_work"
target_filename = "vinca_linux_64.yaml"

repo_name = "Striker146/ros-humble-github-actions"
auth_token_file = open("auth_token.txt")
auth_token_str = auth_token_file.read()
local_repo_dir = "ros-humble-github-actions"


auth = Auth.Token(auth_token_str)

g = Github(auth=auth)

repo = g.get_repo(repo_name)


pr = list(repo.get_pulls(state='open'))

branch_name = pr[0].head.ref
branch_repo = pr[0].head.repo.full_name





clone_url = f"https://github.com/{branch_repo}.git"

repo_local = git.Repo(local_repo_dir)
repo_local.git.checkout(branch_name)
repo_local.remotes.origin.pull(branch_name)

pr_directory = f"{branches_dir}{branch_name}"

if os.path.exists(pr_directory):
    Popen(f"path_remover.bat {pr_directory.replace("/","\\")}")
    sleep(0.5)

print(pr_directory)
pr_repo = git.Repo.clone_from(clone_url, pr_directory)


files_changed = pr[0].get_files()


target_file = next(filter(lambda f: f.filename == target_filename, files_changed), None)

if target_file:
    source_vinca = f"{pr_directory}/{target_file.filename}"
    target_vinca = f"{local_repo_dir}/{"vinca.yaml"}"
    recipes_dir = f"{local_repo_dir}/recipes"
    if os.path.isfile(target_vinca):
        os.remove(target_vinca)
    shutil.copyfile(source_vinca, target_vinca)
    #insert_after_category(target_vinca,"skip_existing:", skip_existing_flag)

    arg_list = ['-s', local_repo_dir]
    parser = builder.get_argparser()
    args =  parser.parse_args(arg_list)
+    builder.main(args)


g.close()