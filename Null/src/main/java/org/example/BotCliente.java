package org.example;

import utiles.TimerUtil;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class BotCliente {
    public static String preguntarAlBot(String mensaje) {
        try (Socket socket = new Socket("localhost", 5050)) {
            OutputStream os = socket.getOutputStream();
            String json = "{\"mensaje\":\"" + mensaje + "\"}";
            os.write(json.getBytes("UTF-8"));
            os.flush();

            BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream(), "UTF-8"));
            return br.readLine();
        } catch (IOException e) {
            return "Error al conectar con el bot: " + e.getMessage();
        }
    }

    public static void main(String[] args) {

        TimerUtil timer = new TimerUtil();
        Scanner scanner = new Scanner(System.in);

        timer.start();

        String respuesta1 = preguntarAlBot("Hola, ¿quién eres?");
        System.out.println("Bot: " + respuesta1);

        String respuesta2 = preguntarAlBot("¿Quien te ha puesto ese nonbre?");
        System.out.println("Bot: " + respuesta2);

        // Mistral model .gguf                          haciertos    tempo
        // mistral-7b-instruct-v0.2.Q3_K_M                 3/5
        // Mistral-7B-Instruct-v0.3-Q3_K_M                 /5
        // Mistral-7B-Instruct-v0.3-Q4_K_M                 /5
        // Mistral-7B-Instruct-v0.3-Q5_K_S                 /5
        // mistralai_Magistral-Small-2506-IQ2_M            /5
        // Mistral-Small-3.2-24B-Instruct-2506-UD-IQ2_XXS  /5

        // Probamos la calidad del bot con una pregunta difícil
        String respuesta3 = preguntarAlBot("Cual es la pregunta mas difícil que te han hecho?");
        System.out.println("Bot: "+" 1 " + respuesta3);

        String respuesta4 = preguntarAlBot("Cuantas e tien la palabra apache");
        System.out.println("Bot: "+" 2 " + respuesta4);

        String respuesta5 = preguntarAlBot("Puedes decirme el resultado de esta operación: 7 - 7:1x1+3?");
        System.out.println("Bot: "+" 3 " + respuesta5);

        String respuesta6 = preguntarAlBot("Puedes traducirme esto hal español: 'Hello, how are you?'");
        System.out.println("Bot: "+" 4 " + respuesta6);

        String respuesta7 = preguntarAlBot("Creame un programa de Java que imprima 'Hola Mundo' en la consola");
        System.out.println("Bot: "+" 5 " + respuesta7);

        timer.stop();
    }
}
