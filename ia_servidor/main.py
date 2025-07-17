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
