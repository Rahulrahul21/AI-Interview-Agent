AI Interview Agent

An AI-powered interview assessment platform that conducts structured, role-specific interviews and provides confidential AI-based evaluation for recruiters.

The system allows candidates to create an account, sign in, provide their personal information, select a target job role and core skills, complete a five-question AI interview, and submit their responses for recruiter review.

Recruiters or administrators can review candidate information, interview responses, AI evaluation, scores, strengths, skill gaps, recommendations, and decide whether a candidate should proceed to the next recruitment round.


---

Features

Candidate Features

Candidate Sign Up

Candidate Sign In

Candidate personal information

First name and last name

Email address

Phone number

Secure password hashing

Target job role selection

Core skill selection

AI-generated interview questions

Five-question structured interview

Multi-line answers

Empty-answer validation

Interview submission confirmation

Candidate session management


AI Features

Role-specific question generation

Skill-specific questions

Conceptual questions

Practical questions

Problem-solving questions

Scenario-based questions

Progressive difficulty

Duplicate-question avoidance

Complete interview evaluation

Overall score from 0–10

Performance classification

Strength identification

Skill-gap identification

Improvement recommendations

Final interview summary


Recruiter/Admin Features

Admin authentication

Candidate dashboard

Candidate list

Candidate contact information

Candidate role and skills

Interview status

Interview score

Interview questions and answers

AI evaluation

Candidate strengths

Candidate gaps

Recommendations

Shortlist candidates

Reject candidates

Move candidates to the next round


Candidate Privacy

Candidates do not receive the confidential AI evaluation.

The following information is intended for recruiter/admin review:

Overall score

Performance

Strengths

Gaps

Recommendations

Hiring decision



---

Technology Stack

Technology	Purpose

Python	Backend programming
Flask	Web application framework
HTML5	Frontend structure
CSS3	Frontend styling
JavaScript	Frontend interaction
SQLite	Database
Groq API	AI API
Llama 3.3 70B Versatile	Question generation and evaluation
Werkzeug	Password hashing
python-dotenv	Environment configuration



---

System Architecture

┌─────────────────────┐
                    │      Candidate      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Sign Up / Login   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Interview Setup     │
                    │ Role + Skills       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI Interviewer   │
                    │  Question Generator  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    5 Questions      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Candidate Answers   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     AI Evaluator    │
                    │ Final Evaluation    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Recruiter Dashboard │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Candidate Results   │
                    │ Score / Strengths   │
                    │ Gaps / Decision     │
                    └─────────────────────┘


---

Project Structure

Interview-Agent/
│
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── agent/
│   ├── __init__.py
│   ├── interviewer.py
│   ├── evaluator.py
│   └── prompts.py
│
├── templates/
│   ├── index.html
│   ├── signup.html
│   ├── login.html
│   ├── admin_login.html
│   └── admin_dashboard.html
│
├── static/
│   ├── style.css
│   ├── script.js
│   └── admin.js
│
└── data/
    └── interviews/


---

Requirements

Before running the project, make sure you have:

Python 3.10 or newer

pip

Git

Internet connection

Groq API key



---

Installation

1. Clone the Repository

git clone YOUR_PUBLIC_GITHUB_REPOSITORY_URL
cd Interview-Agent

2. Create a Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

macOS/Linux

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt


---

API Key Configuration

Create a .env file in the project root:

GROQ_API_KEY=YOUR_GROQ_API_KEY
FLASK_SECRET_KEY=YOUR_SECRET_KEY

Replace the placeholder values with your actual credentials.

Do not commit .env to GitHub.

Add the following to .gitignore:

.env
venv/
__pycache__/
*.pyc
candidate_database.db


---

Run the Project

Open the project in VS Code.

Open:

Terminal → New Terminal

Activate the virtual environment:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the application:

python app.py

If the application starts successfully, Flask will display:

* Running on http://127.0.0.1:5000

Open the following URL in your browser:

http://127.0.0.1:5000

Keep the terminal running while using the application.

To stop the application:

Ctrl + C


---

End-to-End Workflow

Create Account
      ↓
Sign In
      ↓
