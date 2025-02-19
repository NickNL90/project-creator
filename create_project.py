import os
import sys
import subprocess

def ensure_code_in_path():
    """Controleert of het `code`-commando beschikbaar is en voegt het toe aan PATH indien nodig."""
    try:
        subprocess.run(["which", "code"], check=True, capture_output=True)
        print("✅ VS Code 'code' command is beschikbaar!")
    except subprocess.CalledProcessError:
        print("⚠️ VS Code 'code' command is niet gevonden. Probeer het automatisch toe te voegen...")
        try:
            subprocess.run(["osascript", "-e", 'tell application "Visual Studio Code" to activate'], check=True)
            subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "p" using {command down, shift down}'], check=True)
            subprocess.run(["osascript", "-e", 'tell application "System Events" to keystroke "Shell Command: Install \"code\" command in PATH" & return'], check=True)
            subprocess.run("source ~/.zshrc || source ~/.bashrc", shell=True, check=True)
            print("✅ VS Code 'code' command is succesvol toegevoegd aan PATH! Herstart de terminal als het niet direct werkt.")
        except Exception as e:
            print(f"❌ Kon 'code' niet automatisch toevoegen aan PATH: {e}")
            print("🔹 Open VS Code en voer handmatig uit: 'Shell Command: Install \"code\" command in PATH'")

def open_vs_code(project_path):
    """Probeert VS Code te openen met de projectmap."""
    print("🚀 VS Code wordt geopend met de projectmap...")
    try:
        subprocess.run(["code", project_path], check=True)
    except FileNotFoundError:
        print("⚠️ 'code' command niet gevonden. Probeer absolute VS Code-pad te gebruiken...")
        vs_code_path = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
        if os.path.exists(vs_code_path):
            subprocess.run([vs_code_path, project_path])
            print("✅ VS Code geopend via absolute pad!")
        else:
            print("❌ VS Code kon niet worden geopend. Zorg ervoor dat VS Code correct is geïnstalleerd.")

def create_project(project_name):
    """Maakt een nieuwe projectmap, installeert venv, activeert en upgrade pip, zet een private git-repo op en opent VS Code."""
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

    # Stap 6: Maak .gitignore aan in de hoofdmap, niet in venv
    gitignore_path = os.path.join(project_path, ".gitignore")
    print("📄 .gitignore wordt aangemaakt in de hoofdmap...")

    gitignore_content = """# Virtual environment
venv/
__pycache__/
.DS_Store
*.pyc
"""
    try:
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        print("✅ .gitignore aangemaakt in de hoofdmap!")
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

    # Stap 8: Open project in VS Code
    ensure_code_in_path()
    open_vs_code(project_path)

    print("\n🎉 Project is succesvol aangemaakt en de virtual environment is geactiveerd! 🚀")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Gebruik: pyproject <projectnaam> om een nieuw project te maken.")
        sys.exit(1)
    else:
        project_name = sys.argv[1]
        create_project(project_name)
