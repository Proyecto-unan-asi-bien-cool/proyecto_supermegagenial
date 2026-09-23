# Conversor de Unidades con Login

import json
import os

USUARIO_FILE = "usuario.json"


def cargar_usuarios():
    if os.path.exists(USUARIO_FILE):
        with open(USUARIO_FILE, "r", encoding="utf-8") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                return {}
    return {}


def guardar_usuarios(usuarios):
    with open(USUARIO_FILE, "w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)


def solicitar_entero(prompt, min_val=None, max_val=None):
    while True:
        valor = input(prompt)
        try:
            numero = int(valor)
        except ValueError:
            print("Entrada no válida. Ingrese un valor valido.")
            continue

        if min_val is not None and numero < min_val:
            print(f"Ingrese un número mayor o igual a {min_val}.")
            continue
        if max_val is not None and numero > max_val:
            print(f"Ingrese un número menor o igual a {max_val}.")
            continue

        return numero


def solicitar_texto(prompt):
    while True:
        texto = input(prompt).strip()
        if texto:
            return texto
        print("Entrada no válida. Por favor ingrese un valor no vacío.")


def crear_cuenta(usuarios):
    print("\n=== Crear nueva cuenta ===")
    while True:
        usuario = solicitar_texto("Ingrese un nombre de usuario: ")
        if usuario in usuarios:
            print("Ese usuario ya existe. Elija otro nombre.")
            continue
        contraseña = solicitar_texto("Ingrese una contraseña: ")
        confirmacion = solicitar_texto("Repita la contraseña: ")
        if contraseña != confirmacion:
            print("Las contraseñas no coinciden. Intente nuevamente.")
            continue
        usuarios[usuario] = contraseña
        guardar_usuarios(usuarios)
        print(f"Cuenta creada correctamente. Puede iniciar sesión como '{usuario}'.")
        return


def autenticar_usuario(usuarios):
    usuario = solicitar_texto("Usuario: ")
    contraseña = solicitar_texto("Contraseña: ")
    if usuario in usuarios and usuarios[usuario] == contraseña:
        return usuario
    print("Usuario o contraseña incorrectos.")
    return None


def cambiar_contraseña(usuarios):
    print("\n=== Cambiar contraseña ===")
    usuario = autenticar_usuario(usuarios)
    if not usuario:
        return
    nueva_contraseña = solicitar_texto("Ingrese la nueva contraseña: ")
    confirmacion = solicitar_texto("Repita la nueva contraseña: ")
    if nueva_contraseña != confirmacion:
        print("Las contraseñas no coinciden. Intente nuevamente.")
        return
    usuarios[usuario] = nueva_contraseña
    guardar_usuarios(usuarios)
    print("Contraseña actualizada correctamente.")


def cambiar_usuario(usuarios):
    print("\n=== Cambiar nombre de usuario ===")
    usuario = autenticar_usuario(usuarios)
    if not usuario:
        return
    nuevo_usuario = solicitar_texto("Ingrese el nuevo nombre de usuario: ")
    if nuevo_usuario == usuario:
        print("El nombre de usuario debe ser diferente al actual.")
        return
    if nuevo_usuario in usuarios:
        print("Ese nombre de usuario ya existe. Elija otro.")
        return
    usuarios[nuevo_usuario] = usuarios.pop(usuario)
    guardar_usuarios(usuarios)
    print(f"Usuario cambiado a '{nuevo_usuario}' correctamente.")


def eliminar_usuario(usuarios):
    print("\n=== Eliminar usuario ===")
    usuario = autenticar_usuario(usuarios)
    if not usuario:
        return
    confirmacion = solicitar_texto(f"Escriba 'ELIMINAR' para borrar la cuenta '{usuario}': ")
    if confirmacion != "ELIMINAR":
        print("Operación cancelada.")
        return
    usuarios.pop(usuario, None)
    guardar_usuarios(usuarios)
    print("Usuario eliminado correctamente.")


def iniciar_sesion(usuarios):
    while True:
        print("\n====== Menú de acceso ======")
        print("1. Iniciar sesión")
        print("2. Crear cuenta")
        print("3. Cambiar contraseña")
        print("4. Cambiar usuario")
        print("5. Eliminar usuario")
        print("6. Salir")
        opcion = solicitar_entero("Seleccione una opción: ", 1, 6)

        if opcion == 1:
            usuario = autenticar_usuario(usuarios)
            if usuario:
                print(f"Bienvenido {usuario}.")
                return True

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
            return False


print("\n============== conversor de unidades v0.1 alpha ======================")
usuarios = cargar_usuarios()
if not iniciar_sesion(usuarios):
    raise SystemExit


# funciones para realizar las conversiones

def solicitar_float(prompt):
    while True:
        valor = input(prompt)
        try:
            return float(valor)
        except ValueError:
            print("Entrada no válida. Ingrese un número válido.")


def convertir_temperatura_c_f():
    celcius = solicitar_float("Ingrese la temperatura en Celsius: ")
    fahrenheit = (celcius * 9 / 5) + 32
    print(f"La temperatura en Fahrenheit es: {fahrenheit}")


def convertir_temperatura_f_c():
    fahrenheit = solicitar_float("Ingrese la temperatura en Fahrenheit: ")
    celcius = (fahrenheit - 32) * 5 / 9
    print(f"La temperatura en Celsius es: {celcius}")


def convertir_distancia_m_km():
    metros = solicitar_float("Ingrese la distancia en metros: ")
    kilometros = metros / 1000
    print(f"La distancia en kilómetros es: {kilometros}")


def convertir_distancia_km_m():
    kilometros = solicitar_float("Ingrese la distancia en kilómetros: ")
    metros = kilometros * 1000
    print(f"La distancia en metros es: {metros}")

def convertir_distancia_millas_km():
    millas = solicitar_float("Ingrese la distancia en millas: ")
    kilometros = millas * 1.60934
    print(f"La distancia en kilómetros es: {kilometros}")

def convertir_distancia_km_millas():
    kilometros = solicitar_float("Ingrese la distancia en kilómetros: ")
    millas = kilometros / 1.60934
    print(f"La distancia en millas es: {millas}")


def convertir_peso_kg_lb():
    kilogramos = solicitar_float("Ingrese el peso en kilogramos: ")
    libras = kilogramos * 2.20462
    print(f"El peso en libras es: {libras}")


def convertir_peso_lb_kg():
    libras = solicitar_float("Ingrese el peso en libras: ")
    kilogramos = libras / 2.20462
    print(f"El peso en kilogramos es: {kilogramos}")


def mostrar_menu():
    print("\nBienvenido al conversor de unidades, por favor seleccione la categoría que desea convertir:")
    print("1. Temperatura")
    print("2. Distancia")
    print("3. Peso")
    print("4. Salir")


while True:
    mostrar_menu()
    opcion = solicitar_entero("Ingrese el número de la categoría: ", 1, 4)

    match opcion:
        case 1:
            while True:
                print("\nSeleccione la conversión de temperatura:")
                print("1. Celsius a Fahrenheit")
                print("2. Fahrenheit a Celsius")
                opcion_temperatura = solicitar_entero("Ingrese el número de la conversión: ", 1, 2)
                match opcion_temperatura:
                    case 1:
                        convertir_temperatura_c_f()
                        break
                    case 2:
                        convertir_temperatura_f_c()
                        break

        case 2:
            while True:
                print("\nSeleccione la conversión de distancia:")
                print("1. Metros a Kilómetros")
                print("2. Kilómetros a Metros")
                print("3. Millas a Kilómetros")
                print("4. Kilómetros a Millas")
                opcion_distancia = solicitar_entero("Ingrese el número de la conversión: ", 1, 4)
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
            while True:
                print("\nSeleccione la conversión de peso:")
                print("1. Kilogramos a Libras")
                print("2. Libras a Kilogramos")
                opcion_peso = solicitar_entero("Ingrese el número de la conversión: ", 1, 2)
                match opcion_peso:
                    case 1:
                        convertir_peso_kg_lb()
                        break
                    case 2:
                        convertir_peso_lb_kg()
                        break

        case 4:
            print("Gracias por usar el conversor de unidades. ¡Hasta luego!")
            break

    if opcion == 4:
        break

    print("\nVolviendo al menú principal...\n")
