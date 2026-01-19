# Student Guide – Dyslexia Detection & Training Project

---

## 📖 Overview
This guide walks you through **setting up**, **running**, and **using** the Dyslexia Detection & Training web application on your own computer. It is written for students who want to explore the system, upload their own data, and try the training games.

---

## 🛠️ Prerequisites
| Requirement | Why? |
|-------------|------|
| **Python 3.10+** | The backend is built with Django/Python. |
| **Git** | To clone the repository (optional if you already have the folder). |
| **Node.js (optional)** | Only needed if you want to rebuild static assets; the project ships pre‑compiled CSS/JS. |
| **Virtual Environment tool** (`venv` or `conda`) | Keeps dependencies isolated from your system Python. |
| **Internet connection** | To install Python packages the first time. |

---

## 📂 Project Structure (high‑level)
```
Dyslexia/
├─ data_collection/          # Machine‑learning models & data utilities
│   └─ models.py            # Model inference code
├─ user_interface/          # Django app containing templates & static files
│   └─ templates/user_interface/
│        ├─ home.html       # Landing page
│        └─ upload_data.html# Data upload page
├─ TRAINING_GAMES_GUIDE.md  # Description of the training games
├─ requirements.txt          # Python dependencies
└─ manage.py                # Django management script
```

---

## 🚀 Quick‑Start (One‑click) 
1. **Open a terminal** (PowerShell or CMD) and navigate to the project root:
   ```powershell
   cd "c:\Harishma\Maitexa\Project_ Dyslexia\Dyslexia"
   ```
2. **Create & activate a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1   # PowerShell
   # or
   .\venv\Scripts\activate.bat   # CMD
   ```
3. **Install required packages**:
   ```powershell
   pip install -r requirements.txt
   ```
4. **Apply database migrations** (creates the SQLite DB used by Django):
   ```powershell
   python manage.py migrate
   ```
5. **Start the development server**:
   ```powershell
   python manage.py runserver
   ```
   You should see something like:
   ```
   Watching for file changes with StatReloader
   Performing system checks...
   
   System check identified no issues (0 silenced).
   March 19, 2026 - 10:55:12
   Django version 4.2, using settings 'Dyslexia.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```
6. **Open a browser** and go to `http://127.0.0.1:8000/`. You will land on the **Home** page.

---

## 📤 Uploading Your Data
1. Click **"Upload Data"** in the navigation bar (or go directly to `/upload`).
2. Choose a **CSV** file that follows the format described in `data_collection/models.py` (columns: `student_id, text, label`).
3. Press **Submit**. The server will run the dyslexia detection model on each row and display a summary table with predictions.
4. **Tip:** If you receive a *500 Internal Server Error*, check the console for stack traces – most often it’s a missing column or malformed CSV.

---

## 🎮 Training Games
The project ships a set of interactive games designed to improve reading and writing skills. The list and brief description are in `TRAINING_GAMES_GUIDE.md`. To access them:
1. From the Home page, click **"Training Games"**.
2. Choose a game (e.g., *Word Maze*, *Letter Tracing*). Each game runs in the browser using vanilla JavaScript and stores progress locally (in `localStorage`).
3. Follow the on‑screen instructions; most games have a **Start**, **Pause**, and **Reset** button.

---

## 🧩 How the Detection Model Works (Optional Deep‑Dive)
- The model lives in `data_collection/models.py`. It loads a pre‑trained PyTorch model (`model.pt`) and exposes a `predict(text: str) -> str` function.
- When you upload a CSV, the backend iterates over each row, calls `predict`, and writes the result back to a temporary DataFrame that is rendered in the HTML template.
- You can experiment by editing `models.py` (e.g., swapping the model file) and restarting the server.

---

## 🛠️ Common Issues & Troubleshooting
| Symptom | Likely Cause | Fix |
|---------|---------------|-----|
| **ImportError: No module named `torch`** | Dependencies not installed | Re‑run `pip install -r requirements.txt` inside the virtual env. |
| **Page shows “CSRF token missing”** | Session cookies disabled | Ensure your browser accepts cookies for `localhost`. |
| **Server crashes after uploading a large CSV** | Memory limit – the model processes everything in RAM | Split the CSV into smaller chunks (e.g., 500 rows) and upload sequentially. |
| **Static files (CSS/JS) not loading** | `collectstatic` not run (only needed for production) | In dev mode, Django serves static files automatically. Just ensure `DEBUG = True` in `settings.py`. |

---

## 📦 Packaging for Distribution (Advanced)
If you want to share the project with classmates who don’t have Python installed, you can create a **stand‑alone executable** using `PyInstaller`:
```powershell
pip install pyinstaller
pyinstaller --onefile manage.py
```
The resulting `manage.exe` can be run on any Windows machine (no Python needed). You’ll still need the `model.pt` file in the same directory.

---

## 🎓 Next Steps for Students
1. **Experiment** – Try uploading your own text samples and see how the model classifies them.
2. **Improve the Model** – Replace `model.pt` with a model you train on a custom dataset.
3. **Add a New Game** – Follow the pattern in `user_interface/templates/user_interface/` and add a new JavaScript file under `static/js/`.
4. **Contribute** – Fork the repo, push changes, and open a Pull Request.

---

## 📚 Resources
- **Django Documentation:** https://docs.djangoproject.com/en/4.2/
- **PyTorch Quick‑Start:** https://pytorch.org/tutorials/beginner/basics/intro.html
- **Git Basics:** https://git-scm.com/book/en/v2

---

*Happy learning! 🎉*
