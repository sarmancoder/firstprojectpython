from http.server import HTTPServer

from .MyHandler import MyHandler

def main() -> None:
    print("Hello from firstprojectpython!")

    SERVER_PORT = 8080

    httpd = HTTPServer(('', SERVER_PORT), MyHandler)
    print(f'App serving on {SERVER_PORT}')
    httpd.serve_forever()

