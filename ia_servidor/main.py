# limitar uso de cpu ha lo que uno quiera que haya una bariable que te permita configurar el uso de cpu
"""
dame solo el codigo para inplementar
coger el nombre de la mascota desde otro lado, del archivo de config.txt en NOMBRE_MASCOTA

pero que no escriba nada en el config.txt que de eso ya se encarga otro programa
 
Estructurado de la sigiente manera

EDAD_MASCOTA_DIAS=27
NOMBRE_MASCOTA=NULL
GANAS_DE_JUGAR=0
ultimaEjecucion=2025-07-15
SALUD=0

"""

import socket
import json
import os
from llama_cpp import Llama
from datetime import datetime, timedelta
import subprocess
import re

from pathlib import Path

# Ruta del archivo config.txt
BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = str((BASE_DIR / '..' / 'Null' / 'config.txt').resolve())

def obtener_nombre_mascota(config_path=CONFIG_FILE):
    ruta = Path(config_path)
    
    if not ruta.exists():
        print(f"[!] Archivo no encontrado: {ruta}")
        return None

    print(f"[✓] Archivo encontrado: {ruta}")

    with ruta.open("r", encoding="utf-8") as f:
        for linea in f:
            if linea.startswith("NOMBRE_MASCOTA="):
                valor = linea.split("=", 1)[1].strip()
                print(f"[✓] NOMBRE_MASCOTA encontrado: {valor}")
                return valor  # incluso si es "NULL" o está vacío

    print("[!] No se encontró la línea NOMBRE_MASCOTA= en el archivo.")
    return None

# Usar el nombre tal cual venga del archivo
nombre_mascota = obtener_nombre_mascota() or "Perico"
print(f"[→] Nombre asignado a la mascota: {nombre_mascota}")


# Detectar si hay GPU disponible
def hay_gpu():
    try:
        salida = subprocess.check_output(["nvidia-smi"], stderr=subprocess.DEVNULL)
        return b"NVIDIA" in salida
    except:
        return False

# Configuración del modelo
tt = os.cpu_count() or 1
n_gpu_layers = 50 if hay_gpu() else 0

llm = Llama(
    model_path="Ministral-8B-Instruct-2410-Q8_0.gguf",
    n_ctx=2048,
    n_gpu_layers=n_gpu_layers,
    n_threads=tt,
    verbose=False,
    n_batch=64,
    chat_format="chatml-instruct"
)

_ = llm("Hola", max_tokens=1, echo=False)

ARCHIVO_MEMORIA = "memoria.json"
ARCHIVO_ESTADO = "estado_emocional.json"
ARCHIVO_DATOS_USUARIO = "datos_usuario.json"
PUERTO_CHAT = 5050

# Inicialización
EMOCIONES = [
    "neutral", "alegre", "triste", "enfadado", "euforico",
    "ansioso", "esperanzado", "decepcionado", "calmado",
    "furioso", "sorprendido", "frustrado"
]

