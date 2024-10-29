#app/__init__.py
from flask import Flask
from flask_jwt_extended import JWTManager
from app.editoriales.routes import editorialesBP
from app.libros.routes import librosBP
from app.users.routes import usuariosBP
#INICIALOZACION JWTManager
app =  Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'a1b2c3d4e5f678901234567890abcdef'   
jwt = JWTManager(app)

#IMPORTS BLUE PRINT 
app.register_blueprint(editorialesBP,url_prefix="/editoriales")
app.register_blueprint(librosBP,url_prefix="/editoriales/<int:editorial_id>/libros")
app.register_blueprint(usuariosBP, url_prefix="/usuarios")