import sys
import subprocess
from gevent.pywsgi import WSGIServer


def http_response(status_code, content, start_response):
    start_response(status_code, [('Content-Type', 'text/html; charset=utf-8')])

    return [str(content).encode('utf-8')] if content else []


class App(object):
    def __init__(self):
        self.called = 0

    def handle(self, env, start_response):
        if env['PATH_INFO'] == '/':
            self.called += 1
            return http_response('200 OK', 'hi', start_response)
        if env['PATH_INFO'] == '/count':
            return http_response('200 OK', self.called, start_response)
        if env['PATH_INFO'] == '/method':
            return http_response('200 OK', env['REQUEST_METHOD'], start_response)
        if env['PATH_INFO'] == '/redirect':
            return http_response('302 FOUND', [], start_response)
        if env['PATH_INFO'] == '/reset':
            self.called = 0
            return http_response('200 OK', 'done', start_response)
        if env['PATH_INFO'] == '/cookie':
            cookie = env.get('HTTP_COOKIE')
            return http_response('200 OK', str(cookie), start_response)
        if env['PATH_INFO'] == '/header':
            return http_response('200 OK',
                                 '<br>'.join(["{}={}".format(i, env[i]) for i in env if i.startswith('HTTP')]),
                                 start_response)
        return http_response('404 Not Found', 'you are visiting' + env['PATH_INFO'], start_response)


def run_test_app():
    app = App()
    server = WSGIServer(('0.0.0.0', 23333), app.handle)
    server.serve_forever()


def start():
    return subprocess.Popen(
        [sys.executable, '-c', 'from tests.web_app import run_test_app; run_test_app()'])


if __name__ == "__main__":
    run_test_app()
