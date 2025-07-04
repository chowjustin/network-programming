import socket
import base64
import json
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

def post_comment():
    host = 'jsonplaceholder.typicode.com'
    port = 80
    path = '/comments'
    
    comment = {
        "postId": 1,
        "name": "Test Name",
        "email": "test@example.com",
        "body": "This is a test comment."
    }
    body = json.dumps(comment)
    content_length = len(body)
    
    request = (
        f"POST {path} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        f"Content-Type: application/json\r\n"
        f"Content-Length: {content_length}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
        f"{body}"
    )

    id = ""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(request.encode())

        chunk = s.recv(4096).decode()
        raw_response = json.loads(chunk.split("\r\n")[3])
        res_id = raw_response["id"]
        id = res_id
        
    return id


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestCommentPoster(unittest.TestCase):
    @patch('socket.socket')
    def test_post_comment(self, mock_socket):
        # Setup the mock socket
        mock_socket_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_socket_instance
        
        # Define a fake response to be returned by socket.recv
        fake_response = "HTTP/1.1 201 Created\r\nContent-Type: application/json\r\n\r\n{\"id\": 101, \"name\": \"Test Name\"}"
        mock_socket_instance.recv.return_value = fake_response.encode()

        # Call the function
        comment_id = post_comment()

        # Verify that the socket methods were called correctly
        mock_socket_instance.connect.assert_called_with(('jsonplaceholder.typicode.com', 80))
        print(f"connect called with: {mock_socket_instance.connect.call_args}")

        mock_socket_instance.send.assert_called_once()
        print(f"send called with: {mock_socket_instance.send.call_args}")

        mock_socket_instance.recv.assert_called_once()
        print(f"recv called with: {mock_socket_instance.recv.call_args}")

        assert_equal(comment_id, 101)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        comment_id = post_comment()
        print(comment_id)

   # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
