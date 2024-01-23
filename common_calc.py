import configparser
import requests
import argparse
import pandas as pd

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

def chatwork(message):
    # エンドポイントの生成
    ENDPOINT = 'https://api.chatwork.com/v2'
    post_message_url = '{}/rooms/{}/messages'.format(ENDPOINT, '162471617')

    # チャットワークAPIにポストする場合のヘッダー、パラメータを設定
    headers = { 'X-ChatWorkToken': '40d33e296853bac94afbe1f6ef96cd9b'}
    params = { 'body': message }

    # ポストリクエストを実行
    r = requests.post(post_message_url,
                        headers=headers,
                        params=params)

def insert_sql(insert_sql):
    import pymysql.cursors
    conn = pymysql.connect(host='160.251.99.127',user='meiteko',db='auto_trade',charset='utf8mb4',password='Kamihiko1@',cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute(insert_sql)
            conn.commit()
            conn.close()
    except:
        import traceback
        chatwork(insert_sql)
        chatwork("インサートのエラーたまぁ"+traceback.format_exc())

def select_sql(select_sql):
    import pymysql.cursors
    conn = pymysql.connect(host='160.251.99.127',user='meiteko',db='auto_trade',charset='utf8mb4',password='Kamihiko1@',cursorclass=pymysql.cursors.DictCursor)
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_sql)
            result = cursor.fetchall()
            conn.close()
            return result
    except:
        import traceback
        chatwork(select_sql)
        chatwork("セレクトのエラーたまぁ"+traceback.format_exc())
