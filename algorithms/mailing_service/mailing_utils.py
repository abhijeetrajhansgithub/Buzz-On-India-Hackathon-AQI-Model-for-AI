import sqlite3
from typing import Any

# DATABASE = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\database\emailing_list.db"


# Function to add an email to the database
def add_email(email, DATABASE):
    conn: Any = None

    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Insert the email into the table
        cursor.execute('''
            INSERT INTO emailing_list (email) VALUES (?)
        ''', (email,))
        conn.commit()
        print(f"Email '{email}' added successfully.")

    except sqlite3.IntegrityError:
        print(f"Error: Email '{email}' already exists.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the connection
        conn.close()


def get_all_emails(DATABASE):
    conn: Any = None
    try:
        # Connect to the database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Query to get all emails
        cursor.execute('SELECT email FROM emailing_list')
        emails = cursor.fetchall()

        # If there are emails, return them
        if emails:
            return [email[0] for email in emails]
        else:
            return []

    except sqlite3.Error as e:
        print(f"Error retrieving emails: {e}")
    finally:
        # Close the connection
        conn.close()


