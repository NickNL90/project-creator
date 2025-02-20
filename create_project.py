import os
import sys
import subprocess
import json

def ensure_code_in_path():
    """Checks if VS Code is installed and the 'code' command is available."""
    try:
        subprocess.run(["which", "code"], check=True, capture_output=True)
        print("✅ VS Code 'code' command is available!")
    except subprocess.CalledProcessError:
        print("⚠️ VS Code 'code' command not found. Open VS Code en run:")
        print("   'Shell Command: Install \"code\" command in PATH'")

def open_vs_code(project_path, main_file=None):
    """Opens the project in VS Code and ensures the terminal starts with the virtual environment."""
    print("🚀 Opening VS Code with the project directory...")
    try:
        subprocess.run(["code", "--new-window", project_path], check=True)
        if main_file:
            subprocess.run(["code", project_path, "-g", main_file], check=True)
        else:
            subprocess.run(["code", project_path], check=True)
    except FileNotFoundError:
        print("⚠️ 'code' command not found. Ensure VS Code is correctly installed.")

    print("🔹 Open VS Code's terminal (Ctrl+`) and it should automatically activate the virtual environment.")

def setup_vscode_settings(project_path, venv_path):
    """Configures VS Code to automatically activate the virtual environment."""
    vscode_dir = os.path.join(project_path, ".vscode")  # VS Code moet in de root blijven
    os.makedirs(vscode_dir, exist_ok=True)

    settings_json_path = os.path.join(vscode_dir, "settings.json")

    python_path = os.path.join(venv_path, "bin", "python")
    if os.path.exists(python_path):
        python_path = os.path.realpath(python_path)  # Zorgt dat de venv écht wordt gebruikt
    else:
        python_path = sys.executable  # Fallback naar systeem-Python als de venv faalt

    settings_json_content = {
        "python.defaultInterpreterPath": python_path,
        "python.terminal.activateEnvironment": True,
        "terminal.integrated.defaultProfile.osx": "PythonVenv",
        "terminal.integrated.defaultProfile.linux": "PythonVenv",
        "terminal.integrated.defaultProfile.windows": "PythonVenv",
        "terminal.integrated.env.osx": {
            "VIRTUAL_ENV": venv_path,
            "PATH": f"{venv_path}/bin:$PATH"
        },
        "terminal.integrated.env.linux": {
            "VIRTUAL_ENV": venv_path,
            "PATH": f"{venv_path}/bin:$PATH"
        },
        "terminal.integrated.env.windows": {
            "VIRTUAL_ENV": venv_path,
            "PATH": f"{venv_path}\\Scripts;$PATH"
        }
    }

    try:
        with open(settings_json_path, "w") as settings_json_file:
            json.dump(settings_json_content, settings_json_file, indent=4)
        print(f"✅ VS Code settings.json updated at: {settings_json_path}")
    except Exception as e:
        print(f"❌ Error creating settings.json file: {e}")

def create_project(project_name):
    """Creates a new project with a virtual environment and VS Code settings."""
    if not project_name:
        print("❌ Project name is required.")
        return

    print(f"🚀 Creating project: {project_name}")

    home_dir = os.path.expanduser("~")
    projects_dir = os.path.join(home_dir, "PythonProjects")
    project_path = os.path.join(projects_dir, project_name)
    config_dir = os.path.join(project_path, "config")

    os.makedirs(project_path, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)
    os.chdir(project_path)

    print(f"✅ Project directory created at {project_path}")

    # Create virtual environment
    venv_path = os.path.join(project_path, ".venv")
    print(f"🔧 Creating virtual environment at: {venv_path}")

    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment successfully created!")
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment.")
        return

    # Set up VS Code settings
    setup_vscode_settings(project_path, venv_path)

    # Initialize Git repository
    if subprocess.run(["git", "--version"], check=False).returncode == 0:
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized!")

    # Create .gitignore
    gitignore_content = ".venv/\n__pycache__/\n*.pyc\n.DS_Store\n.vscode/"
    with open(os.path.join(project_path, ".gitignore"), "w") as f:
        f.write(gitignore_content)
    print("✅ .gitignore file created!")

    # Create README.md
    with open(os.path.join(project_path, "README.md"), "w") as f:
        f.write(f"# {project_name}\n\n🚀 Welcome to your new Python project!")
    print("✅ README.md created!")

    # Create requirements.txt
    with open(os.path.join(project_path, "requirements.txt"), "w") as f:
        f.write("# pips your project requires.\n")
    print("✅ requirements.txt created!")

    # Create main.py
    main_file = os.path.join(project_path, "main.py")
    main_py_content = f'''\
def main():
    print("Happy coding! Good luck with your project {project_name}.")

if __name__ == "__main__":
    main()
'''
    with open(main_file, "w") as f:
        f.write(main_py_content)
    print("✅ main.py created!")

    # Move dev config files to config/
    with open(os.path.join(config_dir, ".editorconfig"), "w") as f:
        f.write("root = true\n[*]\nindent_style = space\nindent_size = 4\n")
    print("✅ .editorconfig created in config/")

    with open(os.path.join(config_dir, "Makefile"), "w") as f:
        f.write("install:\n\tpip install -r requirements.txt\n\nrun:\n\tpython main.py\n")
    print("✅ Makefile created in config/")

    with open(os.path.join(config_dir, "pyproject.toml"), "w") as f:
        f.write(f"""\
[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = "A new Python project"
authors = ["Your Name <your.email@example.com>"]
""")
    print("✅ pyproject.toml created in config/")

    # Open in VS Code en direct de terminal in de venv starten
    ensure_code_in_path()
    open_vs_code(project_path, main_file)

    print("\n🎉 Project successfully created and virtual environment is set up! 🚀")
    print("🔹 Open a new terminal in VS Code, and your environment should be activated automatically.")

