import streamlit as st
import os
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from history import (
    add_history,
    save_study_session,
    get_study_session,
    update_quiz_score,
    toggle_favorite,
    get_history,
    delete_history
)


# =========================================================
# GEMINI SETUP
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)
# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Voice Notes to Flashcards",
    page_icon="🎙️",
    layout="wide"
)

# =========================================================
# GEMINI SETUP
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)

# =========================================================
# SESSION STATE
# =========================================================

if "study_material" not in st.session_state:
    st.session_state.study_material = None

if "flashcards" not in st.session_state:
    st.session_state.flashcards = []

if "quiz" not in st.session_state:
    st.session_state.quiz = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False

if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

# =========================================================
# AUDIO HISTORY STORAGE
# =========================================================

AUDIO_HISTORY_DIR = Path(__file__).parent / "audio_history"
AUDIO_HISTORY_DIR.mkdir(exist_ok=True)

# =========================================================
# HEADER
# =========================================================

st.title("🎙️ Voice Notes to Flashcards")

st.write(
    "Turn your lecture voice notes into AI-powered "
    "summaries, flashcards and quizzes."
)

st.divider()
# =========================================================
# STUDY HISTORY BUTTON
# =========================================================

if "show_history" not in st.session_state:
    st.session_state.show_history = False

history_button_col1, history_button_col2, history_button_col3 = st.columns(
    [1, 2, 1]
)

with history_button_col2:

    if st.button(
        "📜 Open Study History",
        use_container_width=True,
        key="open_study_history"
    ):
        st.session_state.show_history = not st.session_state.show_history


# =========================================================
# STUDY HISTORY CENTER
# =========================================================

if st.session_state.show_history:

    from history import get_history, delete_history

    st.divider()

    st.header("📜 Study History")

    st.caption(
        "Your previous lecture recordings and uploaded audio files."
    )

    # -----------------------------------------------------
    # GET HISTORY
    # -----------------------------------------------------

    history_records = get_history()

    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    total_sessions = len(history_records)

    recording_count = sum(
        1
        for item in history_records
        if item[2] == "recording"
    )

    upload_count = sum(
        1
        for item in history_records
        if item[2] == "upload"
    )

    st.subheader("📊 Study Statistics")

    stat1, stat2, stat3 = st.columns(3)

    with stat1:
        st.metric(
            "📚 Total Sessions",
            total_sessions
        )

    with stat2:
        st.metric(
            "🎙️ Recordings",
            recording_count
        )

    with stat3:
        st.metric(
            "📁 Uploads",
            upload_count
        )

    # -----------------------------------------------------
    # SEARCH AND FILTER
    # -----------------------------------------------------

    if history_records:

        st.subheader("🔎 Find Previous Lectures")

        search_col, filter_col = st.columns([2, 1])

        with search_col:

            search_text = st.text_input(
                "🔍 Search",
                placeholder="Search by filename or subject...",
                key="history_search"
            )

        with filter_col:

            filter_type = st.selectbox(
                "📂 Type",
                [
                    "All",
                    "🎙️ Recordings",
                    "📁 Uploads"
                ],
                key="history_filter"
            )

        filtered_records = history_records

        # Search
        if search_text:

            search_text_lower = search_text.lower()

            filtered_records = [
                item
                for item in filtered_records
                if (
                    search_text_lower in item[1].lower()
                    or (
                        item[3]
                        and search_text_lower in item[3].lower()
                    )
                )
            ]

        # Filter
        if filter_type == "🎙️ Recordings":

            filtered_records = [
                item
                for item in filtered_records
                if item[2] == "recording"
            ]

        elif filter_type == "📁 Uploads":

            filtered_records = [
                item
                for item in filtered_records
                if item[2] == "upload"
            ]

        st.caption(
            f"Showing {len(filtered_records)} history item(s)"
        )

        # -------------------------------------------------
        # HISTORY ITEMS
        # -------------------------------------------------

        for item in filtered_records:

            history_id = item[0]
            file_name = item[1]
            file_type = item[2]
            item_subject = item[3]
            file_path = item[4]
            created_at = item[5]

            if file_type == "recording":

                icon = "🎙️"
                type_name = "Audio Recording"

            else:

                icon = "📁"
                type_name = "Uploaded Audio"

            with st.container(border=True):

                item_col1, item_col2 = st.columns(
                    [5, 1]
                )

                with item_col1:

                    st.subheader(
                        f"{icon} {file_name}"
                    )

                    st.caption(
                        f"📅 {created_at}  •  "
                        f"🎵 {type_name}"
                    )

                
                with item_col2:

                            if st.button(
        "🗑️ Delete",
        key=f"delete_history_{history_id}",
        use_container_width=True
    ):
                                delete_history(history_id)

        if os.path.exists(file_path):
            os.remove(file_path)

        st.success(
            "History item deleted successfully!"
        )

        st.rerun()

            


                    # =================================================
                    # DELETE HISTORY
                    # =================================================

        if st.button(
                        "🗑️ Delete",
                        key=f"delete_history_{history_id}",
                        use_container_width=True
                    ):

                        delete_history(history_id)

                        # Delete physical audio file
                        if os.path.exists(file_path):

                            os.remove(file_path)

                        st.success(
                            "History item deleted successfully!"
                        )

                        st.rerun()
                    
                        delete_history(history_id)

                        # Delete physical audio file
                        if os.path.exists(file_path):

                            os.remove(file_path)

                        st.success(
                            "History item deleted successfully!"
                        )

                        st.rerun()

    else:

        st.info(
            "📭 No study history yet."
        )

        st.write(
            "Record or upload a lecture to create your first history item."
        )

    st.divider()
    # =========================================================
