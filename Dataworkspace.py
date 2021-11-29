import sqlite3
import bcrypt
from typing import Union

salt = bcrypt.gensalt()

conn = sqlite3.connect('usersdat.db', check_same_thread=False)
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

cur.execute("""CREATE TABLE IF NOT EXISTS authed(
    id INTEGER PRIMARY KEY,
   tguserid TEXT,
   accname TEXT);
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


def check_auth(userid: int) -> Union[bool, str]:
    account = list(cur.execute('SELECT accname FROM authed WHERE tguserid=(?)', (str(userid),)))
    if account:
        print(account)
        return True
    return False


def auth(userid: int, account: str) -> None:
    cur.execute("INSERT INTO authed (tguserid, accname) VALUES(?,?);", (str(userid), account))
    conn.commit()

# print(insert_user('ali2', '123'))
# print(login('ali2', '1223'))
# print(insert_user('BLANK', '1234fas'))
# cur.execute("INSERT INTO authed (tguserid, accname) VALUES(?,?);", ('570805623', 'sasda'))
# conn.commit()
# print(check_auth(570805623))
