from flask import Flask, jsonify
app = Flask(__name__)
tasks = []
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
