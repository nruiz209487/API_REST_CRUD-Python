# app/editoriales/routes.py
from flask import Blueprint,jsonify,request
from .data import editoriales
from flask_jwt_extended import jwt_required


editorialesBP = Blueprint('editoriales',__name__)



# Función para encontrar el siguiente ID disponible para editoriales
def __find_next_id():
    return max(editorial['Id'] for editorial in editoriales) + 1 if editoriales else 1

# Obtener todas las editoriales
@editorialesBP.get("/")
@jwt_required() 
def get_editoriales():
    return jsonify(editoriales)

# Obtener una editorial por ID
@editorialesBP.get("/<int:Id>")
def get_editorial(Id):
    for editorial in editoriales:
        if editorial['Id'] == Id:
            return jsonify(editorial), 200
    return {"error": "Editorial not found"}, 404

# Añadir una nueva editorial
@editorialesBP.post("/")
def post_editorial():
    if request.is_json:
        editorial = request.get_json()
        editorial["Id"] = __find_next_id()
        editoriales.append(editorial)
        return jsonify(editorial), 201
    return {"error": "Request must be JSON"}, 415

# Modificar una editorial por ID
@editorialesBP.put("/<int:id>")
def put_editorial(id):
    if request.is_json:
        new_editorial = request.get_json()
        for editorial in editoriales:
            if editorial["Id"] == id:
                editorial.update(new_editorial)
                return jsonify(editorial), 200
    return {"error": "Request must be JSON"}, 415

# Eliminar una editorial por ID
@editorialesBP.delete("/<int:id>")
def delete_editorial(id):
    global editoriales
    for editorial in editoriales:
        if editorial['Id'] == id:
            editoriales = [c for c in editoriales if c['Id'] != id]
            return {"message": f"Editorial {id} deleted successfully"}, 200
    return {"error": "Editorial not found"}, 404


