import os
import subprocess
import sys
import filecmp
import glob
from time import time
import platform
import shutil

if platform.system() == "Linux":
    import resource

def set_memory_limit(memory_limit_mb):
    """Set memory limit for subprocess execution."""
    if platform.system() == "Linux":
        memory_limit_bytes = memory_limit_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (memory_limit_bytes, memory_limit_bytes))

def run_tests(program_name, program_dir, language, time_limit, memory_limit):
    """
    Run tests for a program and compare the output with expected output.
    Arguments:
        program_name -- the name of the program to test
        language -- the language of the program (c, cpp, java, python)
        time_limit -- the time limit for each test case
        memory_limit -- the memory limit for each test case
    """

    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    INPUT_FILES = os.path.join(BASE_DIR, "test_cases", f"{program_name}_tests", "input*.txt")
    OUTPUT_FILES = os.path.join(BASE_DIR, "test_cases", f"{program_name}_tests", "output*.txt")
    RESULTS_DIR = os.path.join(BASE_DIR, "test_cases", f"{program_name}_tests", "actual_results")

    shutil.rmtree(RESULTS_DIR, ignore_errors=True)
    os.makedirs(RESULTS_DIR, exist_ok=False)

    input_files = sorted(glob.glob(INPUT_FILES), key=lambda x: int(os.path.basename(x).split("input")[1].split(".")[0]))
    output_files = sorted(glob.glob(OUTPUT_FILES), key=lambda x: int(os.path.basename(x).split("output")[1].split(".")[0]))

    for file in input_files:
        print(f"Checking: {file}, Exists? {os.path.exists(file)}")

    if not input_files or not output_files:
        print(f"❌ No test files found for {program_name}!")
        return

    if len(input_files) != len(output_files):
        print(f"❌ Mismatch in number of input and output files for {program_name}!")
        sys.exit(1)

    correct = 0
    total = 0
    all_passed = True  # Start assuming all tests will pass

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

        print(f"Running test {test_number} for {program_name}...")

        try:
            start_time = time()
            with open(input_file, "r") as infile, open(actual_output_file, "w") as outfile:
                subprocess.run(
                        command, 
                        cwd=program_dir, 
                        stdin=infile, 
                        stdout=outfile, 
                        stderr=subprocess.PIPE, 
                        timeout=time_limit, 
                        preexec_fn=lambda: set_memory_limit(memory_limit)
                    )   
            
            elapsed_time = time() - start_time

            if filecmp.cmp(expected_output_file, actual_output_file, shallow=False):
                print(f"  ✅ Test {test_number} passed in {elapsed_time}s!")
                correct += 1
                total += 1
            else:
                print(f"  ❌ Test {test_number} failed! Wrong answer!")
                print(f"     Expected output: {expected_output_file}", end="\t")
                print(f"     Actual output: {actual_output_file}")
                total += 1
                all_passed = False

        except subprocess.CalledProcessError as e:
            elapsed_time = time() - start_time
            print(f"  ❌ Test {test_number} crashed!")
            print(f"     Error: {e.stderr.decode('utf-8')}")
            all_passed = False
            total += 1

        except subprocess.TimeoutExpired:
            elapsed_time = time() - start_time
            print(f"  ❌ Test {test_number} exceeded time limit of {time_limit} seconds! (Runtime: {elapsed_time}s)")
            all_passed = False
            total += 1

        except MemoryError:
            print(f"  ❌ Test {test_number} exceeded memory limit of {memory_limit} MB!")
            all_passed = False
            total += 1

        except FileNotFoundError:
            print(f"  ⚠️ File not found for {program_name}. Ensure {input_file} or {expected_output_file} exists.")
            raise
            sys.exit(1)

        except Exception as e:
            print(f"  ❌ Test {test_number} failed due to an unexpected error!")
            print(f"     Error: {e}")
            all_passed = False
            total += 1

    if all_passed:
        print(f"✅ All tests passed for {program_name}! ({correct}/{total} passed)")
    else:
        print(f"❌ Some tests failed for {program_name}. ({correct}/{total} passed)")
