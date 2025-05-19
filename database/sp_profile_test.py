from sys_config import connection_string
import pyodbc
import json

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

        # Execute a query
        cursor.execute("exec [dbo].[zPyv01_sp_Login_Get_json] @UserName = 'joanxtb@gmail.com', @Password = 'master*10*'")

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
        json_data = json.dumps(result, indent=4)

        print(json_data)

except pyodbc.Error as e:
    print(str(e))


