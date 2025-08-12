# skill-verify-AI
SkillVerifyAI is an AI-powered tool that verifies job applicants’ skills by analyzing resumes and coding profiles (GitHub, HackerRank) using NLP &amp; ML, providing credibility scores, detailed reports, and bulk processing to help recruiters detect fake or exaggerated profiles.

SkillVerifyAI
AI-powered Job Applicant Profile Authenticity Verification
SkillVerifyAI is an AI-driven tool that verifies the authenticity of job applicants’ skills by analyzing their resumes and coding platform profiles (GitHub, HackerRank). It uses Natural Language Processing (NLP) and Machine Learning (ML) to detect exaggerated claims, inconsistencies, and fake profiles.

🚀 Features
Resume Analysis: Extracts and validates skills, education, and experience using NLP.
GitHub Verification: Analyzes repositories, commits, coding activity, and code quality.
HackerRank Scoring: Evaluates coding challenge history and skill levels.
Bulk Processing: Upload multiple resumes and profile links via CSV.
Credibility Scoring: Generates authenticity scores for each applicant.
Reports & Visuals: Provides clear reports with charts for quick decision-making.

🛠 Tech Stack
Backend: Python, Flask
Frontend: HTML, CSS, JavaScript
ML & NLP: Scikit-learn, spaCy/NLTK
Data Processing: Pandas, NumPy
Visualization: Matplotlib, Seaborn

📂 Project Structure
csharp
Copy
Edit
SkillVerifyAI/
│── app.py                # Flask backend
│── static/               # CSS, JS, images
│── templates/            # HTML templates
│── models/               # ML models
│── data/                 # Sample resumes & profiles
│── utils/                # Helper functions
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
⚙️ Installation & Usage
Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/SkillVerifyAI.git
cd SkillVerifyAI
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the app

bash
Copy
Edit
python app.py
Open http://127.0.0.1:5000 in your browser.

📊 Workflow
Upload resume(s) and profile links.

System extracts & processes data.

ML model evaluates authenticity & assigns scores.

View detailed report with insights & charts.
