import sqlite3
import json
from datetime import datetime
from pathlib import Path


# =========================================================
# DATABASE CONFIGURATION
# =========================================================

DB_PATH = Path(__file__).parent / "study_history.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(DB_PATH)


# =========================================================
# CREATE / UPGRADE DATABASE
# =========================================================

def init_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_type TEXT NOT NULL,
            subject TEXT,
            file_path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # =====================================================
    # ADVANCED HISTORY COLUMNS
    # =====================================================

    new_columns = {

        "title": "TEXT",

        "transcript": "TEXT",

        "summary": "TEXT",

        "key_concepts": "TEXT",

        "topics": "TEXT",

        "flashcards": "TEXT",

        "quiz": "TEXT",

        "quiz_score": "INTEGER DEFAULT 0",

        "is_favorite": "INTEGER DEFAULT 0"
    }

    # =====================================================
    # CHECK EXISTING COLUMNS
    # =====================================================

    cursor.execute(
        "PRAGMA table_info(study_history)"
    )

    existing_columns = {
        column[1]
        for column in cursor.fetchall()
    }

    # =====================================================
    # ADD MISSING COLUMNS
    # =====================================================

    for column_name, column_type in new_columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE study_history
                ADD COLUMN {column_name} {column_type}
                """
            )

    connection.commit()
    connection.close()


# =========================================================
# ADD HISTORY ITEM
# =========================================================

def add_history(
    file_name,
    file_type,
    subject,
    file_path
):

    connection = get_connection()
    cursor = connection.cursor()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute(
        """
        INSERT INTO study_history
        (
            file_name,
            file_type,
            subject,
            file_path,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            file_name,
            file_type,
            subject,
            file_path,
            created_at
        )
    )

    connection.commit()

    history_id = cursor.lastrowid

    connection.close()

    return history_id


# =========================================================
# SAVE COMPLETE STUDY SESSION
# =========================================================

def save_study_session(
    history_id,
    title=None,
    transcript=None,
    summary=None,
    key_concepts=None,
    topics=None,
    flashcards=None,
    quiz=None,
    quiz_score=0
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE study_history

        SET
            title = ?,
            transcript = ?,
            summary = ?,
            key_concepts = ?,
            topics = ?,
            flashcards = ?,
            quiz = ?,
            quiz_score = ?

        WHERE id = ?
        """,
        (
            title,

            transcript,

            summary,

            json.dumps(
                key_concepts or []
            ),

            json.dumps(
                topics or []
            ),

            json.dumps(
                flashcards or []
            ),

            json.dumps(
                quiz or []
            ),

            quiz_score,

            history_id
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# GET ALL HISTORY
# =========================================================

def get_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            file_name,
            file_type,
            subject,
            file_path,
            created_at,
            title,
            transcript,
            summary,
            key_concepts,
            topics,
            flashcards,
            quiz,
            quiz_score,
            is_favorite

        FROM study_history

        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


# =========================================================
# GET ONE COMPLETE STUDY SESSION
# =========================================================

def get_study_session(history_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            file_name,
            file_type,
            subject,
            file_path,
            created_at,
            title,
            transcript,
            summary,
            key_concepts,
            topics,
            flashcards,
            quiz,
            quiz_score,
            is_favorite

        FROM study_history

        WHERE id = ?
        """,
        (history_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if not row:
        return None

    # =====================================================
    # CONVERT DATABASE DATA BACK TO PYTHON
    # =====================================================

    session = {

        "id": row[0],

        "file_name": row[1],

        "file_type": row[2],

        "subject": row[3],

        "file_path": row[4],

        "created_at": row[5],

        "title": row[6],

        "transcript": row[7],

        "summary": row[8],

        "key_concepts": json.loads(
            row[9] or "[]"
        ),

        "topics": json.loads(
            row[10] or "[]"
        ),

        "flashcards": json.loads(
            row[11] or "[]"
        ),

        "quiz": json.loads(
            row[12] or "[]"
        ),

        "quiz_score": row[13] or 0,

        "is_favorite": bool(
            row[14]
        )
    }

    return session


# =========================================================
# DELETE ONE HISTORY ITEM
# =========================================================

def delete_history(history_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM study_history
        WHERE id = ?
        """,
        (history_id,)
    )

    connection.commit()
    connection.close()


# =========================================================
# DELETE ALL HISTORY
# =========================================================

def delete_all_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM study_history"
    )

    connection.commit()
    connection.close()


# =========================================================
# TOGGLE FAVORITE
# =========================================================

def toggle_favorite(history_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE study_history

        SET is_favorite =
            CASE
                WHEN is_favorite = 1 THEN 0
                ELSE 1
            END

        WHERE id = ?
        """,
        (history_id,)
    )

    connection.commit()
    connection.close()


# =========================================================
# UPDATE QUIZ SCORE
# =========================================================

def update_quiz_score(
    history_id,
    score
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE study_history

        SET quiz_score = ?

        WHERE id = ?
        """,
        (
            score,
            history_id
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

init_database()