# DISPLAY SELECTED STUDY SESSION
# =========================================================



    selected_id = st.session_state.selected_history_id

    selected_session = get_study_session(selected_id)

    if selected_session:

        st.divider()

        st.header("📖 Previous Study Session")

        st.subheader(
            selected_session.get(
                "title",
                "Study Session"
            )
        )

        st.caption(
            f"📚 Subject: "
            f"{selected_session.get('subject', 'Unknown')}"
        )

        # =================================================
        # TRANSCRIPT
        # =================================================

        st.subheader("📝 Lecture Transcript")

        transcript = selected_session.get(
            "transcript",
            ""
        )

        if transcript:

            with st.expander(
                "View Transcript",
                expanded=True
            ):

                st.write(transcript)

        else:

            st.warning(
                "No transcript was saved for this session."
            )

        # =================================================
        # SUMMARY
        # =================================================

        st.subheader("📖 Summary")

        summary = selected_session.get(
            "summary",
            ""
        )

        if summary:
            st.write(summary)

        else:
            st.info("No summary available.")

        # =================================================
        # KEY CONCEPTS
        # =================================================

        st.subheader("🧠 Key Concepts")

        concepts = selected_session.get(
            "key_concepts",
            []
        )

        if concepts:

            for concept in concepts:

                st.info(
                    f"💡 {concept}"
                )

        else:

            st.info(
                "No key concepts available."
            )

        # =================================================
        # FLASHCARDS
        # =================================================

        st.subheader("📚 Flashcards")

        flashcards = selected_session.get(
            "flashcards",
            []
        )

        if flashcards:

            st.dataframe(
                pd.DataFrame(flashcards),
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No flashcards available."
            )

        # =================================================
        # QUIZ
        # =================================================

        st.subheader("🎯 Quiz")

        quiz = selected_session.get(
            "quiz",
            []
        )

        if quiz:

            for index, question in enumerate(quiz):

                st.write(
                    f"**Question {index + 1}: "
                    f"{question.get('question', '')}**"
                )

                for option in question.get(
                    "options",
                    []
                ):

                    st.write(
                        f"- {option}"
                    )

                st.caption(
                    f"✅ Answer: "
                    f"{question.get('answer', '')}"
                )

        else:

            st.info(
                "No quiz available."
            )

        # =================================================
        # SCORE
        # =================================================

        st.metric(
            "🏆 Quiz Score",
            f"{selected_session.get('quiz_score', 0)}%"
        )

        # =================================================
        # CLOSE
        # =================================================

        if st.button(
            "❌ Close Study Session",
            use_container_width=True,
            key="close_selected_session"
        ):

            st.session_state.selected_history_id = None

            st.rerun()

    else:

        st.error(
            "⚠️ Could not load this study session."
        )
    # =========================================================