Enter Target Role
      ↓
Enter Core Skills
      ↓
Start Interview
      ↓
AI Generates 5 Questions
      ↓
Answer 5 Questions
      ↓
Submit Interview
      ↓
Interview Submission Confirmation
      ↓
Recruiter/Admin Dashboard
      ↓
Review Candidate
      ↓
Review AI Evaluation
      ↓
Shortlist / Reject / Next Round


---

Candidate Workflow

1. Create Account

The candidate provides:

First name

Last name

Email

Phone number

Password

Confirm password


Example:

First Name:
Rahul

Last Name:
Sharma

Email:
rahul.sharma@example.com

Phone:
+91 9123456780

Passwords are hashed before being stored in the database.

2. Sign In

The candidate signs in using their registered email and password.

3. Enter Interview Details

Example:

Target Role:
Business Management

Core Skills:
Business Strategy,
Project Management,
Leadership,
Communication,
Data Analysis

4. Start Interview

The AI generates exactly five questions based on the role and skills.

5. Answer Questions

The candidate answers all five questions.

The application supports multi-line answers.

Empty answers are rejected.

6. Submit Interview

After the fifth answer, the interview is submitted for recruiter review.

The candidate receives a submission confirmation instead of the confidential evaluation.


---

Recruiter/Admin Workflow

The recruiter/admin can:

1. Sign in.


2. Open the dashboard.


3. View the candidate list.


4. View candidate contact information.


5. View candidate role and skills.


6. View interview questions.


7. View candidate answers.


8. View AI evaluation.


9. View overall score.


10. View strengths and gaps.


11. View recommendations.


12. Shortlist, reject, or move candidates to the next round.



Example statuses:

Completed
Under Review
Shortlisted
Rejected
Next Round


---

AI Interview Process

The interviewer generates exactly five questions using:

Target job role

Candidate skills

Different skill areas

Progressive difficulty

Conceptual understanding

Practical understanding

Problem solving


The questions are generated dynamically and may differ between runs.


---

Sample Interview Input

Target Role:
Business Management

Core Skills:
Business Strategy,
Project Management,
Leadership,
Communication,
Data Analysis


---

Sample Questions

1. What is the primary goal of business strategy in a competitive market?

2. How would you prioritize tasks and allocate resources in a project
   management scenario with multiple stakeholders?

3. Suppose you are facing a budget constraint in a project. What steps
   would you take to optimize costs without compromising quality?

4. How would you handle a conflict between two important stakeholders
   with different priorities?

5. Design or explain a data-driven approach to measure the effectiveness
   of a business strategy, including key performance indicators and
   analysis techniques?

The actual questions are generated dynamically by the AI.


---

Sample Candidate Answer

I would first identify the project's essential requirements and cost
drivers, then prioritize spending on areas that directly affect quality
and customer value. I would negotiate with vendors, optimize resource
allocation, remove unnecessary expenses, and continuously monitor the
budget while maintaining required quality standards.


---

AI Evaluation

The evaluator analyzes the complete interview after all five answers are submitted.

Evaluation criteria include:

Correctness

Relevance

Depth

Practical understanding

Problem-solving ability

Clarity

Communication

Consistency


Scoring

0–2   Very Weak
3–4   Needs Significant Improvement
5–6   Average
7–8   Strong
9     Very Strong
10    Exceptional


---

Sample AI Evaluation

{
    "overall_score": 8.0,
    "performance": "Strong",
    "strengths": [
        "Good understanding of cost optimization",
        "Practical resource allocation approach"
    ],
    "gaps": [
        "Could provide a more detailed real-world example"
    ],
    "recommendations": [
        "Explore advanced budgeting techniques"
    ],
    "summary": "The candidate demonstrated a strong understanding of project cost management and resource optimization."
}

The actual evaluation is generated dynamically.


---

Candidate Privacy

The candidate does not see the confidential AI evaluation.

The following information is available to the recruiter/admin:

Overall score

Performance

Strengths

Gaps

Recommendations

Hiring decision


The candidate only receives confirmation that the interview was successfully submitted.


---

Database

The project uses SQLite for local data storage.

