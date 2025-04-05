import requests
import pytest

TRACKER_URL = "http://localhost:5000"

@pytest.fixture
def register_peer():
    """Registers a test peer before running tests"""
    data = {"peer_ip": "127.0.0.1", "filename": "testfile.txt"}
    response = requests.post(f"{TRACKER_URL}/register", json=data)
    assert response.status_code == 200

def test_register_peer(register_peer):
    """Tests if peer registration is successful"""
    response = requests.get(f"{TRACKER_URL}/get_peers", params={"filename": "testfile.txt"})
    assert response.status_code == 200
    assert "peers" in response.json()
    assert "127.0.0.1" in response.json()["peers"]

def test_invalid_file_request():
    """Tests retrieving peers for a non-existent file"""
    response = requests.get(f"{TRACKER_URL}/get_peers", params={"filename": "non_existent.txt"})
    assert response.status_code == 404
