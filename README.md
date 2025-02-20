# 🚀 Project Creator

A Python automation script that generates a fully structured Python project with a virtual environment, Git repository, VS Code configuration, and essential files.

## 📌 Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Features](#features)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 📥 Installation

### Clone the Repository
```bash
git clone https://github.com/NickNL90/project-creator.git
cd project-creator
```

### Installation & Setup

Set up the alias for quick project creation:
```bash
python create_project.py
```
This adds an alias to your `.zshrc` or `.bashrc`, allowing you to create projects using:
```bash
pyproject <project_name>
```

## 🚀 Usage

To create a new Python project, run:
```bash
pyproject <project_name>
```
This command automatically:
- Creates a new project folder in `~/PythonProjects/<project_name>/`
- Initializes a virtual environment (`.venv/`)
- Sets up a Git repository (`git init`)
- Generates essential files (`README.md`, `main.py`, `.gitignore`, etc.)
- Configures VS Code settings for the project
- Automatically opens VS Code with the project and activates the virtual environment 🎉

## 📁 Project Structure

Once a project is created, the directory will look like this:
```
MyNewProject/
│── .venv/             # Virtual environment
│── .git/              # Git repository
│── .gitignore         # Ignore unnecessary files
│── README.md          # Project documentation
│── requirements.txt   # Dependencies
│── main.py            # Main Python file
│── .vscode/           # VS Code settings
│── config/            # Config files
│   ├── .editorconfig  # Code style settings
│   ├── Makefile       # Quick commands
│   ├── pyproject.toml # Python project metadata
```

## ✨ Features

✅ Fast and efficient project setup  
✅ Creates a virtual environment automatically  
✅ Configures VS Code with project settings  
✅ Initializes Git with a `.gitignore` file  
✅ Adds essential files like `README.md`, `requirements.txt`, and `main.py`  
✅ Cross-platform support (macOS, Linux, Windows)  
✅ One command, fully set up 🚀

## ⚙️ Configuration

You can customize project files by modifying `create_project.py`.  
To change VS Code settings, edit `.vscode/settings.json`.

## 🛠 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch:
   ```bash
   git checkout -b feature-branch
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to GitHub:
   ```bash
   git push origin feature-branch
   ```
5. Submit a Pull Request 🎉

## 📜 License

This project is licensed under the MIT License.

## 📬 Contact

**Nick**  
📍 Netherlands  
🚀 Python | Data | Automation  
🔗 GitHub: [NickNL90](https://github.com/NickNL90)

🔥 Ready to start coding Python instantly?  
Just run:
```bash
pyproject <project_name>
```
And your environment is fully set up! 🚀
