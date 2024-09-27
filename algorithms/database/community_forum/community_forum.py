import sqlite3

COMMUNITY_FORUM_DATABASE = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\database\community_forum\community_forum.db"


def create_community_forum_database():
    # forum_db_setup.py

    import sqlite3

    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect(COMMUNITY_FORUM_DATABASE)
    c = conn.cursor()

    # Create a table for storing comments
    c.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            comment TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Commit and close the connection
    conn.commit()
    conn.close()


def show_comments():
    conn = sqlite3.connect(COMMUNITY_FORUM_DATABASE)
    c = conn.cursor()

    c.execute("SELECT * FROM comments")
    rows = c.fetchall()

    for row in rows:
        print(row)

