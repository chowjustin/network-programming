import socket
import base64
import json
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO


def fetch_post_title():
    host = 'jsonplaceholder.typicode.com'
    port = 80
    path = '/posts/1'

    request = (
        f"GET {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    clean_title = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(request.encode())

        chunk = s.recv(4096)
        decoded_chunks = chunk.decode()
        title = decoded_chunks.split("\r\n\r\n")[1]
        title_json = json.loads(title)
        clean_title = title_json["title"]
        
    return clean_title


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestHttpRequest(unittest.TestCase):
    @patch('socket.socket')
    def test_fetch_post_title(self, mock_socket):
        # Setup mock
        sample_response = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"title\": \"sunt aut facere repellat provident occaecati excepturi optio reprehenderit\"}"
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        mock_sock_instance.recv.return_value = sample_response.encode()

        # Call function
        title = fetch_post_title()

        # Assertions
        mock_socket.assert_called_once()
        mock_sock_instance.connect.assert_called_with(('jsonplaceholder.typicode.com', 80))
        print(f"connect called with: {mock_sock_instance.connect.call_args}")

        mock_sock_instance.send.assert_called_once()
        print(f"send called with: {mock_sock_instance.send.call_args}")

        mock_sock_instance.recv.assert_called_once()
        print(f"recv called with: {mock_sock_instance.recv.call_args}")

        assert_equal(title, "sunt aut facere repellat provident occaecati excepturi optio reprehenderit")


if __name__ == '__main__':
    # to run the script without unit test:
    # python solution.py run
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        title = fetch_post_title()
        print(title)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)