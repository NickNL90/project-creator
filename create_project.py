import os
import sys
import subprocess

def create_project(project_name):
    """Maakt een nieuwe projectmap, installeert venv, activeert en upgrade pip, en zet een git-repo op."""
    print("🚀 Script gestart!")

    if not project_name:
        print("❌ Geen projectnaam opgegeven. Gebruik: project <projectnaam>")
        sys.exit(1)

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

    # Stap 5: Maak een git-repo aan
    print("📂 Initialiseren van Git-repository...")
    try:
        subprocess.run(["git", "init"], check=True)
        print("✅ Git-repository aangemaakt!")
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

    # Stap 7: Maak README.md aan
    readme_path = os.path.join(project_path, "README.md")
    print("📜 README.md wordt aangemaakt...")

    readme_content = f"""# {project_name}

## Beschrijving
Dit is het {project_name}-project, automatisch gegenereerd met een Python-script.

## Setup
1. Activeer de virtual environment:
   ```bash
   source venv/bin/activate  # macOS/Linux
   venv\\Scripts\\activate  # Windows
   ```
2. Installeer dependencies:
   ```bash
   pip install -r requirements.txt
   ```
"""
    try:
        with open(readme_path, "w") as f:
            f.write(readme_content)
        print("✅ README.md aangemaakt!")
    except Exception as e:
        print(f"❌ Fout bij aanmaken README.md: {e}")

    print("\n🎉 Project is succesvol aangemaakt! 🚀")

# Controleer of de gebruiker een projectnaam heeft opgegeven
if len(sys.argv) < 2:
    print("❌ Gebruik: project <projectnaam>")
    sys.exit(1)

# Haal de projectnaam op en voer het script uit
project_name = sys.argv[1]
create_project(project_name)
