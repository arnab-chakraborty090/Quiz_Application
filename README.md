# 🐍 Python Quiz Arena

**Python Quiz Arena** is an interactive, web-based Python quiz application developed using Python and Streamlit. It allows users to test their Python knowledge through multiple-choice questions, track their performance, review their answers, and view the leaderboard.

## 🚀 Features

- **Interactive Quiz:** Answer 10 multiple-choice questions about Python.
- **Randomized Questions:** Questions are shuffled for each new quiz.
- **3-Minute Timer:** A countdown timer starts when you click the Start Quiz button.
- **Automatic Scoring:** Earn points for correct answers.
- **Performance Analytics:** View your quiz results through a score visualization.
- **Answer Review:** Review your selected answers alongside the correct answers.
- **Leaderboard:** View saved quiz scores and rankings.
- **Quiz Restart:** Start a new quiz directly from the results page.
- **Responsive Interface:** A user-friendly interface built with Streamlit.

## 🛠️ Technologies Used

| Technology / Library | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application framework |
| JSON | Store and retrieve leaderboard data |
| Random | Shuffle questions |
| Time | Implement the countdown timer |
| Pathlib | Handle file paths |

### Dependencies

The project uses Python's built-in libraries and Streamlit.

The `requirements.txt` file contains:

```txt
streamlit==1.50.0
```

The `json`, `random`, `time`, and `pathlib` modules are included with Python and do not need to be installed separately.

## 📁 Project Structure

```text
Python-Quiz-Arena/
|__Quiz App with Leaderboard.py
├── app.py
├── requirements.txt
├── README.md
└── leaderboard.json

```

**File descriptions:**
- `Quiz App with Leaderboard` - Contains the quiz questions and leaderboard
- `app.py` — Contains the main application code.
- `requirements.txt` — Lists the external Python dependencies.
- `README.md` — Provides project information and setup instructions.
- `leaderboard.json` — Stores leaderboard data when results are saved. The application may create this file automatically.

## 💻 Installation and Setup

Follow these steps to run the application on your computer.

### Step 1: Install Python

Install Python 3.9 or newer.

Verify the installation:

```bash
python --version
```

### Step 2: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Navigate to the project directory:

```bash
cd YOUR-REPOSITORY
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub username and repository name.

Alternatively, download the repository as a ZIP file and extract it.

### Step 3: Create a Virtual Environment (Recommended)

On Windows:

```bash
python -m venv .venv
```

Activate it using Command Prompt:

```bat
.venv\Scripts\activate
```

Or using PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 4: Install Dependencies

Run the following command from the project directory:

```bash
python -m pip install -r requirements.txt
```

This installs Streamlit and its required dependencies.

### Step 5: Run the Application

Start the application using:

```bash
streamlit run app.py
```

Once the application starts, open the local URL displayed in your terminal. It is usually:

```text
http://localhost:8501
```

You can now use Python Quiz Arena in your browser.

To stop the application, press `Ctrl+C` in the terminal.
