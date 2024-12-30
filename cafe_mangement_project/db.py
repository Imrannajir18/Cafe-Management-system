import mysql.connector
from werkzeug.security import check_password_hash

mydb=mysql.connector.connect(
    host='localhost',
    user='Emran18',
    password='891901',
    database='sample',

)
cursor=mydb.cursor()
# hashed_password='pbkdf2:sha256:1000000$BZfHF0wjx6MGaBvU$3d27c9c84312df975dc07a0e4640447d6c272aba3a86b037c5cdcb9c6237ac07'
# cursor.execute("CREATE TABLE user_details(user_id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL, firstname VARCHAR(255), lastname VARCHAR(255), email VARCHAR(255),username varchar(25), password VARCHAR(255))")
cursor.execute("select * from user_details where username='Emran18'")
result=cursor.fetchone()[5]

print(result)
# re_entered_password='Imran@18'

# if check_password_hash(result,re_entered_password):
#     print('Password Matched')
# else:
#     print('Password not matched')

# result=cursor.fetchall()
# print(result)