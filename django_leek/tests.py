import base64
import pickle
from unittest.mock import patch, MagicMock
import socketserver
from functools import partial

from django.test import TestCase
from django.core.management import call_command

from django_leek.server import TaskSocketServer
from django_leek import helpers


@patch.object(socketserver.TCPServer, 'serve_forever')
class LeekCommandTestCase(TestCase):
    def test_leek(self, serve_forever):
        call_command('leek')
        serve_forever.assert_called_with()

    def test_keyboard_interrupt(self, serve_forever):
        serve_forever.side_effect = KeyboardInterrupt
        call_command('leek')

def f():
    pass

class TestServer(TestCase):
    def setUp(self):
        self.request = MagicMock()

    def _request(self, data):
        if isinstance(data, Exception):
            self.request.recv.side_effect = data
        else:
            self.request.recv.return_value = data

    def _response(self):
        return b''.join(call[0][0] for call in self.request.send.call_args_list)

    def act(self):
        TaskSocketServer(self.request, 'client adress', 'server')

    def test_recv_error(self):
        self._request(OSError('Nuclear Winter'))        
        self.act()
