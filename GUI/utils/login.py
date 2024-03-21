from ..database import user_table


def get_users():
    user_pwd = {}
    users = user_table.get_users()
    for u in users:
        user_pwd[u.username] = u.password
    print(user_pwd)
    return user_pwd