#Hernández García Azul Fernanda
#11/10/2026
#El programa es un sistema de consola en Python que administra eventos universitarios guardados en una
#base de datos de SQL Server, usando la librería pyodbc. La función conectar() crea la conexión al servidor y las demás
#funciones la abren y la cierran cada vez que realizan una operación. A través de un menú que se repite hasta que el
#usuario elige salir, es posible mostrar todos los eventos, buscarlos por nombre, consultar cuáles tienen lugar para
#cierto número de asistentes, registrar o cancelar asistentes, agregar eventos nuevos, modificar su fecha, hora, lugar
#o cupo, y ver los eventos próximos con lugares disponibles. Todas las consultas usan parámetros (?) en lugar de
#concatenar texto, lo que evita la inyección SQL, y antes de registrar o cancelar asistentes el código valida que el
#evento exista y que la cantidad sea correcta. Los cambios se confirman con commit(), y cada función maneja los errores
#con try, except y finally, de modo que el programa informe al usuario si hay un problema de conexión o de consulta y
#siempre cierre el cursor y la conexión.

import pyodbc


def conectar():
    try:
        conexion=pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            "SERVER=lazicita\\SQLEXPRESS;"  
            "DATABASE=Eventos;"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        return conexion
    except pyodbc.Error as e:
        print("Error de conexión:",e)
        return None


def imprimir(resultados):
    if not resultados:
        print("\nNo se encontraron eventos.")
        return

    print(f"\n{'ID':<4}{'Nombre':<55}{'Fecha':<12}{'Hora':<8}{'Lugar':<26}{'Cupo':<6}{'Reg.':<6}{'Disp.':<6}")
    print("-" * 123)
    for row in resultados:
        print(f"{row.id:<4}{row.nombre:<55}{str(row.fecha):<12}{str(row.hora)[:5]:<8}"
              f"{row.lugar:<26}{row.cupo:<6}{row.registrados:<6}{row.cupo - row.registrados:<6}")


