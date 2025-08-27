from server import Server
from socket import AF_INET, SOCK_STREAM
import pytest

@pytest.fixture
def mock_server_env(mocker):
    """
    Sets up a mocked Server environment.
    Returns a dictionary with the Server instance and key mocks.
    """
    # Patch socket.socket and get its mock instance
    mock_socket_class = mocker.patch('socket.socket')
    mock_socket_instance = mock_socket_class.return_value

    # Mock client socket and configure accept() and recv()
    mock_client_socket = mocker.MagicMock()
    mock_socket_instance.accept.return_value = (mock_client_socket, ('127.0.0.1', 5000))
    mock_client_socket.recv.return_value = b'GET / HTTP/1.1\r\nHost: localhost\r\n\r\n'

    # Instantiate Server and patch loop_controller
    server = Server()
    mocker.patch.object(server, 'loop_controller', side_effect=[True, False])

    return {
        "server": server,
        "mock_socket_class": mock_socket_class,
        "mock_socket_instance": mock_socket_instance,
        "mock_client_socket": mock_client_socket,
    }

def test_start(mock_server_env):
    """Validates Server.start() behavior."""
    server = mock_server_env["server"]
    socket_cls = mock_server_env["mock_socket_class"]
    socket_inst = mock_server_env["mock_socket_instance"]
    client_socket = mock_server_env["mock_client_socket"]

    server.start()

    socket_cls.assert_called_once_with(AF_INET, SOCK_STREAM)
    socket_inst.accept.assert_called_once()
    client_socket.sendall.assert_called_once()
    client_socket.close.assert_called_once()

def test_stop(mock_server_env):
    """Validates Server.stop() behavior."""
    server = mock_server_env["server"]
    socket_cls = mock_server_env["mock_socket_class"]
    socket_inst = mock_server_env["mock_socket_instance"]

    server.start()
    server.stop()

    socket_cls.assert_called_once_with(AF_INET, SOCK_STREAM)
    socket_inst.close.assert_called_once()