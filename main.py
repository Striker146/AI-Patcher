import requests
import json
import re
from tkinter.filedialog import askopenfilename

print("hello world")


def generate_response(prompt):
    data = {"model":"llama3", "role": "system", "prompt":prompt, "stream": False}
    url = 'http://localhost:11434/api/generate'

    response = requests.post(url, json=data)
    response_json = response.json()
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(F"Failed to get prompt. Got Error {response.status_code}")
    



def generate_repair(file_path,error_path):
    file = open(file_path)
    file_read = file.read()
    error = open(error_path)
    error_read = error.read()
    file.close()
    error.close()
    prompt = f"Generate a new repaired patch. Here is the unix Patch code {file_read}. The error is {error_read}."
    return generate_response(prompt), prompt

def extract_response_code(text):
    code_blocks = re.findall(r'```\s*(.*?)\s*```\n', text, re.DOTALL)
    patch_code = ''
    for block in code_blocks:
        lines = block.split('\n')
        for line in lines:
            patch_code += line + '\n'
    return patch_code

def create_patch():
    print("Patch File: ", end="")
    patch_path = askopenfilename()
    print(f"'{patch_path}'")
    
    print("Error File: ", end="")
    error_path = askopenfilename()
    print(f"'{error_path}'")

    print("Creating patch...")
    repair_response, prompt = generate_repair(patch_path,error_path)

    repaired_patch = extract_response_code(repair_response["response"])
    repaired_file = open("new_patch.txt", "w")
    repaired_file.write(repaired_patch)
    print(f"Patch completed. The filename is '{repaired_file.name}'")
    repaired_file.close()
    


while(1):
    print("1: Generate a new Patch")
    print("2: Exit")
    user_inp = input("Choose an operation: ")
    if user_inp == "1":
        print(":tes")
        create_patch()
    elif user_inp == "2":
        print("Closing...")
        break