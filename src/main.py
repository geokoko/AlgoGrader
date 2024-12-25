import sys
from compiler import compile_program
from tester import run_tests

LANGUAGE_EXTENSIONS = {
    ".c": "c",
    ".cpp": "cpp",
    ".java": "java",
    ".py": "python",
}

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 main.py <program_file_name> <time_limit> <memory_limit>")
        sys.exit(1)

    try:
        language = LANGUAGE_EXTENSIONS[sys.argv[1].split(".")[1]].lower()
    except KeyError:
        print("Unsupported language!")
        sys.exit(1)

    time_limit = float(sys.argv[2])
    memory_limit = int(sys.argv[3])

    compile_program(sys.argv[1], language)
    run_tests(sys.argv[1].split(".")[0], time_limit, memory_limit)

if __name__ == "__main__":
    main()

