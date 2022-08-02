from interpreter.interpreter import interpreter
import glob as g
import sys
import json as js

# A directory containing the provided examples
EXAMPLES_DIR = "src/interpreter/examples/"

def json_to_data(file):
    """
        read a Json file and load it as a dictionary.
        return a dictionary containing all Json data.
    """
    f = open(file)
    return js.load(f)

def extract_body(data):
    return data["program"]["body"]
    
def program_info():
    print("\nProgram informations!\n"+
          "To run this program, you need to choose one of these options:\n"+
            "ex\t: to execute a file provided in the directory of the examples 'ast_examples'\n"+
            "f\t: to run from any (.json or .js) file. This file must be added in the './own_files' folder(which is in the root of the project).\n")

def program_failed_message():
    print("\nProgram Failed! Please choose one of these options:\n"+
              "ex\t: to execute a file provided in the directory of the examples 'ast_examples'\n"+
              "f\t: to run from any .json file. This file must be added in the './own_files' folder(which is in the root of the project).\n")

def max_file_name_lentgh(sub_files):
    return max([len(f) for f in sub_files])
            
def show_files(dir):
    files = [file[file.rindex('/')+1:] for file in g.glob(dir + "*.json")]
    n = len(files)
    def extension(files):
        files.sort(key=lambda x: int(x[:x.index('-')])) 
        ch = "\nHere is the list of the existing(.json) examples:\n\n"
        return ch 
    ch = extension(files)
    if n==1:
        return ch+files[n-1]+"\n"
    for i in range(0, n//2):
        cmp = i
        while cmp < n:                             
            ch += files[cmp] + (max_file_name_lentgh(files[cmp-i: (cmp-i)+n//2])-len(files[cmp])+2)*' '
            cmp += n//2        
        ch += '\n'       
    return ch

files_shown = False

def main():  
    global files_shown
    if not files_shown:
        print(show_files(EXAMPLES_DIR))   
        files_shown = True  
    dir = EXAMPLES_DIR          
    file_name = input('\nEnter file name: ') 
    file_path = dir + file_name.strip(" ")  
    try:
        data = json_to_data(file_path)
        body = extract_body(data)
        print("\nInterpreting... Please wait ...\n-------\n") 
        print(interpreter(body))
    except FileNotFoundError:
        print("\n------------ Error --------------")
        print("Error: file not found! Enter one of the displayed files!")
        print("---------------------------------")
        main()      
if __name__ == "__main__":
    main()

