import re

from agent.prompts import (
    INTERVIEWER_SYSTEM_PROMPT,
    QUESTION_GENERATION_PROMPT
)


class Interviewer:
    """
    Generates exactly 5 role-specific interview questions.
    """

    def __init__(self, client):
        self.client = client


    # ==========================================================
    # GENERATE QUESTIONS
    # ==========================================================

    def generate_questions(
        self,
        role,
        skills
    ):

        prompt = QUESTION_GENERATION_PROMPT.format(
            role=role,
            skills=", ".join(skills)
        )

        response = self.client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": INTERVIEWER_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.4
        )

        text = response.choices[0].message.content.strip()


        # Show AI response in terminal for debugging
        print("\nAI QUESTION RESPONSE:")
        print(text)
        print()


        questions = self._parse_questions(text)


        if len(questions) < 5:

            raise ValueError(
                "AI did not generate 5 valid interview questions."
            )


        return questions[:5]


    # ==========================================================
    # PARSE QUESTIONS
    # ==========================================================

    def _parse_questions(self, text):

        questions = []

        # Normalize text
        text = text.replace(
            "\r\n",
            "\n"
        )

        text = text.replace(
            "**",
            ""
        )

        text = text.replace(
            "__",
            ""
        )


        # ------------------------------------------------------
        # Split response into lines
        # ------------------------------------------------------

        lines = text.split("\n")


        for line in lines:

            line = line.strip()


            if not line:
                continue


            # --------------------------------------------------
            # Remove Markdown bullets and numbering
            # --------------------------------------------------

            line = re.sub(
                r"^\s*(?:question\s*)?\d+\s*[\.\)\:\-]\s*",
                "",
                line,
                flags=re.IGNORECASE
            )


            line = re.sub(
                r"^\s*[-*•]\s*",
                "",
                line
            )


            line = line.strip()


            # --------------------------------------------------
            # Ignore headings
            # --------------------------------------------------

            if line.lower() in [
                "questions",
                "interview questions",
                "questions:",
                "interview questions:"
            ]:

                continue


            # --------------------------------------------------
            # Ignore very short lines
            # --------------------------------------------------

            if len(line) < 15:

                continue


            # --------------------------------------------------
            # Ignore instruction text
            # --------------------------------------------------

            ignored_phrases = [
                "here are",
                "below are",
                "the following questions",
                "interview questions for",
                "target role:",
                "skills:"
            ]

            if any(
                phrase in line.lower()
                for phrase in ignored_phrases
            ):

                continue


            # --------------------------------------------------
            # Accept question
            #
            # We no longer require "?"
            # because AI may sometimes return a question
            # without a question mark.
            # --------------------------------------------------

            if len(line.split()) >= 4:

                questions.append(line)


        # ------------------------------------------------------
        # Remove duplicates
        # ------------------------------------------------------

        unique_questions = []

        for question in questions:

            normalized = question.lower().strip()

            if normalized not in [
                q.lower().strip()
                for q in unique_questions
            ]:

                unique_questions.append(question)


        return unique_questions[:5]