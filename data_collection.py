import sys
import subprocess

python_executable = sys.executable

def run_scripts():
    scripts = [
        "processing/scrape_iits.py",
        "processing/scrape_nits.py",
        "data_cleaner.py"
        "db_connect.py"
    ]

    for script in scripts:
        print(f"Running: {script}")
        result = subprocess.run([python_executable, script], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        if result.returncode != 0:
            print(f"Error encountered in {script}. Stopping execution.")
            break
if __name__ == "__main__":
    run_scripts()