# OPEN SELECTED STUDY SESSION
# =========================================================

if "selected_history_id" in st.session_state:

    selected_id = st.session_state.selected_history_id

    selected_session = get_study_session(
        selected_id
    )

    if selected_session:

        st.divider()

        st.header(
            f"📖 {selected_session.get('title', 'Study Session')}"
        )

        st.caption(
            f"📚 Subject: {selected_session.get('subject', 'Unknown')}"
        )

        # -------------------------------------------------
        # TRANSCRIPT
        # -------------------------------------------------

        st.subheader("📝 Transcript")

        st.write(
            selected_session.get(
                "transcript",
                "No transcript available."
            )
        )

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        st.subheader("📖 Summary")

        st.write(
            selected_session.get(
                "summary",
                "No summary available."
        ))

        # -------------------------------------------------
        # KEY CONCEPTS
        # -------------------------------------------------

        st.subheader("🧠 Key Concepts")

        concepts = selected_session.get(
            "key_concepts",
            []
        )

        for concept in concepts:

            st.info(
                f"💡 {concept}"
            )

        # -------------------------------------------------
        # FLASHCARDS
        # -------------------------------------------------

        st.subheader("📚 Flashcards")

        flashcards = selected_session.get(
            "flashcards",
            []
        )

        if flashcards:

            st.dataframe(
                pd.DataFrame(flashcards),
                use_container_width=True,
                hide_index=True
            )

        # -------------------------------------------------
        # QUIZ
        # -------------------------------------------------

        st.subheader("🎯 Quiz")

        quiz = selected_session.get(
            "quiz",
            []
        )

        if quiz:

            for index, question in enumerate(quiz):

                st.write(
                    f"**{index + 1}. "
                    f"{question.get('question', '')}**"
                )

                options = question.get(
                    "options",
                    []
                )

                for option in options:

                    st.write(
                        f"- {option}"
                    )

                st.caption(
                    f"✅ Answer: "
                    f"{question.get('answer', '')}"
                )

        # -------------------------------------------------
        # QUIZ SCORE
        # -------------------------------------------------

        st.metric(
            "🏆 Previous Quiz Score",
            f"{selected_session.get('quiz_score', 0)}%"
        )

        if st.button(
            "❌ Close Study Session",
            use_container_width=True
        ):

            del st.session_state.selected_history_id

            st.rerun()

# =========================================================
# SIDEBAR SETTINGS
# =========================================================

st.sidebar.header("⚙️ Study Settings")

subject = st.sidebar.selectbox(
    "📚 Subject",
    [
        "Machine Learning",
        "Artificial Intelligence",
        "Python",
        "Data Structures",
        "Database Management Systems",
        "Operating Systems",
        "Computer Networks",
        "Other"
    ]
)

difficulty = st.sidebar.selectbox(
    "🎯 Difficulty",
    [
        "Easy",
        "Intermediate",
        "Hard"
    ]
)

number_of_cards = st.sidebar.slider(
    "📚 Number of Flashcards",
    5,
    30,
    10,
    5
)

include_summary = st.sidebar.checkbox(
    "📝 Generate Summary",
    True
)

include_quiz = st.sidebar.checkbox(
    "🎯 Generate Quiz",
    True
)

# =========================================================
# HOW THE AI STUDY ASSISTANT WORKS
# =========================================================

