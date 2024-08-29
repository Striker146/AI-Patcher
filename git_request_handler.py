from github import Github, Auth
import git
import os
import shutil
import glob
import builder

def delete_files(path):
    os.chmod(path, 0o777)
    for dir in os.listdir(path):
        shutil.rmtree(path)
branches_dir = "branches/"

delete_files(branches_dir)





target_filename = "vinca_linux_64.yaml"

repo_name = "Striker146/ros-humble-github-actions"
auth_token_file = open("auth_token.txt")
auth_token_str = auth_token_file.read()
local_repo_dir = "ros-humble-github-actions/"


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
pr_repo = git.Repo.clone_from(clone_url, pr_directory)



files_changed = pr[0].get_files()


target_file = next(filter(lambda f: f.filename == target_filename, files_changed), None)

if target_file:
    arg_list = ['-s', pr_directory]
    builder.main()


g.close()