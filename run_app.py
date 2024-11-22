import subprocess
from concurrent.futures import ThreadPoolExecutor

def run_command(command, cwd):
    """Run a subprocess command."""
    subprocess.run(command, cwd=cwd, check=True)

# Commands to run
commands = [
    {"command": ["poetry", "run", "python", "run_scraper.py"], "cwd": "scraper"},
    {"command": ["poetry", "run", "python", "main.py"], "cwd": "server"},
]

# Execute commands in parallel
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(run_command, cmd["command"], cmd["cwd"]) for cmd in commands]

    # Wait for all commands to complete
    for future in futures:
        try:
            future.result()  # Will raise an exception if the command failed
        except subprocess.CalledProcessError as e:
            print(f"Command failed with error: {e}")
