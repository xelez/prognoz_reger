from reger import root_app
from paste.httpserver import serve
from paste import reloader

reloader.install()
serve(root_app, host='0.0.0.0', port=8081)
