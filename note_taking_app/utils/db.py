import os
from dotenv import load_dotenv
import mysql.connector

# Load environment variables
load_dotenv()

db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()



def get_notes():
    try:
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM notes ORDER BY id DESC"
        cursor.execute(query)
        notes = cursor.fetchall()
        cursor.close()
        return notes
    except Exception as e:
        print(f"Error fetching notes: {e}")
        return []
    # cursor.execute("SELECT id, title, content FROM notes")
    # return cursor.fetchall()
# def get_notes():
#     try:
#         cursor = db.cursor()
#         cursor.execute("SELECT id, title, content FROM notes")
#         notes = cursor.fetchall()
#         # Debugging: Check if results are fetched properly
#         cursor.close()
#         return notes
#     except Exception as e:
#         print(f"Error retrieving notes: {e}")
#         return []

def add_note_to_db(title, content):
    cursor.execute("INSERT INTO notes (title, content) VALUES (%s, %s)", (title, content))
    db.commit()

def delete_note_from_db(note_id):
    cursor.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    db.commit()

def edit_note_in_db(note_id, title, content):
    cursor.execute("UPDATE notes SET title = %s, content = %s WHERE id = %s", (title, content, note_id))
    db.commit()
    


def update_note_in_db(note_id, title, content):
    try:
        cursor = db.cursor()
 
        query = " UPDATE notes SET title = %s, content = %s WHERE id = %s"
        cursor.execute(query, (title, content, note_id))
        db.commit()
        print("Note updated successfully")
        cursor.close()
        return True
    except Exception as e:
        print(f"Error updating note: {e}")
     



# def update_note_in_db(note_id, title, content):
#     try:
#         cursor = db.cursor()
#         query = """
#         UPDATE notes
#         SET title = %s, content = %s
#         WHERE id = %s
#         """
#         print(f"Executing query: {query} with params: {title}, {content}, {note_id}")
#         cursor.execute(query, (title, content, note_id))
#         db.commit()
#         cursor.close()
#         return True
#     except Exception as e:
#         print(f"Error updating note: {e}")
#         return False