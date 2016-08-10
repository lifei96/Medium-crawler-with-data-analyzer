# -*- coding: utf-8 -*-

import mysql.connector
import secret
import random


def build_database():
    conn = mysql.connector.connect(host=secret.host, port=3306, user=secret.username, password=secret.password,
                                   database='Medium', charset='utf8')
    cur = conn.cursor()
    sql = 'CREATE TABLE users (' \
          'username varchar(255) NOT NULL, ' \
          'visited int NOT NULL, ' \
          'failed int NOT NULL, ' \
          'ip varchar(255) NOT NULL, ' \
          'PRIMARY KEY (username)' \
          ')'
    cur.execute(sql)
    conn.commit()
    file_in = open('ID_list.txt', 'r')
    ID_list = list(set((file_in.read()).split(' ')))
    num = 0
    for ID in ID_list:
        print(ID)
        try:
            sql = "INSERT INTO users VALUE('%s', %s, %s, '%s')" % (ID, 0, 0, secret.ip_list[random.randint(0, len(secret.ip_list)-1)])
            cur.execute(sql)
            conn.commit()
        except:
            print('-----failed')
            continue
        num += 1
        print('%s/%s' % (num, len(ID_list)))
    cur.close()
    conn.close()


if __name__ == '__main__':
    build_database()
