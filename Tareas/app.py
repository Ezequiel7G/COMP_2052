from flask import Flask, render_template

app = Flask(__name__)


tareas = [
    "Estudiar Precalculo",
    "Estudiar Bases de Datos",
    "Practicar Python"
]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/tareas')
def ver_tareas():
    return render_template('tareas.html', tareas=tareas)


if __name__ == '__main__':
    app.run(debug=True)