with st.expander(
    "ℹ️ How this AI Study Assistant works",
    expanded=False
):

    st.markdown("""
### 🎙️ Step 1 — Record or Upload

Record your lecture or upload an existing audio file.

### 🤖 Step 2 — Gemini AI

Gemini analyzes your lecture and identifies the important information.

### 📝 Step 3 — Study Material

The app generates:

- Lecture transcript
- Summary
- Key concepts
- Flashcards
- Practice quiz

### 🎯 Step 4 — Practice

Use the flashcards and quiz to prepare for your exams.
""")
 #=========================================================
# DASHBOARD METRICS
# =========================================================

st.subheader("📊 Study Dashboard")

flashcard_count = len(
    st.session_state.flashcards
)

quiz_count = len(
    st.session_state.quiz
)

score = st.session_state.get(
    "score",
    0
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "📚 Flashcards",
        flashcard_count,
        delta=(
            f"+{flashcard_count}"
            if flashcard_count > 0
            else "Waiting"
        )
    )

with col2:

    st.metric(
        "🎯 Quiz Questions",
        quiz_count,
        delta=(
            f"+{quiz_count}"
            if quiz_count > 0
            else "Waiting"
        )
    )

with col3:

    st.metric(
        "🏆 Quiz Score",
        f"{score}%",
        delta=(
            "Completed"
            if score > 0
            else "Not attempted"
        )
    )

with col4:

    st.metric(
        "🤖 AI Engine",
        "Gemini",
        delta="Online"
    )

st.divider()
with st.expander(
    "ℹ️ How this AI Study Assistant works",
    expanded=False
):

    st.markdown("""
### 🎙️ Step 1 — Record or Upload

Record your lecture or upload an existing audio file.

### 🤖 Step 2 — Gemini AI

Gemini analyzes your lecture and identifies the important information.

### 📝 Step 3 — Study Material

The app generates:

- Lecture transcript
- Summary
- Key concepts
- Flashcards
- Practice quiz

### 🎯 Step 4 — Practice

Use the flashcards and quiz to prepare for your exams.
""")
    
# =========================================================
# AUDIO INPUT
# =========================================================

audio_col1, audio_col2 = st.columns(2)

with audio_col1:

    st.subheader("🎙️ Record Lecture")

    audio_recording = st.audio_input(
        "Record your lecture notes"
    )

    if audio_recording:

        st.success("Recording received! ✅")

        st.audio(audio_recording)

        # Create a unique ID for this recording
        recording_id = (
            f"recording_{len(audio_recording.getvalue())}_"
            f"{audio_recording.type}"
        )

        # Save only if this is a new recording
        if st.session_state.last_audio_id != recording_id:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            recording_filename = (
                f"lecture_recording_{timestamp}.wav"
            )

            recording_path = (
                AUDIO_HISTORY_DIR /
                recording_filename
            )

            with open(recording_path, "wb") as audio_file:
                audio_file.write(
                    audio_recording.getvalue()
                )

            history_id = add_history(
                file_name=recording_filename,
                file_type="recording",
                subject=subject,
                file_path=str(recording_path)
)

            st.session_state.last_history_id = history_id
            st.session_state.last_audio_id = recording_id

            st.success(
                "📜 Recording saved to History!"
            )


with audio_col2:

    st.subheader("📁 Upload Lecture")

    uploaded_audio = st.file_uploader(
        "Upload an audio file",
        type=[
            "mp3",
            "wav",
            "m4a",
            "ogg",
            "webm"
        ]
    )

    if uploaded_audio:

        st.success("Audio uploaded! ✅")

        st.audio(uploaded_audio)

        # Create a unique ID for this uploaded file
        upload_id = (
            f"upload_{uploaded_audio.name}_"
            f"{uploaded_audio.size}"
        )

        # Save only if this is a new upload
        if st.session_state.last_audio_id != upload_id:

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            original_name = Path(
                uploaded_audio.name
            ).stem

            extension = Path(
                uploaded_audio.name
            ).suffix

            upload_filename = (
                f"{original_name}_{timestamp}{extension}"
            )

            upload_path = (
                AUDIO_HISTORY_DIR /
                upload_filename
            )

            with open(upload_path, "wb") as audio_file:
                audio_file.write(
                    uploaded_audio.getvalue()
                )

            add_history(
                file_name=uploaded_audio.name,
                file_type="upload",
                subject=subject,
                file_path=str(upload_path)
            )

            st.session_state.last_audio_id = upload_id

            st.success(
                "📜 Uploaded file saved to History!"
            )