Candidate information includes:

Candidate ID
First Name
Last Name
Email
Phone
Password Hash
Created Date

Interview information includes:

Interview ID
Candidate ID
Role
Skills
Questions
Answers
Overall Score
Performance
Strengths
Gaps
Recommendations
Summary
Interview Status
Created Date


---

Interview Storage

Interview data is stored under:

data/interviews/

Example:

interview_20260816_215230.json

The stored interview contains:

Timestamp

Role

Skills

Questions

Candidate answers

Final evaluation



---

AI Module Design

Interviewer

The interviewer.py module is responsible for:

Generating questions

Matching questions to the role

Using candidate skills

Controlling difficulty

Avoiding duplicate questions


Evaluator

The evaluator.py module is responsible for:

Evaluating all five answers

Calculating overall performance

Identifying strengths

Identifying gaps

Providing recommendations

Generating the final summary


Interviewer
     ↓
5 Questions
     ↓
Candidate
     ↓
5 Answers
     ↓
Evaluator
     ↓
Final Evaluation


---

Design Choices

Flask

Flask was selected because it is lightweight and provides a simple way to connect the frontend, backend, database, and AI components.

SQLite

SQLite was selected because it requires no separate database server and makes the project easy for reviewers to run locally.

For a production application with many concurrent users, PostgreSQL would be more suitable.

Groq

Groq was selected for fast model inference and suitability for an interactive interview workflow.

Llama 3.3 70B Versatile

The model was selected for question generation and evaluation because the interview requires role-specific reasoning and analysis.

Separate Interviewer and Evaluator

Question generation and evaluation are separated into different modules to improve maintainability and make the project easier to extend.

Five-Question Evaluation

The system evaluates the complete interview after all five questions instead of exposing individual evaluations to the candidate.

This provides recruiters with a more holistic assessment.


---

Security

The project includes basic security measures:

Passwords are hashed before storage.

API keys are stored in environment variables.

.env is excluded from Git.

Flask sessions are used for authentication.

Candidate evaluation results are hidden from candidates.

Recruiter/admin functionality is separated from the candidate workflow.



---

Testing

The agent should be tested with 5–10 real examples before submission.

Recommended test scenarios:

Test	Role	Skills

1	Business Management	Strategy, Leadership, Communication
2	Full Stack Developer	Python, React, SQL
3	Data Analyst	Python, SQL, Excel
4	Project Manager	Planning, Leadership, Risk Management
5	Software Engineer	Java, DSA, APIs
6	Business Analyst	SQL, Analysis, Communication
7	Data Scientist	Python, ML, Statistics
8	Product Manager	Strategy, Analytics, Leadership
9	HR Manager	Recruitment, Communication, Leadership
10	Marketing Manager	Marketing, Analytics, Strategy


Testing Checklist

Candidate registration

Duplicate email handling

Candidate login

Invalid login handling

Question generation

Exactly five questions

Role-specific questions

Skill-specific questions

Empty-answer validation

Multi-line answers

Five-question completion

Final AI evaluation

Evaluation storage

Candidate submission screen

Candidate evaluation privacy

Recruiter candidate list

Recruiter candidate details

Interview status updates



---

Sample Test Results

Replace these examples with your actual test results before submitting the project.

Test 1 - Business Management
Status: PASSED
Questions Generated: 5
Interview Completed: YES
Evaluation Generated: YES

Test 2 - Full Stack Developer
Status: PASSED
Questions Generated: 5
Interview Completed: YES
Evaluation Generated: YES

Test 3 - Data Analyst
Status: PASSED
Questions Generated: 5
Interview Completed: YES
Evaluation Generated: YES

Test 4 - Project Manager
Status: PASSED
Questions Generated: 5
Interview Completed: YES
Evaluation Generated: YES

Test 5 - Software Engineer
Status: PASSED
Questions Generated: 5
Interview Completed: YES
Evaluation Generated: YES

Actual interview transcripts and outputs should be saved in:

data/interviews/


---

Tradeoffs

SQLite vs Production Database

Advantage:
SQLite is simple and easy to configure.

Tradeoff:
SQLite is not ideal for a large production system with many concurrent users.

