import os
import json
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for
)

from dotenv import load_dotenv
from groq import Groq

from agent.interviewer import Interviewer
from agent.evaluator import Evaluator

from database import (
    init_db,
    create_candidate,
    verify_candidate
)


# ==========================================================
# SETUP
# ==========================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found. Please check your .env file."
    )

client = Groq(api_key=api_key)

interviewer = Interviewer(client)
evaluator = Evaluator(client)

app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "interview-agent-secret-key"
)

# Initialize candidate database
init_db()


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/")
def home():

    # Candidate must be logged in
    if "candidate_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        candidate_name=session.get("candidate_name")
    )


# ==========================================================
# SIGN UP
# ==========================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template("signup.html")

    first_name = request.form.get(
        "first_name",
        ""
    ).strip()

    last_name = request.form.get(
        "last_name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    phone = request.form.get(
        "phone",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )

    # Validate fields
    if not all([
        first_name,
        last_name,
        email,
        phone,
        password,
        confirm_password
    ]):

        return render_template(
            "signup.html",
            error="Please fill in all fields."
        )

    # Check password
    if password != confirm_password:

        return render_template(
            "signup.html",
            error="Passwords do not match."
        )

    # Minimum password length
    if len(password) < 8:

        return render_template(
            "signup.html",
            error="Password must contain at least 8 characters."
        )

    # Create candidate
    created = create_candidate(
        first_name,
        last_name,
        email,
        phone,
        password
    )

    if not created:

        return render_template(
            "signup.html",
            error="An account with this email already exists."
        )

    return redirect(
        url_for("login")
    )


# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )

    if not email or not password:

        return render_template(
            "login.html",
            error="Please enter your email and password."
        )

    candidate = verify_candidate(
        email,
        password
    )

    if candidate is None:

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    # Store candidate information in session
    session["candidate_id"] = candidate["id"]

    session["candidate_name"] = (
        candidate["first_name"]
        + " "
        + candidate["last_name"]
    )

    session["candidate_email"] = candidate["email"]

    return redirect(
        url_for("home")
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ==========================================================
# START INTERVIEW
# ==========================================================

@app.route("/start", methods=["POST"])
def start_interview():

    # Candidate must be logged in
    if "candidate_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please sign in before starting the interview."
        }), 401

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400

    role = data.get(
        "role",
        ""
    ).strip()

    skills_input = data.get(
        "skills",
        ""
    ).strip()

    if not role:

        return jsonify({
            "success": False,
            "message": "Please enter a job role."
        }), 400

    if not skills_input:

        return jsonify({
            "success": False,
            "message": "Please enter at least one skill."
        }), 400

    skills = [
        skill.strip()
        for skill in skills_input.split(",")
        if skill.strip()
    ]

    try:

        print("\n" + "=" * 60)
        print("GENERATING INTERVIEW QUESTIONS")
        print("=" * 60)

        questions = interviewer.generate_questions(
            role,
            skills
        )

        if len(questions) < 5:

            return jsonify({
                "success": False,
                "message": "Could not generate 5 questions."
            }), 500

        # Use exactly 5 questions
        questions = questions[:5]

        # Store interview information
        session["role"] = role
        session["skills"] = skills
        session["questions"] = questions
        session["answers"] = []
        session["current_question"] = 0

        print(
            f"Candidate: {session.get('candidate_name')}"
        )

        print(
            f"Role: {role}"
        )

        print(
            "5 questions generated successfully."
        )

        return jsonify({
            "success": True,
            "question": questions[0],
            "question_number": 1,
            "total_questions": 5
        })

    except Exception as e:

        print(
            "Question generation error:",
            str(e)
        )

        return jsonify({
            "success": False,
            "message": "An error occurred while generating questions."
        }), 500


# ==========================================================
# SUBMIT ANSWER
# ==========================================================

