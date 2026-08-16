import sqlite3
import json
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# ==========================================================
# DATABASE CONFIGURATION
# ==========================================================

DATABASE = "candidate_database.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_db_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def init_db():

    connection = get_db_connection()

    # ------------------------------------------------------
    # Candidates table
    # ------------------------------------------------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS candidates (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            first_name TEXT NOT NULL,

            last_name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            phone TEXT NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP

        )
    """)


    # ------------------------------------------------------
    # Interviews table
    #
    # Stores interview information separately from
    # candidate login information.
    # ------------------------------------------------------

    connection.execute("""
        CREATE TABLE IF NOT EXISTS interviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            candidate_id INTEGER NOT NULL,

            role TEXT NOT NULL,

            skills TEXT,

            status TEXT DEFAULT 'Completed',

            overall_score REAL DEFAULT 0,

            performance TEXT,

            strengths TEXT,

            gaps TEXT,

            recommendations TEXT,

            summary TEXT,

            questions TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (candidate_id)
                REFERENCES candidates(id)

        )
    """)


    connection.commit()

    connection.close()


# ==========================================================
# CREATE CANDIDATE
# ==========================================================

def create_candidate(
    first_name,
    last_name,
    email,
    phone,
    password
):

    connection = get_db_connection()

    hashed_password = generate_password_hash(
        password
    )

    try:

        connection.execute(
            """
            INSERT INTO candidates
            (
                first_name,
                last_name,
                email,
                phone,
                password
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                first_name,
                last_name,
                email,
                phone,
                hashed_password
            )
        )

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


# ==========================================================
# GET CANDIDATE BY EMAIL
# ==========================================================

def get_candidate_by_email(email):

    connection = get_db_connection()

    candidate = connection.execute(
        """
        SELECT *
        FROM candidates
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    return candidate


# ==========================================================
# GET CANDIDATE BY ID
# ==========================================================

def get_candidate_by_id(candidate_id):

    connection = get_db_connection()

    candidate = connection.execute(
        """
        SELECT *
        FROM candidates
        WHERE id = ?
        """,
        (candidate_id,)
    ).fetchone()

    connection.close()

    return candidate


# ==========================================================
# VERIFY CANDIDATE LOGIN
# ==========================================================

def verify_candidate(
    email,
    password
):

    candidate = get_candidate_by_email(
        email
    )

    if candidate is None:
        return None

    password_valid = check_password_hash(
        candidate["password"],
        password
    )

    if password_valid:
        return candidate

    return None


# ==========================================================
# SAVE INTERVIEW
# ==========================================================

def save_interview(
    candidate_id,
    role,
    skills,
    questions,
    final_report
):

    connection = get_db_connection()

    # ------------------------------------------------------
    # Convert AI report values to database-friendly strings
    # ------------------------------------------------------

    overall_score = final_report.get(
        "overall_score",
        0
    )

    performance = final_report.get(
        "performance",
        ""
    )

    strengths = json.dumps(
        final_report.get(
            "strengths",
            []
        ),
        ensure_ascii=False
    )

    gaps = json.dumps(
        final_report.get(
            "gaps",
            []
        ),
        ensure_ascii=False
    )

    recommendations = json.dumps(
        final_report.get(
            "recommendations",
            []
        ),
        ensure_ascii=False
    )

    summary = final_report.get(
        "summary",
        ""
    )

    questions_json = json.dumps(
        questions,
        ensure_ascii=False
    )

    # ------------------------------------------------------
    # Insert interview
    # ------------------------------------------------------

    cursor = connection.execute(
        """
        INSERT INTO interviews
        (
            candidate_id,
            role,
            skills,
            status,
            overall_score,
            performance,
            strengths,
            gaps,
            recommendations,
            summary,
            questions
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            candidate_id,
            role,
            ", ".join(skills),
            "Completed",
            overall_score,
            performance,
            strengths,
            gaps,
            recommendations,
            summary,
            questions_json
        )
    )

    connection.commit()

    interview_id = cursor.lastrowid

    connection.close()

    return interview_id


# ==========================================================
# GET ALL CANDIDATES
# ==========================================================

def get_all_candidates():

    connection = get_db_connection()

    candidates = connection.execute(
        """
        SELECT
            c.id,
            c.first_name,
            c.last_name,
            c.email,
            c.phone,
            c.created_at,

            i.id AS interview_id,
            i.role,
            i.overall_score,
            i.status,
            i.created_at AS interview_date

        FROM candidates c

        LEFT JOIN interviews i
            ON c.id = i.candidate_id

        ORDER BY c.created_at DESC
        """
    ).fetchall()

    connection.close()

    return candidates


# ==========================================================
# GET CANDIDATE INTERVIEW
# ==========================================================

def get_candidate_interview(
    candidate_id
):

    connection = get_db_connection()

    interview = connection.execute(
        """
        SELECT
            c.id AS candidate_id,
            c.first_name,
            c.last_name,
            c.email,
            c.phone,

            i.id AS interview_id,
            i.role,
            i.skills,
            i.status,
            i.overall_score,
            i.performance,
            i.strengths,
            i.gaps,
            i.recommendations,
            i.summary,
            i.questions,
            i.created_at

        FROM candidates c

        INNER JOIN interviews i
            ON c.id = i.candidate_id

        WHERE c.id = ?

        ORDER BY i.created_at DESC

        LIMIT 1
        """,
        (candidate_id,)
    ).fetchone()

    connection.close()

    return interview


# ==========================================================
# UPDATE INTERVIEW STATUS
# ==========================================================

def update_interview_status(
    interview_id,
    status
):

    allowed_statuses = [
        "Completed",
        "Under Review",
        "Shortlisted",
        "Rejected",
        "Next Round"
    ]

    if status not in allowed_statuses:
        return False

    connection = get_db_connection()

    cursor = connection.execute(
        """
        UPDATE interviews
        SET status = ?
        WHERE id = ?
        """,
        (
            status,
            interview_id
        )
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated


# ==========================================================
# GET INTERVIEW BY ID
# ==========================================================

def get_interview_by_id(
    interview_id
):

    connection = get_db_connection()

    interview = connection.execute(
        """
        SELECT
            c.id AS candidate_id,
            c.first_name,
            c.last_name,
            c.email,
            c.phone,

            i.id AS interview_id,
            i.role,
            i.skills,
            i.status,
            i.overall_score,
            i.performance,
            i.strengths,
            i.gaps,
            i.recommendations,
            i.summary,
            i.questions,
            i.created_at

        FROM interviews i

        INNER JOIN candidates c
            ON i.candidate_id = c.id

        WHERE i.id = ?
        """,
        (interview_id,)
    ).fetchone()

    connection.close()

    return interview