# =========================================================
# GENERATE STUDY MATERIAL
# =========================================================

st.divider()

st.subheader("🚀 Generate Study Material")

st.write(
    f"**Subject:** {subject}  |  "
    f"**Difficulty:** {difficulty}  |  "
    f"**Flashcards:** {number_of_cards}"
)

if st.button(
    "🚀 Generate Study Material",
    use_container_width=True,
    key="generate_study_material"
):

    if not audio_recording and not uploaded_audio:

        st.warning(
            "⚠️ Please record or upload a lecture first."
        )

    else:

        with st.spinner(
            "🤖 Gemini is analyzing your lecture..."
        ):

            try:

                # -----------------------------------------
                # GET AUDIO
                # -----------------------------------------

                if audio_recording:

                    audio_bytes = audio_recording.getvalue()
                    mime_type = audio_recording.type

                else:

                    audio_bytes = uploaded_audio.getvalue()
                    mime_type = uploaded_audio.type

                # -----------------------------------------
                # PROMPT
                # -----------------------------------------

                prompt = f"""
You are an expert academic study assistant.

The student is studying:

Subject: {subject}

Difficulty level: {difficulty}

Create study material from the provided lecture audio.

Return ONLY valid JSON.

Use exactly this structure:

{{
    "transcript": "Complete important transcript of the lecture",
    "summary": "Clear summary of the lecture",
    "key_concepts": [
        "concept 1",
        "concept 2",
        "concept 3"
    ],
    "flashcards": [
        {{
            "question": "Question",
            "answer": "Answer",
            "topic": "Topic",
            "difficulty": "Easy"
        }}
    ],
    "quiz": [
        {{
            "question": "Question",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}

Requirements:

1. Create approximately {number_of_cards} flashcards.
2. Make questions useful for exam preparation.
3. Keep answers accurate and concise.
4. Generate different difficulty levels.
5. Generate 5 quiz questions.
6. Do not invent information that is not supported by the lecture.
7. The transcript should contain the important spoken content.
"""

                # -----------------------------------------
                # GEMINI REQUEST
                # -----------------------------------------

                response = client.models.generate_content(

                    model="gemini-3-flash-preview",

                    contents=[
                        prompt,

                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": audio_bytes
                            }
                        }
                    ]
                )

                # -----------------------------------------
                # CLEAN RESPONSE
                # -----------------------------------------

                result_text = response.text.strip()

                if result_text.startswith("```"):
                    result_text = result_text.replace(
                        "```json", ""
                    ).replace(
                        "```", ""
                    ).strip()

                data = json.loads(result_text)
                

                # -----------------------------------------
                # SAVE RESULTS
                # -----------------------------------------

                st.session_state.study_material = data

                st.session_state.flashcards = data.get(
                    "flashcards",
                    []
                )

                st.session_state.quiz = data.get(
                    "quiz",
                    []
                )

                st.success(
                    "🎉 Study material generated successfully!"
                )

            except json.JSONDecodeError:

                st.error(
                    "Gemini returned an unexpected format."
                )

                st.code(response.text)

            except Exception as e:

                st.error(
                    "Something went wrong while processing "
                    "your lecture."
                )

                st.code(str(e))

# =========================================================
# DISPLAY RESULTS
# =========================================================

