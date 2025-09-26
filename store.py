import json
from user import User

class Store:
    def __init__(self, filename="user.json"):
        self.users = {}
        self.filename = filename
        self.adminEmail = "admin@gmail.com"
        self.adminPassword = "admin123"
        self.load()

    def save(self):
        data = {
            "users": {email: u.to_dict() for email, u in self.users.items()}
        }
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            for email, u in data.get("users", {}).items():
                self.users[email] = User.from_dict(u)
        except FileNotFoundError:
            self.users = {}

    def add_user(self, user: User):
        if user.email in self.users:
            return False
        self.users[user.email] = user
        self.save()
        return True
