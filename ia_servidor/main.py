# limitar uso de cpu ha lo que uno quiera que haya una bariable que te permita configurar el uso de cpu
# cojer el nonbre de la mascota del harchibo de el java de configuracion del config.txt
"""
Estructurado de la sigiente manera

FELICIDAD=0
ENFADO=0
EDAD_MASCOTA_DIAS=27
NOMBRE_MASCOTA=NULL
GANAS_DE_JUGAR=0
TRISTEZA=0
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
            "Eres Perico, una asistente virtual simpática y fiel que vive dentro de una mascota virtual. "
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
        "Eres una mascota virtual llamada Perico.\n"
        "Responde al usuario con simpatía, naturalidad y sin dar listas ni definiciones largas.\n"
        f"Tu estado emocional actual es: {emocion_actual}.\n"
        f"{estilo_emocion(emocion_actual)}\n"
        f"Datos conocidos del usuario:\n{datos_importantes}\n"
        f"Esta es la conversación reciente sobre el tema '{tema}':\n{resumen}\n"
        f"Usuario: {texto_usuario}\n"
        f"Perico:"
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



"""
import socket
import json
import os
from llama_cpp import Llama
from datetime import datetime, timedelta
import subprocess

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

emocion_actual = cargar_estado_emocional()

# Estado inicial del sistema
def get_memoria_inicial():
    return [
        {"role": "system", "content": (
            "Eres Perico, una asistente virtual simpática y fiel que vive dentro de una mascota virtual. "
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
        "La respuesta debe ser una sola frase corta, sin comillas."
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
    historial = mensajes[-5:]
    tema = None
    for m in reversed(mensajes):
        if m.get("role") == "user" and texto_usuario.lower() in m.get("content", "").lower():
            tema = m.get("tema")
            break
    if tema:
        historial = [m for m in mensajes if m.get("tema") == tema and m.get("role") != "system"][-5:]

    resumen = "\n".join([f"{m['role']}: {m['content']}" for m in historial])
    prompt = (
        "Eres una mascota virtual llamada Perico.\n"
        "Responde al usuario con simpatía, naturalidad y sin dar listas ni definiciones largas.\n"
        f"Tu estado emocional actual es: {emocion_actual}.\n"
        f"{estilo_emocion(emocion_actual)}\n"
        f"Esta es la conversación reciente:\n{resumen}\n"
        f"Usuario: {texto_usuario}\n"
        f"Perico:"
    )
    return prompt

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

    tema = detectar_tema(texto_usuario)
    mensajes.append({"role": "user", "content": texto_usuario, "fecha": datetime.now().isoformat(), "tema": tema})
    if len(mensajes) > 100:
        mensajes[:] = mensajes[:1] + mensajes[-99:]

    prompt = construir_prompt(texto_usuario, emocion_actual)
    salida = llm(
        prompt=prompt,
        temperature=temperatura,
        top_p=0.95,
        max_tokens=192,
        stop=["\n"],
        echo=False
    )
    texto = salida["choices"][0]["text"].strip()
    mensajes.append({"role": "assistant", "content": texto, "fecha": datetime.now().isoformat(), "tema": tema})
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
"""


"""
import socket
import json
import os
from llama_cpp import Llama
from datetime import datetime, timedelta
import subprocess

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

emocion_actual = cargar_estado_emocional()

# Estado inicial del sistema
def get_memoria_inicial():
    return [
        {"role": "system", "content": (
            "Eres Perico, una asistente virtual simpática y fiel que vive dentro de una mascota virtual. "
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
                ahora = datetime.now()
                filtrado = []
                for entrada in data:
                    if isinstance(entrada, dict):
                        fecha = entrada.get("fecha")
                        if fecha:
                            try:
                                fecha_dt = datetime.fromisoformat(fecha)
                                if ahora - fecha_dt < timedelta(days=2):
                                    filtrado.append(entrada)
                            except:
                                pass
                        else:
                            filtrado.append(entrada)
                return filtrado or get_memoria_inicial().copy()
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
    resumen = "\n".join([
        f"{m['role']}: {m['content']}" for m in mensajes[-5:] if m['role'] != 'system']
    )
    prompt = (
        "Eres una mascota virtual llamada Perico.\n"
        "Responde al usuario con simpatía, naturalidad y sin dar listas ni definiciones largas.\n"
        f"Tu estado emocional actual es: {emocion_actual}.\n"
        f"{estilo_emocion(emocion_actual)}\n"
        f"Esta es la conversación reciente:\n{resumen}\n"
        f"Usuario: {texto_usuario}\n"
        f"Perico:"
    )
    return prompt

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

    mensajes.append({"role": "user", "content": texto_usuario, "fecha": datetime.now().isoformat(), "tema": "conversación"})
    if len(mensajes) > 30:
        mensajes[:] = mensajes[:1] + mensajes[-29:]

    prompt = construir_prompt(texto_usuario, emocion_actual)
    salida = llm(
        prompt=prompt,
        temperature=temperatura,
        top_p=0.95,
        max_tokens=192,
        stop=["\n"],
        echo=False
    )
    texto = salida["choices"][0]["text"].strip()
    mensajes.append({"role": "assistant", "content": texto, "fecha": datetime.now().isoformat(), "tema": "respuesta"})
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
"""



"""
import socket
import json
import os
from llama_cpp import Llama
from datetime import datetime
import subprocess

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

emocion_actual = cargar_estado_emocional()

# Estado inicial del sistema
def get_memoria_inicial():
    return [
        {"role": "system", "content": (
            "Eres Perico, una asistente virtual simpática y fiel que vive dentro de una mascota virtual. "
            "Habla de forma cercana, natural y muy concisa. RESPONDE SOLO EN ESPAÑOL."
        )}
    ]

def cargar_memoria():
    if not os.path.exists(ARCHIVO_MEMORIA):
        return get_memoria_inicial().copy()
    try:
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data and isinstance(data[0], dict) and "role" in data[0]:
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

# Generar el sentimiento a partir del input del usuario
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
    resumen = "\n".join([f"{m['role']}: {m['content']}" for m in mensajes[-5:] if m['role'] != 'system'])
    prompt = (
        "Eres una mascota virtual llamada Perico.\n"
        "Responde al usuario con simpatía, naturalidad y sin dar listas ni definiciones largas.\n"
        f"Tu estado emocional actual es: {emocion_actual}.\n"
        f"{estilo_emocion(emocion_actual)}\n"
        f"Esta es la conversación reciente:\n{resumen}\n"
        f"Usuario: {texto_usuario}\n"
        f"Perico:"
    )
    return prompt

# Lógica emocional realista
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

    mensajes.append({"role": "user", "content": texto_usuario})
    if len(mensajes) > 20:
        mensajes[:] = [mensajes[0]] + mensajes[-19:]

    prompt = construir_prompt(texto_usuario, emocion_actual)
    salida = llm(
        prompt=prompt,
        temperature=temperatura,
        top_p=0.95,
        max_tokens=192,
        stop=["\n"],
        echo=False
    )
    texto = salida["choices"][0]["text"].strip()
    mensajes.append({"role": "assistant", "content": texto})
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
"""



"""
import socket
import json
import os
import subprocess
from llama_cpp import Llama
from datetime import datetime

# --- Configuración principal ---
tt = os.cpu_count() or 1

def detectar_gpu():
    try:
        # Verifica si hay una GPU NVIDIA disponible
        salida = subprocess.check_output("nvidia-smi", stderr=subprocess.STDOUT)
        return True
    except Exception:
        return False

usa_gpu = detectar_gpu()
gpu_layers = 100 if usa_gpu else 0
print("GPU detectada. Usando", gpu_layers, "capas en la GPU." if usa_gpu else "No se detectó GPU. Usando CPU solamente.")

llm = Llama(
    model_path="Mistral-7B-Instruct-v0.3-Q4_K_M.gguf",
    n_ctx=2048,
    n_gpu_layers=gpu_layers,
    n_threads=tt,
    verbose=False,
    chat_format="chatml-instruct"
)

ARCHIVO_MEMORIA = "memoria.json"
PUERTO_CHAT = 5050

# Instrucciones iniciales separadas por roles
def get_memoria_inicial():
    return [
        {"role": "system", "content": (
            "Eres Perico, una asistente virtual simpática y fiel que vive dentro de una mascota virtual. "
            "Habla de forma cercana, natural y muy concisa."
        )},
        {"role": "assistant", "content": (
            "RESPONDES SOLO EN ESPAÑOL. No uses otro idioma ni definas términos ni hagas listados. "
            "Si sueles hacerlo, detente inmediatamente después de la primera frase."
        )}
    ]

# Carga/guardar memoria de roles
def cargar_memoria():
    if not os.path.exists(ARCHIVO_MEMORIA):
        return get_memoria_inicial().copy()
    try:
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data and isinstance(data[0], dict) and "role" in data[0]:
                return data
    except:
        pass
    return get_memoria_inicial().copy()

def guardar_memoria(mensajes):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(mensajes, f, ensure_ascii=False, indent=2)

# Análisis de sentimiento contextual
def analizar_sentimiento(texto_actual):
    historial_relevante = [m for m in mensajes if m["role"] in ("user", "assistant")][-5:]
    resumen = "\n".join([f"{m['role']}: {m['content']}" for m in historial_relevante])

    prompt = (
        "Eres una IA emocional que evalúa cómo se siente la mascota virtual Perico según las conversaciones recientes.\n"
        "Determina el sentimiento ACTUAL de Perico tras leer las últimas interacciones.\n"
        "Elige una única palabra en minúsculas entre: alegre, triste, neutral, enfadado o sorprendido.\n"
        f"Historial reciente:\n{resumen}\n"
        f"Nuevo mensaje del usuario: {texto_actual}\n"
        "Estado emocional actual de Perico:"
    )

    respuesta = llm(
        prompt=prompt,
        temperature=0.7,
        max_tokens=6,
        stop=["\n"],
        echo=False,
    )
    return respuesta["choices"][0]["text"].strip().lower().split()[0]

# Estado de personalidad según hora y sentimiento
def estado_personalidad(sentimiento):
    h = datetime.now().hour
    if 6 <= h < 12:
        ener = "despierta y enérgica"
    elif 12 <= h < 18:
        ener = "relajada y atenta"
    elif 18 <= h < 22:
        ener = "amigable y reflexiva"
    else:
        ener = "cuidadora y tranquila"
    return f"Estoy {ener} y me siento {sentimiento}"

# Construir prompt final con contexto y estado emocional adaptado
def construir_prompt(mensajes, sentimiento):
    base = estado_personalidad(sentimiento)

    tono = {
        "alegre": "con entusiasmo y cariño",
        "triste": "con voz bajita y un poco apagada",
        "neutral": "con tono tranquilo",
        "enfadado": "respondiendo con molestia contenida",
        "sorprendido": "algo sorprendido y curioso"
    }.get(sentimiento, "de forma natural")

    prompt = f"[INST] Personalidad: {base}. Responde {tono}. [/INST]"
    for m in mensajes:
        if m["role"] in ("system", "user", "assistant"):
            tag = m["role"]
            prompt += f"[INST] {m['content']} [/INST]" if tag != "assistant" else m['content'] + "\n"
    return prompt

mensajes = cargar_memoria()

# Procesa petición chat: analiza sentimiento e integra en prompt
def procesar_mensaje(texto_usuario):
    senti = analizar_sentimiento(texto_usuario)
    mensajes.append({"role": "user", "content": texto_usuario})
    if len(mensajes) > 20:
        mensajes[:] = [mensajes[0]] + mensajes[-19:]
    prompt = construir_prompt(mensajes, senti)
    resp = llm(
        prompt=prompt,
        temperature=0.7,
        max_tokens=128,
        stop=["\n["],
        echo=False
    )
    cont = resp["choices"][0]["text"].strip()
    mensajes.append({"role": "assistant", "content": cont})
    guardar_memoria(mensajes)
    return cont, senti

# Servidor único
def iniciar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", PUERTO_CHAT))
    s.listen(1)
    print(f"Servidor chat listo en puerto {PUERTO_CHAT}...")
    while True:
        conn, _ = s.accept()
        data = conn.recv(4096).decode("utf-8")
        try:
            pet = json.loads(data)
            texto = pet.get("mensaje", "")
            res, senti = procesar_mensaje(texto)
            conn.sendall(json.dumps({"respuesta": res, "sentimiento": senti}).encode("utf-8"))
        except Exception as e:
            conn.sendall(json.dumps({"error": str(e)}).encode("utf-8"))
        finally:
            conn.close()

if __name__ == "__main__":
    iniciar_servidor()
"""


"""
# main.py bueno
import socket
import json
import os
from llama_cpp import Llama
from datetime import datetime

# --- Configuración principal ---
tt = os.cpu_count() or 1

llm = Llama(
    model_path="mistralai_Mistral-Small-3.1-24B-Instruct-2503-IQ2_XXS.gguf",
    n_ctx=2048,
    n_gpu_layers=8,
    n_threads=tt,
    verbose=False,
    chat_format="chatml-instruct"
)

ARCHIVO_MEMORIA = "memoria.json"
PUERTO_CHAT = 5050

# Instrucciones iniciales separadas por roles
def get_memoria_inicial():
    return [
        {"role": "system", "content": (
            "Eres Perico, una asistente virtual simpática y fiel que vive dentro de una mascota virtual. "
            "Habla de forma cercana, natural y muy concisa."
        )},
        {"role": "assistant", "content": (
            "RESPONDES SOLO EN ESPAÑOL. No uses otro idioma ni definas términos ni hagas listados. "
            "Si sueles hacerlo, detente inmediatamente después de la primera frase."
        )}
    ]

# Carga/guardar memoria de roles

def cargar_memoria():
    if not os.path.exists(ARCHIVO_MEMORIA):
        return get_memoria_inicial().copy()
    try:
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data and isinstance(data[0], dict) and "role" in data[0]:
                return data
    except:
        pass
    return get_memoria_inicial().copy()

def guardar_memoria(mensajes):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(mensajes, f, ensure_ascii=False, indent=2)

# Análisis de sentimiento contextual

def analizar_sentimiento(texto_actual):
    historial_relevante = [m for m in mensajes if m["role"] in ("user", "assistant")][-5:]
    resumen = "\n".join([f"{m['role']}: {m['content']}" for m in historial_relevante])

    prompt = (
        "Eres una IA emocional que evalúa cómo se siente la mascota virtual Perico según las conversaciones recientes.\n"
        "Determina el sentimiento ACTUAL de Perico tras leer las últimas interacciones.\n"
        "Elige una única palabra en minúsculas entre: alegre, triste, neutral, enfadado o sorprendido.\n"
        f"Historial reciente:\n{resumen}\n"
        f"Nuevo mensaje del usuario: {texto_actual}\n"
        "Estado emocional actual de Perico:"
    )

    respuesta = llm(
        prompt=prompt,
        temperature=0,
        max_tokens=6,
        stop=["\n"],
        echo=False
    )
    return respuesta["choices"][0]["text"].strip().lower().split()[0]

# Estado de personalidad según hora y sentimiento

def estado_personalidad(sentimiento):
    h = datetime.now().hour
    if 6 <= h < 12:
        ener = "despierta y enérgica"
    elif 12 <= h < 18:
        ener = "relajada y atenta"
    elif 18 <= h < 22:
        ener = "amigable y reflexiva"
    else:
        ener = "cuidadora y tranquila"
    return f"Estoy {ener} y me siento {sentimiento}"

# Construir prompt final con contexto y estado emocional adaptado

def construir_prompt(mensajes, sentimiento):
    base = estado_personalidad(sentimiento)

    tono = {
        "alegre": "con entusiasmo y cariño",
        "triste": "con voz bajita y un poco apagada",
        "neutral": "con tono tranquilo",
        "enfadado": "respondiendo con molestia contenida",
        "sorprendido": "algo sorprendido y curioso"
    }.get(sentimiento, "de forma natural")

    prompt = f"[INST] Personalidad: {base}. Responde {tono}. [/INST]"
    for m in mensajes:
        if m["role"] in ("system", "user", "assistant"):
            tag = m["role"]
            prompt += f"[INST] {m['content']} [/INST]" if tag != "assistant" else m['content'] + "\n"
    return prompt

mensajes = cargar_memoria()

# Procesa petición chat: analiza sentimiento e integra en prompt

def procesar_mensaje(texto_usuario):
    senti = analizar_sentimiento(texto_usuario)
    mensajes.append({"role": "user", "content": texto_usuario})
    if len(mensajes) > 20:
        mensajes[:] = [mensajes[0]] + mensajes[-19:]
    prompt = construir_prompt(mensajes, senti)
    resp = llm(
        prompt=prompt,
        temperature=0.7,
        max_tokens=128,
        stop=["\n["],
        echo=False
    )
    cont = resp["choices"][0]["text"].strip()
    mensajes.append({"role": "assistant", "content": cont})
    guardar_memoria(mensajes)
    return cont, senti

# Servidor único

def iniciar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", PUERTO_CHAT))
    s.listen(1)
    print(f"Servidor chat listo en puerto {PUERTO_CHAT}...")
    while True:
        conn, _ = s.accept()
        data = conn.recv(4096).decode("utf-8")
        try:
            pet = json.loads(data)
            texto = pet.get("mensaje", "")
            res, senti = procesar_mensaje(texto)
            conn.sendall(json.dumps({"respuesta": res, "sentimiento": senti}).encode("utf-8"))
        except Exception as e:
            conn.sendall(json.dumps({"error": str(e)}).encode("utf-8"))
        finally:
            conn.close()

if __name__ == "__main__":
    iniciar_servidor()
"""




"""
antiguos
import socket
import json
import os
from llama_cpp import Llama

# Carga el modelo
llm = Llama(model_path="mistral-7b-instruct-v0.2.Q3_K_M.gguf", n_ctx=2048)

ARCHIVO_MEMORIA = "memoria.json"

# Instrucciones iniciales si no existe memoria previa o falla al parsear
memoria_inicial = [
    {
        "role": "system",
        "content": (
            "Tu nombre es Botín. Eres un asistente virtual simpático y fiel "
            "que vive en una mascota virtual.\nSiempre hablas en español "
            "y acompañas a tu dueño, Lucas. Nunca dices que eres una IA.\n"
            "Habla de forma cercana y natural."
        )
    }
]

def cargar_memoria():
    if not os.path.exists(ARCHIVO_MEMORIA):
        return memoria_inicial.copy()
    try:
        with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except (json.JSONDecodeError, IOError):
        # Si el JSON está vacío o corrupto, reiniciamos
        return memoria_inicial.copy()
    mensajes = memoria_inicial.copy()
    # Detectar formato antiguo: [{'usuario','bot'},...]
    if raw and isinstance(raw[0], dict) and "usuario" in raw[0]:
        for intercambio in raw:
            mensajes.append({"role": "user",      "content": intercambio["usuario"]})
            mensajes.append({"role": "assistant", "content": intercambio["bot"]})
    # Si ya está en formato de roles
    elif raw and isinstance(raw[0], dict) and "role" in raw[0]:
        mensajes = raw
    return mensajes

def guardar_memoria(mensajes):
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(mensajes, f, ensure_ascii=False, indent=2)

def construir_prompt(mensajes):
    prompt = ""
    for m in mensajes:
        if m["role"] in ("system", "user"):
            prompt += f"[INST] {m['content']} [/INST]"
        else:  # assistant
            prompt += m["content"] + "\n"
    return prompt

mensajes = cargar_memoria()

def procesar_mensaje(texto_usuario):
    mensajes.append({"role": "user", "content": texto_usuario})

    # Limitar historial (incluyendo system inicial)
    if len(mensajes) > 20:
        mensajes[:] = [mensajes[0]] + mensajes[-19:]

    prompt = construir_prompt(mensajes)

    resp = llm(
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        stop=["</s>"],
        echo=False
    )
    # llama_cpp.py devuelve .choices[0]['text']
    contenido = resp["choices"][0]["text"].strip()

    mensajes.append({"role": "assistant", "content": contenido})
    guardar_memoria(mensajes)
    return contenido

def iniciar_servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 5050))
    s.listen(1)
    print("Servidor esperando conexiones en el puerto 5050...")
    while True:
        conn, _ = s.accept()
        data = conn.recv(4096).decode("utf-8")
        try:
            pet = json.loads(data)
            respuesta = procesar_mensaje(pet["mensaje"])
            conn.sendall(respuesta.encode("utf-8"))
        except Exception as e:
            conn.sendall(f"Error procesando el mensaje: {e}".encode("utf-8"))
        finally:
            conn.close()

if __name__ == "__main__":
    iniciar_servidor()
"""

"""
import socket
import json
import os
from llama_cpp import Llama

# ⚙️ Configuración
MODELO_PATH = "mistral-7b-instruct-v0.2.Q3_K_M.gguf"
MEMORIA_FILE = "memoria.json"
N_MEMORIA = 5  # cuántos intercambios pasados usar como contexto
PORT = 5050

# 🧠 Cargar modelo
modelo = Llama(model_path=MODELO_PATH, n_ctx=2048,n_gpu_layers=20, verbose=True)

# 🧠 Cargar memoria
def cargar_memoria():
    if os.path.exists(MEMORIA_FILE):
        with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 💾 Guardar nuevo intercambio
def guardar_en_memoria(usuario, bot):
    memoria = cargar_memoria()
    memoria.append({"usuario": usuario, "bot": bot})
    with open(MEMORIA_FILE, "w", encoding="utf-8") as f:
        json.dump(memoria[-50:], f, indent=2, ensure_ascii=False)

# 🤖 Preparar prompt con contexto
def construir_prompt(pregunta):
    memoria = cargar_memoria()[-N_MEMORIA:]
    historial = "\n".join([f"Usuario: {m['usuario']}\nBot: {m['bot']}" for m in memoria])
    prompt = f"{historial}\nUsuario: {pregunta}\nBot:"
    return f"[INST] {prompt} [/INST]"

# 🎙️ Escuchar por socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', PORT))
s.listen(1)
print(f"Servidor con memoria listo en puerto {PORT}")

while True:
    conn, addr = s.accept()
    data = conn.recv(4096).decode("utf-8")
    if not data:
        conn.close()
        continue
    try:
        entrada = json.loads(data)
        prompt = construir_prompt(entrada["mensaje"])
        respuesta = modelo(prompt, max_tokens=150, stop=["</s>"])["choices"][0]["text"].strip()
        guardar_en_memoria(entrada["mensaje"], respuesta)
        conn.sendall(respuesta.encode("utf-8"))
    except Exception as e:
        conn.sendall(f"Error: {str(e)}".encode("utf-8"))
    conn.close()
"""
