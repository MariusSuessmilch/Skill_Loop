# models/progress.py
from typing import Dict

class UserProgress:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.general_level = 1
        self.topic_levels: Dict[str, int] = {
            'variables': 0,
            'operators': 0,
            'if_else': 0,
            'loops': 0,
            'lists': 0,
            'functions': 0,
            'strings': 0,
            'dictionaries': 0,
            'classes': 0,
        }

    def increment(self, topic: str, amount: int = 1):
        self.general_level += amount
        if topic in self.topic_levels:
            self.topic_levels[topic] += amount
        else:
            self.topic_levels[topic] = amount

# In-memory store for demo (replace with DB for production)
user_progress_store: Dict[str, UserProgress] = {}

def get_user_progress(user_id: str) -> UserProgress:
    if user_id not in user_progress_store:
        user_progress_store[user_id] = UserProgress(user_id)
    return user_progress_store[user_id]