def create_alias():
    """Creates the alias for pyproject and reloads the shell configuration."""
    home = os.path.expanduser("~")

    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        shell_config = os.path.join(home, ".zshrc") if os.path.exists(os.path.join(home, ".zshrc")) else os.path.join(home, ".bashrc")
        alias_command = 'alias pyproject="python3 ~/PythonProjects/project-creator/create_project.py"'

        try:
            # Controleer of de alias al bestaat
            with open(shell_config, "r") as file:
                if alias_command in file.read():
                    print("✅ Alias 'pyproject' is al ingesteld.")
                    return

            # Alias toevoegen aan het configuratiebestand
            with open(shell_config, "a") as file:
                file.write(f"\n{alias_command}\n")

            print("🔄 Herladen van shell configuratie...")

            # 🚀 Forceer herladen van de shell-instellingen zonder subprocess source-issue
            subprocess.run(f"exec $SHELL", shell=True, executable="/bin/bash")

            # ✅ Controleer of de alias direct actief is
            test_alias = subprocess.run("command -v pyproject", shell=True, capture_output=True, text=True)
            if test_alias.returncode == 0:
                print("✅ Alias 'pyproject' is direct actief! 🚀")
            else:
                print("⚠️ Alias is toegevoegd, maar lijkt niet direct actief. Open een nieuwe terminal en test opnieuw.")

        except Exception as e:
            print(f"❌ Error creating alias: {e}")

    elif sys.platform == "win32":
        alias_command = 'doskey pyproject=python3 %USERPROFILE%\\PythonProjects\\project-creator\\create_project.py $*'
        persistent_alias = 'setx PYPROJECT_PATH "python3 %USERPROFILE%\\PythonProjects\\project-creator\\create_project.py"'

        try:
            # ✅ Zet de alias tijdelijk in de huidige sessie
            subprocess.run(alias_command, shell=True, executable="cmd.exe")

            # ✅ Maak de alias persistent (bij herstart nog steeds actief)
            subprocess.run(persistent_alias, shell=True, executable="cmd.exe")

            print("🔄 Herladen van Windows omgevingsvariabelen...")
            subprocess.run("refreshenv", shell=True, executable="cmd.exe")

            # ✅ Controleer of de alias direct actief is
            test_command = "where pyproject"
            test_alias = subprocess.run(test_command, shell=True, capture_output=True, text=True)

            if test_alias.returncode == 0:
                print("✅ Alias 'pyproject' is direct actief! 🚀")
            else:
                print("⚠️ Alias is toegevoegd, maar lijkt niet direct actief. Open een nieuwe terminal en test opnieuw.")

        except Exception as e:
            print(f"❌ Error creating alias on Windows: {e}")

def uninstall_pyproject():
    """Removes the alias and script completely."""
    home = os.path.expanduser("~")
    shell_config = os.path.join(home, ".zshrc") if os.path.exists(os.path.join(home, ".zshrc")) else os.path.join(home, ".bashrc")
    alias_command = 'alias pyproject="python3 ~/PythonProjects/project-creator/create_project.py"'

    try:
        if os.path.exists(shell_config):
            with open(shell_config, "r") as file:
                lines = file.readlines()
            with open(shell_config, "w") as file:
                file.writelines(line for line in lines if alias_command not in line)

        subprocess.run(f"source {shell_config}", shell=True)
        print("✅ 'pyproject' alias succesvol verwijderd! 🚀")

    except Exception as e:
        print(f"❌ Fout bij het verwijderen van pyproject: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        create_alias()
    elif sys.argv[1] == '--uninstall':
        uninstall_pyproject()
    else:
        create_project(sys.argv[1])