import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.compiler import compile_program
from src.tester import run_tests

LANGUAGE_EXTENSIONS = {
    "c": "c",
    "cpp": "cpp",
    "java": "java",
    "py": "python",
}

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <path_to_program> [<time_limit>] [<memory_limit>]")
        sys.exit(1)
    
    # Extract the path to the program
    program_path = os.path.abspath(sys.argv[1])
    
    # Extract directory, full filename, and split out name + extension
    program_dir = os.path.dirname(program_path)
    program_file = os.path.basename(program_path)
    program_name, program_ext = os.path.splitext(program_file)

    # Ensure the language is recognized
    ext_no_dot = program_ext.replace('.', '')  # eg. ".java" -> "java"
    try:
        language = LANGUAGE_EXTENSIONS[ext_no_dot.lower()]
    except KeyError:
        print("Unsupported language or invalid file extension!")
        sys.exit(1)

    # If time_limit is provided, parse it; otherwise use default=12
    if len(sys.argv) >= 3:
        time_limit = float(sys.argv[2])
    else:
        time_limit = 12

    # If memory_limit is provided, parse it; otherwise use default=128
    if len(sys.argv) >= 4:
        memory_limit = int(sys.argv[3])
    else:
        memory_limit = 128

    # Compile the program
    compile_program(program_path, language)
    
    # Run tests with the specified or default time/memory limits
    run_tests(program_name, program_dir, language, time_limit=time_limit, memory_limit=memory_limit)

if __name__ == "__main__":
    main()

