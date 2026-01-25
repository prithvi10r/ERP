import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

current_username = "jaanu"
new_username = "Jaanu"
new_password = "Jaanu@123"

cursor.execute("SELECT * FROM staff WHERE username=?", (current_username,))
staff = cursor.fetchone()

if staff:
    cursor.execute(
        "UPDATE staff SET username=?, password=? WHERE username=?",
        (new_username, new_password, current_username)
    )
    conn.commit()
    print(f"Username and password updated successfully: {new_username}, {new_password}")
else:
    print(f"Staff '{current_username}' not found in DB")

conn.close()
