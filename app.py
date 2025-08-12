# app.py
from flask import Flask, request, render_template
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Store applicant submissions
applicants = []

# Dummy model training
def train_dummy_model():
    data = {
        'resume_length': [250, 800, 500, 1200, 100],
        'buzzword_count': [5, 25, 12, 40, 3],
        'plagiarism_score': [0.1, 0.9, 0.4, 0.95, 0.05],
        'label': [0, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    X = df[['resume_length', 'buzzword_count', 'plagiarism_score']]
    y = df['label']
    model = RandomForestClassifier()
    model.fit(X, y)
    return model

model = train_dummy_model()

def extract_features(text):
    resume_length = len(text)
    buzzwords = ['synergy', 'dynamic', 'go-getter', 'passionate', 'hardworking']
    buzzword_count = sum(text.lower().count(word) for word in buzzwords)
    plagiarism_score = random.uniform(0, 1)
    return [[resume_length, buzzword_count, plagiarism_score]]

def extract_skills(text, required_skills):
    text = text.lower()
    return [skill for skill in required_skills if skill in text]

def analyze_github_profile(github_url):
    try:
        username = github_url.rstrip('/').split('/')[-1]
        user_resp = requests.get(f"https://api.github.com/users/{username}")
        if user_resp.status_code != 200:
            return None, "❌ GitHub user not found"
        repo_resp = requests.get(f"https://api.github.com/users/{username}/repos")
        repos = repo_resp.json()
        if not repos:
            return False, "⚠️ No repositories found"
        languages = {repo['language'] for repo in repos if repo['language']}
        return True, f"✅ {len(repos)} repos using: {', '.join(languages)}"
    except:
        return None, "❌ Error checking GitHub profile"

def score_hackerrank_profile(hr_url):
    score = 0
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(hr_url, headers=headers, timeout=5)
        if resp.status_code != 200:
            return 0, "❌ HackerRank profile not accessible."
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator=' ').lower()
        score += 2  # Profile accessible
        if "badge" in text:
            score += 2
        if "certificate" in text or "certification" in text:
            score += 3
        if any(skill in text for skill in ['python', 'sql', 'java', 'c++']):
            score += 3
        return score, f"✅ HackerRank Score: {score}/10"
    except:
        return 0, "❌ Error checking HackerRank profile."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    file = request.files.get('resume')
    github_url = request.form.get('github')
    hr_url = request.form.get('hackerrank')
    required_skills_input = request.form.get('skills') or ""
    required_skills = [s.strip().lower() for s in required_skills_input.split(',') if s.strip()]

    if not file or not github_url:
        return render_template('result.html', error="❌ Resume and GitHub profile are required.")

    text = file.read().decode('utf-8', errors='ignore')
    features = extract_features(text)
    prediction = model.predict(features)[0]
    result = "✅ Genuine" if prediction == 0 else "❌ Likely Fake"

    matched_skills = extract_skills(text, required_skills)
    unmatched_skills = list(set(required_skills) - set(matched_skills))
    skill_match = "✅ Skilled" if matched_skills else "⚠️ Skill Gap"

    github_valid, github_result = analyze_github_profile(github_url)
    if github_valid is None:
        return render_template('result.html', error="❌ Invalid GitHub URL or user not found.")

    hr_result = "Not Provided"
    if hr_url:
        _, hr_result = score_hackerrank_profile(hr_url)

    applicants.append({
        'result': result,
        'skill_match': skill_match,
        'github_result': github_result,
        'hr_result': hr_result,
        'matched': len(matched_skills),
        'unmatched': len(unmatched_skills),
        'total_skills': len(matched_skills) + len(unmatched_skills)
    })

    return render_template('result.html', result=result, skill_match=skill_match,
                           matched_skills=matched_skills, unmatched_skills=unmatched_skills,
                           github_result=github_result, hr_result=hr_result)

@app.route('/dashboard')
def dashboard():
    genuine = sum(1 for a in applicants if "Genuine" in a['result'])
    fake = len(applicants) - genuine
    skill_match = sum(1 for a in applicants if "Skilled" in a['skill_match'])
    return render_template("dashboard.html", applicants=applicants,
                           genuine=genuine, fake=fake, skill_match=skill_match)

if __name__ == '__main__':
    app.run(debug=True)
