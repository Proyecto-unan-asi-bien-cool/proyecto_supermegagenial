
# Conversor de Unidades con Login

import json  # Permite leer y guardar datos en archivos JSON.
import os    # Permite comprobar si existe un archivo.

USUARIO_FILE = "usuario.json"  # Nombre del archivo donde se guardan los usuarios.


# Carga los usuarios guardados en el archivo JSON.
def cargar_usuarios():
    if os.path.exists(USUARIO_FILE):  # Comprueba si el archivo existe.
        with open(USUARIO_FILE, "r", encoding="utf-8") as archivo:
            try:
                return json.load(archivo)  # Lee los datos y los convierte en un diccionario.
            except json.JSONDecodeError:
                return {}  # Devuelve un diccionario vacío si el archivo está dañado.
    return {}  # Si el archivo no existe, devuelve un diccionario vacío.


# Guarda los usuarios en el archivo JSON.
def guardar_usuarios(usuarios):
    with open(USUARIO_FILE, "w", encoding="utf-8") as archivo:
        # Guarda los datos con formato legible y permite caracteres especiales.
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)


# Solicita un número entero y comprueba que esté dentro del rango permitido.
def solicitar_entero(prompt, min_val=None, max_val=None):
    while True:  # Repite la solicitud hasta recibir un valor válido.
        valor = input(prompt)
        try:
            numero = int(valor)  # Convierte el texto introducido en un entero.
        except ValueError:
            print("Entrada no válida. Ingrese un valor válido.")
            continue  # Vuelve al inicio del ciclo.

        # Comprueba que el número no sea menor que el mínimo permitido.
        if min_val is not None and numero < min_val:
            print(f"Ingrese un número mayor o igual a {min_val}.")
            continue

        # Comprueba que el número no supere el máximo permitido.
        if max_val is not None and numero > max_val:
            print(f"Ingrese un número menor o igual a {max_val}.")
            continue

        return numero  # Devuelve el número cuando es válido.


# Solicita un texto y evita que el usuario lo deje vacío.
def solicitar_texto(prompt):
    while True:
        texto = input(prompt).strip()  # Elimina espacios al inicio y al final.
        if texto:
            return texto
        print("Entrada no válida. Por favor ingrese un valor no vacío.")


# Permite registrar una cuenta nueva.
def crear_cuenta(usuarios):
    print("\n=== Crear nueva cuenta ===")
    while True:
        usuario = solicitar_texto("Ingrese un nombre de usuario: ")

        # Comprueba si el nombre ya está registrado.
        if usuario in usuarios:
            print("Ese usuario ya existe. Elija otro nombre.")
            continue

        contraseña = solicitar_texto("Ingrese una contraseña: ")
        confirmacion = solicitar_texto("Repita la contraseña: ")

        # Comprueba que ambas contraseñas coincidan.
        if contraseña != confirmacion:
            print("Las contraseñas no coinciden. Intente nuevamente.")
            continue

        usuarios[usuario] = contraseña  # Registra el usuario y su contraseña.
        guardar_usuarios(usuarios)  # Guarda los cambios en el archivo.
        print(f"Cuenta creada correctamente. Puede iniciar sesión como '{usuario}'.")
        return


# Verifica las credenciales del usuario.
def autenticar_usuario(usuarios):
    usuario = solicitar_texto("Usuario: ")
    contraseña = solicitar_texto("Contraseña: ")

    # Comprueba que el usuario exista y que su contraseña coincida.
    if usuario in usuarios and usuarios[usuario] == contraseña:
        return usuario  # Devuelve el nombre si la autenticación es correcta.

    print("Usuario o contraseña incorrectos.")
    return None  # Indica que la autenticación falló.


# Permite cambiar la contraseña de una cuenta existente.
def cambiar_contraseña(usuarios):
    print("\n=== Cambiar contraseña ===")
    usuario = autenticar_usuario(usuarios)  # Solicita las credenciales actuales.

    if not usuario:
        return  # Cancela la operación si falla la autenticación.

    nueva_contraseña = solicitar_texto("Ingrese la nueva contraseña: ")
    confirmacion = solicitar_texto("Repita la nueva contraseña: ")

    if nueva_contraseña != confirmacion:
        print("Las contraseñas no coinciden. Intente nuevamente.")
        return

    usuarios[usuario] = nueva_contraseña  # Actualiza la contraseña.
    guardar_usuarios(usuarios)  # Guarda el cambio.
    print("Contraseña actualizada correctamente.")


