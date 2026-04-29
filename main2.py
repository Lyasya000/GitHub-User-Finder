import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os
from datetime import datetime


class GitHubUserFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # Favorites list
        self.favorites = []
        self.favorites_file = "favorites.json"
        self.load_favorites()

        # Current search results
        self.search_results = []

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        search_frame.columnconfigure(1, weight=1)

        ttk.Label(search_frame, text="Search GitHub User:").grid(row=0, column=0, padx=(0, 10))

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.search_user())

        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_user)
        self.search_button.grid(row=0, column=2)

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))

        # Search results tab
        self.search_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.search_tab, text="Search Results")

        # Favorites tab
        self.favorites_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.favorites_tab, text="Favorites")

        # Setup search results
        self.setup_search_tab()

        # Setup favorites tab
        self.setup_favorites_tab()

        # Status bar
        self.status_bar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

    def setup_search_tab(self):
        # Treeview for search results
        columns = ("Username", "Name", "Location", "Followers", "Action")
        self.search_tree = ttk.Treeview(self.search_tab, columns=columns, show="headings", height=15)

        # Define headings
        self.search_tree.heading("Username", text="Username")
        self.search_tree.heading("Name", text="Name")
        self.search_tree.heading("Location", text="Location")
        self.search_tree.heading("Followers", text="Followers")
        self.search_tree.heading("Action", text="Action")

        # Define column widths
        self.search_tree.column("Username", width=150)
        self.search_tree.column("Name", width=150)
        self.search_tree.column("Location", width=150)
        self.search_tree.column("Followers", width=100)
        self.search_tree.column("Action", width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.search_tab, orient=tk.VERTICAL, command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar.set)

        self.search_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.search_tab.columnconfigure(0, weight=1)
        self.search_tab.rowconfigure(0, weight=1)

    def setup_favorites_tab(self):


# Treeview for favorites
15: 23
columns = ("Username", "Name", "Location", "Followers", "Added", "Action")
self.favorites_tree = ttk.Treeview(self.favorites_tab, columns=columns, show="headings", height=15)

# Define headings
self.favorites_tree.heading("Username", text="Username")
self.favorites_tree.heading("Name", text="Name")
self.favorites_tree.heading("Location", text="Location")
self.favorites_tree.heading("Followers", text="Followers")
self.favorites_tree.heading("Added", text="Added")
self.favorites_tree.heading("Action", text="Action")

# Define column widths
self.favorites_tree.column("Username", width=150)
self.favorites_tree.column("Name", width=150)
self.favorites_tree.column("Location", width=150)
self.favorites_tree.column("Followers", width=80)
self.favorites_tree.column("Added", width=120)
self.favorites_tree.column("Action", width=100)

# Scrollbar
scrollbar = ttk.Scrollbar(self.favorites_tab, orient=tk.VERTICAL, command=self.favorites_tree.yview)
self.favorites_tree.configure(yscrollcommand=scrollbar.set)

self.favorites_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

self.favorites_tab.columnconfigure(0, weight=1)
self.favorites_tab.rowconfigure(0, weight=1)

# Refresh favorites display
self.refresh_favorites_display()


def search_user(self):
    username = self.search_entry.get().strip()

    # Validation: Check if search field is empty
    if not username:
        messagebox.showwarning("Warning", "Search field cannot be empty!")
        self.status_bar.config(text="Error: Search field is empty")
        return

    self.status_bar.config(text=f"Searching for user: {username}...")

    try:
        # GitHub API endpoint
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url)

        if response.status_code == 200:
            user_data = response.json()
            self.display_search_result(user_data)
            self.status_bar.config(text=f"Found user: {username}")
        elif response.status_code == 404:
            messagebox.showinfo("Not Found", f"User '{username}' not found on GitHub!")
            self.status_bar.config(text=f"User '{username}' not found")
            # Clear previous results
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)
        else:
            messagebox.showerror("Error", f"API Error: {response.status_code}")
            self.status_bar.config(text=f"API Error: {response.status_code}")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network error: {str(e)}")
        self.status_bar.config(text="Network error occurred")


def display_search_result(self, user_data):
    # Clear previous results
    for item in self.search_tree.get_children():
        self.search_tree.delete(item)

    # Store user data
    self.search_results = [user_data]

    # Check if user is already in favorites
    is_favorite = any(fav["login"] == user_data["login"] for fav in self.favorites)

    # Insert into treeview
    item_id = self.search_tree.insert("", tk.END, values=(
        user_data["login"],
        user_data.get("name", "N/A"),
        user_data.get("location", "N/A"),
        user_data.get("followers", 0),
        "Remove from Favorites" if is_favorite else "Add to Favorites"
    ))

    # Bind double-click to show user details
    self.search_tree.tag_bind(item_id, "<Double-1>",
                              15: 23
    lambda e, u=user_data: self.show_user_details(u))

    # Bind click on action button
    self.search_tree.bind("<ButtonRelease-1>", self.on_search_tree_click)


def on_search_tree_click(self, event):
    region = self.search_tree.identify_region(event.x, event.y)
    if region == "cell":
        column = self.search_tree.identify_column(event.x)
        if column == "#6":  # Action column
            item = self.search_tree.selection()[0] if self.search_tree.selection() else None
            if item:
                values = self.search_tree.item(item, "values")
                username = values[0]
                user_data = next((u for u in self.search_results if u["login"] == username), None)
                if user_data:
                    if values[4] == "Add to Favorites":
                        self.add_to_favorites(user_data)
                    else:
                        self.remove_from_favorites(username)