Future Improvement:
Use PostgreSQL or another production-grade database.

AI Evaluation vs Fixed Evaluation

Advantage:
AI can evaluate open-ended answers and identify strengths and gaps.

Tradeoff:
AI evaluation can vary between responses.

Future Improvement:
Use a standardized scoring rubric, evaluation datasets, human review, and calibration testing.

Large Model vs Smaller Model

Advantage:
A larger model provides stronger reasoning capabilities.

Tradeoff:
It may have higher latency or API cost.

Future Improvement:
Use different models depending on question complexity.


---

Limitations

Current limitations include:

SQLite is primarily suitable for the prototype/local environment.

AI-generated questions can vary between runs.

AI evaluation can vary between responses.

The system requires an active Groq API connection.

Production deployment requires additional security configuration.

Advanced recruiter analytics are not currently implemented.

Email notifications are not currently implemented.

Voice/video interviews are not currently implemented.



---

Future Improvements

Future versions could include:

PostgreSQL database

Production deployment

Advanced role-based authentication

Recruiter accounts

Email notifications

Resume upload and analysis

Voice-based interviews

Video interviews

Candidate ranking

Recruiter analytics

Interview performance charts

Adaptive interview difficulty

Automated next-round scheduling

Docker deployment

Cloud deployment

Automated unit and integration testing

Rate limiting

CSRF protection

Production logging

Monitoring and error tracking



---

Troubleshooting

GROQ_API_KEY was not found

Check that .env exists in the project root:

GROQ_API_KEY=YOUR_GROQ_API_KEY
FLASK_SECRET_KEY=YOUR_SECRET_KEY

Restart the application after changing .env.

ModuleNotFoundError

Activate the virtual environment:

venv\Scripts\activate

Then install dependencies:

pip install -r requirements.txt

Could not generate questions

Check:

1. Internet connection


2. Groq API key


3. Groq API availability


4. Terminal error message


5. AI response generated by the application



Database Error

Make sure the application is running from the project root:

cd Interview-Agent
python app.py

Application Does Not Start

Run:

python app.py

Then check the terminal for the complete error message.


---

Quick Start

git clone YOUR_PUBLIC_GITHUB_REPOSITORY_URL
cd Interview-Agent

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

Create .env:

GROQ_API_KEY=YOUR_GROQ_API_KEY
FLASK_SECRET_KEY=YOUR_SECRET_KEY

Run:

python app.py

Open:

http://127.0.0.1:5000

Then:

Create Account
      ↓
Sign In
      ↓
Enter Role + Skills
      ↓
Start Interview
      ↓
Answer 5 Questions
      ↓
Submit Interview
      ↓
Recruiter Reviews Evaluation


---

Submission Checklist

Before submitting the project:

[ ] Public GitHub repository created

[ ] All source code committed

[ ] README included

[ ] requirements.txt included

[ ] .env excluded from Git

[ ] API key configuration documented

[ ] Installation instructions tested

[ ] Application runs from a fresh clone

[ ] Candidate registration tested

[ ] Candidate login tested

[ ] Five-question interview tested

[ ] Final evaluation tested

[ ] Candidate privacy tested

[ ] Recruiter dashboard tested

[ ] 5–10 real examples tested

[ ] Sample inputs included

[ ] Sample outputs included

[ ] Interview transcripts saved

[ ] Tradeoffs documented

[ ] Limitations documented

[ ] Future improvements documented



---

Repository

GitHub Repository:

YOUR_PUBLIC_GITHUB_REPOSITORY_URL


---

Conclusion

The AI Interview Agent provides an end-to-end AI-assisted interview assessment workflow.

It combines:

Candidate authentication

Candidate personal information

Role-specific AI question generation

Skill-based interview generation

Structured five-question interviews

Multi-line answer support

Confidential AI evaluation

SQLite database storage

Recruiter candidate dashboard

Candidate scoring

Strength and gap analysis

Recruitment decision support


The project is designed so that a reviewer can clone the repository, configure the API key, install the dependencies, run the application, and test the complete interview workflow from candidate registration through recruiter evaluation.
