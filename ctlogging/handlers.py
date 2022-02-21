from logging import  Handler
from uuid import uuid4
import mysql.connector


class MysqlHandler(Handler):

    def __init__(self, host, database, user, password, port):
        Handler.__init__(self)
        self.conn = mysql.connector.connect(host=host,
                        port=port,
						database=database,
						user=user,
						password=password)                       
        self.cursorObject = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursorObject.execute("""
            CREATE TABLE IF NOT EXISTS log (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                level VARCHAR(20), 
                name VARCHAR(100), 
                msg LONGTEXT,
                time DATETIME DEFAULT NULL
                )""")

    def emit(self, record):
        level = record.levelname
        name = record.name
        time = record.asctime.split(",")[0]
        msg = record.msg
        sql = f'INSERT INTO log (time, level, name, msg) values ("{time}","{level}","{name}","{msg}");'
        self.cursorObject.execute(sql)
        self.conn.commit()

