"""
Definitions for the system
All possible use in other parts of the system
"""
# Default Language for system idiom messages.

sys_idiom_English = "ENG"
sys_idiom_Portuguese_Brazil = "PT-BR"
sys_idiom_Spanish = "ESP"
sys_idiom_Lithuanian = "LT"

# Definition of the Idiom
sys_idiom = sys_idiom_Portuguese_Brazil

# Driver ODBC Version.
driver_odbc = '{ODBC Driver 17 for SQL Server}'

# Connection Available Configurations
server_ip_production = '52.116.11.2'  # Production Server LIVE -- BE AWARE OF IT.
server_ip_development = '52.116.11.8'  # File Server - Development Environment.
server_ip_student = '52.116.11.8'  # File Server - Development Environment.

# Connections configurations:
# Database:
database_name_production = 'SL'
database_name_development = 'SL_DEV'
database_name_student = 'FernandoLT'

# User:
user_name_production = 'sa'
user_name_development = 'sa'
user_name_student = 'student'

# Password:
password_conn_production = 'Sxdcfv!13'
password_conn_development = 'Sxdcfv!13'
password_conn_student = 'Student123#$'

# Nicknames for the environments:
environment_production = 'production'
environment_development = 'development'
environment_student = 'student'

# DEFAULT: Student ( minimal problems with changes ) Keep like that to avoid production errors.
server_ip = server_ip_student
database_name = database_name_student
user_name = user_name_student
password_conn = password_conn_student

""" ============================= 
    === CONFIGURATION RUNNING ===
    =============================
"""

# Connection choice for this system: Here you will define the actual environment to connect.
environment = environment_production

# The system will obey the environment choice.
if environment == environment_production:
    server_ip = server_ip_production
    database_name = database_name_production
    user_name = user_name_production
    password_conn = password_conn_production

if environment == environment_development:
    server_ip = server_ip_development
    database_name = database_name_development
    user_name = user_name_development
    password_conn = password_conn_production

if environment == environment_student:
    server_ip = server_ip_student
    database_name = database_name_student
    user_name = user_name_student
    password_conn = password_conn_student

# Connection string to export and used by the database layer.
connection_string = (f'DRIVER={driver_odbc};'
                     f'SERVER={server_ip};'
                     f'DATABASE={database_name};'
                     f'UID={user_name};'
                     f'PWD={password_conn}')
