import sqlite3
from app.config import Config
from langchain_core.tools import tool


class MemoryManager:
    def __init__(self):
        self.db_path = Config.DB_PATH
    

    def save_fact(self,content:str,category:str = "general"):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO user_memory (content,category) VALUES(?,?)",#prevent SQL injection attacks and safely insert variables.
            (content,category)

        )
        conn.commit()
        conn.close()
        return f"Saved to memory: {content}"
    

    def get_all_memories(self):
        """Retrieves everything the AI knows so far."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT content FROM user_memory"
        )
        rows = cursor.fetchall()
        conn.close()
        #Return as a simple list of  strings
        return [row[0] for row in rows]
    
    def get_memories_string(self):
          #fetch all memories and turn them into a single block of text
          memories = self.get_all_memories()
          if not memories:
                return "No past memories found."
          #format:"-fact 1 \n - fact 2"
          return "\n".join([f"-{m}" for m in memories])


    
@tool # this converts function into a callable capabiltiy for the llm
def store_user_fact(fact:str):# here fact -> input from the AI
                """
                Use this tool when the user tells you something personal about themselves that you should remember for the future(e.g.,their name,job,likes,or plans.)
                """
                manager = MemoryManager()#Creates an instance of memory system
                return manager.save_fact(fact)
