# AI-Powered Resume to Portfolio Generator
## Introduction

Transform your resume into a stunning personal portfolio website in seconds using OpenRouter’s GPT-3.5. This intelligent tool automatically extracts structured data such as education, experience, skills, certifications, and projects from your uploaded PDF resume. The extracted content is fully editable, and the final portfolio—styled with a modern glassmorphism UI—can be downloaded as a standalone HTML file for easy sharing or deployment.
## Key Features
#### Resume Upload  
Upload a PDF resume directly through the web interface.

####  AI-Powered Parsing  
Automatically extract structured sections using OpenRouter's GPT-3.5 model.

####  Editable Sections  
Modify extracted content including skills, education, experience, and more.

####  Add New Sections  
Dynamically add custom sections to your portfolio.

#### Profile Image Upload  
Upload and display a round profile picture on the portfolio.

####  Glassmorphism UI  
Modern, clean interface using Bootstrap and glassy visual effects.

#### HTML Download  
Download the final portfolio as a fully functional HTML page.

####  MongoDB Integration  
Resume and portfolio data are stored in MongoDB for persistent access.

## System Architechture

1.Resume Upload → PDF sent to backend

2.Flask Server → Parses and formats resume text

3.GPT-3.5 via OpenRouter → Classifies and structures sections

4.MongoDB → Stores portfolio data for editing and display

5.Bootstrap UI → Displays editable, downloadable portfolio

6.Download Option → Save full HTML copy of the site 


