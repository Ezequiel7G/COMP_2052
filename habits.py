from flask import Flask, jsonify, request

app = Flask(__name__)

habits = [

    {
        "id": 1,
        "name": "Hacer ejercicio",
        "frequency": "daily",
    },
    {
        "id": 2,
        "name": "Dormir 8 horas",
        "frequency": "daily",
    },
    {
        "id": 3,
        "name": "Estudiar 2 horas",
        "frequency": "daily",
    }
]


next_id = 4


@app.route('/api/v1/habits', methods=['GET'])
def list_habits():
    return jsonify(habits), 200


@app.route('/api/v1/habits', methods=['POST'])
def create_habit():

    global next_id
    data = request.get_json()
    if not data or 'name' not in data or 'frequency' not in data:
        return jsonify({"error": "Falta 'name' o 'frequency'"}), 400

    habit = {
        "id": next_id,
        "name": data['name'],
        "frequency": data['frequency'],

    }
    next_id += 1
    habits.append(habit)

    return jsonify(habit), 201


if __name__ == '__main__':
    app.run(debug=True)
