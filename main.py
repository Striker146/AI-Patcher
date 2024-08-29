import requests
import json
import re
from tkinter.filedialog import askopenfilename
from time import sleep
import tkinter as tk
from time import time
import argparse

print("hello world")
root = tk.Tk()
root.withdraw()

def generate_response(prompt):
    data = {"model":"llama3", "role": "system", "prompt":prompt, "stream": False}
    url = 'http://localhost:11434/api/generate'

    response = requests.post(url, json=data)
    response_json = response.json()
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(F"Failed to get prompt. Got Error {response.status_code}")
    



def generate_repair(error, script=None,patch=None):

    if not script == None:
        script_prompt = f"Here is the relevant script ```{script}```. "
    else:
        script_prompt = ""
    
    if not patch == None:
        patch_prompt = f"Here is the existing unix Patch code ```{patch}```. "
    else:
        patch_prompt = ""
    
    error_prompt = f"The error is that is causing the build to fail is ```{error}```. "
    
    prompt = "generate a new repaired patch from the provided data. " + error_prompt + patch_prompt + script_prompt

    
    
    return generate_response(prompt), prompt



def extract_response_code(text):
    code_blocks = re.findall(r'```\s*(.*?)\s*```\n', text, re.DOTALL)
    patch_code = ''
    for block in code_blocks:
        lines = block.split('\n')
        for line in lines:
            patch_code += line + '\n'
    return patch_code

def create_patch(error_file, patch_file=None, script_file=None):
    """
    print("Give any relevant Files")
    print("Relevant Script File: ", end="")
    script_path = askopenfilename()
    print(f"'{script_path}'")
    
    print("Error logs")
    print("Error File: ", end="")
    error_path = askopenfilename()
    print(f"'{error_path}'")
    
    print("Existing Patch File")
    print("Existing Patch File: ", end="")
    patch_path = askopenfilename()
    print(f"'{patch_path}'")
    """
    


    print("Creating patch...")
    repair_response, prompt = generate_repair(script=script_file, error=error_file,patch=patch_file)
    print(repair_response["response"])
    repaired_patch = extract_response_code(repair_response["response"])
    repaired_file = open("new_patch.txt", "w")
    repaired_file.write(repaired_patch)
    print(f"Patch completed. The filename is '{repaired_file.name}'")
    repaired_file.close()


    
def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process error and patch files.")

    # Add a required argument for the error file
    parser.add_argument(
        "-e", "--errorfile", 
        required=False, 
        type=str, 
        default="etest.txt",
        help="Path to the error file"
    )

    # Add an optional argument for the patch file
    parser.add_argument(
        "-p", "--patchfile", 
        required=False, 
        type=str,
        default="test.txt", 
        help="Path to the patch file (optional)"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Access the arguments
    error_file = open(args.errorfile,"r",encoding="utf-8").read()
    patch_file = open(args.patchfile,"r",encoding="utf-8").read()
    print(error_file)
    print(patch_file)
    create_patch(error_file=error_file, patch_file=patch_file)


if __name__ == "__main__":
    main()

"""
while(1):
    print("1: Generate a new Patch")
    print("2: Exit")
    user_inp = input("Choose an operation: ")
    if user_inp == "1":
        start_t = time()
        create_patch()
        end_t = time()
    elif user_inp == "2":
        print("Closing...")
        break
    print(f"Time Taken : {round(end_t - start_t)}")
"""