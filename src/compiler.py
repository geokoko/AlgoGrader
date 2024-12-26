import subprocess
import os
import sys

def compile_program(source_file, language):
    """
    Compile a source file into an executable file.
    Supported languages: C, C++, Java.
    """
    try:
        if language == "c":
            subprocess.run(["gcc", source_file, "-o", f"{source_file.split('.')[0]}.o"], check=True)
        elif language == "cpp":
            subprocess.run(["g++", source_file, "-o", f"{source_file.split('.')[0]}.o"], check=True)
        elif language == "java":
            subprocess.run(["javac", source_file], check=True)
        else:
            print(f"Unsupported language: {language}")
            sys.exit(1)

    except subprocess.CalledProcessError:
        print(f"Failed to compile {source_file}!")
        sys.exit(1)

