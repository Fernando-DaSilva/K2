import datetime
import sqlite3


def log(log_text: str):
    db = "log.db"
    conn = sqlite3.connect(db)

    try:
        # Connect to SQLite database
        cursor = conn.cursor()

        sql_insert_command = "insert into log (log_text, date_created, status) values ('" + log_text + "',"
        sql_insert_command = sql_insert_command + "datetime('now'),"
        sql_insert_command = sql_insert_command + "'new log')"

        # Insert data into the table
        cursor.execute(sql_insert_command)

        # Commit changes and close connection
        conn.commit()

        log_error(str(log_text))

    except Exception as e:
        log_error(str(e))

    finally:
        conn.close()


def log_error(message: str):

    log_file = "sys_error_log.txt"

    # Get current date and time
    current_time = datetime.datetime.now()

    # Format the log message
    log_message = f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {message}\n"

    # Append the log message to the log file
    with open(log_file, "a") as file:
        file.write(log_message)
