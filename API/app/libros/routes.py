# app/libros/routes.py
from flask import Blueprint, jsonify, request
from .data import libros


librosBP = Blueprint('libros', __name__)
# Función para encontrar el siguiente ID disponible para libros
def __find_next_id_libro():
    return max(libro['Id'] for libro in libros) + 1 if libros else 1

# Obtener todos los libros de una editorial
@librosBP.get("/")
def get_libros(editorial_id):
    libros_editorial = [libro for libro in libros if libro['IdEditorial'] == editorial_id]
    return jsonify(libros_editorial), 200

# Obtener un libro por ID dentro de una editorial
@librosBP.get("/<int:libro_id>")
def get_libro(editorial_id, libro_id):
    for libro in libros:
        if libro['Id'] == libro_id and libro['IdEditorial'] == editorial_id:
            return jsonify(libro), 200
    return {"error": "Libro not found"}, 404

# Añadir un nuevo libro a una editorial
@librosBP.post("/")
def post_libro(editorial_id):
    if request.is_json:
        new_libro = request.get_json()
        new_libro["Id"] = __find_next_id_libro()
        new_libro["IdEditorial"] = editorial_id
        libros.append(new_libro)
        return jsonify(new_libro), 201
    return {"error": "Request must be JSON"}, 415

# Modificar un libro por ID dentro de una editorial
@librosBP.put("/<int:libro_id>")
def put_libro(editorial_id, libro_id):
    if request.is_json:
        updated_libro = request.get_json()
        for libro in libros:
            if libro['Id'] == libro_id and libro['IdEditorial'] == editorial_id:
                libro.update(updated_libro)
                return jsonify(libro), 200
    return {"error": "Libro or Editorial not found or request must be JSON"}, 415

# Eliminar un libro por ID dentro de una editorial
@librosBP.delete("/<int:libro_id>")
def delete_libro(editorial_id, libro_id):
    global libros
    libros = [l for l in libros if not (l['Id'] == libro_id and l['IdEditorial'] == editorial_id)]
    return {"message": f"Libro {libro_id} deleted successfully"}, 200
