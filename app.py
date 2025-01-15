# app.py

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
)
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Inicializar la aplicación Flask
app = Flask(__name__)

# Configuraciones de la aplicación
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or "una_clave_por_defecto"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL") or "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializar la base de datos
db = SQLAlchemy(app)

# Inicializar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Ruta a la página de inicio de sesión

# Clave de la API de GPT
GPT_API_KEY = os.getenv("GPT_API_KEY")

# =======================
# Modelos de la Base de Datos
# =======================

class User(UserMixin, db.Model):
    """
    Modelo de Usuario que hereda de UserMixin para integrar con Flask-Login.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)  # Nombre de usuario único
    email = db.Column(db.String(120), unique=True, nullable=False)    # Correo electrónico único
    password_hash = db.Column(db.String(128), nullable=False)         # Hash de la contraseña

    # Relación uno a uno con Demographics
    demographics = db.relationship("Demographics", backref="user", uselist=False)

    # Relación uno a muchos con Survey
    surveys = db.relationship("Survey", backref="user", lazy=True)

    def set_password(self, password):
        """
        Establece la contraseña del usuario almacenando su hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        """
        return check_password_hash(self.password_hash, password)


class Demographics(db.Model):
    """
    Modelo de Demografía asociado a un Usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)            # Edad del usuario
    gender = db.Column(db.String(20), nullable=False)      # Género del usuario
    location = db.Column(db.String(100), nullable=False)  # Ubicación del usuario

    # Foreign key para relacionar con el usuario
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Survey(db.Model):
    """
    Modelo de Encuesta asociado a un Usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    soft_skills = db.Column(db.Text, nullable=False)        # Habilidades blandas del usuario
    hard_skills = db.Column(db.Text, nullable=False)        # Habilidades duras del usuario
    profile_analysis = db.Column(db.Text)                   # Análisis de perfil generado por GPT

    # Foreign key para relacionar con el usuario
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


# =======================
# Formularios utilizando Flask-WTF
# =======================

class RegistrationForm(FlaskForm):
    """
    Formulario de Registro de Usuario.
    """
    username = StringField("Usuario", validators=[DataRequired()])
    email = StringField("Correo Electrónico", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    password2 = PasswordField(
        "Repite la Contraseña", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Registrarse")

    def validate_username(self, username):
        """
        Valida que el nombre de usuario no esté ya registrado.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Este nombre de usuario ya está en uso.")

    def validate_email(self, email):
        """
        Valida que el correo electrónico no esté ya registrado.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Este correo electrónico ya está registrado.")


class LoginForm(FlaskForm):
    """
    Formulario de Inicio de Sesión.
    """
    username = StringField("Usuario", validators=[DataRequired()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Iniciar Sesión")


class DemographicsForm(FlaskForm):
    """
    Formulario de Datos Demográficos.
    """
    age = IntegerField("Edad", validators=[DataRequired(), NumberRange(min=18, max=100)])
    gender = SelectField(
        "Género",
        choices=[
            ("Masculino", "Masculino"),
            ("Femenino", "Femenino"),
            ("Otro", "Otro"),
        ],
        validators=[DataRequired()],
    )
    location = StringField("Ubicación", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class SurveyForm(FlaskForm):
    """
    Formulario de Encuesta de Habilidades.
    """
    soft_skills = TextAreaField("Habilidades Blandas", validators=[DataRequired()])
    hard_skills = TextAreaField("Habilidades Duras", validators=[DataRequired()])
    submit = SubmitField("Enviar Encuesta")


# =======================
# Cargar usuario para Flask-Login
# =======================

@login_manager.user_loader
def load_user(user_id):
    """
    Carga un usuario por su ID.
    """
    return User.query.get(int(user_id))


# =======================
# Rutas de la Aplicación
# =======================

@app.route("/")
def index():
    """
    Ruta para la página de inicio.
    """
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Ruta para el registro de nuevos usuarios.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        # Crear un nuevo usuario con los datos del formulario
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Establecer la contraseña con hash
        db.session.add(user)                     # Agregar el usuario a la sesión
        db.session.commit()                      # Guardar los cambios en la base de datos
        flash("¡Te has registrado exitosamente! Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))        # Redirigir al formulario de inicio de sesión
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Ruta para el inicio de sesión de usuarios.
    """
    form = LoginForm()
    if form.validate_on_submit():
        # Buscar al usuario por nombre de usuario
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Iniciar sesión del usuario
            login_user(user)
            flash("Has iniciado sesión correctamente.", "success")
            next_page = request.args.get("next")  # Obtener la siguiente página si existe
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    """
    Ruta para cerrar la sesión del usuario.
    """
    logout_user()
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("index"))


