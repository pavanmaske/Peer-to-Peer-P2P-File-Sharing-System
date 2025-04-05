import os
from peer.utils import split_file, merge_chunks

TEST_FILE = "test_file.txt"
CHUNK_FOLDER = "test_chunks"

def setup_module():
    """Creates a test file before running tests"""
    with open(TEST_FILE, "wb") as f:
        f.write(b"A" * 1024 * 1024 * 3)  # 3MB file

def teardown_module():
    """Cleans up test files after tests"""
    os.remove(TEST_FILE)
    for file in os.listdir(CHUNK_FOLDER):
        os.remove(os.path.join(CHUNK_FOLDER, file))
    os.rmdir(CHUNK_FOLDER)

def test_split_file():
    """Tests if file is correctly split into chunks"""
    split_file(TEST_FILE, CHUNK_FOLDER)
    chunks = os.listdir(CHUNK_FOLDER)
    assert len(chunks) == 3  # 3MB file should create 3 chunks

def test_merge_chunks():
    """Tests if chunks can be merged back into the original file"""
    merge_chunks("merged_test_file.txt", CHUNK_FOLDER, 3)
    assert os.path.exists("merged_test_file.txt")
    assert os.path.getsize("merged_test_file.txt") == 1024 * 1024 * 3  # 3MB
    os.remove("merged_test_file.txt")
