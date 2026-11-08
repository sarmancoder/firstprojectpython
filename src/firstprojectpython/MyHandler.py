from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
import os
from .DBConnection import DBConnection
from .templates import city_template, html_template
from pathlib import Path
import mimetypes

class MyHandler(BaseHTTPRequestHandler):
    db_connection: DBConnection

    def __init__(self, *args, **kwargs):
        self.db_connection = DBConnection()
        # Pasamos *args y **kwargs hacia la clase padre para que el servidor no falle
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        if self.path == '/':
            data = self.db_connection.retrieve_cities()
            
            list_cities = f"<ul>{''.join(city_template(c) for c in data)}</ul>"

            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"{html_template(list_cities)}".encode('utf-8'))
            return
        
        self._lookForFile()

    def _lookForFile(self):
        __dirname = Path.cwd()
    
        # Limpiamos el self.path para quitarle la barra inicial '/' si la tiene, 
        # ya que si empieza por '/' Path lo interpretará como ruta absoluta y pisará __dirname.
        clean_path = self.path.lstrip('/')
        
        # Unimos usando el operador / de pathlib
        publicPath = __dirname / os.path.join("public", clean_path)
        
        if publicPath.is_file():
            print(f"Entregando {publicPath}")
            # Detectamos el tipo de contenido automáticamente (.ico, .css, .js, etc.)
            content_type, _ = mimetypes.guess_type(str(publicPath))
            content_type = content_type or "application/octet-stream"

            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", content_type)
            self.end_headers()

            # Abrimos el archivo en modo binario ('rb') y lo enviamos
            with open(publicPath, "rb") as f:
                self.wfile.write(f.read())
        else:
            print(f"NO ENCONTRADO {publicPath}")

            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Not found")