import streamlit as st
import openai

# Configurar la API Key usando los secretos de Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Función para analizar el archivo y encontrar preguntas frecuentes
def analizar_preguntas_frecuentes(contenido):
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # O usa "gpt-4" si tienes acceso a ese modelo
        messages=[
            {"role": "system", "content": "Eres un asistente que identifica preguntas frecuentes en chats de soporte técnico."},
            {"role": "user", "content": f"Analiza el siguiente contenido y extrae solo las preguntas frecuentes:\n\n{contenido}"}
        ]
    )
    preguntas = respuesta.choices[0].message['content']
    return preguntas

# Interfaz de Streamlit
st.title("Analizador de Preguntas Frecuentes en Chats de Soporte")

# Input 1: Cantidad de archivos a analizar
cantidad_archivos = st.number_input("Cantidad de archivos a analizar", min_value=1, step=1)

# Lista para almacenar las preguntas frecuentes sin duplicados
preguntas_frecuentes_consolidadas = set()

# Loop para cargar archivos iterativamente
for i in range(cantidad_archivos):
    st.write(f"Sube el archivo #{i+1}")
    archivo_subido = st.file_uploader(f"Sube el archivo .txt #{i+1}", type="txt", key=i)
    
    if archivo_subido:
        # Leer el contenido del archivo
        contenido = archivo_subido.read().decode("utf-8")
        
        # Analizar el archivo para encontrar preguntas frecuentes
        preguntas_frecuentes = analizar_preguntas_frecuentes(contenido)
        
        # Procesar las preguntas para eliminar duplicados
        for pregunta in preguntas_frecuentes.split("\n"):
            preguntas_frecuentes_consolidadas.add(pregunta.strip())

# Output final: Descargar preguntas consolidadas
if st.button("Generar Archivo de Preguntas Frecuentes Consolidado"):
    resultado_final = "\n".join(preguntas_frecuentes_consolidadas)
    
    # Crear el archivo final con las preguntas consolidadas
    st.download_button(
        label="Descargar Preguntas Frecuentes",
        data=resultado_final,
        file_name="preguntas_frecuentes.txt",
        mime="text/plain"
    )
