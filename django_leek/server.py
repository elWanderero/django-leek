import logging
import socketserver
import threading

from . import worker_manager


log = logging.getLogger(__name__)


Dcommands = {
    'ping': worker_manager.ping,
    'waiting': worker_manager.waiting,
    'handled': worker_manager.hanled,
    'stop': worker_manager.stop
}


class TaskSocketServer(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            data = self.request.recv(5000).strip()
            if data in Dcommands.keys():
                try:
                    worker_response = Dcommands[data]()
                    if worker_response == 'Worker Off':
                        response = (False, worker_response.encode())
                    else:
                        response = (True, worker_response.encode(),)
                    self.request.send(str(response).encode())
                except Exception as e:
                    response =  (False, "TaskServer Command: {}".format(e).encode(),)
                    self.request.send(str(response).encode())
            else:
                # assume a serialized task
                try:
                    response = worker_manager.put_task(data)
                    self.request.send(str(response).encode())
                except Exception as e:
                    response = (False, "TaskServer Put: {}".format(e).encode(),)
                    self.request.send(str(response).encode())

        except OSError as e:
            # in case of network error, just log
            log.exception("network error")
