from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from models.task import Task
from sqlalchemy.ext.declarative import declarative_base
from models import db

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gabrielfers:12345@localhost/taskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

Task=Task

# Criação do banco de dados
with app.app_context():
    print("Criando banco de dados...")
    db.create_all()

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        new_task = Task(title=data['title'], description=data.get("description", ""))
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"Message": "Nova tarefa criada com sucesso"}), 201
    except KeyError:
        return jsonify({"Message": "Erro ao criar nova tarefa"}), 400

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "total_tasks": len(tasks)
    }
    return jsonify(output), 200

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify(task.to_dict()), 200
    return jsonify({"Message": "Tarefa não encontrada"}), 404

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)
    if task:
        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.completed = data.get("completed", task.completed)
        db.session.commit()
        return jsonify({"Message": "Tarefa atualizada com sucesso"}), 200
    return jsonify({"Message": "Tarefa não encontrada"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"Message": "Tarefa removida com sucesso"}), 200
    return jsonify({"Message": "Tarefa não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)

