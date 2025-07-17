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
