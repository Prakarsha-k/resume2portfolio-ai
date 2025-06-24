import os
import json
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI
import pymongo
from bson import ObjectId

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# MongoDB setup
mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["portfolio_db"]
collection = db["portfolios"]

# OpenRouter AI setup
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Extract text from PDF resume
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return '\n'.join([page.extract_text() for page in pdf.pages if page.extract_text()])

# Call LLM to convert resume text into structured JSON
def generate_portfolio_from_resume(resume_text):
    prompt = f"""
You are a portfolio generator AI. Your job is to extract structured portfolio data from the given resume. Follow these instructions strictly.

🎯 Output format must be a valid JSON object with only the specified keys.

🧠 Classification Rules:
- "about": A short summary or objective section.
- "education": Include degree, institution, year, and CGPA or marks (if available).
- "experience": List of job roles/internships with company names and dates.
- "skills": Classify clearly and list them. Preferably group into two rows (can be handled in frontend).
- "projects": Each must contain a title, short description, and a separate list of technologies used.
- "certifications": Include certification title, issuing organization, and date (if available).
- "achievements": Awards or milestones only (not certs).
- "other_activities": Optional hobbies or non-tech involvement.
- Provide: "linkedin", "github", "email" if available.

🧾 Output JSON Format:
{{
  "name": "Your Name",
  "about": "Brief summary or objective",
  "education": [
    "B.Tech in CSE - ABC University (2022), CGPA: 8.7"
  ],
  "experience": [
    "Software Engineer Intern at ABC Corp (May 2023 - July 2023): Built internal tools using Flask and MongoDB."
  ],
  "skills": ["Python", "Machine Learning", "Public Speaking", "Leadership"],
  "projects": [
    {{
      "title": "AI Health Bot",
      "description": "An AI-powered chatbot for preliminary diagnosis",
      "technologies_used": ["Python", "NLP", "Flask"]
    }}
  ],
  "certifications": [
    {{
      "title": "AWS Certified Developer",
      "description": "Issued by Amazon Web Services, March 2023"
    }}
  ],
  "achievements": ["Won Smart India Hackathon 2023"],
  "other_activities": ["Member of Tech Club", "Volunteer at NGO"],
  "linkedin": "https://linkedin.com/in/yourprofile",
  "github": "https://github.com/yourprofile",
  "email": "your.email@example.com"
}}

Resume:
---
{resume_text}
---

Return a valid JSON only. No explanation.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        raw = response.choices[0].message.content.strip()
        return {k.lower(): v for k, v in json.loads(raw).items()}
    except Exception as e:
        print("❌ LLM error:", e)
        return {}

# Home page with resume upload
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        resume = request.files["resume"]
        profile = request.files.get("profile_pic")

        if resume and resume.filename.endswith(".pdf"):
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            resume.save(filepath)

            resume_text = extract_text_from_pdf(filepath)
            portfolio_data = generate_portfolio_from_resume(resume_text)

            profile_path = ""
            if profile:
                profile_filename = secure_filename(profile.filename)
                profile_path = os.path.join(app.config["UPLOAD_FOLDER"], profile_filename)
                profile.save(profile_path)

            entry = {
                "name": portfolio_data.get("name", "My Portfolio"),
                "portfolio": portfolio_data,
                "profile_pic": profile_path
            }
            inserted = collection.insert_one(entry)
            return redirect(url_for("portfolio", id=str(inserted.inserted_id)))
    return render_template("index.html")

# Portfolio display page
@app.route("/portfolio/<id>")
def portfolio(id):
    data = collection.find_one({"_id": ObjectId(id)})
    return render_template("portfolio.html",
                           name=data.get("name", "My Portfolio"),
                           profile_pic=data.get("profile_pic", ""),
                           portfolio=data.get("portfolio", {}),
                           id=id)

# HTML download route
@app.route("/download_html/<id>")
def download_html(id):
    data = collection.find_one({"_id": ObjectId(id)})
    rendered = render_template("portfolio.html",
                                name=data.get("name", "My Portfolio"),
                                profile_pic=data.get("profile_pic", ""),
                                portfolio=data.get("portfolio", {}),
                                id=id)
    filename = os.path.join("static", f"{id}_portfolio.html")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(rendered)
    return redirect(url_for("static", filename=f"{id}_portfolio.html"))

# Portfolio edit page
@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    data = collection.find_one({"_id": ObjectId(id)})
    portfolio = data.get("portfolio", {})

    if request.method == "POST":
        updated = {}

        for key in request.form:
            # Skip new section form fields here
            if key in ("new_key", "new_value"):
                continue

            value = request.form.get(key, "").strip()
            if not value:
                continue

            if key == "skills":
                updated[key] = [[s.strip() for s in value.split(",") if s.strip()]for row in value.split("\n") if row.strip()]
            elif  key == "certifications":
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, list):
                        updated[key] = parsed
                except:
                    updated[key] = []
            #updated[key] = [line.strip() for line in value.split("\n") if line.strip()]
                
            elif key == "projects":
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, list):
                        updated[key] = parsed
                except:
                    updated[key] = []
            else:
                updated[key] = value

        # ✅ Handle new custom section
        new_key = request.form.get("new_key", "").strip()
        new_value = request.form.get("new_value", "").strip()
        if new_key and new_value:
            try:
                updated[new_key] = json.loads(new_value)
            except:
                updated[new_key] = new_value

        collection.update_one({"_id": ObjectId(id)}, {"$set": {"portfolio": updated}})
        return redirect(url_for("portfolio", id=id))

    return render_template("edit_portfolio.html",
                           name=data.get("name", "My Portfolio"),
                           profile_pic=data.get("profile_pic", ""),
                           portfolio=portfolio,
                           id=id)

# Run the server
if __name__ == "__main__":
    app.run(debug=True)
