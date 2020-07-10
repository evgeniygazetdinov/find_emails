
import os
import sqlite3
 

database_name = "webstudio_database.db"

#IMPLEMETED IN PURE SQL FOR EDUCATED AIMS

class Web_studio_db():
    def __init__(self,database_name):
        self.db_name = database_name
        if not os.path.exists(database_name):
            self.create_db()
            self.put_sended_emails_into_db()



    def create_db(self):        
        conn = sqlite3.connect() 
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE web_studios
                        (name text, website text, email text,
                        date_send timestamp)
                    """)
        conn.commit()