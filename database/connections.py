import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///my_database.db")
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
            return None
        
    def get_table_names(self):
        inspector=inspect(self.engine)
        return inspector.get_table_names()
    def get_table_schema(self,table_name:str):
        inspector=inspect(self.engine)
        columns=inspector.get_columns(table_name)
        primary_keys=inspector.get_pk_constraint(table_name)['constrained_columns']
        foreign_keys=inspector.get_foreign_keys(table_name)
        schema={
            'columns': columns,
            'primary_keys': primary_keys,
            'foreign_keys': foreign_keys
        }
        return schema
    def close(self):
        self.engine.dispose()

if __name__ == "__main__":
    db_manager=DatabaseManager(DATABASE_URL)
    print("Schema for 'customers' table:")
    print(db_manager.get_table_schema('customers'))
    db_manager.close()          
        

        