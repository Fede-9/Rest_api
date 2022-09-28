from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/rest_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id','title','description')

# cuando sea una sola tarea trabajo con este
task_schema = TaskSchema()
# cuando son muchas tareas trabajo con este
tasks_schema = TaskSchema(many=True)

# crear las tareas
@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    
    new_task = Task(title, description)
    db.session.add(new_task)
    db.session.commit()

    # le respondemos al cliente para que vea lo que ha creado
    return task_schema.jsonify(new_task)

# mostrar la lista de tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    # aca obtengo una lista de datos
    result = tasks_schema.dump(all_tasks)

    return jsonify(result)


# consultar tareas
@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

# actualizar tarea
@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']
    
    # le asigno los nuevos datos
    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)



# eliminar tareas
@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)


@app.route('/')
def index():
    return jsonify({'message': 'Bienvenido a mi API'})

if __name__ == '__main__':
    app.run(debug=True)