if st.session_state.study_material:

    data = st.session_state.study_material

    st.divider()

    # =====================================================
    # TABS
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📝 Summary",
            "🧠 Key Concepts",
            "📚 Flashcards",
            "🎯 Quiz"
        ]
    )

    # =====================================================
    # SUMMARY
    # =====================================================

    with tab1:

        st.subheader("📝 Lecture Transcript")

        with st.expander("View Transcript", expanded=True):

            st.write(
                data.get(
                    "transcript",
                    "No transcript available."
                )
            )

        st.subheader("📖 Summary")

        st.write(
            data.get(
                "summary",
                "No summary available."
            )
        )

    # =====================================================
    # KEY CONCEPTS
    # =====================================================

    with tab2:

        st.subheader("🧠 Key Concepts")

        concepts = data.get(
            "key_concepts",
            []
        )

        if concepts:

            for concept in concepts:

                st.info(
                    f"💡 {concept}"
                )

        else:

            st.info(
                "No key concepts generated."
            )

    # =====================================================
    # FLASHCARDS
    # =====================================================

    with tab3:

        st.subheader("📚 Your Flashcards")

        flashcards = data.get(
            "flashcards",
            []
        )

        if flashcards:

            flashcard_df = pd.DataFrame(
                flashcards
            )

            st.subheader(
                "📊 Flashcard Analytics"
            )

            if "difficulty" in flashcard_df.columns:

                difficulty_counts = (
                    flashcard_df[
                        "difficulty"
                    ].value_counts()
                )

                st.bar_chart(
                    difficulty_counts
                )

            st.subheader(
                "✏️ Edit Your Flashcards"
            )

            st.caption(
                "Edit your flashcards before downloading them."
            )

            edited_df = st.data_editor(
                flashcard_df,
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "⬇️ Download Flashcards CSV",
                edited_df.to_csv(
                    index=False
                ),
                "flashcards.csv",
                "text/csv"
            )

        else:

            st.info(
                "No flashcards available."
            )

    # =====================================================
    # QUIZ
    # =====================================================

    with tab4:

        st.subheader("🎯 Practice Quiz")

        quiz_questions = data.get(
            "quiz",
            []
        )

        if quiz_questions:

            with st.form(
                "quiz_form"
            ):

                user_answers = {}

                for index, question in enumerate(
                    quiz_questions
                ):

                    st.write(
                        f"### Question {index + 1}"
                    )

                    st.write(
                        question.get(
                            "question",
                            "Question unavailable"
                        )
                    )

                    options = question.get(
                        "options",
                        []
                    )

                    user_answers[index] = st.radio(
                        "Choose your answer:",
                        options,
                        key=f"quiz_answer_{index}"
                    )

                    st.divider()

                submit_quiz = st.form_submit_button(
                    "🏆 Submit Quiz",
                    use_container_width=True
                )

            if submit_quiz:

                score = 0

                for index, question in enumerate(
                    quiz_questions
                ):

                    correct_answer = question.get(
                        "answer",
                        ""
                    )

                    if (
                        user_answers[index]
                        == correct_answer
                    ):

                        score += 1

                total = len(
                    quiz_questions
                )

                percentage = int(
                    (score / total) * 100
                )

                st.session_state.score = percentage
                st.session_state.quiz_completed = True
                st.rerun()

                st.success(
                    f"🎉 Quiz completed! "
                    f"You scored {score}/{total}"
                )

                st.metric(
                    "🏆 Your Score",
                    f"{percentage}%"
                )

                if percentage >= 80:

                    st.balloons()

                    st.success(
                        "🔥 Excellent! You have a strong "
                        "understanding of this topic."
                    )

                elif percentage >= 50:

                    st.warning(
                        "👍 Good attempt! Review the "
                        "flashcards and try again."
                    )

                else:

                    st.error(
                        "📖 Keep practicing! Review the "
                        "summary and flashcards."
                    )

        else:

            st.info(
                "No quiz questions available."
            )

else:

    st.info(
        "🎙️ Record or upload a lecture and click "
        "'Generate Study Material' to begin."
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🎙️ Voice Notes to Flashcards | "
    "Powered by Gemini AI"
)
