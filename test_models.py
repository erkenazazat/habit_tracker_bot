import unittest
from models import HabitManager

class TestHabitManager(unittest.TestCase):
    def setUp(self):
        self.manager = HabitManager()
        self.manager.data = {}
        self.user_id = 12345

    def test_add_habit(self):
        self.manager.add_habit(
            self.user_id,
            "Workout",
            "Running",
            "08:00",
            [0, 1, 2]
        )
        habits = self.manager.get_user_habits(
            self.user_id
        )
        self.assertEqual(
            len(habits),
            1
        )
        self.assertEqual(
            habits[0]["name"],
            "Workout"
        )

if __name__ == "__main__":
    unittest.main()