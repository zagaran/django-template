import glob
import os
from os import path


def main():
    delete_empty_files()
    print_next_steps()


def delete_empty_files():
    exempt_files = ["__init__.py"]
    file_paths = glob.glob("**", recursive=True) 

    for file_path in file_paths:
        if not path.isfile(file_path):
            continue
        if path.split(file_path)[-1] in exempt_files:
            continue
        with open(file_path, 'r') as file:
            contents = file.read()
        if not contents.strip():
            os.remove(file_path)


def print_next_steps():
    print("\n\nWelcome to your new project.")
    print("\ncd {{cookiecutter.project_slug}}")
    print("Then set up a virtual environment (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)")
    print("Then run the following commands:\n")
    commands = [
        "pip install pip-tools"
        "pip-compile --upgrade",
        "pip install -r requirements.txt",
        "cp config/.env.example config/.env",
        "python manage.py makemigrations",
    ]
    if "{{ cookiecutter.django_react }}".lower() == "enabled":
        commands.append("npm install -g npm-check-updates")
    for command in commands:
        print(command)


if __name__ == "__main__":
    main()