from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store peer information { "filename": ["peer1_ip", "peer2_ip"] }
peer_registry = {}

@app.route('/register', methods=['POST'])
def register_peer():
    """
    Registers a peer along with the file it is sharing.
    Expects JSON: {"peer_ip": "192.168.1.2", "filename": "example.txt"}
    """
    data = request.json
    peer_ip = data.get('peer_ip')
    filename = data.get('filename')

    if not peer_ip or not filename:
        return jsonify({"error": "Invalid request, missing peer_ip or filename"}), 400

    if filename not in peer_registry:
        peer_registry[filename] = []

    if peer_ip not in peer_registry[filename]:
        peer_registry[filename].append(peer_ip)

    return jsonify({"message": "Peer registered successfully", "peers": peer_registry[filename]}), 200


@app.route('/get_peers', methods=['GET'])
def get_peers():
    """
    Returns a list of peers sharing a requested file.
    Expects query param: ?filename=example.txt
    """
    filename = request.args.get('filename')

    if not filename or filename not in peer_registry:
        return jsonify({"error": "File not found"}), 404

    return jsonify({"peers": peer_registry[filename]}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
