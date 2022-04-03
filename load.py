import pandas as pd
import sqlite3


class ReadSql():

    def __init__(self, file, table_name, col):
        self.file = file
        self.table_name = table_name
        self.column = col
        self.con = sqlite3.connect(self.file)

    def dataframe(self, where_statement=None):
        if where_statement: 
            self.args = where_statement
            additional_statement = "WHERE " + " AND ".join(self.args)
        else: additional_statement = ""
        
        data = pd.read_sql_query(f"SELECT {self.column} from {self.table_name} {additional_statement}" , self.con)
        return data

if __name__ == '__main__':
    pass