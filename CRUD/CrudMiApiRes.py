import requests
from time import sleep

# Función que muestra las opciones disponibles
def mostrarDatos():
    print("OPCIONES:")
    print("1. Post (Añadir).")
    print("2. Get (Obtener todos).")
    print("3. Patch (Modificar).")
    print("4. Delete (Eliminar).")
    print("5. Get (Obtener una).")
    print("6. Nuevo usuario.")
    print("0. Salida.")

# Función para manejar la autenticación y obtener el token
def registrarUsuario():
    username = input("Escribe tu nuevo nombre de usuario: ")
    password = input("Escribe tu nueva contraseña: ")
    resultado = requests.post(
        "http://localhost:5050/usuarios/registro",
        json={"username": username, "password": password},
        headers={"Content-Type": "application/json"}
    )
    print(resultado.text)



# Función para manejar la autenticación y obtener el token
def obtener_token():
    username = input("Usuario: ")
    password = input("Contraseña: ")
    resultado = requests.post(
        "http://localhost:5050/usuarios/login",
        json={"username": username, "password": password},
        headers={"Content-Type": "application/json"}
    )
    if resultado.status_code == 200:
        token = resultado.json().get("token")
        return token
    else:
        print("Error de autenticación:", resultado.text)
        return None

# Función para añadir una nueva editorial
def post(token, userid, title, completed):
    try:
        response = requests.post(
            "http://localhost:5050/editoriales/",
            json={"UserId": userid, "Title": title, "Completed": completed},
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        if response.status_code == 201:
            print("Editorial añadida:", response.json())
        else:
            print("Error al añadir la editorial:", response.text)
    except Exception as e:
        print("Error en la solicitud POST:", e)

# Función para obtener todas las editoriales
def get(token):
    try:
        response = requests.get(
            "http://localhost:5050/editoriales",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            print("Lista de editoriales:", response.json())
        else:
            print("Error al obtener las editoriales:", response.text)
    except Exception as e:
        print("Error en la solicitud GET:", e)

# Función para obtener todas las editoriales
def getEditorial(token,editorial_id):
    try:
        response = requests.get(
            f"http://localhost:5050/editoriales/{editorial_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            print("Lista de editoriales:", response.json())
        else:
            print("Error al obtener las editoriales:", response.text)
    except Exception as e:
        print("Error en la solicitud GET:", e)

# Función para modificar una editorial
def patch(token, editorial_id, title, completed):
    try:
        response = requests.put(  # Cambié patch a put para actualizar la editorial completa
            f"http://localhost:5050/editoriales/{editorial_id}",
            json={"Title": title, "Completed": completed},
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        )
        if response.status_code == 200:
            print("Editorial modificada:", response.json())
        else:
            print("Error al modificar la editorial:", response.text)
    except Exception as e:
        print("Error en la solicitud PUT:", e)

# Función para eliminar una editorial
def delete(token, editorial_id):
    try:
        response = requests.delete(
            f"http://localhost:5050/editoriales/{editorial_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            print(f"Editorial {editorial_id} eliminada con éxito.")
        else:
            print("Error al eliminar la editorial:", response.text)
    except Exception as e:
        print("Error en la solicitud DELETE:", e)

# Bucle principal para interactuar con el usuario
def main():
    
    print("1.Iniciar Sesion")
    print("2.Acceder con nuevo usuario")
    opcion = int(input("Seleccione una opción: "))
    if (opcion==1):
        token = obtener_token()
    elif(opcion==2):
        registrarUsuario()
        token = obtener_token()
    if not token:
        print("No se pudo autenticar. Salida del programa.")
        return

    salida = False
    while not salida:
        mostrarDatos()
        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:  # Añadir nueva editorial
            userid = int(input("Introduce el ID del usuario: "))
            title = input("Introduce el título: ")
            completed = input("Completado (True/False): ").strip().lower() == "true"
            post(token, userid, title, completed)
        elif opcion == 2:  # Obtener todas las editoriales
            get(token)
        elif opcion == 3:  # Modificar editorial1
            editorial_id = int(input("Introduce el ID de la editorial a modificar: "))
            title = input("Introduce el nuevo título: ")
            completed = input("Nuevo estado (True/False): ").strip().lower() == "true"
            patch(token, editorial_id, title, completed)
        elif opcion == 4:  # Eliminar editorial
            editorial_id = int(input("Introduce el ID de la editorial a eliminar: "))
            delete(token, editorial_id)
        elif opcion == 5:  # Obtener editorial
            editorial_id = int(input("Introduce el ID de la editorial: "))
            getEditorial(token,editorial_id)
        elif opcion == 6:  # Obtener editorial1
            registrarUsuario()
        elif opcion == 0:  # Salir
            salida = True
        else:
            print("OPCIÓN NO VÁLIDA")

        sleep(2)  # Pausa la ejecución durante 2 segundos

    print("Ha salido del programa.")

# Ejecutar el programa
if __name__ == "__main__":
    main()
