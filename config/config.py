import os

# General Configuration
TRACKER_URL = "http://localhost:5000"

# Peer Configuration
PEER_IP = "127.0.0.1"
PEER_PORT = 6000
SHARED_FOLDER = "shared_files"

# File Chunking Configuration
CHUNK_SIZE = 1024 * 1024  # 1MB

# Ensure shared folder exists
if not os.path.exists(SHARED_FOLDER):
    os.makedirs(SHARED_FOLDER)
