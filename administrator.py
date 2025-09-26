from user import User

class Administrator(User):
    def __init__(self, email="admin@gmail.com", password="admin123"):
        super().__init__(
            name="Admin",
            phone="000",
            email=email,
            gender="N/A",
            governorate="Cairo",
            password=password,
            age=22,
            nationalID="000"
        )

    def add_item(self, category, item):
        return category.add_item(item)

    def update_item(self, category, old_name, new_item):
        return category.update_item(old_name, new_item)

    def delete_item(self, category, item_name):
        return category.delete_item(item_name)

    def apply_discount(self, category, percent):
        for item in category.items:
            item.price -= item.price * (percent / 100)
        return True
    def view_all_users(self, store):
        return [user.to_dict() for user in store.users.values()]
    def view_all_items(self, store):
        all_items = []
        for category in store.categories.values():
            all_items.extend([item.to_dict() for item in category.items])
        return all_items
    