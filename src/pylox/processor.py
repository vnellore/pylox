import sys
from os import path
from pylox.scanner import Scanner

had_error = False

def run_prompt():
    print("Running in interactive mode")

def run_file(filePath):
    if (path.exists(filePath)):
        with open(filePath) as file:
            content = file.read()
            run(content)
            if (had_error):
                sys.exit("Error in code")
    else:
        print("Invalid file path specified!")

def run(file_contents):
    scannr = Scanner(file_contents)
    tokens = scannr.scanTokens()
    print(tokens)

def error(line, message):
    report(line, "", message)

def report(line, where, message):
    print(f"[line {line} Error: {where} : {message}]")
    had_error = True

def process():
    if (len(sys.argv) > 2):
        print("Usage: pylox [script]")
    elif (len(sys.argv) == 2):
        run_file(sys.argv[1])
    else:
        run_prompt()
