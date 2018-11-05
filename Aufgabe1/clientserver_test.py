import os
import unittest
import time

import clientserver

class TestEchoService(unittest.TestCase):
    def setUp(self):
        time.sleep(3)
        super().setUp()
        server = clientserver.Server()
        pid = os.fork()
        if pid == 0:
            server.serve()
            os._exit(0)
        self.client = clientserver.Client()

    def test_srv_get(self):
        msg = self.client.get('alice')
        self.assertEqual(msg, 'alice - 8765')

    def test_srv_getAll(self):
        msg = self.client.getAll()
        self.assertEqual(msg, {'natalia': '1234', 'alice': '8765', 'jana': '2921', 'hendrik': '1801'})

    def test_srv_get_wrong_name(self):
        msg = self.client.get('bob')
        self.assertEqual(msg, 'No data found for bob')

if __name__ == '__main__':
    unittest.main()