@app.route("/submit", methods=["POST"])
def submit_answer():

    # Candidate must be logged in
    if "candidate_id" not in session:

        return jsonify({
            "success": False,
            "message": "Please sign in before submitting answers."
        }), 401

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "Invalid request."
        }), 400

    answer = data.get(
        "answer",
        ""
    ).strip()

    if not answer:

        return jsonify({
            "success": False,
            "message": "Please enter an answer."
        }), 400

    questions = session.get(
        "questions",
        []
    )

    answers = session.get(
        "answers",
        []
    )

    if not questions:

        return jsonify({
            "success": False,
            "message": "No active interview found."
        }), 400

    # Prevent more than 5 answers
    if len(answers) >= 5:

        return jsonify({
            "success": False,
            "message": "This interview has already been completed."
        }), 400

    # Save current answer
    answers.append(answer)

    session["answers"] = answers
    session.modified = True

    print(
        f"\nAnswer {len(answers)} of 5 received."
    )

    # ======================================================
    # ALL 5 QUESTIONS COMPLETED
    # ======================================================

    if len(answers) == 5:

        print("\n" + "=" * 60)
        print("ALL 5 ANSWERS RECEIVED")
        print("=" * 60)

        role = session.get(
            "role",
            ""
        )

        skills = session.get(
            "skills",
            []
        )

        # Create evaluation results
        results = []

        for index in range(5):

            results.append({
                "question_number": index + 1,
                "question": questions[index],
                "answer": answers[index]
            })

        try:

            print(
                "\nGenerating final AI evaluation..."
            )

            # Evaluate all 5 answers together
            final_report = evaluator.final_evaluation(
                role,
                skills,
                results
            )

            print(
                "\nFinal evaluation generated successfully."
            )

            # ==================================================
            # SAVE INTERVIEW
            # ==================================================

            os.makedirs(
                "data/interviews",
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            candidate_id = session.get(
                "candidate_id"
            )

            filename = (
                f"data/interviews/"
                f"candidate_{candidate_id}_"
                f"interview_{timestamp}.json"
            )

            interview_data = {

                "candidate_id": candidate_id,

                "candidate_name": session.get(
                    "candidate_name"
                ),

                "candidate_email": session.get(
                    "candidate_email"
                ),

                "timestamp": datetime.now().isoformat(),

                "role": role,

                "skills": skills,

                "questions": results,

                "final_evaluation": final_report
            }

            with open(
                filename,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    interview_data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            print(
                f"\nInterview saved to: {filename}"
            )

            # Store only completion status
            # Do NOT send evaluation to candidate
            session["interview_completed"] = True

            # Remove confidential evaluation from session
            session.pop(
                "final_report",
                None
            )

            return jsonify({
                "success": True,
                "completed": True,
                "message": "Interview submitted successfully."
            })

        except Exception as e:

            print(
                "\nEvaluation error:",
                str(e)
            )

            return jsonify({
                "success": False,
                "message": "Could not generate final evaluation."
            }), 500

    # ======================================================
    # MORE QUESTIONS REMAIN
    # ======================================================

    next_question_number = len(answers) + 1

    session["current_question"] = len(answers)

    return jsonify({
        "success": True,
        "completed": False,
        "question": questions[len(answers)],
        "question_number": next_question_number,
        "total_questions": 5
    })


# ==========================================================
# RESULT / SUBMISSION PAGE
# ==========================================================

@app.route("/result")
def result():

    if "candidate_id" not in session:

        return redirect(
            url_for("login")
        )

    # Candidate should never receive the evaluation
    return redirect(
        url_for("home")
    )


# ==========================================================
# RESET INTERVIEW
# ==========================================================

@app.route("/reset")
def reset():

    # Do NOT clear login information
    candidate_id = session.get(
        "candidate_id"
    )

    candidate_name = session.get(
        "candidate_name"
    )

    candidate_email = session.get(
        "candidate_email"
    )

    # Clear only interview information
    session.pop(
        "role",
        None
    )

    session.pop(
        "skills",
        None
    )

    session.pop(
        "questions",
        None
    )

    session.pop(
        "answers",
        None
    )

    session.pop(
        "current_question",
        None
    )

    session.pop(
        "interview_completed",
        None
    )

    # Restore candidate information
    if candidate_id is not None:

        session["candidate_id"] = candidate_id

    if candidate_name is not None:

        session["candidate_name"] = candidate_name

    if candidate_email is not None:

        session["candidate_email"] = candidate_email

    return jsonify({
        "success": True
    })


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )