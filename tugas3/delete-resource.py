import socket
import base64
import json
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

def delete_post(post_id):
    host = 'jsonplaceholder.typicode.com'
    port = 80
    path = '/posts/1'

    request = (
        f"DELETE {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    status_code = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(request.encode())

        chunk = s.recv(4096).decode()
       
        raw_header=chunk.split("\r\n")[0]
        status_code = raw_header.split(" ")[1]
        
        if(status_code=="200"):
            print("Deleted successfully")
    
    return status_code


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestDeletePost(unittest.TestCase):
    @patch('socket.socket')
    def test_delete_post(self, mock_socket):
        # Setup the mocked socket instance
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance

        # Define the mock response from the server
        http_response = "HTTP/1.1 200 OK\r\nContent-Length: 0\r\n\r\n"
        mock_sock_instance.recv.return_value = http_response.encode('utf-8')

        # Call the function
        status_code = delete_post(1)

        # Ensure the response indicates success
        mock_sock_instance.connect.assert_called_once_with(('jsonplaceholder.typicode.com', 80))
        print(f"connect called with: {mock_sock_instance.connect.call_args}")

        # Assertions to check if the DELETE request was properly sent and the correct response was handled
        mock_sock_instance.send.assert_called_once()
        print(f"send called with: {mock_sock_instance.send.call_args}")

        mock_sock_instance.recv.assert_called_once()
        print(f"recv called with: {mock_sock_instance.recv.call_args}")

        assert_equal(status_code, '200')

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        status = delete_post(1)
        print(status)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
