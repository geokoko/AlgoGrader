import os
import sys
import subprocess
from colorama import Fore, Style

def compile_program(source_file, language):
    """
    Compile a source file into an executable file.
    Supported languages: C, C++, Java.
    """

    try:
        if language == "c":
            result = subprocess.run(
                ["gcc", source_file, "-o", f"{os.path.splitext(source_file)[0]}.o", "-std=c11", "-Wall"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        elif language == "cpp":
            result = subprocess.run(
                ["g++", source_file, "-o", f"{os.path.splitext(source_file)[0]}.o", "-std=c++17", "-Wall"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        elif language == "java":
            result = subprocess.run(
                ["javac", source_file],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        else:
            print(f"Unsupported language: {language}")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}❌ Compilation Failed! {Style.RESET_ALL}")
        # Safely handle stderr and stdout
        error_message = e.stderr.decode("utf-8") if e.stderr else "No error details available."
        print(error_message)
        sys.exit(1)

    except FileNotFoundError:
        print(f"{Fore.RED}❌ Compiler not found! Make sure GCC, G++, or Java is installed. {Style.RESET_ALL}")
        sys.exit(1)

