# -*- coding: utf-8 -*-

import mysql.connector
import secret
import random


def allocate():
    conn = mysql.connector.connect(host=secret.host, port=3306, user=secret.username, password=secret.password,
                                   database='Medium', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT username FROM users"
    cur.execute(sql)
    result = cur.fetchall()
    username_list = []
    for user in result:
        username_list.append(user[0])
    for i in range(5):
        random.shuffle(username_list)
    num = len(username_list) / len(secret.ip_list) + 1
    for i in range(len(username_list)):
        sql = "UPDATE users SET ip='%s' WHERE username='%s'" % (secret.ip_list[i/num], username_list[i])
        cur.execute(sql)
        conn.commit()
        print(i)
    cur.close()
    conn.close()


if __name__ == '__main__':
    allocate()

