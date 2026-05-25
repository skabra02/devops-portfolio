from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
next_id = 1

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json()

    if not data or 'title' not in data:
        return jsonify({"error": "title is required"}), 400

    task = {
        "id": next_id,
        "title": data['title'],
        "done": False
    }
    tasks.append(task)
    next_id += 1

    return jsonify({"task": task}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
