# Null — Mascota virtual con emociones

Null es un proyecto de mascota virtual con personalidad, animaciones y respuestas generadas por IA. La idea principal es que la mascota viva en el escritorio, reaccione a la interacción del usuario y muestre estados emocionales que cambian con el tiempo y con el tipo de conversación.

Este repositorio combina una aplicación Java de escritorio con un servidor local de IA en Python para generar respuestas y detectar emociones.

---

## ✨ Características principales

- Interfaz gráfica en Swing para una mascota animada
- Sistema de estados emocionales y cambios de humor
- Memoria y contexto de conversación
- Movimientos autónomos en la pantalla
- Respuestas generadas por un modelo local de lenguaje
- Personalización del nombre de la mascota a través de configuración
- Comunicación entre la parte Java y el backend de IA

---

## 🧩 Estructura del proyecto

- `Null/` — aplicación desktop principal desarrollada en Java
- `ia_servidor/` — servidor local en Python con llama.cpp y un modelo GGUF
- `LICENSE` — licencia del proyecto
- `arranque.txt` — notas de ejecución rápida

### Dentro de `Null/`

- `src/main/java/org/example/` — lógica principal de la mascota
- `config.txt` — configuración del nombre y estado de la mascota
- `resources/` — imágenes y assets gráficos
- `pom.xml` — configuración de Maven

### Dentro de `ia_servidor/`

- `main.py` — backend de IA y servidor socket
- `requeriments.txt` — dependencias de Python
- modelos `.gguf` — modelos locales usados para generar respuestas

---

## 🛠️ Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Java 17+
- Maven 3.9+
- Python 3.10+
- pip
- Un modelo GGUF compatible en la carpeta `ia_servidor/`

> El proyecto usa `llama.cpp` a través de Python, por lo que el modelo local debe estar disponible para que el servidor pueda responder.

---

## 🚀 Instalación y ejecución

### 1) Clonar el repositorio

```bash
git clone https://github.com/Rccrawler/Null-mascota.git
cd Null-mascota
```

### 2) Ejecutar el servidor de IA

```bash
cd ia_servidor
python -m venv .venv
# En Windows
.venv\Scripts\activate
pip install -r requeriments.txt
python main.py
```

Asegúrate de que el modelo GGUF esté en la misma carpeta o ajusta la ruta del archivo en `main.py` si es necesario.

### 3) Ejecutar la mascota desktop

Abre otra terminal y ejecuta:

```bash
cd Null
mvn clean compile
java -cp target/classes org.example.MascotaDesktop
```

Si prefieres, también puedes abrir el proyecto en IntelliJ IDEA o VS Code y ejecutar la clase `org.example.MascotaDesktop` desde el IDE.

---

## ⚙️ Configuración

El archivo `Null/config.txt` contiene datos como:

```txt
NOMBRE_MASCOTA=NULL
ESTADO_EMOCIONAL=0
EDAD_MASCOTA_DIAS=92
GANAS_DE_JUGAR=1
```

Puedes modificar el nombre de la mascota o cambiar valores de estado según tu uso del proyecto.

---

## 🧠 Cómo funciona

La aplicación desktop se comunica con el servidor local mediante sockets. El servidor analiza el texto del usuario, detecta emoción y genera una respuesta natural con un modelo local de lenguaje. La mascota refleja ese estado en su comportamiento visual y emocional.

---

## 📌 Notas

- El proyecto está pensado como una mascota virtual local y experimental.
- La calidad y velocidad de las respuestas dependen del modelo GGUF elegido y del hardware disponible.
- Es una base ideal para ampliar con más animaciones, memoria, personalidad o integración con más servicios.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si quieres mejorar la mascota, añadir nuevos estados emocionales, optimizar la IA o pulir la interfaz, puedes abrir un pull request o proponer cambios en el repositorio.

---

## 📄 Licencia

Este proyecto se distribuye bajo la licencia [LICENSE](LICENSE).

