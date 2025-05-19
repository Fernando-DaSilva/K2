from db_procedures import db_select, db_execute, create_table_sqlite, select_sqlite
from sys_log import log, log_error
from sp_profiles import Profiles


def test1_CheckUserReadFromDatabase():
    '''
    This test read the info from the User in the database.
    :return: JSON Object
    '''
    rows = db_select("select top 1 NameFirst, NameLast from [User] where Id = 1 order by Id FOR JSON PATH")
    print(rows)


def test2():
    create_table_sqlite("create table log (log_text text, date_created text, status text)", "log.db")


def test3():
    log("Hello World")


def test4():
    select_sqlite("select * from log","log.db")


def test5():
    log_error("error test: Hello World")


def test6():
    result = db_execute("exec [dbo].[zPy_Sys_v01_sp_Login_Get_json] @UserName = 'joanxtb@gmail.com', @Password = 'master*10*'")
    print(result)

def test7():
    profiles = Profiles()
    users = profiles.profile_login("api_key_1", "joanxtb@gmail.com", "master*10*")
    print(users)


if __name__ == "__main__":
    test7()