def mostrar_eventos():
    conexion=conectar()
    if conexion is None:
        return
    cursor=conexion.cursor()
    try:
        sql= """
        SELECT * FROM eventos 
        ORDER BY fecha, hora
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        imprimir(resultados)
    except pyodbc.Error as e:
        print("Error en la consulta:", e)
    finally:
        cursor.close()
        conexion.close()


def buscar_evento(texto):
    conexion=conectar()
    if conexion is None:
        return
    cursor=conexion.cursor()
    try:
        sql= """
        SELECT * FROM eventos 
        WHERE nombre LIKE ?
        """
        cursor.execute(sql, ("%" + texto + "%",))
        resultados=cursor.fetchall()
        imprimir(resultados)
    except pyodbc.Error as e:
        print("Error en la búsqueda:", e)
    finally:
        cursor.close()
        conexion.close()


def eventos_con_disponibilidad(asistentes):
    conexion=conectar()
    if conexion is None:
        return
    cursor=conexion.cursor()
    try:
        sql = """
        SELECT * FROM eventos 
        WHERE cupo - registrados >= ?
        ORDER BY fecha, hora
        """
        cursor.execute(sql, (asistentes,))
        resultados = cursor.fetchall()
        imprimir(resultados)
    except pyodbc.Error as e:
        print("Error en la consulta:", e)
    finally:
        cursor.close()
        conexion.close()


def registrar_asistentes(id_evento, cantidad):
    if cantidad<= 0:
        print("La cantidad debe ser mayor que cero.")
        return
    conexion=conectar()
    if conexion is None:
        return
    cursor=conexion.cursor()
    try:
        sql= """
        SELECT cupo, registrados FROM eventos 
        WHERE id = ?
        """
        cursor.execute(sql, (id_evento,))
        evento = cursor.fetchone()

        if evento is None:
            print("El evento no existe.")
        elif cantidad > evento.cupo - evento.registrados:
            print("No hay cupo suficiente. Disponibles:", evento.cupo - evento.registrados)
        else:
            sql= """
            UPDATE eventos 
            SET registrados = registrados + ? 
            WHERE id = ?
            """
            cursor.execute(sql, (cantidad, id_evento))
            conexion.commit()
            print(f"Registrados actuales: {evento.registrados}")
            print(f"Nuevos asistentes: {cantidad}")
            print(f"Nuevo total de registrados: {evento.registrados + cantidad}")
    except pyodbc.Error as e:
        print("Error al registrar asistentes:", e)
    finally:
        cursor.close()
        conexion.close()


def cancelar_registros(id_evento, cantidad):
    if cantidad <= 0:
        print("La cantidad debe ser mayor que cero.")
        return
    conexion= conectar()
    if conexion is None:
        return
    cursor= conexion.cursor()
    try:
        sql= """
        SELECT registrados FROM eventos 
        WHERE id = ?
        """
        cursor.execute(sql, (id_evento,))
        evento = cursor.fetchone()

        if evento is None:
            print("El evento no existe.")
        elif cantidad > evento.registrados:
            print("Solo hay", evento.registrados, "registrados; no puedes cancelar", cantidad)
        else:
            sql = """
            UPDATE eventos 
            SET registrados = registrados - ? 
            WHERE id = ?
            """
            cursor.execute(sql, (cantidad, id_evento))
            conexion.commit()
            print("Nuevo total de registrados:", evento.registrados - cantidad)
    except pyodbc.Error as e:
        print("Error al cancelar registros:", e)
    finally:
        cursor.close()
        conexion.close()


def agregar_evento(nombre, fecha, hora, lugar, cupo):
    conexion = conectar()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        sql = """
        INSERT INTO eventos 
        (nombre, fecha, hora, lugar, cupo, registrados) 
        VALUES (?, ?, ?, ?, ?, 0)
        """  # registrados SIEMPRE empieza en 0
        cursor.execute(sql, (nombre, fecha, hora, lugar, cupo))
        conexion.commit()
        print("Evento agregado correctamente.")
    except pyodbc.Error as e:
        print("Error al agregar el evento:", e)
    finally:
        cursor.close()
        conexion.close()


def modificar_evento(id_evento, opcion, nuevo_valor):
    conexion = conectar()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        if opcion == "1":
            sql = "UPDATE eventos SET fecha = ? WHERE id = ?"
        elif opcion == "2":
            sql = "UPDATE eventos SET hora = ? WHERE id = ?"
        elif opcion == "3":
            sql = "UPDATE eventos SET lugar = ? WHERE id = ?"
        elif opcion == "4":
            sql = "UPDATE eventos SET cupo = ? WHERE id = ?"
        else:
            print("Opción no válida.")
            return

        cursor.execute(sql, (nuevo_valor, id_evento))
        conexion.commit()
        if cursor.rowcount == 0:
            print("El evento no existe.")
        else:
            print("Evento actualizado correctamente.")
    except pyodbc.Error as e:
        print("Error al modificar el evento:", e)
    finally:
        cursor.close()
        conexion.close()


def mostrar_eventos_proximos():
    conexion = conectar()
    if conexion is None:
        return
    cursor = conexion.cursor()
    try:
        sql = """
        SELECT * FROM eventos 
        WHERE fecha >= CAST(GETDATE() AS DATE) 
        AND cupo - registrados > 0 
        ORDER BY fecha, hora
        """
        cursor.execute(sql)
        resultados = cursor.fetchall()
        imprimir(resultados)
    except pyodbc.Error as e:
        print("Error en la consulta:", e)
    finally:
        cursor.close()
        conexion.close()



if __name__ == "__main__":
    while True:
        print("\n===== SISTEMA DE EVENTOS UNIVERSITARIOS =====\n")
        print("1. Mostrar eventos")
        print("2. Buscar evento")
        print("3. Consultar eventos con disponibilidad")
        print("4. Registrar asistentes")
        print("5. Cancelar registros")
        print("6. Agregar evento")
        print("7. Modificar evento")
        print("8. Mostrar eventos próximos")
        print("9. Salir")
        opcion = input("\nElige una opción: ")

        try:
            if opcion == "1":
                mostrar_eventos()
            elif opcion == "2":
                buscar_evento(input("Texto a buscar: "))
            elif opcion == "3":
                eventos_con_disponibilidad(int(input("Número de asistentes: ")))
            elif opcion == "4":
                registrar_asistentes(int(input("ID del evento: ")),
                                     int(input("Número de asistentes: ")))
            elif opcion == "5":
                cancelar_registros(int(input("ID del evento: ")),
                                   int(input("Registros a cancelar: ")))
            elif opcion == "6":
                agregar_evento(input("Nombre: "),
                               input("Fecha (AAAA-MM-DD): "),
                               input("Hora (HH:MM): "),
                               input("Lugar: "),
                               int(input("Cupo: ")))
            elif opcion == "7":
                id_evento = int(input("ID del evento: "))
                print("1. Fecha  2. Hora  3. Lugar  4. Cupo")
                campo = input("¿Qué quieres modificar? ")
                valor = input("Nuevo valor: ")
                if campo == "4":
                    valor = int(valor)
                modificar_evento(id_evento, campo, valor)
            elif opcion == "8":
                mostrar_eventos_proximos()
            elif opcion == "9":
                print("Hasta pronto.")
                break
            else:
                print("Opción no válida.")
        except ValueError:
            print("Dato inválido: escribe un número donde se pide un número.")