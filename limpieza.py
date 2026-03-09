
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
df.drop(columns=["Year", "Publisher", "Rank"])

#identificar los datos malucos
for columns in df.columns:
    print(df[columns].value_counts())
    print()
    print(df[columns].isna().sum())

#verificar la cantidad de datos faltantes (nulos) por cada columna
df_null = df.isnull().sum()

#mostrar el resultado por variable
print("Datos faltantes por columna:")
print(df_null)

#calcular el total de datos faltantes en todo el dataframe
total_null = df_null.sum()
print(f"\nTotal de datos faltantes en el dataset: {total_null}")

#definimos los valores dañinos
basura = ["NA", "ERROR", "UNKNOW"]

#limpieza de ventas por las regiones
regiones = ["JP_Sales", "NA_Sales", "EU_Sales", "Other_Sales", "Global_Sales"]

#convertir a número, calcular mediana y rellenar los valores nulos con sus medianas
for reg in regiones:
    df[reg] = pd.to_numeric(df[reg], errors="coerce")
    mediana = df[reg].median()
    df[reg] = df[reg].fillna(mediana)

print("Limpieza completada para análisis regional")
print(df[regiones].describe().round(2))

#quitar espacios vacios 
df["Genre"] = df["Genre"].str.strip()

#limpiar texto variable de texto (Genre)
df = df[~df["Genre"].isin(["NA", "ERROR", "UNKNOW"]) & df["Genre"].notna()]

#aseguramos la misma escritura en los datos
df["Genre"] = df["Genre"].str.capitalize()
#verificacion
print(df["Genre"].unique())

#quitar espacios vacios y aseguramos la misma escritura
df["Platform"] = df["Platform"].str.strip()

#limpiar texto variable de texto (Platform)
df = df[~df["Platform"].isin(["NA", "ERROR", "UNKNOW"]) & df["Platform"].notna()]

#aseguramos la misma escritura en los datos
df["Platform"] = df["Platform"].str.capitalize()
#verificacion
print(df["Platform"].unique())

#conteo de filas están totalmente duplicadas
print("Total de filas duplicadas:", df.duplicated().sum())

#ver las filas que están repetidas
df_duplicados = df[df.duplicated(keep=False)]
print(df_duplicados.head())