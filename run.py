import threading

from server import serve_pages
from web_socket_server import start_server

threading.Thread(target=start_server).start()
serve_pages()