@app.route("/demographics", methods=["GET", "POST"])
@login_required
def demographics():
    """
    Ruta para el formulario de datos demográficos.
    """
    form = DemographicsForm()
    if form.validate_on_submit():
        # Crear una instancia de Demographics con los datos del formulario
        demographics = Demographics(
            age=form.age.data,
            gender=form.gender.data,
            location=form.location.data,
            user=current_user,  # Asociar con el usuario actual
        )
        db.session.add(demographics)  # Agregar a la sesión
        db.session.commit()           # Guardar en la base de datos
        flash("Datos demográficos guardados.", "success")
        return redirect(url_for("survey"))  # Redirigir al formulario de encuesta
    return render_template("demographics.html", form=form)


@app.route("/survey", methods=["GET", "POST"])
@login_required
def survey():
    """
    Ruta para el formulario de encuesta de habilidades.
    """
    form = SurveyForm()
    if form.validate_on_submit():
        # Crear una instancia de Survey con los datos del formulario
        survey = Survey(
            soft_skills=form.soft_skills.data,
            hard_skills=form.hard_skills.data,
            user=current_user,  # Asociar con el usuario actual
        )
        db.session.add(survey)  # Agregar a la sesión
        db.session.commit()      # Guardar en la base de datos
        flash("Encuesta completada.", "success")

        # Llamar a la función para analizar el perfil utilizando la API de GPT
        analysis = analyze_profile(current_user)
        survey.profile_analysis = analysis  # Almacenar el análisis en la encuesta
        db.session.commit()                  # Actualizar la base de datos

        flash("Perfil analizado.", "info")
        return redirect(url_for("dashboard"))
    return render_template("survey.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    """
    Ruta para el dashboard del usuario.
    Muestra el análisis del perfil más reciente.
    """
    # Obtener todas las encuestas del usuario
    surveys = Survey.query.filter_by(user_id=current_user.id).all()

    # Obtener la encuesta más reciente si existe
    latest_survey = surveys[-1] if surveys else None

    return render_template("dashboard.html", survey=latest_survey)


def analyze_profile(user):
    """
    Función para analizar el perfil del usuario utilizando la API de Chat GPT.
    """
    demographics = user.demographics
    survey = user.surveys[-1] if user.surveys else None

    if not demographics or not survey:
        return "Datos insuficientes para el análisis del perfil."

    # Crear el prompt para la API de Chat GPT
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"""
            Analiza el perfil del siguiente usuario basado en sus datos demográficos y habilidades:

            Edad: {demographics.age}
            Género: {demographics.gender}
            Ubicación: {demographics.location}
            Habilidades Blandas: {survey.soft_skills}
            Habilidades Duras: {survey.hard_skills}

            Proporciona un resumen detallado del perfil del usuario.
            """
        }
    ]

    headers = {
        "Authorization": f"Bearer {GPT_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "gpt-4o-mini",  # Cambia a "gpt-4" si tienes acceso
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7,
    }

    try:
        # Realizar la solicitud POST a la API de OpenAI
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()  # Lanza una excepción si la respuesta tiene un error HTTP
        analysis_text = response.json()["choices"][0]["message"]["content"].strip()
        return analysis_text
    except requests.exceptions.RequestException as e:
        # Manejar errores de la solicitud
        print(f"Error al llamar a la API de GPT: {e}")
        return "Error en el análisis del perfil."

# =======================
# Ejecutar la Aplicación
# =======================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crear tablas en la base de datos si no existen
    app.run(debug=True)
