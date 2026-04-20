# Resume Analyser

A FastAPI application for analysing resumes against job descriptions.

## Features
- Upload a PDF resume
- Extract skills from resume and job description text
- Match skills and calculate a score
- Provide suggestions for missing skills using AI

## Project structure
- `app/main.py` - FastAPI application and endpoint definitions
- `app/extractor.py` - Extracts skills from text
- `app/matcher.py` - Matches resume skills to job description skills
- `app/ai_agent.py` - Generates suggestions for missing skills
- `index.html` - Front-end UI served by the API
- `requirements.txt` - Python dependencies

## Setup
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   uvicorn app.main:app --reload
   ```
4. Open the app in a browser at `http://127.0.0.1:8000`

## GitHub upload
If you want to upload this project to GitHub:

```bash
cd /Users/shikharpandav/Desktop/resume-analyser
git init
git add .
git commit -m "Initial commit"
```

Then create a GitHub repository and push:

```bash
git branch -M main
git remote add origin <YOUR_GITHUB_REPO_URL>
git push -u origin main
```

If you use GitHub CLI:

```bash
gh repo create <repo-name> --public --source=. --remote=origin
git push -u origin main
```

## Notes
- Do not commit the `.env` file or `.venv` folder.
- Add any missing dependencies to `requirements.txt` before sharing.