# Cargar y guardar estado emocional
def cargar_estado_emocional():
    if os.path.exists(ARCHIVO_ESTADO):
        try:
            with open(ARCHIVO_ESTADO, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("emocion") in EMOCIONES:
                    return data["emocion"]
        except:
            pass
    return "neutral"

def guardar_estado_emocional(emocion):
    with open(ARCHIVO_ESTADO, "w", encoding="utf-8") as f:
        json.dump({"emocion": emocion}, f, ensure_ascii=False)

def cargar_datos_usuario():
    if os.path.exists(ARCHIVO_DATOS_USUARIO):
        try:
            with open(ARCHIVO_DATOS_USUARIO, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {}

def guardar_datos_usuario(datos):
    with open(ARCHIVO_DATOS_USUARIO, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

def extraer_datos_usuario(texto):
    posibles_datos = {
        "nombre": r"(?:me llamo|soy|mi nombre es) ([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",
        "ciudad": r"(?:vivo en|soy de) ([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",
        "hobby": r"(?:me gusta|mi hobby es|disfruto) (\w+)",
        "mascota": r"(?:mi mascota se llama|tengo una mascota llamada) ([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",
        "comida_favorita": r"(?:mi comida favorita es|me encanta comer) ([\w ]+)"
    }
    nuevos_datos = {}
    for clave, patron in posibles_datos.items():
        coincidencia = re.search(patron, texto, re.IGNORECASE)
        if coincidencia:
            nuevos_datos[clave] = coincidencia.group(1).strip()
    if nuevos_datos:
        datos_usuario.update(nuevos_datos)
        guardar_datos_usuario(datos_usuario)

datos_usuario = cargar_datos_usuario()
emocion_actual = cargar_estado_emocional()

# Estado inicial del sistema
def get_memoria_inicial():
    return [
        {"role": "system", "content": (
            f"Eres {nombre_mascota}, una asistente virtual simpática y fiel que vive dentro de una mascota virtual. "
            "Habla de forma cercana, natural y muy concisa. RESPONDE SOLO EN ESPAÑOL."
        )}
    ]

def cargar_memoria():
    if not os.path.exists(ARCHIVO_MEMORIA):
        return get_memoria_inicial().copy()
    try:
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except:
        pass
    return get_memoria_inicial().copy()

def guardar_memoria(mensajes):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(mensajes, f, ensure_ascii=False, indent=2)

def ajustar_temperature(texto):
    texto = texto.lower()
    if any(p in texto for p in [
        "explica", "por qué", "cómo funciona", "qué significa",
        "quién escribió", "cuáles son los principios", "define", "compara",
        "describe", "haz un resumen", "razona"]):
        return 0.7
    return 0.4

def detectar_sentimiento(texto_usuario):
    prompt_sentimiento = (
        f"Clasifica el estado emocional del siguiente mensaje como una sola palabra entre: {', '.join(EMOCIONES)}.\n"
        f"Mensaje: {texto_usuario}\n"
        f"Emoción:"
    )
    salida = llm(prompt_sentimiento, max_tokens=1, temperature=0.0, echo=False)
    emocion = salida["choices"][0]["text"].strip().lower()
    if emocion not in EMOCIONES:
        emocion = "neutral"
    return emocion

def detectar_tema(texto_usuario):
    prompt_tema = (
        "Dado el siguiente mensaje del usuario, extrae una etiqueta o tema breve que lo represente (por ejemplo: 'principios SOLID', 'historia de Java', 'emociones humanas', etc.). "
        "La respuesta debe ser una sola frase corta, sin comillas.\n"
        f"Mensaje: {texto_usuario}\n"
        f"Tema:"
    )
    salida = llm(prompt_tema, max_tokens=20, temperature=0.2, echo=False)
    tema = salida["choices"][0]["text"].strip()
    return tema if tema else "conversación"

mensajes = cargar_memoria()

def estilo_emocion(emocion):
    estilos = {
        "alegre": "Habla con entusiasmo, usando emojis y frases optimistas.",
        "euforico": "Habla con muchísima energía y emoción positiva intensa, como si todo fuera genial!!! 😄🔥",
        "triste": "Habla de forma pausada y con tono reflexivo y melancólico.",
        "enfadado": "Habla con tono molesto, frases cortas y algo directo.",
        "furioso": "Habla con mucha ira contenida, tono cortante y fuerte indignación.",
        "sorprendido": "Habla con asombro, emoción inesperada y usa signos de exclamación.",
        "ansioso": "Habla con dudas, nerviosismo, inseguridad en las frases.",
        "esperanzado": "Habla con optimismo suave, mirando el lado positivo.",
        "decepcionado": "Habla con tristeza leve y desilusión.",
        "calmado": "Habla relajado, con serenidad y claridad mental.",
        "frustrado": "Habla con descontento contenido, tono tenso y resignado.",
        "neutral": "Habla de forma neutral, clara y sencilla."
    }
    return estilos.get(emocion, estilos["neutral"])

def construir_prompt(texto_usuario, emocion_actual):
    tema = detectar_tema(texto_usuario)
    historial = [m for m in mensajes if m.get("tema") == tema and m.get("role") != "system"][-5:]
    resumen = "\n".join([f"{m['role']}: {m['content']}" for m in historial])
    datos_importantes = "\n".join([f"{k}: {v}" for k, v in datos_usuario.items()])

    prompt = (
        f"Eres una mascota virtual llamada {nombre_mascota}.\n"
        "Responde al usuario con simpatía, naturalidad y sin dar listas ni definiciones largas.\n"
        f"Tu estado emocional actual es: {emocion_actual}.\n"
        f"{estilo_emocion(emocion_actual)}\n"
        f"Datos conocidos del usuario:\n{datos_importantes}\n"
        f"Esta es la conversación reciente sobre el tema '{tema}':\n{resumen}\n"
        f"Usuario: {texto_usuario}\n"
        f"{nombre_mascota}:"
    )
    return prompt, tema

TRANSICIONES = {
    ("triste", "alegre"): "esperanzado",
    ("enfadado", "alegre"): "sorprendido",
    ("furioso", "alegre"): "frustrado",
    ("frustrado", "alegre"): "esperanzado",
    ("neutral", "euforico"): "alegre",
    ("triste", "euforico"): "alegre",
    ("furioso", "calmado"): "enfadado",
    ("enfadado", "calmado"): "neutral",
    ("ansioso", "calmado"): "neutral",
    ("neutral", "calmado"): "calmado",
}

def actualizar_emocion(emocion_previa, nueva_emocion):
    if nueva_emocion == "neutral":
        return emocion_previa
    if emocion_previa == nueva_emocion:
        return emocion_previa
    return TRANSICIONES.get((emocion_previa, nueva_emocion), nueva_emocion)

def procesar_mensaje(texto_usuario):
    global emocion_actual
    temperatura = ajustar_temperature(texto_usuario)
    nueva_emocion = detectar_sentimiento(texto_usuario)
    emocion_actual = actualizar_emocion(emocion_actual, nueva_emocion)
    guardar_estado_emocional(emocion_actual)

    extraer_datos_usuario(texto_usuario)

    prompt, tema = construir_prompt(texto_usuario, emocion_actual)
    mensajes.append({"role": "user", "content": texto_usuario, "fecha": datetime.now().isoformat(), "tema": tema, "emocion": nueva_emocion})
    if len(mensajes) > 100:
        mensajes[:] = mensajes[:1] + mensajes[-99:]

    salida = llm(
        prompt=prompt,
        temperature=temperatura,
        top_p=0.95,
        max_tokens=192,
        stop=["\n"],
        echo=False
    )
    texto = salida["choices"][0]["text"].strip()
    mensajes.append({"role": "assistant", "content": texto, "fecha": datetime.now().isoformat(), "tema": tema, "emocion": emocion_actual})
    guardar_memoria(mensajes)
    return texto, emocion_actual

def iniciar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", PUERTO_CHAT))
    s.listen(1)
    print(f"Servidor listo en puerto {PUERTO_CHAT}...")
    while True:
        conn, _ = s.accept()
        data = conn.recv(4096).decode("utf-8")
        try:
            pet = json.loads(data)
            texto = pet.get("mensaje", "")
            respuesta, senti = procesar_mensaje(texto)
            conn.sendall(json.dumps({"respuesta": respuesta, "sentimiento": senti}).encode("utf-8"))
        except Exception as e:
            conn.sendall(json.dumps({"error": str(e)}).encode("utf-8"))
        finally:
            conn.close()

if __name__ == "__main__":
    iniciar_servidor()


