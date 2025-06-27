# AI-Powered Resume to Portfolio Generator
## Introduction

Transform your resume into a stunning personal portfolio website in seconds using OpenRouter’s GPT-3.5. This intelligent tool automatically extracts structured data such as education, experience, skills, certifications, and projects from your uploaded PDF resume. The extracted content is fully editable, and the final portfolio—styled with a modern glassmorphism UI—can be downloaded as a standalone HTML file for easy sharing or deployment.

## Key Features

**1.Resume Upload**  
Upload a PDF resume directly through the web interface.

**2.AI-Powered Parsing**  
Automatically extract structured sections using OpenRouter's GPT-3.5 model.

**3.Editable Sections**  
Modify extracted content including skills, education, experience, and more.

**4.Add New Sections**  
Dynamically add custom sections to your portfolio.

**5.Profile Image Upload**  
Upload and display a round profile picture on the portfolio.

**6.Glassmorphism UI**  
Modern, clean interface using Bootstrap and glassy visual effects.

**7.HTML Download**  
Download the final portfolio as a fully functional HTML page.

**8.MongoDB Integration**  
Resume and portfolio data are stored in MongoDB for persistent access.

## System Architechture

1.Resume Upload → PDF sent to backend

2.Flask Server → Parses and formats resume text

3.GPT-3.5 via OpenRouter → Classifies and structures sections

4.MongoDB → Stores portfolio data for editing and display

5.Bootstrap UI → Displays editable, downloadable portfolio

6.Download Option → Save full HTML copy of the site 

## Project Setup

### Prerequisites

1.Python 3.8+
2.MongoDB Atlas account (for cloud DB)
3.OpenRouter API key (for GPT-3.5)
4.pip (Python package manager)

##  Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/ai-portfolio-generator.git
cd ai-portfolio-generator
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3.Set Environment Variables
Create a .env file in the root directory and add:
```bash
MONGO_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/<dbname>
OPENROUTER_API_KEY=your_api_key_here
```
### 4. Run the App
   ```bash
python app.py
```
### 5. Access Locally
Open your browser and navigate to:
```bash
http://localhost:5000
```
##  Usage

1. **Upload Resume**  
   Navigate to the homepage and upload your resume in PDF format.

2. **Generate Portfolio**  
   The AI extracts and classifies your resume data into sections like Education, Experience, Skills, Projects, etc.

3. **Edit Portfolio**  
   You can update any section, modify content, or even add new sections dynamically through the Edit interface.

4. **Upload Profile Picture**  
   Optionally upload a profile picture which appears at the top of your portfolio.

5. **View & Navigate Portfolio**  
   The generated portfolio is displayed with a stylish glassmorphic design and sticky sidebar navigation for smooth scrolling.

6. **Download Portfolio**  
   Download the complete portfolio as a standalone HTML file for hosting or sharing.
   
## License 
**This project is provided under an "All Rights Reserved" license. Redistribution, modification, or commercial use of the software is prohibited without explicit permission from the author(s). The software is provided "as is" without any warranties or guarantees.**








