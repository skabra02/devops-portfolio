from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []
next_id = 1

def find_task(task_id):
    return next((t for t in tasks if t['id'] == task_id), None)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    return jsonify({"task": task})

@app.route('/tasks', methods=['POST'])
def create_task():
    global next_id
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "title is required"}), 400
    task = {"id": next_id, "title": data['title'], "done": False}
    tasks.append(task)
    next_id += 1
    return jsonify({"task": task}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def replace_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "title and done are required"}), 400
    task['title'] = data['title']
    task['done'] = data.get('done', False)
    return jsonify({"task": task})

@app.route('/tasks/<int:task_id>', methods=['PATCH'])
def update_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    data = request.get_json()
    if 'title' in data:
        task['title'] = data['title']
    if 'done' in data:
        task['done'] = data['done']
    return jsonify({"task": task})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if not task:
        return jsonify({"error": "task not found"}), 404
    tasks.remove(task)
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
