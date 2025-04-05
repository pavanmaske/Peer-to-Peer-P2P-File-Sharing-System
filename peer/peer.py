import socket
import threading
import requests
import os
import sys
from utils import split_file, merge_chunks

TRACKER_URL = "http://localhost:5000"

class Peer:
    def __init__(self, peer_ip, port, shared_folder):
        self.peer_ip = peer_ip
        self.port = port
        self.shared_folder = shared_folder

    def register_with_tracker(self, filename):
        """ Registers this peer with the tracker """
        data = {"peer_ip": self.peer_ip, "filename": filename}
        response = requests.post(f"{TRACKER_URL}/register", json=data)
        print(response.json())

    def get_peers_for_file(self, filename):
        """ Fetches a list of peers that have the requested file """
        response = requests.get(f"{TRACKER_URL}/get_peers", params={"filename": filename})
        return response.json().get("peers", [])

    def send_file_chunk(self, conn, filename, chunk_id):
        """ Sends a requested file chunk to a connected peer """
        chunk_path = os.path.join(self.shared_folder, f"{filename}.part{chunk_id}")
        if os.path.exists(chunk_path):
            with open(chunk_path, "rb") as f:
                conn.sendall(f.read())
        conn.close()

    def handle_peer_request(self, conn):
        """ Handles incoming requests from other peers """
        data = conn.recv(1024).decode()
        filename, chunk_id = data.split("|")
        self.send_file_chunk(conn, filename, chunk_id)

    def start_peer_server(self):
        """ Starts the peer server to accept file requests from other peers """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.peer_ip, self.port))
        server.listen(5)
        print(f"Peer server started at {self.peer_ip}:{self.port}")

        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.handle_peer_request, args=(conn,)).start()

    def download_file(self, filename):
        """ Downloads a file from available peers """
        peers = self.get_peers_for_file(filename)
        if not peers:
            print("No peers available for this file.")
            return

        chunk_count = 4  # Assume 4 chunks for simplicity
        for chunk_id in range(chunk_count):
            peer_ip = peers[chunk_id % len(peers)]  # Distribute load across peers
            self.request_chunk_from_peer(peer_ip, filename, chunk_id)

        merge_chunks(filename, self.shared_folder, chunk_count)

    def request_chunk_from_peer(self, peer_ip, filename, chunk_id):
        """ Requests a specific file chunk from a peer """
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_ip, self.port))
            peer_socket.send(f"{filename}|{chunk_id}".encode())

            chunk_path = os.path.join(self.shared_folder, f"{filename}.part{chunk_id}")
            with open(chunk_path, "wb") as f:
                while chunk := peer_socket.recv(4096):
                    f.write(chunk)

            peer_socket.close()
        except Exception as e:
            print(f"Failed to download chunk {chunk_id} from {peer_ip}: {e}")

if __name__ == "__main__":
    peer = Peer("127.0.0.1", 6000, "shared_files")
    threading.Thread(target=peer.start_peer_server).start()
    peer.register_with_tracker("example.txt")
    peer.download_file("example.txt")
