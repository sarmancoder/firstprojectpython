from mysql.connector import MySQLConnection

class DBConnection(MySQLConnection):

    def __init__(self, **kwargs):
        # Puedes definir valores por defecto y sobrescribirlos con kwargs si quieres
        config = {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "password": "",  # tu contraseña si la tienes
            "database": "world",
        }
        # Actualizamos con lo que le pases al instanciar (si pasas algo)
        config.update(kwargs)

        # Llamamos al constructor de la clase padre (MySQLConnection)
        super().__init__(**config)

    def retrieve_cities(self):
        with self.cursor() as cur:
            cur.execute("SELECT * FROM city")
            data = cur.fetchall()  # <-- Se llama sobre el cursor y en minúsculas
        return data