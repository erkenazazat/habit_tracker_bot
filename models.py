import json
import os
from datetime import datetime, timedelta

def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[{datetime.now()}] Method called: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

class HabitManager:
    def __init__(self, file_path="habits.json", sug_path="suggestions.json"):
        self.file_path = file_path
        self.sug_path = sug_path
        self.data=self._load_data()

    def _load_data(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {"users":{}, "languages":{}}
        except (json.JSONDecodeError, IOError):
            return {"users":{}, "languages":{}}

    def _save_data(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Saving error:{e}")

    def load_suggestions(self, lang):
        try:
            if os.path.exists(self.sug_path):
                with open(self.sug_path, "r", encoding="utf-8") as f:
                    sug_data = json.load(f)
                    return sug_data.get(lang, [])
            return []
        except Exception:
            return []

    def get_profile_stats(self, user_id):
        user_id = str(user_id)
        habits = self.get_user_habits(user_id)
        total_habits = len(habits)
        max_streak = 0
        for h in habits:
            if h["streak"] > max_streak:
                max_streak = h["streak"]
        return total_habits, max_streak

    def set_language(self, user_id, lang):
        if "languages" not in self.data:
            self.data["languages"] = {}
        self.data["languages"][str(user_id)] = lang
        self._save_data()

    def get_language(self, user_id):
        return self.data.get("languages", {}).get(str(user_id), "ru")

    @log_action
    def add_habit(self, user_id, name, description, time_str, days_list):
        user_id = str(user_id)
        if "users" not in self.data:
            self.data["users"] = {}
        if user_id not in self.data["users"]:
            self.data["users"][user_id] = []

        habit_dict = {
            "name": name,
            "description": description,
            "time_str": time_str,
            "days_list": days_list,
            "streak": 0,
            "last_checked": ""
        }
        self.data["users"][user_id].append(habit_dict)
        self._save_data()

    def check_and_reset_streaks(self, user_id):
        user_id = str(user_id)
        if "users" not in self.data or user_id not in self.data["users"]:
            return
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        updated = False
        for h in self.data["users"][user_id]:
            if h["streak"] > 0 and h["last_checked"]:
                last_date = datetime.strptime(h["last_checked"], "%Y-%m-%d").date()
                if last_date < yesterday:
                    h["streak"] = 0
                    h["last_checked"] = ""
                    updated = True
        if updated:
            self._save_data()

    def get_user_habits(self, user_id):
        user_id = str(user_id)
        self.check_and_reset_streaks(user_id)
        return self.data.get("users", {}).get(user_id, [])

    @log_action
    def check_habit(self, user_id, habit_index):
        user_id = str(user_id)
        today_str = datetime.now().strftime("%Y-%m-%d")
        if user_id in self.data["users"] and 0 <= habit_index < len(self.data["users"][user_id]):
            h = self.data["users"][user_id][habit_index]
            if h["last_checked"] == today_str:
                return "already_checked"
            h["streak"] += 1
            h["last_checked"] = today_str
            self._save_data()
            return "success"
        return "error"

    @log_action
    def delete_habit(self, user_id, habit_index):
        user_id = str(user_id)
        if user_id in self.data["users"] and 0 <= habit_index < len(self.data["users"][user_id]):
            self.data["users"][user_id].pop(habit_index)
            self._save_data()
            return True
        return False