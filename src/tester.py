import os
import subprocess
import sys
import filecmp
import glob
from time import time
import platform
import shutil
from colorama import Fore, Style

if platform.system() == "Linux":
    import resource

def set_memory_limit(memory_limit_mb):
        if platform.system() == "Linux":
            memory_limit_bytes = memory_limit_mb * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))

def run_tests(program_name, program_dir, language, time_limit, memory_limit):
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    INPUT_FILES = os.path.join(BASE_DIR, "test_cases", f"{program_name}_tests", "input*.txt")
    OUTPUT_FILES = os.path.join(BASE_DIR, "test_cases", f"{program_name}_tests", "output*.txt")
    RESULTS_DIR = os.path.join(BASE_DIR, "test_cases", f"{program_name}_tests", "actual_results")

    shutil.rmtree(RESULTS_DIR, ignore_errors=True)
    os.makedirs(RESULTS_DIR, exist_ok=False)

    print("Actual output results will be stored at:", RESULTS_DIR)

    input_files = sorted(glob.glob(INPUT_FILES), key=lambda x: int(os.path.basename(x).split("input")[1].split(".")[0]))
    output_files = sorted(glob.glob(OUTPUT_FILES), key=lambda x: int(os.path.basename(x).split("output")[1].split(".")[0]))

    if not input_files or not output_files:
        print(f"{Fore.RED}❌{Style.RESET_ALL} No test files found for {program_name}!")
        return

    if len(input_files) != len(output_files):
        print(f"{Fore.RED}❌{Style.RESET_ALL} Mismatch in number of input and output files for {program_name}!{Style.RESET_ALL}")
        sys.exit(1)

    correct = 0
    total = 0
    all_passed = True

    for input_file, expected_output_file in zip(input_files, output_files):
        test_number = os.path.basename(input_file).split(".")[0].split("input")[1]
        actual_output_file = os.path.join(RESULTS_DIR, f"output{test_number}.txt")

        command = []
        if language == 'c' or language == 'cpp':
            command = [f'./{program_name}.o']
        elif language == 'java':
            command = ['java', '-cp', '.', f'{program_name}']
        elif language == 'python':
            command = ['python3', f'{program_name}.py']

        try:
            start_time = time()
            with open(input_file, "r") as infile, open(actual_output_file, "w") as outfile:
                rst = subprocess.run(
                        command, 
                        cwd=program_dir, 
                        stdin=infile, 
                        stdout=outfile, 
                        stderr=subprocess.PIPE, 
                        timeout=time_limit, 
                        preexec_fn=lambda: set_memory_limit(memory_limit)
                    )
                if rst.stderr:
                    print(f"{Fore.YELLOW}⚠ {Style.RESET_ALL} Test case {test_number}: Program wrote to stderr:", rst.stderr.decode('utf-8'))
                    all_passed = False
                    total += 1
                    continue

                if rst.returncode == 139:
                    print(f"{Fore.RED}❌{Style.RESET_ALL} Segmentation Fault in Test {test_number}!")
                    all_passed = False
                    total += 1
                    continue
            
            elapsed_time = time() - start_time

            if filecmp.cmp(expected_output_file, actual_output_file, shallow=False):
                print(f"{Fore.GREEN}✔ {Style.RESET_ALL} Test {test_number} passed in {round(elapsed_time, 2)}s!")
                correct += 1
                total += 1
            else:
                print(f"{Fore.RED}❌{Style.RESET_ALL} Test {test_number} failed! Wrong answer!")
                with open(expected_output_file, 'r') as expected_file, open(actual_output_file, 'r') as actual_file:
                    expected_content = expected_file.read()
                    actual_content = actual_file.read()
                    print(f"{Fore.YELLOW}Expected: {expected_content}{Style.RESET_ALL}")
                    print(f"{Fore.CYAN}Actual: {actual_content}{Style.RESET_ALL}")
                all_passed = False
                total += 1
                all_passed = False

        except subprocess.CalledProcessError as e:
            elapsed_time = time() - start_time
            print(f"{Fore.RED}❌{Style.RESET_ALL} Test {test_number} crashed!{Style.RESET_ALL}")
            print(f"{Fore.RED}Error: {Style.RESET_ALL} {e.stderr.decode('utf-8')}{Style.RESET_ALL}")
            all_passed = False
            total += 1

        except subprocess.TimeoutExpired:
            elapsed_time = time() - start_time
            print(f"{Fore.RED}❌{Style.RESET_ALL} Test {test_number} exceeded time limit of {time_limit} seconds! (Runtime: {elapsed_time}s){Style.RESET_ALL}")
            all_passed = False
            total += 1

        except MemoryError:
            print(f"{Fore.RED}❌{Style.RESET_ALL} Test {test_number} exceeded memory limit of {memory_limit} MB!{Style.RESET_ALL}")
            all_passed = False
            total += 1

        except FileNotFoundError:
            print(f"{Fore.YELLOW}⚠ {Style.RESET_ALL} File not found for {program_name}. Ensure {input_file} or {expected_output_file} exists.{Style.RESET_ALL}")
            raise

        except Exception as e:
            print(f"{Fore.RED}❌{Style.RESET_ALL} Test {test_number} failed due to an unexpected error!")
            print(f"     Error: {e}")
            all_passed = False
            total += 1

    if all_passed:
        print(f"{Fore.GREEN}✅{Style.RESET_ALL} All tests passed for {program_name}! ({correct}/{total} passed)")
    else:
        print(f"{Fore.RED}❌{Style.RESET_ALL} Some tests failed for {program_name}. ({correct}/{total} passed){Style.RESET_ALL}")

if __name__ == "__main__":
    if not os.path.exists("venv"):
        os.system("python3 -m venv venv") # Check if venv exists, if not create it
    os.system("source venv/bin/activate && pip show colorama > /dev/null || pip install colorama") # Install colorama if not installed

