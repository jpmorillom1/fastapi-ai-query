import os
import google.generativeai as genai
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_API_KEY2 = os.getenv("OPENROUTER_API_KEY2")
    DATA_PATH = os.getenv("DATA_PATH", "app/data/data.xlsx")  # Valor por defecto

def dividir_en_chunks(df: pd.DataFrame, chunk_size: int = 5) -> list[pd.DataFrame]:

    return [df.iloc[i:i + chunk_size] for i in range(0, len(df), chunk_size)]




def configure_gemini():
    if not Config.GEMINI_API_KEY:
        print("XDD")
        raise ValueError("GEMINI_API_KEY no está configurada en las variables de entorno")
    genai.configure(api_key=Config.GEMINI_API_KEY)

def obtener_datos():
    try:
        df = pd.read_excel(Config.DATA_PATH, engine="openpyxl")
        return df.sample(n=10, random_state=10)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo de datos en {Config.DATA_PATH}")
    except Exception as e:
        raise Exception(f"Error al leer los datos: {str(e)}")

def get_openai_client(api_key: str):
    if not api_key:
        raise ValueError("API key no proporcionada para OpenAI client")
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )


def get_response(prompt: str, model_name: str) -> tuple[str, str]:
    if not prompt or not model_name:
        raise ValueError("Prompt y model_name son requeridos")
    
    datos = obtener_datos()
    df_preview = datos.head(5).to_html(classes="df-preview", index=False)

    # Dividir en chunks
    chunks = dividir_en_chunks(datos, chunk_size=5)
    respuestas = []

    try:
        if model_name == "gemini":
            model = genai.GenerativeModel('gemini-2.5-flash')
            for i, chunk in enumerate(chunks):
                context = f"{prompt}\n\nDatos (parte {i+1}):\n{chunk.to_markdown(index=False)}"
                response = model.generate_content(context)
                respuestas.append(response.text)
            return "\n\n".join(respuestas), df_preview

        elif model_name == "deepseek":
            client = get_openai_client(Config.OPENROUTER_API_KEY)
            for i, chunk in enumerate(chunks):
                context = f"{prompt}\n\nDatos (parte {i+1}):\n{chunk.to_markdown(index=False)}"
                completion = client.chat.completions.create(
                    model="deepseek/deepseek-r1-0528:free",
                    messages=[{"role": "user", "content": "en español responde: " + context}]
                )
                respuestas.append(completion.choices[0].message.content)
            return "\n\n".join(respuestas), df_preview

        elif model_name == "llama3":
            client = get_openai_client(Config.OPENROUTER_API_KEY2)
            for i, chunk in enumerate(chunks):
                context = f"{prompt}\n\nDatos (parte {i+1}):\n{chunk.to_markdown(index=False)}"
                completion = client.chat.completions.create(
                    model="nvidia/llama-3.3-nemotron-super-49b-v1:free",
                    messages=[{"role": "user", "content": context}]
                )
                respuestas.append(completion.choices[0].message.content)
            return "\n\n".join(respuestas), df_preview

        else:
            raise ValueError(f"Modelo '{model_name}' no soportado")

    except Exception as e:
        raise Exception(f"Error al obtener respuesta del modelo: {str(e)}")


#def get_response(prompt: str, model_name: str) -> tuple[str, str]:



    """
    Obtiene respuesta del modelo seleccionado
    Retorna: (respuesta, vista_previa_html)
    """
    # Validación inicial
    if not prompt or not model_name:
        raise ValueError("Prompt y model_name son requeridos")
    
    # Obtener datos
    datos = obtener_datos()
    df_preview = datos.head(5).to_html(classes="df-preview", index=False)
    context = f"{prompt}\n\nDatos de contexto:\n{datos.to_markdown()}"

    # Procesar según modelo
    try:
        if model_name == "gemini":
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(context)
            return response.text, df_preview

        elif model_name == "deepseek":
            client = get_openai_client(Config.OPENROUTER_API_KEY)
            completion = client.chat.completions.create(
                model="deepseek/deepseek-r1-0528:free",
                messages=[{"role": "user", "content": "en español responde: "+context}]
            )
            return completion.choices[0].message.content, df_preview

        elif model_name == "llama3":
            client = get_openai_client(Config.OPENROUTER_API_KEY2)
            completion = client.chat.completions.create(
                model="nvidia/llama-3.3-nemotron-super-49b-v1:free",
                messages=[{"role": "user", "content": context}]
            )
            return completion.choices[0].message.content, df_preview

        else:
            raise ValueError(f"Modelo '{model_name}' no soportado")
            
    except Exception as e:
        raise Exception(f"Error al obtener respuesta del modelo: {str(e)}")