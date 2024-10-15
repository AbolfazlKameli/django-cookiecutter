import os
import subprocess

project_dir = os.path.join(os.getcwd())


def run_git_init():
    os.chdir(project_dir)
    subprocess.run(['git', 'init'], check=True)


if __name__ == "__main__":
    run_git_init()
