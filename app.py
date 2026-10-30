import json
import random
import time
from pathlib import Path

import streamlit as st

# Keep leaderboard.json in the same folder as this app.py file.
SCORE_FILE = Path(__file__).with_name("leaderboard.json")

# Questions from the original command-line quiz.
QUESTIONS = [
    {
        "question": "What is the output of print(2 ** 3) in Python?",
        "options": ["A. 6", "B. 8", "C. 9", "D. 5"],
        "answer": "B",
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["A. function", "B. fun", "C. def", "D. define"],
        "answer": "C",
    },
    {
        "question": "Which data type stores True or False?",
        "options": ["A. int", "B. str", "C. list", "D. bool"],
        "answer": "D",
    },
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["A. //", "B. #", "C. <!--", "D. **"],
        "answer": "B",
    },
    {
        "question": "Which function is used to display output in Python?",
        "options": ["A. input()", "B. show()", "C. print()", "D. display()"],
        "answer": "C",
    },
    {
        "question": "Which collection stores key-value pairs?",
        "options": ["A. List", "B. Tuple", "C. Set", "D. Dictionary"],
        "answer": "D",
    },
    {
        "question": "What is the result of 10 // 3 in Python?",
        "options": ["A. 3", "B. 3.33", "C. 1", "D. 4"],
        "answer": "A",
    },
    {
        "question": "Which method adds an item to the end of a list?",
        "options": ["A. add()", "B. append()", "C. insert_end()", "D. push()"],
        "answer": "B",
    },
    {
        "question": "Which loop repeats while a condition is True?",
        "options": ["A. if", "B. def", "C. while", "D. class"],
        "answer": "C",
    },
    {
        "question": "Which keyword is used to create a class in Python?",
        "options": ["A. object", "B. class", "C. create", "D. struct"],
        "answer": "B",
    },
]


