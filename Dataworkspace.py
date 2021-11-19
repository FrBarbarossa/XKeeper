import sqlite3
import bcrypt

salt = bcrypt.gensalt()

conn = sqlite3.connect('usersdat.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INTEGER PRIMARY KEY,
   username TEXT,
   password TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS folders(
   userid INTEGER PRIMARY KEY,
   folderplace TEXT);
""")
conn.commit()


def insert_user(name: str, password: str) -> bool:
    user = list(cur.execute("SELECT userid FROM users WHERE username=(?)", (name,)))
    if not user:
        newfolder = ("Asds",)  # Формирование ссылки на таблицу
        psw = bcrypt.hashpw(password.encode(), salt)
        user = (name, psw)
        cur.execute("INSERT INTO users (username, password) VALUES(?,?);", user)
        cur.execute("INSERT INTO folders (folderplace) VALUES(?);", newfolder)
        conn.commit()
        return True
    return False


def get_folder(name: str) -> str:
    user_id = list(cur.execute("SELECT userid FROM users WHERE username=(?)", (name,)))
    if user_id:
        user_id = user_id[0][0]
        folderlink = list(cur.execute("SELECT folderplace FROM folders WHERE userid=(?)", (user_id,)))[0][0]
        print(folderlink)


def login(name: str, password: str) -> bool:
    user = list(cur.execute("SELECT password FROM users WHERE username=(?)", (name,)))
    if user:
        psw = bcrypt.checkpw(password.encode(), user[0][0])
        if psw:
            return True
    return False


# print(insert_user('ali2', '123'))
print(login('ali2', '1223'))
# print(insert_user('BLANK', '1234fas'))

