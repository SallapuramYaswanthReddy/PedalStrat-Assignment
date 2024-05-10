from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration for SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"Task('{self.title}', '{self.description}', '{self.due_date}')"

# Create database tables
db.create_all()

# Routes for CRUD operations

# Retrieve all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_json = [{'id': task.id, 'title': task.title, 'description': task.description, 'due_date': task.due_date} for task in tasks]
    return jsonify(tasks_json)

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(title=data['title'], description=data['description'], due_date=data['due_date'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description, 'due_date': new_task.due_date}), 201

# Retrieve a single task by its ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'due_date': task.due_date})
    else:
        return jsonify({'message': 'Task not found'}), 404

# Update an existing task
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        data = request.json
        task.title = data['title']
        task.description = data['description']
        task.due_date = data['due_date']
        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'due_date': task.due_date})
    else:
        return jsonify({'message': 'Task not found'}), 404

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'message': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
