import tkinter as tk
from tkinter import messagebox
import json
from user import User
from administrator import Administrator
from store import Store
from category import Category
from item import Item

def load_categories():
    try:
        with open("categories.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

class shoppingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Shopping System")
        self.root.configure(bg="#1C2526")  
        self.root.geometry("800x600")  
        self.store = Store()

        if not hasattr(self.store, 'categories'):
            self.store.categories = {}
        if not hasattr(self.store, 'cart'):
            self.store.cart = {'items': [], 'total_price': 0}
        if not hasattr(self.store, 'users'):
            self.store.users = {}

        self.current_user = None
        self.container = tk.Frame(self.root, bg="#1C2526")
        self.container.pack(fill="both", expand=True)
        self.history = []

        categories_data = load_categories()
        for cat_name, items_list in categories_data.items():
            self.store.categories[cat_name] = Category(
                cat_name, [Item(**item) for item in items_list]
            )

        self.show_login()

    def save_categories(self):
        data = {}
        for cat_name, cat_obj in self.store.categories.items():
            data[cat_name] = [item.to_dict() for item in cat_obj.items]
        with open("categories.json", "w") as f:
            json.dump(data, f, indent=4)

    def clear(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def push(self, fn):
        self.history.append(fn)

    def back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.history[-1]()

    def show_login(self):
        self.clear()
        self.history = [self.show_login]
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        
        tk.Label(f, text="🛒 Online Shopping", font=("Helvetica", 24, "bold"), fg="#FFD700", bg="#1C2526").pack(pady=20)
        
        form_frame = tk.Frame(f, bg="#2E2E2E", padx=20, pady=20)
        form_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(form_frame, text="Login", font=("Helvetica", 18, "bold"), fg="white", bg="#2E2E2E").pack(pady=10)
        tk.Label(form_frame, text="Email", font=("Helvetica", 12), fg="white", bg="#2E2E2E").pack()
        email = tk.Entry(form_frame, width=30, font=("Helvetica", 12), bg="#3C3F41", fg="white", insertbackground="white")
        email.pack(pady=5)
        tk.Label(form_frame, text="Password", font=("Helvetica", 12), fg="white", bg="#2E2E2E").pack()
        password = tk.Entry(form_frame, width=30, font=("Helvetica", 12), bg="#3C3F41", fg="white", insertbackground="white", show="*")
        password.pack(pady=5)

        def login():
            e, p = email.get(), password.get()
            if e == self.store.adminEmail and p == self.store.adminPassword:
                self.current_user = Administrator()
                self.show_admin_page()
                return
            u = self.store.users.get(e)
            if u and u.password == p:
                self.current_user = u
                self.store.cart = {'items': [], 'total_price': 0}
                self.show_home()
            else:
                messagebox.showerror("ERROR", "Invalid data")

        login_btn = tk.Button(form_frame, text="Login", font=("Helvetica", 12, "bold"), bg="#FFD700", fg="black", command=login)
        login_btn.pack(pady=10)
        self.add_hover(login_btn, "#FFD700", "#FFEA00")  

        reg_btn = tk.Button(form_frame, text="Register", font=("Helvetica", 12), bg="#FF4500", fg="white", command=self.register)
        reg_btn.pack(pady=5)
        self.add_hover(reg_btn, "#FF4500", "#FF6347")  

    def add_hover(self, button, original_bg, hover_bg):
        button.bind("<Enter>", lambda e: button.config(bg=hover_bg))
        button.bind("<Leave>", lambda e: button.config(bg=original_bg))

    def register(self):
        self.clear()
        self.push(self.register)
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        
        form_frame = tk.Frame(f, bg="#2E2E2E", padx=20, pady=20)
        form_frame.pack(pady=10, padx=10, fill="x")
        
        tk.Label(form_frame, text="Register", font=("Helvetica", 18, "bold"), fg="white", bg="#2E2E2E").pack(pady=10)
        labels = ["Name", "Phone", "Email", "Gender", "Governorate", "Password", "Age", "National ID"]
        entries = {}
        for l in labels:
            tk.Label(form_frame, text=l, font=("Helvetica", 12), fg="white", bg="#2E2E2E").pack()
            e = tk.Entry(form_frame, width=30, font=("Helvetica", 12), bg="#3C3F41", fg="white", insertbackground="white", show="*" if l == "Password" else None)
            e.pack(pady=5)
            entries[l] = e

        def submit():
            try:
                u = User(
                    entries["Name"].get(),
                    entries["Phone"].get(),
                    entries["Email"].get(),
                    entries["Gender"].get(),
                    entries["Governorate"].get(),
                    entries["Password"].get(),
                    int(entries["Age"].get()),
                    entries["National ID"].get()
                )
            except:
                messagebox.showerror("ERROR", "Invalid data")
                return
            if not self.store.add_user(u):
                messagebox.showerror("ERROR", "Email exists")
            else:
                messagebox.showinfo("OK", "Registered successfully")
                self.show_login()

        reg_btn = tk.Button(form_frame, text="Register", font=("Helvetica", 12, "bold"), bg="#FFD700", fg="black", command=submit)
        reg_btn.pack(pady=10)
        self.add_hover(reg_btn, "#FFD700", "#FFEA00")

    def logout(self):
        self.current_user = None
        self.store.cart = {'items': [], 'total_price': 0}
        self.show_login()

    def show_home(self):
        self.clear()
        self.push(self.show_home)
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        
        tk.Label(f, text="🛒 Welcome to Our Shop", font=("Helvetica", 20, "bold"), fg="#FFD700", bg="#1C2526").pack(pady=20)
        categories = load_categories()
        for cat in categories.keys():
            btn = tk.Button(f, text=cat, font=("Helvetica", 12), bg="#FF4500", fg="white", width=30, 
                      command=lambda c=cat: self.show_products(c))
            btn.pack(pady=5)
            self.add_hover(btn, "#FF4500", "#FF6347")

        cart_btn = tk.Button(f, text="View Cart 🛍", font=("Helvetica", 12), bg="#FFD700", fg="black", command=self.show_cart)
        cart_btn.pack(pady=10)
        self.add_hover(cart_btn, "#FFD700", "#FFEA00")

        logout_btn = tk.Button(f, text="Logout", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.logout)
        logout_btn.pack(pady=5)
        self.add_hover(logout_btn, "#FF4444", "#FF6666")

    def show_products(self, category_name):
        self.clear()
        self.push(lambda: self.show_products(category_name))
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        
        tk.Label(f, text=f"{category_name} Products", font=("Helvetica", 16, "bold"), fg="white", bg="#1C2526").pack(pady=10)
        search_frame = tk.Frame(f, bg="#1C2526")
        search_frame.pack(pady=5)
        tk.Label(search_frame, text="Search:", font=("Helvetica", 12), fg="white", bg="#1C2526").pack(side="left")
        self.search_entry = tk.Entry(search_frame, width=20, font=("Helvetica", 12), bg="#3C3F41", fg="white", insertbackground="white")
        self.search_entry.pack(side="left")
        search_btn = tk.Button(search_frame, text="Search", font=("Helvetica", 12), bg="#FFD700", fg="black", command=lambda: self.do_search(category_name))
        search_btn.pack(side="left", padx=5)
        self.add_hover(search_btn, "#FFD700", "#FFEA00")
        
        sort_frame = tk.Frame(f, bg="#1C2526")
        sort_frame.pack(pady=5)
        asc_btn = tk.Button(sort_frame, text="Sort Asc (Price)", font=("Helvetica", 12), bg="#FF4500", fg="white", command=lambda: self.do_sort(category_name, True))
        asc_btn.pack(side="left", padx=5)
        self.add_hover(asc_btn, "#FF4500", "#FF6347")
        desc_btn = tk.Button(sort_frame, text="Sort Desc (Price)", font=("Helvetica", 12), bg="#FF4500", fg="white", command=lambda: self.do_sort(category_name, False))
        desc_btn.pack(side="left", padx=5)
        self.add_hover(desc_btn, "#FF4500", "#FF6347")
        
        self.list_frame = tk.Frame(f, bg="#1C2526")
        self.list_frame.pack(pady=10, fill="both", expand=True)
        categories_data = load_categories()
        items_data = categories_data.get(category_name, [])
        self.store.categories[category_name] = Category(category_name, [Item(**i) for i in items_data])
        self.display_items(self.list_frame, self.store.categories[category_name].items)
        back_btn = tk.Button(f, text="Back", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.back)
        back_btn.pack(pady=10)
        self.add_hover(back_btn, "#FF4444", "#FF6666")

    def do_search(self, category_name):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Search", "Enter a search term first")
            return
        category_obj = self.store.categories.get(category_name)
        if not category_obj:
            messagebox.showerror("Error", "Category not found.")
            return
        category_obj.bubble_sort(ascending=True, key='name')  
        found_item = category_obj.binary_search(query, key='name')
        self.display_items(self.list_frame, [found_item] if found_item else [])

    def do_sort(self, category_name, ascending):
        category_obj = self.store.categories.get(category_name)
        if not category_obj:
            messagebox.showerror("Error", "Category not found.")
            return
        category_obj.bubble_sort(ascending=ascending, key='price')
        self.display_items(self.list_frame, category_obj.items)

    def display_items(self, frame, items):
        for widget in frame.winfo_children():
            widget.destroy()
        if not items:
            tk.Label(frame, text="No items to display.", font=("Helvetica", 12), fg="white", bg="#1C2526").pack(pady=10)
            return
        for item in items:
            text = f"{item.name} - {item.price} EGP - {item.brand} - {item.model_year}"
            tk.Label(frame, text=text, font=("Helvetica", 12), fg="white", bg="#1C2526").pack(anchor="w", pady=2)
            add_btn = tk.Button(frame, text="Add to Cart 🛍", font=("Helvetica", 12), bg="#FFD700", fg="black", command=lambda i=item: self.add_to_cart(i))
            add_btn.pack(pady=2)
            self.add_hover(add_btn, "#FFD700", "#FFEA00")

    def add_to_cart(self, item):
        self.store.cart['items'].append(item)
        self.store.cart['total_price'] += item.price
        messagebox.showinfo("Cart", f"{item.name} added to cart!")

    def show_cart(self):
        self.clear()
        self.push(self.show_cart)
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        tk.Label(f, text="Your Cart 🛍", font=("Helvetica", 16, "bold"), fg="white", bg="#1C2526").pack(pady=10)
        if not self.store.cart['items']:
            tk.Label(f, text="Cart is empty", font=("Helvetica", 12), fg="white", bg="#1C2526").pack()
        else:
            for item in self.store.cart['items']:
                text = f"{item.name} - {item.price} EGP"
                tk.Label(f, text=text, font=("Helvetica", 12), fg="white", bg="#1C2526").pack(anchor="w", pady=2)
            total = sum(i.price for i in self.store.cart['items']) 
            delivery_fees = self.calculate_delivery_fees()
            total_with_fees = total + delivery_fees
            tk.Label(f, text=f"Items Total: {total} EGP", font=("Helvetica", 12), fg="white", bg="#1C2526").pack(pady=5)
            tk.Label(f, text=f"Delivery Fees: {delivery_fees} EGP", font=("Helvetica", 12), fg="white", bg="#1C2526").pack(pady=5)
            tk.Label(f, text=f"Final Total: {total_with_fees} EGP", font=("Helvetica", 14, "bold"), fg="#FFD700", bg="#1C2526").pack(pady=10)
            checkout_btn = tk.Button(f, text="Checkout", font=("Helvetica", 12, "bold"), bg="#FF4500", fg="white", command=self.checkout)
            checkout_btn.pack(pady=5)
            self.add_hover(checkout_btn, "#FF4500", "#FF6347")
        back_btn = tk.Button(f, text="Back", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.back)
        back_btn.pack(pady=10)
        self.add_hover(back_btn, "#FF4444", "#FF6666")

    def checkout(self):
        delivery_fees = self.calculate_delivery_fees()
        final_total = sum(i.price for i in self.store.cart['items']) + delivery_fees
        invoice_text = "----- Invoice -----\n"
        for item in self.store.cart['items']:
            invoice_text += f"{item.name} - {item.price} EGP\n"
        invoice_text += f"\nItems Total: {sum(i.price for i in self.store.cart['items'])} EGP"
        invoice_text += f"\nDelivery Fees: {delivery_fees} EGP"
        invoice_text += f"\nFinal Total: {final_total} EGP\n"
        invoice_text += "-------------------"
        messagebox.showinfo("Checkout Invoice", invoice_text)
        self.store.cart = {'items': [], 'total_price': 0}
        self.show_home()

    def calculate_delivery_fees(self):
        fees = {
            "Cairo": 20,
            "Giza": 30,
            "Alexandria": 45,
            "Luxor": 60,
            "Aswan": 75,
            "Suez": 40
        }
        user_governorate = self.current_user.governorate.strip().title() if self.current_user else "Other"
        return fees.get(user_governorate, 50)

    def show_admin_page(self):
        self.clear()
        self.history = [self.show_admin_page]
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        tk.Label(f, text="Admin Panel ⚙", font=("Helvetica", 16, "bold"), fg="white", bg="#1C2526").pack(pady=10)
        add_btn = tk.Button(f, text="Add Item", font=("Helvetica", 12), bg="#FF4500", fg="white", command=self.add_item_page)
        add_btn.pack(pady=5)
        self.add_hover(add_btn, "#FF4500", "#FF6347")
        update_btn = tk.Button(f, text="Update Item", font=("Helvetica", 12), bg="#FF4500", fg="white", command=self.update_item_page)
        update_btn.pack(pady=5)
        self.add_hover(update_btn, "#FF4500", "#FF6347")
        delete_btn = tk.Button(f, text="Delete Item", font=("Helvetica", 12), bg="#FF4500", fg="white", command=self.delete_item_page)
        delete_btn.pack(pady=5)
        self.add_hover(delete_btn, "#FF4500", "#FF6347")
        discount_btn = tk.Button(f, text="Apply Discount", font=("Helvetica", 12), bg="#FF4500", fg="white", command=self.apply_discount_page)
        discount_btn.pack(pady=5)
        self.add_hover(discount_btn, "#FF4500", "#FF6347")
        users_btn = tk.Button(f, text="View All Users", font=("Helvetica", 12), bg="#FF4500", fg="white", command=self.view_all_users_page)
        users_btn.pack(pady=5)
        self.add_hover(users_btn, "#FF4500", "#FF6347")
        items_btn = tk.Button(f, text="View All Items", font=("Helvetica", 12), bg="#FF4500", fg="white", command=self.view_all_items_page)
        items_btn.pack(pady=5)
        self.add_hover(items_btn, "#FF4500", "#FF6347")
        logout_btn = tk.Button(f, text="Logout", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.logout)
        logout_btn.pack(pady=10)
        self.add_hover(logout_btn, "#FF4444", "#FF6666")

    def apply_discount_page(self):
        self.clear()
        self.push(self.apply_discount_page)
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        form_frame = tk.Frame(f, bg="#2E2E2E", padx=20, pady=20)
        form_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(form_frame, text="Apply Discount", font=("Helvetica", 16, "bold"), fg="white", bg="#2E2E2E").pack(pady=10)
        tk.Label(form_frame, text="Category", font=("Helvetica", 12), fg="white", bg="#2E2E2E").pack()
        category_entry = tk.Entry(form_frame, width=30, font=("Helvetica", 12), bg="#3C3F41", fg="white", insertbackground="white")
        category_entry.pack(pady=5)
        tk.Label(form_frame, text="Discount Percent", font=("Helvetica", 12), fg="white", bg="#2E2E2E").pack()
        percent_entry = tk.Entry(form_frame, width=30, font=("Helvetica", 12), bg="#3C3F41", fg="white", insertbackground="white")
        percent_entry.pack(pady=5)

        def submit_discount():
            category_name = category_entry.get()
            category_obj = self.store.categories.get(category_name)
            if not category_obj:
                messagebox.showerror("Error", "Category not found!")
                return
            try:
                percent = float(percent_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid percent.")
                return
            if self.current_user.apply_discount(category_obj, percent):
                self.save_categories()
                messagebox.showinfo("Success", f"Discount {percent}% applied to {category_name}!")
                self.back()
            else:
                messagebox.showerror("Error", "Failed to apply discount.")

        submit_btn = tk.Button(form_frame, text="Apply Discount", font=("Helvetica", 12, "bold"), bg="#FFD700", fg="black", command=submit_discount)
        submit_btn.pack(pady=10)
        self.add_hover(submit_btn, "#FFD700", "#FFEA00")
        back_btn = tk.Button(form_frame, text="Back", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.back)
        back_btn.pack(pady=5)
        self.add_hover(back_btn, "#FF4444", "#FF6666")

    def view_all_users_page(self):
        self.clear()
        self.push(self.view_all_users_page)
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        tk.Label(f, text="All Users", font=("Helvetica", 16, "bold"), fg="white", bg="#1C2526").pack(pady=10)
        users_list = self.current_user.view_all_users(self.store)
        if not users_list:
            tk.Label(f, text="No users found.", font=("Helvetica", 12), fg="white", bg="#1C2526").pack(pady=10)
        else:
            for user in users_list:
                text = f"Name: {user['name']}, Email: {user['email']}, Governorate: {user['governorate']}"
                tk.Label(f, text=text, font=("Helvetica", 12), fg="white", bg="#1C2526").pack(anchor="w", pady=2)
        back_btn = tk.Button(f, text="Back", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.back)
        back_btn.pack(pady=10)
        self.add_hover(back_btn, "#FF4444", "#FF6666")

    def view_all_items_page(self):
        self.clear()
        self.push(self.view_all_items_page)
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        tk.Label(f, text="All Items", font=("Helvetica", 16, "bold"), fg="white", bg="#1C2526").pack(pady=10)
        items_list = self.current_user.view_all_items(self.store)
        if not items_list:
            tk.Label(f, text="No items found.", font=("Helvetica", 12), fg="white", bg="#1C2526").pack(pady=10)
        else:
            for item in items_list:
                text = f"Name: {item['name']}, Price: {item['price']}, Brand: {item['brand']}, Model Year: {item['model_year']}"
                tk.Label(f, text=text, font=("Helvetica", 12), fg="white", bg="#1C2526").pack(anchor="w", pady=2)
        back_btn = tk.Button(f, text="Back", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.back)
        back_btn.pack(pady=10)
        self.add_hover(back_btn, "#FF4444", "#FF6666")

    def add_item_page(self):
        self.clear()
        self.push(self.add_item_page)
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        form_frame = tk.Frame(f, bg="#2E2E2E", padx=20, pady=20)
        form_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(form_frame, text="Add New Item", font=("Helvetica", 16, "bold"), fg="white", bg="#2E2E2E").pack(pady=10)
        labels = ["Category", "Name", "Price", "Brand", "Model Year"]
        entries = {}
        for l in labels:
            tk.Label(form_frame, text=l, font=("Helvetica", 12), fg="white", bg="#2E2E2E").pack()
            e = tk.Entry(form_frame, width=30, font=("Helvetica", 12), bg="#3C3F41", fg="white", insertbackground="white")
            e.pack(pady=5)
            entries[l] = e

        def submit_add():
            category_name = entries["Category"].get()
            category_obj = self.store.categories.get(category_name)
            if not category_obj:
                messagebox.showerror("Error", "Category not found!")
                return
            try:
                new_item = Item(
                    name=entries["Name"].get(),
                    price=float(entries["Price"].get()),
                    brand=entries["Brand"].get(),
                    model_year=int(entries["Model Year"].get())
                )
            except ValueError:
                messagebox.showerror("Error", "Invalid data type.")
                return
            if self.current_user.add_item(category_obj, new_item):
                self.save_categories()
                messagebox.showinfo("Success", "Item added successfully!")
                self.back()
            else:
                messagebox.showerror("Error", "Failed to add item.")

        add_btn = tk.Button(form_frame, text="Add Item", font=("Helvetica", 12, "bold"), bg="#FFD700", fg="black", command=submit_add)
        add_btn.pack(pady=10)
        self.add_hover(add_btn, "#FFD700", "#FFEA00")
        back_btn = tk.Button(form_frame, text="Back", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.back)
        back_btn.pack(pady=5)
        self.add_hover(back_btn, "#FF4444", "#FF6666")

    def update_item_page(self):
        self.clear()
        self.push(self.update_item_page)
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        form_frame = tk.Frame(f, bg="#2E2E2E", padx=20, pady=20)
        form_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(form_frame, text="Update Item", font=("Helvetica", 16, "bold"), fg="white", bg="#2E2E2E").pack(pady=10)
        labels = ["Category", "Old Name", "New Name", "New Price", "New Brand", "New Model Year"]
        entries = {}
        for l in labels:
            tk.Label(form_frame, text=l, font=("Helvetica", 12), fg="white", bg="#2E2E2E").pack()
            e = tk.Entry(form_frame, width=30, font=("Helvetica", 12), bg="#3C3F41", fg="white", insertbackground="white")
            e.pack(pady=5)
            entries[l] = e

        def submit_update():
            category_name = entries["Category"].get()
            category_obj = self.store.categories.get(category_name)
            if not category_obj:
                messagebox.showerror("Error", "Category not found!")
                return
            try:
                new_item = Item(
                    name=entries["New Name"].get(),
                    price=float(entries["New Price"].get()),
                    brand=entries["New Brand"].get(),
                    model_year=int(entries["New Model Year"].get())
                )
            except ValueError:
                messagebox.showerror("Error", "Invalid data type.")
                return
            old_name = entries["Old Name"].get()
            if self.current_user.update_item(category_obj, old_name, new_item):
                self.save_categories()
                messagebox.showinfo("Success", "Item updated successfully!")
                self.back()
            else:
                messagebox.showerror("Error", "Old item name not found.")

        update_btn = tk.Button(form_frame, text="Update Item", font=("Helvetica", 12, "bold"), bg="#FFD700", fg="black", command=submit_update)
        update_btn.pack(pady=10)
        self.add_hover(update_btn, "#FFD700", "#FFEA00")
        back_btn = tk.Button(form_frame, text="Back", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.back)
        back_btn.pack(pady=5)
        self.add_hover(back_btn, "#FF4444", "#FF6666")

    def delete_item_page(self):
        self.clear()
        self.push(self.delete_item_page)
        f = tk.Frame(self.container, padx=20, pady=20, bg="#1C2526")
        f.pack(expand=True)
        form_frame = tk.Frame(f, bg="#2E2E2E", padx=20, pady=20)
        form_frame.pack(pady=10, padx=10, fill="x")
        tk.Label(form_frame, text="Delete Item", font=("Helvetica", 16, "bold"), fg="white", bg="#2E2E2E").pack(pady=10)
        labels = ["Category", "Item Name"]
        entries = {}
        for l in labels:
            tk.Label(form_frame, text=l, font=("Helvetica", 12), fg="white", bg="#2E2E2E").pack()
            e = tk.Entry(form_frame, width=30, font=("Helvetica", 12), bg="#3C3F41", fg="white", insertbackground="white")
            e.pack(pady=5)
            entries[l] = e

        def submit_delete():
            category_name = entries["Category"].get()
            category_obj = self.store.categories.get(category_name)
            if not category_obj:
                messagebox.showerror("Error", "Category not found!")
                return
            item_name = entries["Item Name"].get()
            if self.current_user.delete_item(category_obj, item_name):
                self.save_categories()
                messagebox.showinfo("Success", "Item deleted successfully!")
                self.back()
            else:
                messagebox.showerror("Error", "Item name not found.")

        delete_btn = tk.Button(form_frame, text="Delete Item", font=("Helvetica", 12, "bold"), bg="#FFD700", fg="black", command=submit_delete)
        delete_btn.pack(pady=10)
        self.add_hover(delete_btn, "#FFD700", "#FFEA00")
        back_btn = tk.Button(form_frame, text="Back", font=("Helvetica", 12), bg="#FF4444", fg="white", command=self.back)
        back_btn.pack(pady=5)
        self.add_hover(back_btn, "#FF4444", "#FF6666")

if __name__ == "__main__":
    root = tk.Tk()
    app = shoppingApp(root)
    root.mainloop()