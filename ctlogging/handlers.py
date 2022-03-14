from logging import Handler
import os


DB_CONN_STR: str = os.environ.get("DB_CONN_STR", None)


class MysqlHandler(Handler):
    def __init__(
        self,
        host: str = None,
        database: str = None,
        user: str = None,
        password: str = None,
        port: str = None,
        conn_str: str = DB_CONN_STR,
    ):
        import mysql.connector

        Handler.__init__(self)
        if conn_str is not None:
            connectParams = dict(entry.split("=") for entry in conn_str.split(";"))
            self.conn = mysql.connector.connect(**connectParams)
        else:
            self.conn = mysql.connector.connect(
                host=host, port=port, database=database, user=user, password=password
            )
        self.cursorObject = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursorObject.execute(
            """
            CREATE TABLE IF NOT EXISTS log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                correlation_id VARCHAR(100),
                time DATETIME DEFAULT NULL,
                level VARCHAR(20),
                name VARCHAR(100),
                msg LONGTEXT
                )"""
        )

    def emit(self, record):
        level = record.levelname
        name = record.name
        time = record.asctime.split(",")[0]
        msg = record.msg
        correlation_id = record.correlation_id
        if correlation_id is None:
            correlation_id = "NONE"
        sql = f"""
            INSERT INTO log (time, level, name, msg, correlation_id)
            values ("{time}","{level}","{name}","{msg}", "{correlation_id}");
            """
        self.cursorObject.execute(sql)
        self.conn.commit()


class MssqlHandler(Handler):
    def __init__(self, conn_str: str = DB_CONN_STR):
        import pyodbc

        Handler.__init__(self)
        assert (
            conn_str is not None
        ), "Missing connection string, either pass conn_str from yaml or set env DB_CONN_STR"
        self.conn = pyodbc.connect(conn_str)
        self.cursorObject = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursorObject.execute(
            """
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='log' and xtype='U')
                CREATE TABLE [dbo].[log] (
                    [id] [int] NOT NULL IDENTITY(1,1) PRIMARY KEY,
                    [correlation_id] [varchar](50) NOT NULL,
                    [time] [datetime] NOT NULL,
                    [level] [varchar](20) NOT NULL,
                    [name] [varchar](100) NOT NULL,
                    [msg] [ntext] NULL,
                )
            """
        )

    def emit(self, record):
        level = record.levelname
        name = record.name
        time = record.asctime.split(",")[0]
        msg = record.msg
        correlation_id = record.correlation_id
        if correlation_id is None:
            correlation_id = "NONE"
        sql = f"""
            INSERT INTO log (time, level, name, msg, correlation_id)
            values ('{time}','{level}','{name}','{msg}','{correlation_id}');
            """
        self.cursorObject.execute(sql)
        self.conn.commit()