# Permite cambiar el nombre de usuario.
def cambiar_usuario(usuarios):
    print("\n=== Cambiar nombre de usuario ===")
    usuario = autenticar_usuario(usuarios)

    if not usuario:
        return

    nuevo_usuario = solicitar_texto("Ingrese el nuevo nombre de usuario: ")

    # Evita que el nuevo nombre sea igual al actual.
    if nuevo_usuario == usuario:
        print("El nombre de usuario debe ser diferente al actual.")
        return

    # Evita registrar un nombre que ya pertenezca a otra cuenta.
    if nuevo_usuario in usuarios:
        print("Ese nombre de usuario ya existe. Elija otro.")
        return

    # Crea la nueva entrada y elimina la anterior.
    usuarios[nuevo_usuario] = usuarios.pop(usuario)
    guardar_usuarios(usuarios)
    print(f"Usuario cambiado a '{nuevo_usuario}' correctamente.")


# Permite eliminar una cuenta después de confirmar la identidad.
def eliminar_usuario(usuarios):
    print("\n=== Eliminar usuario ===")
    usuario = autenticar_usuario(usuarios)

    if not usuario:
        return

    # Solicita una palabra de confirmación para evitar eliminaciones accidentales.
    confirmacion = solicitar_texto(
        f"Escriba 'ELIMINAR' para borrar la cuenta '{usuario}': "
    )

    if confirmacion != "ELIMINAR":
        print("Operación cancelada.")
        return

    usuarios.pop(usuario, None)  # Elimina la cuenta del diccionario.
    guardar_usuarios(usuarios)  # Actualiza el archivo JSON.
    print("Usuario eliminado correctamente.")


# Muestra el menú de acceso y controla las opciones de la cuenta.
def iniciar_sesion(usuarios):
    while True:
        print("\n====== Menú de acceso ======")
        print("1. Iniciar sesión")
        print("2. Crear cuenta")
        print("3. Cambiar contraseña")
        print("4. Cambiar usuario")
        print("5. Eliminar usuario")
        print("6. Salir")

        # Solo permite seleccionar números del 1 al 6.
        opcion = solicitar_entero("Seleccione una opción: ", 1, 6)

        if opcion == 1:
            usuario = autenticar_usuario(usuarios)
            if usuario:
                print(f"Bienvenido {usuario}.")
                return True  # Permite continuar al conversor.

        elif opcion == 2:
            crear_cuenta(usuarios)

        elif opcion == 3:
            cambiar_contraseña(usuarios)

        elif opcion == 4:
            cambiar_usuario(usuarios)

        elif opcion == 5:
            eliminar_usuario(usuarios)

        else:
            print("Saliendo del sistema. Hasta luego.")
            return False  # Indica que se debe cerrar el programa.


# Muestra el título e inicia el proceso de autenticación.
print("\n============== conversor de unidades v0.1 alpha ======================")
usuarios = cargar_usuarios()

# Si el usuario elige salir, el conversor no se ejecuta.
if not iniciar_sesion(usuarios):
    raise SystemExit


# ================= FUNCIONES DE CONVERSIÓN =================

# Solicita un número decimal y repite la solicitud si la entrada no es válida.
def solicitar_float(prompt):
    while True:
        valor = input(prompt)
        try:
            return float(valor)  # Convierte el texto en un número decimal.
        except ValueError:
            print("Entrada no válida. Ingrese un número válido.")


# Convierte grados Celsius a Fahrenheit.
def convertir_temperatura_c_f():
    celcius = solicitar_float("Ingrese la temperatura en Celsius: ")
    fahrenheit = (celcius * 9 / 5) + 32  # Fórmula de conversión.
    print(f"La temperatura en Fahrenheit es: {fahrenheit}")


# Convierte grados Fahrenheit a Celsius.
def convertir_temperatura_f_c():
    fahrenheit = solicitar_float("Ingrese la temperatura en Fahrenheit: ")
    celcius = (fahrenheit - 32) * 5 / 9  # Fórmula de conversión.
    print(f"La temperatura en Celsius es: {celcius}")


