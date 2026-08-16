import json

from agent.prompts import (
    INTERVIEWER_SYSTEM_PROMPT,
    FINAL_EVALUATION_PROMPT
)


class Evaluator:
    """
    Evaluates all 5 candidate answers together
    after the interview is completed.

    The evaluation is intended for the recruiter,
    not for the candidate.
    """

    def __init__(self, client):
        self.client = client


    # ======================================================
    # FINAL EVALUATION
    # ======================================================

    def final_evaluation(
        self,
        role,
        skills,
        results
    ):
        """
        Evaluate all 5 answers together and return
        a structured JSON interview report.
        """

        prompt = FINAL_EVALUATION_PROMPT.format(
            role=role,
            skills=", ".join(skills),
            results=json.dumps(
                results,
                indent=2,
                ensure_ascii=False
            )
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

            temperature=0.2
        )


        text = response.choices[0].message.content.strip()


        # ==================================================
        # REMOVE MARKDOWN CODE FENCES
        # ==================================================

        if text.startswith("```"):

            text = text.replace(
                "```json",
                ""
            )

            text = text.replace(
                "```",
                ""
            )

            text = text.strip()


        # ==================================================
        # PARSE JSON
        # ==================================================

        try:

            evaluation = json.loads(text)


            # Make sure required fields exist
            evaluation.setdefault(
                "overall_score",
                0
            )

            evaluation.setdefault(
                "performance",
                "Not specified"
            )

            evaluation.setdefault(
                "strengths",
                []
            )

            evaluation.setdefault(
                "gaps",
                []
            )

            evaluation.setdefault(
                "recommendations",
                []
            )

            evaluation.setdefault(
                "summary",
                ""
            )


            # Keep score within 0-10
            try:

                score = float(
                    evaluation["overall_score"]
                )

                score = max(
                    0,
                    min(
                        10,
                        score
                    )
                )

                evaluation["overall_score"] = score

            except (
                ValueError,
                TypeError
            ):

                evaluation["overall_score"] = 0


            return evaluation


        except json.JSONDecodeError:

            # ==================================================
            # FALLBACK
            # ==================================================

            return {
                "overall_score": 0,

                "performance":
                    "Evaluation generated but JSON parsing failed.",

                "strengths": [],

                "gaps": [],

                "recommendations": [],

                "summary": text
            }