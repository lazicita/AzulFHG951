# Nombre completo: Azul Fernanda Hernandez Garcia
# Grupo: 951
# Fecha de realizacion: 28/09/2026
# Descripcion del problema: Se hacen funciones para el preprocesamiento de un
# DataFrame: calcular el porcentaje de nulos por columna, contar renglones
# duplicados, eliminar columnas con muchos nulos, sustituir valores nulos con
# mean, bfill o ffill y eliminar renglones duplicados.

import pandas as pd
import numpy as np


def crear_datos():
    datos={
        "nombre": ["Ana", "Juan", "Maria", "Jose", None, "Ana"],
        "edad": [20, 22, None, 23, None, 20],
        "salario": [15000, 20000, None, None, 20000, 15000],
        "pais": ["MEX", "MEX", "MEX", "USA", np.nan, "MEX"],
        "comentarios": ["ok", None, None, None, None, "ok"]
    }
    df=pd.DataFrame(datos)
    return df


def porcentaje_nulos(df: pd.DataFrame):
    porcentajes=df.isnull().sum()/len(df)
    return porcentajes


def contar_duplicados(df: pd.DataFrame):
    cantidad=df.duplicated().sum()
    return cantidad


def eliminar_columnas_nulos(df: pd.DataFrame, maximo):
    if maximo < 0 or maximo > 1:
        print("Error: El porcentaje maximo debe estar entre 0 y 1")
        return []
    porcentajes=porcentaje_nulos(df)
    columnas_eliminar=porcentajes[porcentajes >= maximo].index.tolist()
    df.drop(columns=columnas_eliminar, inplace=True)
    return columnas_eliminar


def sustituir_nulos(df: pd.DataFrame, columnas, metodo):
    metodos_validos=["mean", "bfill", "ffill"]
    posicion=metodos_validos.index(metodo)
    for columna in columnas:
        if metodo == "mean":
            df[columna]=df[columna].fillna(df[columna].mean())
        elif metodo == "bfill":
            df[columna]=df[columna].bfill()
        else:
            df[columna]=df[columna].ffill()
    return df


def eliminar_duplicados(df: pd.DataFrame):
    antes=len(df)
    df.drop_duplicates(inplace=True)
    eliminados=antes - len(df)
    return eliminados


if __name__ == "__main__":
    df=crear_datos()
    print("DataFrame original:")
    print(df)

    print("\n--- Ejercicio 1: Porcentaje de nulos por columna ---")
    print(porcentaje_nulos(df))

    print("\n--- Ejercicio 2: Renglones duplicados ---")
    print(contar_duplicados(df))

    print("\n--- Ejercicio 3: Eliminar columnas con muchos nulos ---")
    df3=df.copy()
    eliminadas=eliminar_columnas_nulos(df3, 0.5)
    print("Columnas eliminadas:", eliminadas)
    print(df3)
    print("Probando con un porcentaje invalido (1.5):")
    eliminar_columnas_nulos(df.copy(), 1.5)

    print("\n--- Ejercicio 4: Sustituir valores nulos ---")
    print("Con mean (edad y salario):")
    print(sustituir_nulos(df.copy(), ["edad", "salario"], "mean"))
    print("\nCon bfill (edad):")
    print(sustituir_nulos(df.copy(), ["edad"], "bfill"))
    print("\nCon ffill (edad):")
    print(sustituir_nulos(df.copy(), ["edad"], "ffill"))
    try:
        sustituir_nulos(df.copy(), ["edad"], "mediana")
    except ValueError:
        print("\nError: El metodo solo puede ser mean, bfill o ffill")

    print("\n--- Ejercicio 5: Eliminar renglones duplicados ---")
    df5=df.copy()
    eliminados=eliminar_duplicados(df5)
    print("Renglones eliminados:", eliminados)
    print(df5)