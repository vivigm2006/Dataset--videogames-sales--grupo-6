# Cargar librerías necesarias
library(tidyverse)
library(readr)

# 1. Cargar la data
df<-X12_Videogame_Sales_1_

# 2. Revisar data inicial
head(df, 5)

# 3. Revisión de los datos (tipos y dimensión)
glimpse(df) # Similar a dtypes y head combinados
dim(df)

# 4. Eliminar columnas que no son pertinentes
df <- df %>% select(-Year, -Publisher)

# 5. Verificar cantidad de datos faltantes (nulos)
conteo_nulos <- colSums(is.na(df))
print("Datos faltantes por columna:")
print(conteo_nulos)

# 6. Definir valores dañinos y limpiar variables de texto
basura <- c("NA", "ERROR", "UNKNOW")

df <- df %>%
  mutate(
    # Quitar espacios y normalizar escritura
    Genre = str_to_title(str_trim(Genre)),    # str_to_title es similar a capitalize
    Platform = str_to_upper(str_trim(Platform)),
    Name = str_trim(Name)
  ) %>%
  # Filtrar filas que tengan valores basura o sean NA en Genre y Platform
  filter(
    !Genre %in% basura, !is.na(Genre),
    !Platform %in% basura, !is.na(Platform)
  )

# 7. Verificación de únicos
unique(df$Genre)
unique(df$Platform)
unique(df$Name)

# 8. Limpieza de ventas por regiones (conversión y mediana)
regiones <- c("JP_Sales", "NA_Sales", "EU_Sales", "Other_Sales", "Global_Sales")

df <- df %>%
  mutate(across(all_of(regiones), ~ {
    val <- as.numeric(.)
    # Remplazar NAs (producidos por coerce) con la mediana
    if_else(is.na(val), median(val, na.rm = TRUE), val)
  }))

# 9. Mostrar resumen regional
print("Limpieza completada para análisis regional")
df %>% select(all_of(regiones)) %>% summary()

# 10. Conteo de filas duplicadas
total_duplicados <- sum(duplicated(df))
print(paste("Total de filas duplicadas:", total_duplicados))

# 11. Guardar el archivo limpio
write_csv
