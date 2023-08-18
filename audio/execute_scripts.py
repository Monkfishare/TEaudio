import subprocess

def run_script(script_name):
    try:
        subprocess.run(['python', script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
    else:
        print(f"{script_name} executed successfully.")

if __name__ == "__main__":
    scripts_to_run = ["audio_links.py", "check_accessibility.py"]

    for script in scripts_to_run:
        run_script(script)
