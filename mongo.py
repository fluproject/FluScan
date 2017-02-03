import pymongo

class ConexionMongoDB(object):
    def __init__(self, uri):
        self.MONGODB_URI = uri
        self.db = ""
        self.client = ""
        self.coleccion = ""

    def __del__(self):
        pass

    def open_conexion(self):
        self.client = pymongo.MongoClient(self.MONGODB_URI)
        self.db = self.client.get_default_database()

    def close_conexion(self):
        self.client.close()

    def insert_doc(self, coleccion, doc):
        try:
            #print doc
            colecc = self.db[coleccion]
            colecc.insert(doc)
            print(" ***********   Document Saved   **************\n")
        except Exception, e:
            print "\nERROR: %s" % str(e)
            print(" **********  Document not Saved  *************\n")
