
import json
import os
import random

SCORE_FILE = "leaderboard.json"

# Quiz questions
questions = [
    {
        "question": "What is the output of print(2 ** 3) in Python?",
        "options": ["A. 6", "B. 8", "C. 9", "D. 5"],
        "answer": "B"
    },
    {
        "question": "Which keyword is used to define a function in Python?",
        "options": ["A. function", "B. fun", "C. def", "D. define"],
        "answer": "C"
    },
    {
        "question": "Which data type stores True or False?",
        "options": ["A. int", "B. str", "C. list", "D. bool"],
        "answer": "D"
    },
    {
        "question": "Which symbol is used for comments in Python?",
        "options": ["A. //", "B. #", "C. <!--", "D. **"],
        "answer": "B"
    },
    {
        "question": "Which function is used to display output in Python?",
        "options": ["A. input()", "B. show()", "C. print()", "D. display()"],
        "answer": "C"
    },
    {
        "question": "Which collection stores key-value pairs?",
        "options": ["A. List", "B. Tuple", "C. Set", "D. Dictionary"],
        "answer": "D"
    },
    {
        "question": "What is the result of 10 // 3 in Python?",
        "options": ["A. 3", "B. 3.33", "C. 1", "D. 4"],
        "answer": "A"
    },
    {
        "question": "Which method adds an item to the end of a list?",
        "options": ["A. add()", "B. append()", "C. insert_end()", "D. push()"],
        "answer": "B"
    },
    {
        "question": "Which loop repeats while a condition is True?",
        "options": ["A. if", "B. def", "C. while", "D. class"],
        "answer": "C"
    },
    {
        "question": "Which keyword is used to create a class in Python?",
        "options": ["A. object", "B. class", "C. create", "D. struct"],
        "answer": "B"
    }
]


def load_leaderboard():
    """Load saved scores from the JSON file."""
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_leaderboard(scores):
    """Save scores to the JSON file."""
    with open(SCORE_FILE, "w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)


def play_quiz():
    """Run the quiz and calculate the score."""
    name = input("\nEnter your name: ").strip()

    if not name:
        name = "Anonymous"

    score = 0
    quiz_questions = questions.copy()
    random.shuffle(quiz_questions)

    print("\n========== QUIZ START ==========")
    print("Choose A, B, C, or D.")
    print("Each correct answer earns 1 point.\n")

    for number, item in enumerate(quiz_questions, start=1):
        print(f"Q{number}. {item['question']}")

        for option in item["options"]:
            print(option)

        while True:
            choice = input("Your answer: ").strip().upper()
            if choice in ("A", "B", "C", "D"):
                break
            print("Invalid choice. Enter A, B, C, or D.")

        if choice == item["answer"]:
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! Correct answer: {item['answer']}\n")

    total = len(quiz_questions)
    percentage = (score / total) * 100

    print("========== QUIZ RESULT ==========")
    print(f"Player: {name}")
    print(f"Score: {score}/{total}")
    print(f"Percentage: {percentage:.2f}%")

    scores = load_leaderboard()
    scores.append({
        "name": name,
        "score": score,
        "total": total
    })

    # Highest score first; earlier entries win ties.
    scores.sort(key=lambda player: player["score"], reverse=True)
    save_leaderboard(scores)

    print("\nYour score has been saved!")


def show_leaderboard():
    """Display the top players."""
    scores = load_leaderboard()

    print("\n========== LEADERBOARD ==========")

    if not scores:
        print("No scores available yet. Play the quiz first!")
        return

    print(f"{'Rank':<8}{'Player':<20}{'Score':<12}")
    print("-" * 40)

    for rank, player in enumerate(scores[:10], start=1):
        print(
            f"{rank:<8}"
            f"{player.get('name', 'Anonymous')[:19]:<20}"
            f"{player.get('score', 0)}/{player.get('total', 10):<12}"
        )


def main():
    """Main menu."""
    while True:
        print("\n================================")
        print("       PYTHON QUIZ APP")
        print("================================")
        print("1. Play Quiz")
        print("2. View Leaderboard")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            play_quiz()
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            print("Thank you for playing. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
