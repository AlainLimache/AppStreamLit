import sqlite3
import streamlit_authenticator as stauth

class UserDatabase:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def create_connection(self):
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                email TEXT,
                                name TEXT,
                                password TEXT,
                                role TEXT
                            )""")
        self.conn.commit()
        self.add_user("admin", "admin@admin.com", "Admin Admin", "admin", "admin")

    def get_credentials(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()
        credentials = {}
        credentials["usernames"] = {}
        for row in rows:
            username, email, name, password, role = row
            credentials["usernames"][username] = {"email": email, "name": name, "password": password}
        return credentials
    
    def add_user(self, username, email, name, password, role):
        if not self.user_exists(username):
            hashed_password = stauth.Hasher([password]).generate()
            self.cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (username, email, name, hashed_password[0], role))
            self.conn.commit()
            return True
        return False


    def update_credentials(self, credentials):
        for username, user_data in credentials.items():
            self.cursor.execute("UPDATE users SET email=?, name=?, password=? WHERE username=?", (user_data["email"], user_data["name"], user_data["password"], username))
        self.conn.commit()

    def user_exists(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()
        return row is not None
    
    def get_role(self, username):
        self.cursor.execute("SELECT role FROM users WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if(row is not None):
            return row[0]
