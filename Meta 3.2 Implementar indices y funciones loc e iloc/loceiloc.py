# Nombre completo: Azul Fernanda Hernandez García
# Grupo: 951
# Fecha de realizacion: 08/11/2026
# Descripcion del problema: Se crea un DataFrame con las ventas mensuales de
# tres productos (A, B y C) durante los primeros tres meses del año, con datos
# aleatorios entre 100 y 1000. Despues se hacen funciones para seleccionar
# datos usando loc e iloc, y una funcion para cambiar el valor de una venta.

import pandas as pd
import numpy as np



def crear_ventas():
    meses=["Enero", "Febrero", "Marzo"]
    productos=["A", "B", "C"]
    datos=np.random.randint(100, 1001, size=(3, 3))
    ventas=pd.DataFrame(datos, index=meses, columns=productos)
    return ventas



def seleccionar_loc(df, filas, columnas):
    resultado=df.loc[filas, columnas]
    return resultado


def seleccionar_iloc(df, filas, columnas):
    resultado=df.iloc[filas, columnas]
    return resultado



def cambiar_venta(df, producto, mes, nuevo_valor):
    df.loc[mes, producto]=nuevo_valor
    return df


if __name__ == "__main__":
    ventas=crear_ventas()
    print("DataFrame de ventas:")
    print(ventas)

    print("\n--- Ejercicio 2: usando loc ---")

    print("\n2.1 Ventas del producto A en enero:")
    print(seleccionar_loc(ventas, "Enero", "A"))

    print("\n2.2 Ventas de todos los productos en febrero:")
    print(seleccionar_loc(ventas, "Febrero", ["A", "B", "C"]))

    print("\n2.3 Ventas de todos los productos en el primer y tercer mes:")
    print(seleccionar_loc(ventas, ["Enero", "Marzo"], ["A", "B", "C"]))

    print("\n--- Ejercicio 3: usando iloc ---")

    print("\n3.1 Ventas del primer mes para todos los productos:")
    print(seleccionar_iloc(ventas, 0, slice(None)))

    print("\n3.2 Ventas del segundo producto en todos los meses:")
    print(seleccionar_iloc(ventas, slice(None), 1))

    print("\n3.3 Ventas del segundo y tercer mes para el primer producto:")
    print(seleccionar_iloc(ventas, [1, 2], 0))

    print("\n--- Ejercicio 4: cambiar un valor ---")

    print("\n4.1 Cambiar las ventas del producto B en marzo a 1200:")
    ventas=cambiar_venta(ventas, "B", "Marzo", 1200)
    print(ventas)