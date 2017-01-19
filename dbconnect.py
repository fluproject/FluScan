import MySQLdb

class Dbconnect(object):
    def __init__(self, dbcon):
        # Database connection
        self.dbhost = dbcon['dbhost']
        self.dbuser = dbcon['dbuser']
        self.dbpass = dbcon['dbpass']
        self.dbname = dbcon['dbname']

    def runquery(self, query=''):
        datos = [self.dbhost, self.dbuser, self.dbpass, self.dbname]
        conn = MySQLdb.connect(*datos)
        cursor = conn.cursor()
        cursor.execute(query)
        if query.upper().startswith('SELECT'):
            data = cursor.fetchall()
        else:
            conn.commit()
            data = None
        cursor.close()
        conn.close()
        return data
