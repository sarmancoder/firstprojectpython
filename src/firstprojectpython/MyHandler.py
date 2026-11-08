from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from .DBConnection import DBConnection
from .templates import city_template, html_template

class MyHandler(BaseHTTPRequestHandler):
    db_connection: DBConnection

    def __init__(self, *args, **kwargs):
        self.db_connection = DBConnection()
        # Pasamos *args y **kwargs hacia la clase padre para que el servidor no falle
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(HTTPStatus.NO_CONTENT)  # 204 No Content
            self.end_headers()
            return

        data = self.db_connection.retrieve_cities()

        list_cities = f"<ul>{''.join(city_template(c) for c in data)}</ul>"

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f"{html_template(list_cities)}".encode('utf-8'))