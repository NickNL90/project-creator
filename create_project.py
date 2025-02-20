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
    except FileNotFoundError:
        print("⚠️ 'code' command not found. Ensure VS Code is correctly installed.")

    print("🔹 Open VS Code's terminal (Ctrl+`) and it should automatically activate the virtual environment.")

def setup_vscode_settings(project_path, venv_path):
    """Configures VS Code to automatically activate the virtual environment."""
    vscode_dir = os.path.join(project_path, ".vscode")
    os.makedirs(vscode_dir, exist_ok=True)

    settings_json_path = os.path.join(vscode_dir, "settings.json")
    python_path = os.path.join(venv_path, "bin", "python") if os.path.exists(os.path.join(venv_path, "bin", "python")) else sys.executable

    settings_json_content = {
    "python.defaultInterpreterPath": python_path,
    "python.terminal.activateEnvironment": True,

    "terminal.integrated.profiles.osx": {
        "PythonVenv": {
            "path": "zsh",
            "args": ["-i", "-c", "source .venv/bin/activate; exec zsh"]
        }
    },
    "terminal.integrated.profiles.linux": {
        "PythonVenv": {
            "path": "bash",
            "args": ["-i", "-c", "source .venv/bin/activate; exec bash"]
        }
    },
    "terminal.integrated.profiles.windows": {
        "PythonVenv": {
            "path": "cmd.exe",
            "args": ["/k", ".venv\\Scripts\\activate"]
        }
    },
    "terminal.integrated.defaultProfile.osx": "PythonVenv",
    "terminal.integrated.defaultProfile.linux": "PythonVenv",
    "terminal.integrated.defaultProfile.windows": "PythonVenv"
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

    home_dir = os.path.expanduser("~")
    projects_dir = os.path.join(home_dir, "PythonProjects")
    project_path = os.path.join(projects_dir, project_name)
    config_dir = os.path.join(project_path, "config")  # Config-map toevoegen

    os.makedirs(project_path, exist_ok=True)
    os.makedirs(config_dir, exist_ok=True)  # Zorg ervoor dat de config-map wordt aangemaakt
    os.chdir(project_path)

    print(f"✅ Project directory created at {project_path}")

    # Virtual Environment
    venv_path = os.path.join(project_path, ".venv")
    print(f"🔧 Creating virtual environment at: {venv_path}")
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("✅ Virtual environment successfully created!")
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment.")
        return

    # Setup VS Code settings (blijft in de root)
    setup_vscode_settings(project_path, venv_path)

    # Git Setup
    if subprocess.run(["git", "--version"], check=False).returncode == 0:
        subprocess.run(["git", "init"], check=True)
        print("✅ Git repository initialized!")

    # Create Project Files
    files = {
        ".gitignore": ".venv/\n__pycache__/\n*.pyc\n.DS_Store\n.vscode/",
        "README.md": f"# {project_name}\n\n🚀 Welcome to your new Python project!",
        "requirements.txt": "# Add your dependencies here",
        "main.py": f'''\
def main():
    print("Happy coding! Good luck with your project {project_name}.")

if __name__ == "__main__":
    main()
''',
    }

    for filename, content in files.items():
        with open(os.path.join(project_path, filename), "w") as f:
            f.write(content)
        print(f"✅ {filename} created!")

    # Config-bestanden aanmaken in de config/ map
    config_files = {
        ".editorconfig": "root = true\n[*]\nindent_style = space\nindent_size = 4\n",
        "Makefile": "install:\n\tpip install -r requirements.txt\n\nrun:\n\tpython main.py\n",
        "pyproject.toml": f"""[tool.poetry]
name = "{project_name}"
version = "0.1.0"
description = "A new Python project"
authors = ["Your Name <your.email@example.com>"]
"""
    }

    for filename, content in config_files.items():
        with open(os.path.join(config_dir, filename), "w") as f:
            f.write(content)
        print(f"✅ {filename} created in config/")

    ensure_code_in_path()
    open_vs_code(project_path, main_file=os.path.join(project_path, "main.py"))

    print("\n🎉 Project successfully created and virtual environment is set up! 🚀")
    print("🔹 Open a new terminal in VS Code, and your environment should be activated automatically.")

def create_alias():
    """Creates the alias for pyproject and reloads the shell configuration."""
    home = os.path.expanduser("~")
    alias_command = 'alias pyproject="python3 ~/PythonProjects/project-creator/create_project.py"'

    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        shell_config = os.path.join(home, ".zshrc") if os.path.exists(os.path.join(home, ".zshrc")) else os.path.join(home, ".bashrc")
        
        try:
            with open(shell_config, "r") as file:
                if alias_command in file.read():
                    print("✅ Alias 'pyproject' is al ingesteld.")
                    return

            with open(shell_config, "a") as file:
                file.write(f"\n{alias_command}\n")

            print("🔄 Herladen van shell configuratie...")
            subprocess.run("exec $SHELL", shell=True, executable="/bin/bash")

            test_alias = subprocess.run("command -v pyproject", shell=True, capture_output=True, text=True)
            if test_alias.returncode == 0:
                print("✅ Alias 'pyproject' is direct actief! 🚀")
            else:
                print("⚠️ Alias toegevoegd, maar mogelijk pas actief in een nieuwe terminal.")

        except Exception as e:
            print(f"❌ Error creating alias: {e}")

    elif sys.platform == "win32":
        try:
            alias_command = 'setx PYPROJECT_PATH "python3 %USERPROFILE%\\PythonProjects\\project-creator\\create_project.py"'
            subprocess.run(alias_command, shell=True, executable="cmd.exe")

            print("🔄 Herladen van Windows omgevingsvariabelen...")
            subprocess.run("refreshenv", shell=True, executable="cmd.exe")

            test_alias = subprocess.run("where pyproject", shell=True, capture_output=True, text=True)
            if test_alias.returncode == 0:
                print("✅ Alias 'pyproject' is direct actief! 🚀")
            else:
                print("⚠️ Alias toegevoegd, maar mogelijk pas actief na een herstart.")

        except Exception as e:
            print(f"❌ Error creating alias on Windows: {e}")

def uninstall_pyproject():
    """Removes the alias and script completely."""
    home = os.path.expanduser("~")
    alias_command = 'alias pyproject="python3 ~/PythonProjects/project-creator/create_project.py"'

    if sys.platform == "darwin" or sys.platform.startswith("linux"):
        shell_config = os.path.join(home, ".zshrc") if os.path.exists(os.path.join(home, ".zshrc")) else os.path.join(home, ".bashrc")
        try:
            if os.path.exists(shell_config):
                with open(shell_config, "r") as file:
                    lines = file.readlines()
                with open(shell_config, "w") as file:
                    file.writelines(line for line in lines if alias_command not in line)

            subprocess.run("exec $SHELL", shell=True, executable="/bin/bash")
            print("✅ 'pyproject' alias succesvol verwijderd! 🚀")

        except Exception as e:
            print(f"❌ Error removing alias: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        create_alias()
    elif sys.argv[1] == '--uninstall':
        uninstall_pyproject()
    else:
        create_project(sys.argv[1])