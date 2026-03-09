from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
class DatabaseManager:
    def __init__(self, db_url):
        self.engine=create_engine(db_url, echo=False)
        self.Session=sessionmaker(bind=self.engine)

    def execute_query(self,query:str):
        try:
            with self.Session() as session:
                result=session.execute(text(query))
                if result.returns_rows:
                    return result.fetchall()
                else:
                   session.commit()
                   return result.rowcount
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        
    def get_table_names(self):
        inspector=inspect(self.engine)
        return inspector.get_table_names()
    def close(self):
        self.engine.dispose()

if __name__ == "__main__":
    db_manager=DatabaseManager('sqlite:///my_database.db')
    customers=db_manager.execute_query('SELECT * FROM customers')
    print("Customers:", customers)
    
    db_manager.close()          
        

        