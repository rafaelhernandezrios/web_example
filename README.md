# Proyecto de Análisis de Perfiles con Flask y OpenAI

Este proyecto es una aplicación web basada en Flask que permite a los usuarios:

1. Registrarse e iniciar sesión.
2. Completar un formulario de datos demográficos.
3. Responder una encuesta sobre habilidades blandas y duras.
4. Analizar su perfil mediante la API de OpenAI.
5. Ver un análisis del perfil en un dashboard.

El proyecto está diseñado como una introducción para estudiantes interesados en desarrollo web y puede escalarse a aplicaciones más complejas.

---

## **Requisitos Previos**

Asegúrate de tener instalados los siguientes programas:

- **Python 3.9 o superior**
- **pip** (Administrador de paquetes de Python)
- **Git** (Opcional, para clonar el repositorio)

Además, necesitas una clave de la API de OpenAI. Puedes obtenerla registrándote en [OpenAI](https://platform.openai.com/signup/).

---

## **Instalación del Proyecto**

Sigue estos pasos para configurar el proyecto localmente:

1. **Clonar el Repositorio:**

   Si estás utilizando Git, clona el repositorio:

   ```bash
   git clone https://github.com/rafaelhernandezrios/web_example/
   cd web_example
   ```

2. **Crear un Entorno Virtual:**

   Crea y activa un entorno virtual para evitar conflictos entre dependencias.

   - **En macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

   - **En Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instalar Dependencias:**

   Instala las dependencias requeridas desde el archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno:**

   Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes variables:

   ```plaintext
   SECRET_KEY=una_clave_secreta_segura
   DATABASE_URL=sqlite:///site.db
   GPT_API_KEY=tu_clave_api_de_openai
   ```

   - Genera una clave secreta segura con:
     ```python
     import secrets
     print(secrets.token_hex(16))
     ```

5. **Inicializar la Base de Datos:**

   Ejecuta el siguiente comando para crear las tablas en la base de datos:

   ```bash
   python app.py
   ```

   Esto también iniciará el servidor.

6. **Acceder a la Aplicación:**

   Abre un navegador y visita:

   ```plaintext
   http://localhost:5000/
   ```

---

## **Estructura del Proyecto**

```
proyecto-flask/
|   app.py             # Archivo principal de la aplicación
|   requirements.txt  # Dependencias del proyecto
|   .env              # Variables de entorno (no subir a GitHub)
|   templates/       # Plantillas HTML
|   static/          # Archivos estáticos (CSS, imágenes, JS)
|     styles.css   # Archivo CSS para diseño
|   README.md         # Documentación del proyecto
```

---

## **Instrucciones para Escalar el Proyecto**

### **1. Agregar Nuevas Vistas**

1. Crea un nuevo archivo HTML en la carpeta `templates/` con el diseño deseado.

   Por ejemplo, `nueva_vista.html`:
   ```html
   {% extends "base.html" %}

   {% block content %}
   <h1>Mi Nueva Vista</h1>
   <p>Esta es una nueva página.</p>
   {% endblock %}
   ```

2. Define una nueva ruta en `app.py`:

   ```python
   @app.route("/nueva-vista")
   def nueva_vista():
       return render_template("nueva_vista.html")
   ```

3. Reinicia el servidor y accede a `http://localhost:5000/nueva-vista`.

---

### **2. Modificar Diseños en CSS**

El archivo `styles.css` en la carpeta `static/` contiene el diseño de la aplicación.

- Abre `static/styles.css` en un editor de texto.
- Realiza cambios en las clases o agrega nuevas.

Ejemplo:
```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f9;
    color: #333;
}

h1 {
    color: #800020; /* Cambiar a guinda */
}
```
- Guarda los cambios y recarga el navegador para ver el nuevo diseño.

---

### **3. Conectar una Base de Datos Diferente**

El proyecto utiliza SQLite por defecto, pero puedes cambiar a otra base de datos (como PostgreSQL o MySQL).

1. Actualiza la variable `DATABASE_URL` en el archivo `.env`. Ejemplo para PostgreSQL:
   ```plaintext
   DATABASE_URL=postgresql://usuario:contraseña@localhost/nombre_base_datos
   ```

2. Instala el controlador necesario:
   ```bash
   pip install psycopg2
   ```

3. Aplica las migraciones necesarias (si estás usando Flask-Migrate).

---

### **4. Integrar APIs Adicionales**

Puedes agregar otras APIs siguiendo el modelo utilizado para OpenAI. Por ejemplo:

1. Instala la biblioteca de la API.
2. Configura las claves en `.env`.
3. Define funciones para llamar a la API y mostrar los resultados en una nueva vista.

---

### **5. Crear Formularios Adicionales**

1. Define un nuevo formulario en `app.py` utilizando Flask-WTF:

   ```python
   class NuevoFormulario(FlaskForm):
       campo = StringField("Campo", validators=[DataRequired()])
       submit = SubmitField("Enviar")
   ```

2. Agrega una ruta para manejar el formulario:

   ```python
   @app.route("/nuevo-formulario", methods=["GET", "POST"])
   def nuevo_formulario():
       form = NuevoFormulario()
       if form.validate_on_submit():
           # Procesar los datos del formulario
           return redirect(url_for("index"))
       return render_template("nuevo_formulario.html", form=form)
   ```

3. Crea el archivo `nuevo_formulario.html` en `templates/` para el diseño del formulario.

---

### **6. Desplegar en Producción**

Para desplegar la aplicación en un servidor como Heroku o PythonAnywhere:

1. Instala las herramientas necesarias (por ejemplo, `gunicorn` para Heroku):
   ```bash
   pip install gunicorn
   ```

2. Crea un archivo `Procfile` con el siguiente contenido:
   ```plaintext
   web: gunicorn app:app
   ```

3. Sigue la documentación del proveedor para configurar y desplegar la aplicación.

---

## **Recursos Adicionales**

- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Documentación de Flask-WTF](https://flask-wtf.readthedocs.io/)
- [Documentación de OpenAI](https://platform.openai.com/docs/)
- [Tutorial Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

---

## **Conclusión**

Este proyecto sirve como base para aprender los fundamentos del desarrollo web con Flask. Puedes personalizarlo, escalarlo y adaptarlo a tus necesidades para construir aplicaciones web más complejas. ¡Explora, experimenta y diviértete programando!
"# web_example" 
