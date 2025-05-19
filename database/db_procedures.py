from sys_config import connection_string
from sys_log import log
import pyodbc
import sqlite3
import json


def db_select(query):
    try:
        # Establish the connection
        with pyodbc.connect(connection_string) as conn:
            # Create a cursor object
            cursor = conn.cursor()

            # Execute the query
            cursor.execute(query)

            # Fetch and print all rows
            rows = cursor.fetchall()
            return rows

    except pyodbc.Error as e:
        log(str(e))


def db_execute(query):
    try:
        # Establish the connection
        with pyodbc.connect(connection_string) as conn:

            # Increasing the max buffer size (for very large queries)
            conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
            conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
            conn.setencoding(encoding='utf-8')

            # Example of setting TEXTSIZE to a large value for SQL Server
            # This is crucial when dealing with large text or image data
            conn.execute("SET TEXTSIZE 2147483647")  # Max size in bytes

            # Create a cursor with increased arraysize for large datasets
            cursor = conn.cursor()
            cursor.arraysize = 1000  # Adjust based on expected result set size

            # Create a cursor object
            cursor = conn.cursor()

            # Execute the query
            cursor.execute(query)

            # Fetch all rows from the cursor
            rows = cursor.fetchall()

            # Get column names from the cursor description
            columns = [column[0] for column in cursor.description]

            # Convert the rows to a list of dictionaries
            result = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                result.append(row_dict)

            # Convert the list of dictionaries to a JSON object
            json_data = json.dumps(result, separators=(',', ':'))

            return json_data

    except pyodbc.Error as e:
        log(str(e))


'''###############################################  SQLite #################################################'''


def create_table_sqlite(sql_create_table, database_name):
    """
    Create a table in the database defined in the parameters
    :rtype: object
    :param sql_create_table: The CREATE TABLE command string.
    :param database_name: The database where the Table will be created.
    :return: None.
    """
    # Connect to SQLite database
    conn = sqlite3.connect(database_name)
    try:
        # Create a cursor object
        cursor = conn.cursor()

        print(sql_create_table)

        # Create a table
        cursor.execute(sql_create_table)

        # Commit changes and close connection
        conn.commit()

    except Exception as e:
        log(str(e))

    finally:
        conn.close()


def select_sqlite(my_select_command, database_name):
    """
    Select information from the database_name based on the my_select_command
    :param my_select_command: SELECT instruction
    :param database_name: Name of the database where the information is saved
    :return: None.
    """
    # Connect to SQLite database
    conn = sqlite3.connect(database_name)
    try:
        cursor = conn.cursor()

        # Select and fetch data from the table
        cursor.execute(my_select_command)
        rows = cursor.fetchall()

        print(f"from the database: {database_name}")

        for row in rows:
            print(row)

    except Exception as e:
        log(str(e))

    finally:
        conn.close()
