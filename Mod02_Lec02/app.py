from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'


class RegistrationForm(FlaskForm):
    nombre = StringField(
        'Nombre',
        validators=[
            DataRequired(message='El nombre es obligatorio.'),
            Length(min=3, message='El nombre debe tener al menos 3 caracteres.')
        ]
    )
    correo = StringField(
        'Correo',
        validators=[
            DataRequired(message='El correo electrónico es obligatorio.'),
            Email(message='Ingrese un correo electrónico válido.')
        ]
    )
    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(message='La contraseña es obligatoria.'),
            Length(min=6, message='La contraseña debe tener al menos 6 caracteres.')
        ]
    )
    submit = SubmitField('Registrarse')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        flash(f"Usuario {form.nombre.data} registrado con éxito.", 'success')
        return redirect(url_for('register'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
