import pandas as pd
import sqlite3


class SqlCreator():

    def __init__(self, dataframe, table_name):
        self.dataframe = dataframe
        self.table_name = table_name
        self.dataframe.columns = self.dataframe.columns.str.lower().str.strip()

    def tosql(self, sql_file):
        self.sql_file = sql_file
        con = sqlite3.connect(self.sql_file)
        self.dataframe.to_sql(self.table_name, con, if_exists='replace')
        con.close()


if __name__ == '__main__':
    pass