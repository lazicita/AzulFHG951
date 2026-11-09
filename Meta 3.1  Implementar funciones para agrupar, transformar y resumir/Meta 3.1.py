# Nombre completo: Azul Fernanda Hernandez Garcia
# Grupo: 951
# Fecha de realizacion: 03/11/2026
# Descripcion del problema: Con los datos de ventas de frutas de tres tiendas
# se hacen funciones para asignar codigos numericos con map(), agrupar con
# groupby() para sacar totales y promedios, y crear tablas resumen con
# pivot_table().

import pandas as pd


def crear_datos():
    datos={
        "Tienda": ["A", "A", "A", "B", "B", "B", "C", "C", "C"],
        "Producto": ["Manzana", "Plátano", "Naranja", "Manzana", "Plátano", "Naranja", "Manzana", "Plátano", "Naranja"],
        "Categoría": ["Fruta", "Fruta", "Fruta", "Fruta", "Fruta", "Fruta", "Fruta", "Fruta", "Fruta"],
        "Precio": [30, 20, 35, 25, 30, 45, 35, 20, 25],
        "Cantidad Vendida": [50, 30, 20, 60, 25, 35, 55, 20, 30],
        "Calificación": ["A", "B", "C", "A", "B", "A", "C", "B", "A"]
    }
    df=pd.DataFrame(datos)
    df["Total Ventas"]=df["Precio"]*df["Cantidad Vendida"]
    return df


def asignar_codigo(df):
    codigos_tienda={"A": 1, "B": 2, "C": 3}
    codigos_calificacion={"A": 3, "B": 2, "C": 1}
    df["Código de Tienda"]=df["Tienda"].map(codigos_tienda)
    df["Calificación Numérica"]=df["Calificación"].map(codigos_calificacion)
    return df


def total_ventas_tienda(df):
    res=df.groupby("Tienda")["Total Ventas"].sum()
    return res


def precio_promedio_tienda(df):
    res=df.groupby("Tienda")["Precio"].mean()
    return res


def cantidad_producto_tienda(df):
    tabla=pd.pivot_table(df, values="Cantidad Vendida", index="Producto", columns="Tienda", aggfunc="sum")
    return tabla


def ventas_producto_tienda(df):
    tabla=pd.pivot_table(df, values="Total Ventas", index="Producto", columns="Tienda", aggfunc="sum")
    return tabla


if __name__ == "__main__":
    df=crear_datos()
    print("Datos originales:")
    print(df)

    print("\n--- Ejercicio 1: Asignar codigo ---")
    df=asignar_codigo(df)
    print(df)

    print("\n--- Ejercicio 2: Total de ventas por tienda ---")
    print(total_ventas_tienda(df))

    print("\n--- Ejercicio 3: Precio promedio por tienda ---")
    print(precio_promedio_tienda(df))

    print("\n--- Ejercicio 4: Cantidad vendida por producto y tienda ---")
    print(cantidad_producto_tienda(df))

    print("\n--- Ejercicio 5: Total de ventas por tienda y producto ---")
    print(ventas_producto_tienda(df))