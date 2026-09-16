import json
import random
import os

class QuestionManager:
    def __init__(self, filename="questions.json"):
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(base_path, filename)
        self.questions = self.load_questions()

    def load_questions(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading questions file: {e}")
            return []

    def get_random_board_questions(self):
        # Selects 9 random questions from the 12 available
        selected = random.sample(self.questions, min(9, len(self.questions)))
        board = []
        for q_item in selected:
            board.append({
                "q": q_item["q"],
                "ans": q_item["ans"],
                "status": "available"
            })
        return board

    @staticmethod
    def validate_answer(user_input, valid_answers):
        if not user_input:
            return False
        clean_input = str(user_input).strip().lower()
        return any(clean_input == str(ans).strip().lower() for ans in valid_answers)