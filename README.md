# AI Interview Agent

An AI-powered interview assessment platform that conducts structured,
role-specific interviews and provides confidential AI-based evaluation
for recruiters.

The system allows candidates to create an account, complete a
five-question AI interview, and submit their responses for recruiter
review. Recruiters can review candidate information, interview
responses, AI evaluation, and decide whether a candidate should proceed
to the next recruitment round.

---

## 1. Project Overview

### Problem

Traditional interview screening can be time-consuming and may result in
inconsistent evaluation across candidates.

Recruiters need a structured way to:

- Collect candidate information
- Conduct consistent interviews
- Evaluate candidate responses
- Identify strengths and skill gaps
- Review candidates efficiently
- Decide who should proceed to the next round

### Solution

The AI Interview Agent provides an end-to-end interview workflow.

The system:

1. Registers candidates.
2. Authenticates candidates.
3. Collects the target role and core skills.
4. Generates exactly 5 role-specific interview questions.
5. Collects candidate answers.
6. Evaluates the complete interview after all 5 questions.
7. Generates a confidential AI evaluation.
8. Stores candidate and interview information.
9. Provides recruiter/admin access to candidate results.
10. Supports recruitment decisions such as shortlisting and moving
   candidates to the next round.

---

# 2. Main Features

## Candidate Features

- Candidate registration
- Candidate login
- Candidate personal information
- Email and phone collection
- Password hashing
- Target role selection
- Core skill selection
- AI-generated interview questions
- Five-question structured interview
- Multi-line answers
- Empty-answer validation
- Interview submission confirmation
- Candidate session management

## AI Interview Features

- Role-specific question generation
- Skill-specific questions
- Conceptual questions
- Practical questions
- Problem-solving questions
- Scenario-based questions
- Progressive difficulty
- Duplicate-question avoidance
- Evaluation after all five questions
- Overall score from 0 to 10
- Performance classification
- Strength identification
- Skill-gap identification
- Improvement recommendations
- Final interview summary

## Recruiter/Admin Features

- Admin authentication
- Candidate dashboard
- Candidate list
- Candidate contact information
- Candidate role and skills
- Interview status
- Interview score
- Complete interview responses
- AI evaluation
- Candidate strengths
- Candidate gaps
- Recommendations
- Shortlist candidates
- Reject candidates
- Move candidates to the next round

## Candidate Privacy

The candidate does not receive the confidential AI evaluation.

After completing all five questions, the candidate sees a submission
confirmation instead of:

- Overall score
- Strengths
- Skill gaps
- Recommendations
- Hiring decision

These details are intended for recruiter/admin review.

---

# 3. Technology Stack

## Frontend

- HTML5
- CSS3
- JavaScript

## Backend

- Python
- Flask

## AI

- Groq API
- Llama 3.3 70B Versatile

## Database

- SQLite

## Security

- Werkzeug password hashing
- Flask sessions
- Environment variables
- Candidate/admin access separation

---

# 4. Project Architecture

```text
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
                    │    Interviewer      │
                    │  Question Generator │
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
                    │     Evaluator       │
                    │ Final AI Evaluation │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
       ┌──────────────────┐        ┌────────────────────┐
       │ Candidate        │        │ Recruiter/Admin    │
       │ Submission Page  │        │ Dashboard          │
       └──────────────────┘        └─────────┬──────────┘
                                             │
                                             ▼
                                  ┌────────────────────┐
                                  │ Candidate Results  │
                                  │ Score / Strengths  │
                                  │ Gaps / Decision    │
                                  └────────────────────┘
