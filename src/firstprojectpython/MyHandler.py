from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from mysql import connector
from templates import city_template, html_template

cnx = connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    database="world"
    )

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(HTTPStatus.NO_CONTENT)  # 204 No Content
            self.end_headers()
            return
        with cnx.cursor() as cur:
            cur.execute("SELECT * FROM city")
            data = cur.fetchall()  # <-- Se llama sobre el cursor y en minúsculas

        list_cities = f"<ul>{''.join(city_template(c) for c in data)}</ul>"

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(f"{html_template(list_cities)}".encode('utf-8'))