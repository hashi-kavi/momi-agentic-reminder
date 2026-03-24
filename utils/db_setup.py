import sqlite3
from app.config import Config

def init_db():
    conn = sqlite3.connect(Config.DB_PATH)# connecting to the ddatabase
    cursor = conn.cursor()#like a pointer/control to execute SQL commands ,use for run queries,create table ,insert table

    # Table for Facts (Memory)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_memory(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   content TEXT NOT NULL,
                   category TEXT, --e.g.,'preference', 'fact','name'
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
    
    # Table for Reminders
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   task TEXT NOT NULL,
                   remind_at DATETIME NOT NULL,
                   status TEXT DEFAULT 'pending'
                   
                   )
                   ''')
    conn.commit()#Saves all changes to the database
    conn.close()#Closes database connection
    print("Database Initialized at ",Config.DB_PATH)

if __name__ == "__main__":

    init_db()

