import json
import random

# List of fixed filenames and the corresponding number of questions to select
FILE_QUESTION_COUNT = {
    "Section 1 GENERAL HEALTH AND SAFETY AT WORK.json": 6,
    "Section 2 MANUAL HANDLING OPERATIONS.json": 4,
    "Section 3 REPORTING ACCIDENTS.json": 3,
    "Section 4 PERSONAL PROTECTIVE EQUIPMENT AT WORK.json": 4,
    "Section 5 HEALTH AND HYGIENE.json": 3,
    "Section 6 FIRE AND EMERGENCY.json": 9,
    "Section 7 WORK AT HEIGHT.json": 5,
    "Section 8 WORK EQUIPMENT.json": 4,
    "Section 9 SPECIAL SITE HAZARDS.json": 3,
    "Section 10 ELECTROTECHNICAL.json": 6,
    "Section 11 ENVIROMENTAL.json": 3
}

def load_questions(filename):
    """Load questions from a file."""
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: File '{filename}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Warning: File '{filename}' is not a valid JSON file.")
        return []

def select_questions(questions, count):
    """Randomly select a specified number of questions."""
    return random.sample(questions, min(len(questions), count))

def ask_question(question):
    """Ask a question and process the answer."""
    print(f"\nQuestion: {question['question']}")
    for option in question['options']:
        print(f"  {option['label']}: {option['text']}")

    user_answer = input("Your answer: ").strip().upper()
    correct_option = next(opt['label'] for opt in question['options'] if opt['is_correct'])
    correct_text = next(opt['text'] for opt in question['options'] if opt['is_correct'])

    if user_answer == correct_option:
        print("Correct!")
        return True
    else:
        print(f"Incorrect! The correct answer was {correct_option}: {correct_text}")
        return False

def main():
    """Main program loop."""
    print("Welcome to the ECS HSE Assessment!")

    section_scores = {}
    total_questions = 0
    total_correct = 0

    for filename, question_count in FILE_QUESTION_COUNT.items():
        questions = load_questions(filename)
        selected_questions = select_questions(questions, question_count)

        correct_answers = 0
        for question in selected_questions:
            if ask_question(question):
                correct_answers += 1

        section_scores[filename] = {
            "correct": correct_answers,
            "total": len(selected_questions)
        }

        total_questions += len(selected_questions)
        total_correct += correct_answers

    # Display section scores
    print("\n--- Assessment Results ---")
    for section, scores in section_scores.items():
        section_name = section.split('.')[0]  # Extract section name
        correct = scores["correct"]
        total = scores["total"]
        percentage = (correct / total) * 100 if total > 0 else 0
        print(f"{section_name}: {correct}/{total} ({percentage:.2f}%)")

    # Display overall score
    overall_percentage = (total_correct / total_questions) * 100 if total_questions > 0 else 0
    print(f"\nOverall Score: {total_correct}/{total_questions} ({overall_percentage:.2f}%)")
    
    # Wait for user input to exit
    input("\nPress Enter to exit the program...")

if __name__ == "__main__":
    main()
