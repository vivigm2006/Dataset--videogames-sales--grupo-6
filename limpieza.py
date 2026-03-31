import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
df = pd.read_csv("12. Videogame Sales.csv")
print(df)

#revisar data inicial
df.head(5)

#revision de los datos
print("tipos de datos", df.dtypes)
print()
print("dimension de la data", df.shape)

#eliminar columnas que no son pertinentes en nuestra investigacion
df = df.drop(columns=["Year", "Publisher"])
print(df)

#verificar la cantidad de datos faltantes (nulos) por cada columna
conteo_nulos = df.isnull().sum()

#mostrar el resultado por variable
print("Datos faltantes por columna:")
print(conteo_nulos)

#definimos los valores dañinos
basura = ["NA", "ERROR", "UNKNOW"]

#quitar espacios vacios y aseguramos la misma escritura en cda variable
df["Genre"] = df["Genre"].str.strip().str.capitalize()
df["Platform"] = df["Platform"].str.strip().str.upper()
df["Name"] = df["Name"].str.strip()

#limpiar variable de texto (Genre y Platform)
df = df[~df["Genre"].isin(["NA", "ERROR", "UNKNOW"]) & df["Genre"].notna()]
df = df[~df["Platform"].isin(["NA", "ERROR", "UNKNOW"]) & df["Platform"].notna()]

#verificacion
print(df["Genre"].unique())
print(df["Platform"].unique())
print(df["Name"].unique())

#limpieza de ventas por las regiones
regiones = ["JP_Sales", "NA_Sales", "EU_Sales", "Other_Sales", "Global_Sales"]

#convertir a número, calcular mediana y rellenar los valores posiblemente malos con sus medianas
for reg in regiones:
    df[reg] = pd.to_numeric(df[reg], errors="coerce")
    mediana = df[reg].median()
    df[reg] = df[reg].fillna(mediana)

print("Limpieza completada para análisis regional")
print(df[regiones].describe().round(2))

#conteo de filas están totalmente duplicadas
print("Total de filas duplicadas:", df.duplicated().sum())

df.to_csv("12. Videogame_Sales_Limpio.csv")
