import os
import sys
import subprocess

def create_project(project_name):
    """Maakt een nieuwe projectmap, installeert venv, activeert en upgrade pip, en zet een private git-repo op."""
    print("🚀 Script gestart!")

    print(f"📌 Projectnaam: {project_name}")

    # Stap 1: Maak de projectmap
    project_path = os.path.join(os.getcwd(), project_name)
    print(f"📂 Projectmap wordt aangemaakt op: {project_path}")

    try:
        os.makedirs(project_path, exist_ok=True)
        print("✅ Projectmap aangemaakt!")
    except Exception as e:
        print(f"❌ Fout bij maken van projectmap: {e}")
        return

    # Stap 2: Navigeer naar de projectmap
    os.chdir(project_path)
    print(f"📌 Verplaatst naar projectmap: {os.getcwd()}")

    # Stap 3: Maak een virtual environment
    venv_path = os.path.join(project_path, "venv")
    print(f"🔧 Virtual environment wordt aangemaakt in: {venv_path}")

    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment succesvol aangemaakt!")
    except Exception as e:
        print(f"❌ Fout bij aanmaken van venv: {e}")
        return

    # Stap 4: Activeer venv en upgrade pip
    if sys.platform in ["darwin", "linux"]:
        activate_command = f"source {venv_path}/bin/activate"
    else:  # Windows
        activate_command = f"{venv_path}\\Scripts\\activate"

    print("🚀 Activeer je venv met:")
    print(f"    {activate_command}  # Kopieer en plak dit in de terminal")

    print("🔄 Pip wordt geüpgraded...")
    try:
        subprocess.run(f"{activate_command} && pip install --upgrade pip", shell=True, check=True)
        print("✅ Pip is geüpgraded!")
    except Exception as e:
        print(f"❌ Fout bij updaten van pip: {e}")

    # Stap 5: Maak een git-repo aan en zet deze op privé
    print("📂 Initialiseren van private Git-repository...")
    try:
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "branch", "-M", "main"], check=True)
        print("✅ Private Git-repository aangemaakt!")
    except Exception as e:
        print(f"❌ Fout bij git init: {e}")

    # Stap 6: Maak .gitignore aan
    gitignore_path = os.path.join(project_path, ".gitignore")
    print("📄 .gitignore wordt aangemaakt...")

    gitignore_content = """# Virtual environment
venv/
__pycache__/
.DS_Store
*.pyc
"""
    try:
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        print("✅ .gitignore aangemaakt!")
    except Exception as e:
        print(f"❌ Fout bij aanmaken .gitignore: {e}")

    # Stap 7: Maak README.md en requirements.txt aan
    readme_path = os.path.join(project_path, "README.md")
    print("📜 README.md en requirements.txt worden aangemaakt...")

    readme_content = f"""# {project_name}

## Beschrijving
Dit is het {project_name}-project, automatisch gegenereerd met een Python-script.
"""
    try:
        with open(readme_path, "w") as f:
            f.write(readme_content)
        with open(os.path.join(project_path, "requirements.txt"), "w") as f:
            f.write("")
        print("✅ README.md en requirements.txt aangemaakt!")
    except Exception as e:
        print(f"❌ Fout bij aanmaken README.md of requirements.txt: {e}")

    print("\n🎉 Project is succesvol aangemaakt! 🚀")

def setup_alias():
    """Voegt de alias toe aan .zshrc of .bashrc zodat 'python project' direct gebruikt kan worden."""
    home = os.path.expanduser("~")
    shell_config = os.path.join(home, ".zshrc") if os.path.exists(os.path.join(home, ".zshrc")) else os.path.join(home, ".bashrc")
    alias_command = 'alias project="python3 ~/project-creator/create_project.py"'

    try:
        with open(shell_config, "r") as file:
            if alias_command in file.read():
                print("✅ Alias is geïnstalleerd, create your project with 'python project <your projectname>'")
                return
    except FileNotFoundError:
        return

    try:
        with open(shell_config, "a") as file:
            file.write(f"\n{alias_command}\n")
        subprocess.run(f"source {shell_config}", shell=True)
        print("✅ Python projects can be made with 'python project <your projectname>'")
    except Exception as e:
        print(f"❌ Fout bij toevoegen alias: {e}")

if __name__ == "__main__":
    setup_alias()
    if len(sys.argv) < 2:
        sys.exit(1)
    else:
        project_name = sys.argv[1]
        create_project(project_name)
