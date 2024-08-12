from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'id': new_task.id, 'title': new_task.title, 'completed': new_task.completed})

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    data = request.get_json()
    task = Task.query.get(id)
    if task:
        task.title = data['title']
        task.completed = data['completed']
        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted'})
    return jsonify({'error': 'Task not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