def load_leaderboard():
    """Load saved scores, returning an empty list if the file is missing/invalid."""
    if not SCORE_FILE.exists():
        return []
    try:
        with SCORE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_leaderboard(scores):
    """Persist scores to the JSON file."""
    with SCORE_FILE.open("w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)


def save_result(name, score, total):
    scores = load_leaderboard()
    scores.append({"name": name, "score": score, "total": total})
    # Highest score first; preserve earlier entries when scores are tied.
    scores.sort(key=lambda player: player.get("score", 0), reverse=True)
    save_leaderboard(scores)


def start_new_quiz():
    quiz_questions = QUESTIONS.copy()
    random.shuffle(quiz_questions)
    st.session_state.quiz_questions = quiz_questions
    st.session_state.current_question = 0
    st.session_state.answers = {}
    st.session_state.quiz_finished = False
    st.session_state.result_saved = False
    st.session_state.quiz_started = False
    st.session_state.quiz_deadline = None
    st.session_state.time_expired = False
    st.session_state.show_leaderboard_hint = False


def begin_quiz():
    """Start the quiz and begin its three-minute countdown."""
    st.session_state.quiz_started = True
    st.session_state.quiz_deadline = time.time() + 180
    st.session_state.time_expired = False


def return_to_quiz_home():
    """Reset quiz state and navigate home before the next script run."""
    start_new_quiz()
    st.session_state.page_navigation = "Play Quiz"


@st.fragment(run_every="1s")
def show_quiz_timer():
    """Refresh the visible countdown once per second without an extra package."""
    remaining = max(0, int(st.session_state.quiz_deadline - time.time()))
    minutes, seconds = divmod(remaining, 60)
    timer_color = "#c62828" if remaining <= 30 else "#303f9f"
    timer_html = (
        '<div class="timer-card"><span class="timer-label">⏱️ Time remaining</span>'
        f'<span class="timer-value" style="color:{timer_color}">{minutes:02d}:{seconds:02d}</span></div>'
    )
    st.markdown(timer_html, unsafe_allow_html=True)
    if remaining <= 0 and not st.session_state.quiz_finished:
        st.session_state.quiz_finished = True
        st.session_state.time_expired = True
        st.rerun()


st.set_page_config(page_title="Python Quiz Arena", page_icon="🧠", layout="centered")

# Custom theme: the page is rendered by Streamlit, so no separate HTML file is needed.
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #eef2ff 0%, #f8faff 48%, #e8f7ff 100%); color: #18213b; }
[data-testid="stMainBlockContainer"] { max-width: 850px; padding-top: 2rem; padding-bottom: 3rem; }
[data-testid="stHeader"] { background: transparent; }
h1, h2, h3 { color: #26358b !important; letter-spacing: -0.025em; }
h1 { text-align: center; font-weight: 800 !important; }
[data-testid="stCaptionContainer"] { text-align: center; color: #5b6480; }
.hero-card { background: linear-gradient(135deg, #303f9f, #536dfe); color: white; padding: 28px 26px; border-radius: 22px; box-shadow: 0 14px 35px rgba(48,63,159,.20); margin: 8px 0 22px; }
.hero-card h2 { color: white !important; margin: 0 0 8px 0; font-size: 1.8rem; }
.hero-card p { color: #eef1ff; margin: 0; font-size: 1rem; line-height: 1.6; }
.feature-card { background: rgba(255,255,255,.88); border: 1px solid #e0e7ff; border-radius: 16px; padding: 17px 16px; min-height: 85px; box-shadow: 0 5px 18px rgba(31,48,110,.05); }
.feature-card strong { color: #303f9f; font-size: 1.02rem; }
.feature-card span { color: #626d89; font-size: .9rem; }
.stButton > button, .stFormSubmitButton > button { background: linear-gradient(135deg, #3949ab, #536dfe); color: #fff; border: 0; border-radius: 11px; padding: .7rem 1rem; font-weight: 700; box-shadow: 0 5px 12px rgba(57,73,171,.15); transition: transform .15s ease, filter .15s ease; }
.stButton > button:hover, .stFormSubmitButton > button:hover { color: white; filter: brightness(.94); border: 0; transform: translateY(-1px); }
.stTextInput input { border-radius: 10px; border-color: #d7def6; background: #fff; }
.stRadio [role="radiogroup"] { gap: 8px; }
.stRadio [role="radiogroup"] label { background: #fff; border: 1px solid #e0e6f8; border-radius: 10px; padding: 10px 12px; transition: border-color .15s ease; }
.stRadio [role="radiogroup"] label:hover { border-color: #7986cb; }
.stProgress > div > div > div { background: linear-gradient(90deg, #3949ab, #7986ff); }
[data-testid="stSidebar"] { background: #eef1ff; }
[data-testid="stDataFrame"] { border: 1px solid #e0e6f8; border-radius: 12px; overflow: hidden; }
.timer-card { display:flex; justify-content:space-between; align-items:center; gap:12px; background:#fff; border:1px solid #dfe5fb; border-radius:14px; padding:13px 16px; margin:8px 0 15px; box-shadow:0 5px 16px rgba(31,48,110,.05); }
.timer-label { color:#66708c; font-size:.9rem; font-weight:600; }
.timer-value { color:#303f9f; font-size:1.35rem; font-weight:800; font-variant-numeric:tabular-nums; }
@media (max-width: 600px) { [data-testid="stMainBlockContainer"] { padding: 1rem; } .hero-card { padding: 22px 18px; } }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Python Quiz Arena")
st.caption("Think fast. Test your Python skills. Climb the leaderboard.")
st.markdown("""
<div class="hero-card">
  <h2>Ready to challenge yourself?</h2>
  <p>Take a quick Python knowledge challenge, earn points for every correct answer,
  and see how you rank against other players. Click Start Quiz when you are ready; the three-minute timer starts then.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a page", ["Play Quiz", "Leaderboard"], key="page_navigation")
    st.divider()
    st.write("**Quiz rules**")
    st.write("• 10 multiple-choice questions")
    st.write("• 1 point for each correct answer")
    st.write("• Questions are shuffled for each attempt")

if "quiz_questions" not in st.session_state:
    start_new_quiz()

if page == "Play Quiz":
    if not st.session_state.quiz_started and not st.session_state.quiz_finished:
        # Landing page: the timer does not begin until the user clicks Start Quiz.
        st.subheader("Welcome to your Python challenge!")
        card1, card2, card3 = st.columns(3)
        with card1:
            st.markdown('<div class="feature-card">📝 <strong>10 Questions</strong><br><span>Multiple choice</span></div>', unsafe_allow_html=True)
        with card2:
            st.markdown('<div class="feature-card">⚡ <strong>3 Minutes</strong><br><span>Starts when you begin</span></div>', unsafe_allow_html=True)
        with card3:
            st.markdown('<div class="feature-card">🏆 <strong>10 Points</strong><br><span>One per answer</span></div>', unsafe_allow_html=True)
        st.write("Enter your name, then press **Start Quiz** when you're ready. Your timer will start only after you press the button.")
        player_name = st.text_input(
            "Enter your name",
            value=st.session_state.get("player_name", ""),
            placeholder="Your name",
            key="landing_player_name",
        )
        st.session_state.player_name = player_name.strip() or "Anonymous"
        if st.button("🚀 Start Quiz", type="primary", use_container_width=True):
            begin_quiz()
            st.rerun()

    elif not st.session_state.quiz_finished:
        st.subheader("🚀 Your challenge is in progress")
        show_quiz_timer()
        quiz_questions = st.session_state.quiz_questions
        index = st.session_state.current_question
        total = len(quiz_questions)

        st.progress(index / total)
        st.write(f"Question **{index + 1}** of **{total}**")

        item = quiz_questions[index]
        st.markdown(f"### {item['question']}")

        # Use a separate form for each question so an answer is submitted once.
        with st.form(key=f"question_form_{index}"):
            choice = st.radio(
                "Choose one answer:",
                item["options"],
                index=None,
                key=f"answer_widget_{index}",
            )
            submitted = st.form_submit_button(
                "Submit answer" if index < total - 1 else "Submit final answer",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            if choice is None:
                st.warning("Please select an answer before continuing.")
            else:
                selected_letter = choice[0]
                st.session_state.answers[index] = selected_letter
                if index + 1 < total:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.session_state.quiz_finished = True
                    st.rerun()

    else:
        quiz_questions = st.session_state.quiz_questions
        answers = st.session_state.answers
        total = len(quiz_questions)
        score = sum(
            1
            for index, item in enumerate(quiz_questions)
            if answers.get(index) == item["answer"]
        )
        percentage = score / total * 100

        st.subheader("🏁 Quiz Results")
        if st.session_state.get("time_expired", False):
            st.warning("Time is up! Your quiz has been submitted with the answers you completed.")
        st.success(f"You scored **{score}/{total}** ({percentage:.0f}%).")

        # Visual breakdown of the final score.
        incorrect = sum(
            1
            for index, item in enumerate(quiz_questions)
            if index in answers and answers[index] != item["answer"]
        )
        unanswered = total - len(answers)
        st.subheader("📊 Score Visualization")
        st.caption("A breakdown of correct, incorrect, and unanswered questions.")
        st.bar_chart(
            {
                "Answer type": ["Correct", "Incorrect", "Unanswered"],
                "Count": [score, incorrect, unanswered],
            },
            x="Answer type",
            y="Count",
        )
        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("Correct", score)
        metric2.metric("Incorrect", incorrect)
        metric3.metric("Unanswered", unanswered)

        if percentage == 100:
            st.balloons()
            st.write("Perfect score! Excellent work.")
        elif percentage >= 70:
            st.write("Great job! Keep practising.")
        elif percentage >= 40:
            st.write("Good effort—review the answers and try again.")
        else:
            st.write("Keep learning. You can improve with another attempt!")

        if not st.session_state.result_saved:
            save_result(st.session_state.get("player_name", "Anonymous"), score, total)
            st.session_state.result_saved = True

        with st.expander("Review your answers"):
            for index, item in enumerate(quiz_questions, start=1):
                selected = answers.get(index - 1)
                correct = item["answer"]
                is_correct = selected == correct
                st.markdown(f"**Q{index}. {item['question']}**")
                st.write(f"Your answer: {selected or 'Not answered'}")
                st.write(f"Correct answer: {correct}")
                if is_correct:
                    st.success("Correct")
                else:
                    st.error("Incorrect")
                st.divider()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Start New Quiz", type="primary", use_container_width=True):
                start_new_quiz()
                st.rerun()
        with col2:
            if st.button("View leaderboard", use_container_width=True):
                st.session_state.show_leaderboard_hint = True
                st.rerun()

        if st.session_state.get("show_leaderboard_hint"):
            st.info("Choose **Leaderboard** in the sidebar to view the rankings.")

elif page == "Leaderboard":
    st.subheader("🏆 Hall of Fame")
    st.markdown("See the top scores and take another attempt to move up the rankings.")
    scores = load_leaderboard()
    if not scores:
        st.info("No scores available yet. Play the quiz first!")
    else:
        top_scores = scores[:10]
        rows = [
            {
                "Rank": rank,
                "Player": player.get("name", "Anonymous"),
                "Score": f"{player.get('score', 0)}/{player.get('total', 10)}",
            }
            for rank, player in enumerate(top_scores, start=1)
        ]
        st.dataframe(rows, hide_index=True, use_container_width=True)

    # Use a callback so the radio widget's session-state key is changed
    # before Streamlit reconstructs the page, avoiding a widget-state error.
    st.button(
        "🏠 Return to Quiz Home",
        type="primary",
        on_click=return_to_quiz_home,
    )
