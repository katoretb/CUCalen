import MySQLdb
from os import getenv
from dotenv import load_dotenv
from route.func.errmaker import errmaker

load_dotenv()

class sqry():
    def __init__(s):
        s.db = MySQLdb.connect(
            host = getenv('HOST'),
            user = getenv('USER'),
            password = getenv('PASS'),
            database = 'CUCalen'
        )
        s.cursor = s.db.cursor()

    def sqadd(s, table, keys, values):
        try:
            k = ", ".join(keys)
            v = "', '".join(values)
            s.cursor.execute(f"INSERT INTO {table} ({k}) VALUES ('{v}')")
            s.db.commit()
            return "all good", False
        except Exception as error:
            print("An exception occurred:", error)
            return errmaker(500, "sql insert err"), True

    def sqdel(s, table, condi):
        try:
            s.cursor.execute(f"DELETE FROM {table} WHERE {condi}")
            s.db.commit()
            return "all good", False
        except Exception as error:
            print("An exception occurred:", error)
            return errmaker(500, "sql delete err"), True

    def squpd(s, table, kvdict, condi):
        try:
            kvl = []
            for k, v in kvdict.items():
                kvl.append(f"{k}={v}")
            kvs = ", ".join(kvl)
            s.cursor.execute(f"UPDATE {table} SET {kvs} WHERE {condi}")
            s.db.commit()
            return "all good", False
        except Exception as error:
            print("An exception occurred:", error)
            return errmaker(500, "sql update err"), True

    def sqsel(s, table, keys, condi="1"):
        try:
            k = ", ".join(keys)
            s.cursor.execute(f"SELECT {k} FROM {table} WHERE {condi}")
            return s.cursor.fetchall(), False
        except Exception as error:
            print("An exception occurred:", error)
            return errmaker(500, "sql select err"), True

    def sqcre(s, table, column):
        try:
            c = ', '.join(column)
            s.cursor.execute(f"CREATE TABLE {table} ({c})")
            return "all good", False
        except Exception as error:
            print("An exception occurred:", error)
            return errmaker(500, "sql create err"), True
        
    def kill_connect(s):
        s.cursor.close()
        s.db.close()
        return
