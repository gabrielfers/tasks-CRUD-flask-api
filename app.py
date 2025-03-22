from flask import Flask, request, jsonify
from models.Task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        global task_id_control
        data = request.get_json()
        new_task = Task(id=task_id_control, title=data['title'], description=data.get("description", ""))
        task_id_control += 1
        tasks.append(new_task)
        return jsonify({"Message": "Nova tarefa criada com sucesso"})
    except KeyError:
        return jsonify({"Message": "Erro ao criar nova tarefa"}), 400
    
@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    
    output = {
        "tasks": task_list,
        "total_tasks": len(tasks)
    }
    return jsonify(output)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    for task in tasks:
        if task.id == task_id:
            return jsonify(task.to_dict())
    return jsonify({"Message": "Tarefa não encontrada"}), 404

@app.route('/tasks/<int:task_id_update>', methods=['PUT'])
def update_task(task_id_update):
    data = request.get_json()
    for task in tasks:
        if task.id == task_id_update:
            task.title = data.get("title", task.title)
            task.description = data.get("description", task.description)
            task.completed = data.get("completed", task.completed)
            return jsonify({"Message": "Tarefa atualizada com sucesso"})
    return jsonify({"Message": "Tarefa não encontrada"}), 404
    
@app.route('/tasks/<int:task_id_delete>', methods=['DELETE'])
def delete_task(task_id_delete):
    for task in tasks:
        if task.id == task_id_delete:
            tasks.remove(task)
            return jsonify({"Message": "Tarefa removida com sucesso"})
    return jsonify({"Message": "Tarefa não encontrada"}), 404
    
if __name__ == '__main__':
    app.run(debug=True)

