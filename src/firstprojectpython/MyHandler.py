from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
import os
from .DBConnection import DBConnection
from .templates import city_template
from pathlib import Path
import mimetypes

def render(file: str, vars):
    project_dir = Path.cwd()
    ft = os.path.join(project_dir, "templates", file + ".html")
    ft_contents = open(ft).read()
    for x in vars:
        ft_contents = ft_contents.replace("{" + x + "}", vars[x])
    return ft_contents

class MyHandler(BaseHTTPRequestHandler):
    db_connection: DBConnection
    project_dir: Path

    def __init__(self, *args, **kwargs):
        self.db_connection = DBConnection()
        self.project_dir = Path.cwd()
        # Pasamos *args y **kwargs hacia la clase padre para que el servidor no falle
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        if self.path == '/':
            data = self.db_connection.retrieve_cities()
            
            list_cities = render("cities", {
                'cities': f"<ul>{''.join(city_template(c) for c in data)}</ul>"
            })

            content = render("layout", {
                'content': list_cities
            })

            self.send_response(HTTPStatus.OK)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            # self.wfile.write(f"{html_template(list_cities)}".encode('utf-8'))
            return
        
        self._lookForFile()

    def _lookForFile(self):
        # Limpiamos el self.path para quitarle la barra inicial '/' si la tiene, 
        # ya que si empieza por '/' Path lo interpretará como ruta absoluta y pisará __dirname.
        clean_path = self.path.lstrip('/')
        
        # Unimos usando el operador / de pathlib
        publicPath = self.project_dir / os.path.join("public", clean_path)
        
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