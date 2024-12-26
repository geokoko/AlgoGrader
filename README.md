# AlgoGrader
This is a simple tool designed for algorithmic testing. It supports multiple programming languages, enforces time and memory limits, and compares actual output with expected output for correctness.

## Installation
Clone the repository:
```bash
git clone https://github.com/geokoko/AlgoGrader.git
cd AlgoGrader
```

## Usage
To run the program, use the following command:
```bash
python3 main.py <program_path> [<time_limit>] [<memory_limit>] 
```

### Arguments
- `program_path`: The path to the program you want to test.

Optional arguments:
- `time_limit`: The time limit in seconds. Default is 12 seconds.
- `memory_limit`: The memory limit in megabytes. Default is 128 megabytes.


## Test Case Format
1. Input files should be named `input<i>.txt`, where `i` is the test case number.
2. Expected output files should be named `output<i>.txt`, where `i` is the test case number.
3. Actual results are stored in the `actual_results\` directory automatically during execution.
