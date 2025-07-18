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




""" # funciona bien
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
EMOCIONES = ["alegre", "triste", "neutral", "enfadado", "sorprendido"]

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

# Construcción del prompt con estado emocional
mensajes = cargar_memoria()

def construir_prompt(texto_usuario, emocion_actual):
    resumen = "\n".join([f"{m['role']}: {m['content']}" for m in mensajes[-5:] if m['role'] != 'system'])
    prompt = (
        "Eres una mascota virtual llamada Perico.\n"
        "Responde al usuario con simpatía, naturalidad y sin dar listas ni definiciones largas.\n"
        f"Tu estado emocional actual es: {emocion_actual}.\n"
        f"Esta es la conversación reciente:\n{resumen}\n"
        f"Usuario: {texto_usuario}\n"
        f"Perico:"
    )
    return prompt

# Lógica emocional realista
def actualizar_emocion(emocion_previa, nueva_emocion):
    if nueva_emocion == "neutral":
        return emocion_previa  # mantener estado si neutral
    if emocion_previa == "triste" and nueva_emocion == "alegre":
        return "neutral"  # mejora progresiva
    if emocion_previa == "enfadado" and nueva_emocion == "alegre":
        return "sorprendido"  # transición brusca
    if emocion_previa == nueva_emocion:
        return emocion_previa
    return nueva_emocion

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
from llama_cpp import Llama
from datetime import datetime
import subprocess

def hay_gpu():
    try:
        salida = subprocess.check_output(["nvidia-smi"], stderr=subprocess.DEVNULL)
        return b"NVIDIA" in salida
    except:
        return False

# Configuración de hilos
tt = os.cpu_count() or 1

# Si hay GPU, usamos capas aceleradas
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
PUERTO_CHAT = 5050

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
        "describe", "haz un resumen", "razona"
    ]):
        return 0.7
    return 0.4

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

mensajes = cargar_memoria()

def construir_prompt_con_sentimiento(mensajes, texto_usuario):
    resumen = "\n".join([f"{m['role']}: {m['content']}" for m in mensajes[-5:] if m['role'] != 'system'])

    prompt = (
        "Eres una mascota virtual llamada Perico.\n"
        "Responde al usuario con simpatía, naturalidad y sin dar listas ni definiciones largas.\n"
        f"Esta es la conversación reciente:\n{resumen}\n"
        f"Usuario: {texto_usuario}\n"
        "Ahora responde como Perico y al final, di entre corchetes cómo se siente (alegre, triste, neutral, enfadado o sorprendido).\n"
        "Perico:"
    )
    return prompt

def procesar_mensaje(texto_usuario):
    temperatura = ajustar_temperature(texto_usuario)
    mensajes.append({"role": "user", "content": texto_usuario})
    if len(mensajes) > 20:
        mensajes[:] = [mensajes[0]] + mensajes[-19:]

    prompt = construir_prompt_con_sentimiento(mensajes, texto_usuario)

    salida = llm(
        prompt=prompt,
        temperature=temperatura,
        top_p=0.95,
        max_tokens=192,
        stop=["\n"],
        echo=False
    )

    texto_bruto = salida["choices"][0]["text"].strip()
    texto_limpio = texto_bruto
    sentimiento = "neutral"

    if "[" in texto_bruto and "]" in texto_bruto:
        posible = texto_bruto.split("[")[-1].split("]")[0].strip().lower()
        if posible in ["alegre", "triste", "neutral", "enfadado", "sorprendido"]:
            sentimiento = posible
            texto_limpio = texto_bruto.split("[")[0].strip()

    mensajes.append({"role": "assistant", "content": texto_limpio})
    guardar_memoria(mensajes)
    return texto_limpio, sentimiento

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
# main.py
import socket
import json
import os
from llama_cpp import Llama
from datetime import datetime

# --- Configuración principal ---
tt = os.cpu_count() or 1

llm = Llama(
    model_path="Ministral-8B-Instruct-2410-Q8_0.gguf",
    n_ctx=2048,
    n_gpu_layers=50,
    n_threads=tt,
    verbose=False,
    n_batch=64,
    chat_format="chatml-instruct"
)

_ = llm("Hola", max_tokens=1, echo=False)  # warm-up rápido

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

# NUEVA: Ajustar temperatura según tipo de pregunta
def ajustar_temperature(texto):
    texto = texto.lower()
    if any(p in texto for p in [
        "explica", "por qué", "cómo funciona", "qué significa",
        "quién escribió", "cuáles son los principios", "define", "compara",
        "describe", "haz un resumen", "razona"
    ]):
        return 0.7  # Más razonamiento
    return 0.4  # Default para charla

mensajes = cargar_memoria()

# Procesa petición chat: analiza sentimiento e integra en prompt
def procesar_mensaje(texto_usuario):
    senti = analizar_sentimiento(texto_usuario)
    mensajes.append({"role": "user", "content": texto_usuario})
    if len(mensajes) > 20:
        mensajes[:] = [mensajes[0]] + mensajes[-19:]
    prompt = construir_prompt(mensajes, senti)
    temp = ajustar_temperature(texto_usuario)

    resp = llm(
        prompt=prompt,
        temperature=temp,
        top_p=0.95,
        max_tokens=192,
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
    model_path="Ministral-8B-Instruct-2410-Q8_0.gguf",
    n_ctx=2048,
    n_gpu_layers=50,
    n_threads=tt,
    verbose=False,
    n_batch=64,
    chat_format="chatml-instruct"
)

_ = llm("Hola", max_tokens=1, echo=False)  # warm-up rápido


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
        temperature=0.4,
        top_p=0.95,
        max_tokens=192,
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
