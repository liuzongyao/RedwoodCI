import psycopg2
class DBConnect:
    def __init__(self):
        pass

    def connectDB(self, params):
        db_name = params.get("DB_NAME")
        db_port = params.get("DB_PORT", "5432")
        db_user = params.get("DB_USER")
        db_password = params.get("DB_PASSWORD")
        db_host = params.get("DB_HOST")
        conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
        print type(conn)
        return conn
    def select_db(self, params):
        data=''
        psql = params.get("psql", "")
        conn = params.get("conn")
        cur = conn.cursor()
        cur.execute(psql)
        rows = cur.fetchall()
        for row in rows:
            for value in row:
                data += "{},".format(value)
        conn.close()
        print data
        return data

    def assert_substring_in(self, params):
        data = params.get('data')
        substring = params.get('substring')
        assert substring in data