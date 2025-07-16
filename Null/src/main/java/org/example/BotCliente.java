package org.example;

import java.io.*;
import java.net.*;

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
        String respuesta1 = preguntarAlBot("Hola, ¿quién eres?");
        System.out.println("Bot: " + respuesta1);

        String respuesta2 = preguntarAlBot("¿Quien te ha puesto ese nonbre?");
        System.out.println("Bot: " + respuesta2);
    }
}
