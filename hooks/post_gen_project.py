import glob
import os
import shutil
from os import path


CONDITIONAL_REMOVE_PATHS = [
    "{% if cookiecutter.elastic_beanstalk == 'disabled' %}.ebextensions{% endif %}",
    "{% if cookiecutter.elastic_beanstalk == 'disabled' %}.elasticbeanstalk{% endif %}",
    "{% if cookiecutter.elastic_beanstalk == 'disabled' %}.platform{% endif %}",
    "{% if cookiecutter.docker == 'disabled' %}Dockerfile{% endif %}",
    "{% if cookiecutter.docker == 'disabled' %}.dockerignore{% endif %}",
    "{% if cookiecutter.pre_commit == 'disabled' %}.pre-commit-config.yaml{% endif %}",
    "{% if cookiecutter.django_react == 'disabled' %}config/webpack_loader.py{% endif %}",
    "{% if cookiecutter.django_react == 'disabled' %}nwb.config.js{% endif %}",
    "{% if cookiecutter.django_react == 'disabled' and cookiecutter.sass_bootstrap == 'disabled' %}package.json{% endif %}",
]


def main():
    delete_conditional_paths()
    delete_empty_files()
    print_next_steps()


def delete_conditional_paths():
    for path in CONDITIONAL_REMOVE_PATHS:
        if path and os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)


def delete_empty_files():
    exempt_files = ["__init__.py"]
    file_paths = glob.glob("**", recursive=True)

    for file_path in file_paths:
        if not path.isfile(file_path):
            continue
        if path.split(file_path)[-1] in exempt_files:
            continue
        with open(file_path, 'r') as file:
            try:
                contents = file.read()
            except UnicodeDecodeError:
                pass
        if not contents.strip():
            os.remove(file_path)


def print_next_steps():
    print("\n\nWelcome to your new project.")
    print("\ncd {{cookiecutter.project_slug}}")
    print("Then set up a virtual environment (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment)")
    print("Then run the following commands:\n")
    commands = [
        "pip install pip-tools",
        "pip-compile requirements.txt --upgrade",
        "pip-compile requirements-dev.txt --upgrade",
        "pip install -r requirements-dev.txt",
        "cp config/.env.example config/.env",
        "python manage.py makemigrations",
    ]
    if "{{ cookiecutter.elastic_beanstalk }}".lower() == "enabled":
        commands.append("git add --chmod=+x -- .platform/*/*/*.sh")
    if "{{ cookiecutter.django_react }}".lower() == "enabled":
        commands.append("npm install")
    for command in commands:
        print(command)


if __name__ == "__main__":
    main()
