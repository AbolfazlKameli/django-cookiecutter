import os
import subprocess


def run_git_init():
    project_dir = os.path.join(os.getcwd())
    os.chdir(project_dir)
    subprocess.run(['git', 'init'], check=True)


if __name__ == "__main__":
    run_git_init()
