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
