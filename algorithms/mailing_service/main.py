import sqlite3
from typing import Any

DATABASE = r"B:\Computer Science and Engineering\BOIHackathon - AQI Model for AI\algorithms\database\emailing_list.db"

# Function to connect to the database and create the table if it doesn't exist
def create_table():
    conn: Any = None

    try:
        # Connect to the database (or create it if it doesn't exist)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Create the emailing_list table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emailing_list (
                email TEXT PRIMARY KEY
            )
        ''')
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
    finally:
        # Close the connection
        conn.close()


# Function to add an email to the database
def add_email(email):
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


# Function to retrieve all emails from the database
def get_all_emails():
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



# # Example usage
# if __name__ == '__main__':
#     create_table()  # Create table if it doesn't exist
#     recipient_list = ["abhijeetrajhans.ar@gmail.com", "shreyasiray11@gmail.com",
#                       "abhijeet.229301491@muj.manipal.edu", "abhijeetrajhans.04@gmail.com",
#                       "shreyasi.229302125@muj.manipal.edu"]
#
#     for email in recipient_list:
#         add_email(email)
#
#     # Get and print all emails from the database
#     emails = get_all_emails()
#     print("Emailing list:", emails)
