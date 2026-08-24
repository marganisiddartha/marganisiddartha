🎙️ Voice Notes to Flashcards

An AI-powered Streamlit application that converts lecture recordings and
uploaded audio into structured study material.

🚀 Features

🎙️ Record or upload lecture audio

📝 Generate lecture transcripts

📖 Generate AI-powered summaries

🧠 Extract key concepts

🃏 Generate flashcards

🎯 Generate practice quizzes

🏆 Calculate and display quiz scores

📜 Maintain study history

🗃️ Store study sessions using SQLite

🗑️ Delete previous history items

📊 Dashboard with study statistics

🤖 Gemini-powered study material generation

🛠️ Technologies Used

Python

Streamlit

Google Gemini API

Pandas

SQLite

python-dotenv

Audio processing and transcription libraries

📁 Project Structure

voice_notes_flashcards/
├── app.py
├── history.py
├── .gitignore
├── .env
├── study_history.db
├── audio_history/
└── .venv/

.env, .venv/, study_history.db, and audio_history/ should not
be uploaded to GitHub.

⚙️ Installation

1. Clone the repository

git clone YOUR_GITHUB_REPOSITORY_URL
cd voice_notes_flashcards

2. Create a virtual environment

python -m venv .venv
.venv\Scripts\Activate.ps1

3. Install dependencies

pip install streamlit pandas python-dotenv google-genai

Install any additional audio/transcription packages required by your
app.py.

🔑 Gemini API Key Setup

Create a .env file in the project root:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY

Never commit your .env file or expose your API key publicly.

▶️ Run the Application

python -m streamlit run app.py

Then open the local URL shown in the terminal, normally:

http://localhost:8501

🧠 How It Works

The user records or uploads a lecture.

The application processes the audio.

The lecture content is sent to the configured AI model.

Gemini generates structured study material.

The application displays the transcript, summary, key concepts,
flashcards, and quiz.

Quiz answers are evaluated and the score is updated.

Study sessions are stored in a local SQLite database.

Study history can be managed from the History section.

📚 Study History

The application stores study-session information such as:

File name and type

Subject

Audio path

Creation date

Transcript

Summary

Key concepts

Flashcards

Quiz

Quiz score

Favorite status

🔐 Security

The Gemini API key is loaded from .env instead of being hard-coded.

The .gitignore excludes sensitive and local files:

.env
.venv/
__pycache__/
*.pyc
study_history.db
audio_history/

🎯 Project Goal

Voice Notes to Flashcards helps students convert lecture recordings into
organized learning resources automatically, reducing the time required
to create notes, flashcards, and practice quizzes manually.

🔮 Future Improvements

Cloud-based study history

User authentication

Advanced learning analytics

Spaced-repetition flashcards

Voice-based quiz interaction

Multi-language support

PDF export

Mobile-friendly interface

👨‍💻 Author

Margani Siddartha

CSE Student & Developer