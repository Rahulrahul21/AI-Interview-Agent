
import os
import json
from datetime import datetime

from dotenv import load_dotenv
from groq import Groq

from agent.interviewer import Interviewer
from agent.evaluator import Evaluator


# ==========================================================
# SETUP
# ==========================================================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: GROQ_API_KEY was not found.")
    print("Please check your .env file.")
    exit()

client = Groq(api_key=api_key)

interviewer = Interviewer(client)
evaluator = Evaluator(client)


# ==========================================================
# DISPLAY HEADER
# ==========================================================

print("=" * 60)
print("              AI INTERVIEW AGENT")
print("=" * 60)


# ==========================================================
# GET CANDIDATE INFORMATION
# ==========================================================

role = input("\nEnter the target job role: ").strip()

skills_input = input(
    "Enter skills separated by commas: "
).strip()

skills = [
    skill.strip()
    for skill in skills_input.split(",")
    if skill.strip()
]


# ==========================================================
# GENERATE QUESTIONS
# ==========================================================

print("\nGenerating interview questions...")

questions = interviewer.generate_questions(
    role,
    skills
)

if len(questions) < 5:
    print("\nCould not generate 5 questions.")
    print("Generated questions:", questions)
    exit()

# Use only first 5 questions
questions = questions[:5]

print("\n5 questions generated successfully.")


# ==========================================================
# CONDUCT INTERVIEW
# ==========================================================

results = []

for index, question in enumerate(questions, start=1):

    print("\n" + "-" * 60)
    print(f"QUESTION {index} OF 5")
    print("-" * 60)

    print(question)

    print("\nYour answer:")
    print("(You can write multiple lines.)")
    print("(Press Enter twice when you are completely finished.)")

    answer_lines = []
    empty_line_count = 0

    while True:

        line = input()

        # --------------------------------------------------
        # Handle blank lines
        # --------------------------------------------------

        if line.strip() == "":

            # If no answer has been entered yet
            if not answer_lines:
                print("Please enter an answer.")
                continue

            # First blank line
            if empty_line_count == 0:
                empty_line_count = 1
                answer_lines.append("")
                continue

            # Second consecutive blank line = answer finished
            break

        # --------------------------------------------------
        # Normal text
        # --------------------------------------------------

        answer_lines.append(line)
        empty_line_count = 0

    # Remove unnecessary blank lines from beginning/end
    answer = "\n".join(answer_lines).strip()

    if not answer:
        print("Answer cannot be empty.")
        continue

    # ------------------------------------------------------
    # IMPORTANT:
    # DO NOT EVALUATE THE ANSWER HERE
    # ------------------------------------------------------

    print("\nAnswer recorded successfully.")

    results.append(
        {
            "question_number": index,
            "question": question,
            "answer": answer
        }
    )


# ==========================================================
# ALL 5 QUESTIONS COMPLETED
# NOW PERFORM FINAL EVALUATION
# ==========================================================

print("\n" + "=" * 60)
print("              INTERVIEW COMPLETED")
print("=" * 60)

print("\nAll 5 answers have been recorded.")
print("Evaluating the complete interview...")
print("Please wait...\n")


final_report = evaluator.final_evaluation(
    role,
    skills,
    results
)


# ==========================================================
# DISPLAY FINAL EVALUATION
# ==========================================================

print("\n" + "=" * 60)
print("              FINAL EVALUATION")
print("=" * 60)

print("\n")
print(final_report)


# ==========================================================
# SAVE TRANSCRIPT
# ==========================================================

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

filename = (
    f"data/interviews/"
    f"interview_{timestamp}.json"
)

interview_data = {
    "timestamp": datetime.now().isoformat(),
    "role": role,
    "skills": skills,
    "questions": results,
    "final_evaluation": final_report
}


# Create directory if it does not exist
os.makedirs(
    "data/interviews",
    exist_ok=True
)


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


print("\n" + "=" * 60)
print("Interview completed successfully!")
print(f"Transcript saved to: {filename}")
print("=" * 60)