# Convierte metros a kilómetros.
def convertir_distancia_m_km():
    metros = solicitar_float("Ingrese la distancia en metros: ")
    kilometros = metros / 1000
    print(f"La distancia en kilómetros es: {kilometros}")


# Convierte kilómetros a metros.
def convertir_distancia_km_m():
    kilometros = solicitar_float("Ingrese la distancia en kilómetros: ")
    metros = kilometros * 1000
    print(f"La distancia en metros es: {metros}")


# Convierte millas a kilómetros.
def convertir_distancia_millas_km():
    millas = solicitar_float("Ingrese la distancia en millas: ")
    kilometros = millas * 1.60934
    print(f"La distancia en kilómetros es: {kilometros}")


# Convierte kilómetros a millas.
def convertir_distancia_km_millas():
    kilometros = solicitar_float("Ingrese la distancia en kilómetros: ")
    millas = kilometros / 1.60934
    print(f"La distancia en millas es: {millas}")


# Convierte kilogramos a libras.
def convertir_peso_kg_lb():
    kilogramos = solicitar_float("Ingrese el peso en kilogramos: ")
    libras = kilogramos * 2.20462
    print(f"El peso en libras es: {libras}")


# Convierte libras a kilogramos.
def convertir_peso_lb_kg():
    libras = solicitar_float("Ingrese el peso en libras: ")
    kilogramos = libras / 2.20462
    print(f"El peso en kilogramos es: {kilogramos}")


# Muestra las categorías disponibles en el conversor.
def mostrar_menu():
    print("\nBienvenido al conversor de unidades, por favor seleccione la categoría que desea convertir:")
    print("1. Temperatura")
    print("2. Distancia")
    print("3. Peso")
    print("4. Salir")


# Bucle principal: mantiene el conversor activo hasta que el usuario salga.
while True:
    mostrar_menu()
    opcion = solicitar_entero("Ingrese el número de la categoría: ", 1, 4)

    # Ejecuta el bloque correspondiente a la opción seleccionada.
    match opcion:

        case 1:
            # Submenú de conversiones de temperatura.
            while True:
                print("\nSeleccione la conversión de temperatura:")
                print("1. Celsius a Fahrenheit")
                print("2. Fahrenheit a Celsius")

                opcion_temperatura = solicitar_entero(
                    "Ingrese el número de la conversión: ", 1, 2
                )

                match opcion_temperatura:
                    case 1:
                        convertir_temperatura_c_f()
                        break  # Regresa al menú principal tras convertir.
                    case 2:
                        convertir_temperatura_f_c()
                        break

        case 2:
            # Submenú de conversiones de distancia.
            while True:
                print("\nSeleccione la conversión de distancia:")
                print("1. Metros a Kilómetros")
                print("2. Kilómetros a Metros")
                print("3. Millas a Kilómetros")
                print("4. Kilómetros a Millas")

                opcion_distancia = solicitar_entero(
                    "Ingrese el número de la conversión: ", 1, 4
                )

                match opcion_distancia:
                    case 1:
                        convertir_distancia_m_km()
                        break
                    case 2:
                        convertir_distancia_km_m()
                        break
                    case 3:
                        convertir_distancia_millas_km()
                        break
                    case 4:
                        convertir_distancia_km_millas()
                        break

        case 3:
            # Submenú de conversiones de peso.
            while True:
                print("\nSeleccione la conversión de peso:")
                print("1. Kilogramos a Libras")
                print("2. Libras a Kilogramos")

                opcion_peso = solicitar_entero(
                    "Ingrese el número de la conversión: ", 1, 2
                )

                match opcion_peso:
                    case 1:
                        convertir_peso_kg_lb()
                        break
                    case 2:
                        convertir_peso_lb_kg()
                        break

        case 4:
            print("Gracias por usar el conversor de unidades. ¡Hasta luego!")
            break  # Termina el bucle principal.

    # Informa al usuario que volverá a seleccionar una categoría.
    if opcion == 4:
        break

    print("\nVolviendo al menú principal...\n")