def add_to_favorites(self, user_data):
    # Check if already in favorites
    if any(fav["login"] == user_data["login"] for fav in self.favorites):
        messagebox.showinfo("Info", "User already in favorites!")
        return

    # Add with timestamp
    favorite_user = {
        **user_data,
        "added_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    self.favorites.append(favorite_user)
    self.save_favorites()
    self.refresh_favorites_display()

    # Update search results display
    for item in self.search_tree.get_children():
        if self.search_tree.item(item, "values")[0] == user_data["login"]:
            self.search_tree.item(item, values=(
                user_data["login"],
                user_data.get("name", "N/A"),
                user_data.get("location", "N/A"),
                user_data.get("followers", 0),
                "Remove from Favorites"
            ))
            break

    self.status_bar.config(text=f"Added {user_data['login']} to favorites")


def remove_from_favorites(self, username):
    self.favorites = [fav for fav in self.favorites if fav["login"] != username]
    self.save_favorites()
    self.refresh_favorites_display()

    # Update search results if this user is currently displayed
    for item in self.search_tree.get_children():
        if self.search_tree.item(item, "values")[0] == username:
            user_data = next((u for u in self.search_results if u["login"] == username), None)
            if user_data:
                self.search_tree.item(item, values=(
                    user_data["login"],
                    user_data.get("name", "N/A"),
                    user_data.get("location", "N/A"),
                    user_data.get("followers", 0),
                    "Add to Favorites"
                ))
            break

    self.status_bar.config(text=f"Removed {username} from favorites")


def refresh_favorites_display(self):
    # Clear current display
    for item in self.favorites_tree.get_children():
        self.favorites_tree.delete(item)

    # Insert all favorites
    for fav in self.favorites:
        item_id = self.favorites_tree.insert("", tk.END, values=(
            fav["login"],
            fav.get("name", "N/A"),
            fav.get("location", "N/A"),
            fav.get("followers", 0),
            fav.get("added_at", "N/A"),
            "Remove"
        ))
        self.favorites_tree.tag_bind(item_id, "<Double-1>",
                                     lambda e, u=fav: self.show_user_details(u))

    # Bind click on action button


15: 23
self.favorites_tree.bind("<ButtonRelease-1>", self.on_favorites_tree_click)


def on_favorites_tree_click(self, event):
    region = self.favorites_tree.identify_region(event.x, event.y)
    if region == "cell":
        column = self.favorites_tree.identify_column(event.x)
        if column == "#7":  # Action column
            item = self.favorites_tree.selection()[0] if self.favorites_tree.selection() else None
            if item:
                values = self.favorites_tree.item(item, "values")
                username = values[0]
                self.remove_from_favorites(username)


def show_user_details(self, user_data):
    # Create details window
    details_window = tk.Toplevel(self.root)
    details_window.title(f"User Details: {user_data['login']}")
    details_window.geometry("500x600")
    details_window.resizable(True, True)

    # Main frame
    frame = ttk.Frame(details_window, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)

    # Avatar
    if user_data.get("avatar_url"):
        try:
            from PIL import Image, ImageTk
            import urllib.request
            avatar_url = user_data["avatar_url"]
            with urllib.request.urlopen(avatar_url) as u:
                raw_data = u.read()
            from io import BytesIO
            img = Image.open(BytesIO(raw_data))
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            avatar_label = ttk.Label(frame, image=photo)
            avatar_label.image = photo
            avatar_label.pack(pady=(0, 10))
        except:
            pass

    # User info
    info_frame = ttk.Frame(frame)
    info_frame.pack(fill=tk.BOTH, expand=True)

    info = [
        ("Username:", user_data.get("login", "N/A")),
        ("Name:", user_data.get("name", "N/A")),
        ("Company:", user_data.get("company", "N/A")),
        ("Blog:", user_data.get("blog", "N/A")),
        ("Location:", user_data.get("location", "N/A")),
        ("Email:", user_data.get("email", "N/A")),
        ("Bio:", user_data.get("bio", "N/A")),
        ("Public Repos:", user_data.get("public_repos", 0)),
        ("Followers:", user_data.get("followers", 0)),
        ("Following:", user_data.get("following", 0)),
        ("Created at:", user_data.get("created_at", "N/A")[:10]),
        ("Profile URL:", user_data.get("html_url", "N/A"))
    ]

    for label, value in info:
        ttk.Label(info_frame, text=label, font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(5, 0))
        ttk.Label(info_frame, text=str(value), font=("Arial", 10)).pack(anchor=tk.W, pady=(0, 5))


def load_favorites(self):
    if os.path.exists(self.favorites_file):
        try:
            with open(self.favorites_file, "r", encoding="utf-8") as f:
                self.favorites = json.load(f)
        except:
            self.favorites = []
    else:
        self.favorites = []


def save_favorites(self):
    with open(self.favorites_file, "w", encoding="utf-8") as f:
        json.dump(self.favorites, f, indent=4, ensure_ascii=False)


def main():
    root = tk.Tk()
    app = GitHubUserFinder(root)
    root.mainloop()


if __name__ == "__main__":
    main()
