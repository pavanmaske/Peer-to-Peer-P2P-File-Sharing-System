import os

CHUNK_SIZE = 1024 * 1024  # 1MB

def split_file(filename, output_folder):
    """ Splits a file into chunks """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(filename, "rb") as f:
        chunk_id = 0
        while chunk := f.read(CHUNK_SIZE):
            chunk_path = os.path.join(output_folder, f"{filename}.part{chunk_id}")
            with open(chunk_path, "wb") as chunk_file:
                chunk_file.write(chunk)
            chunk_id += 1

def merge_chunks(filename, input_folder, chunk_count):
    """ Merges chunks into a single file """
    with open(filename, "wb") as output_file:
        for chunk_id in range(chunk_count):
            chunk_path = os.path.join(input_folder, f"{filename}.part{chunk_id}")
            if os.path.exists(chunk_path):
                with open(chunk_path, "rb") as chunk_file:
                    output_file.write(chunk_file.read())
