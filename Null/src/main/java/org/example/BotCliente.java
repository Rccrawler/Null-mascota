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

        boolean probar_modelos = false; // Cambiar a true si quieres probar los modelos

        timer.start();

        String respuesta1 = preguntarAlBot("Hola, ¿quién eres?");
        System.out.println("Bot: " + respuesta1);

        String respuesta2 = preguntarAlBot("¿Quien te ha puesto ese nonbre?");
        System.out.println("Bot: " + respuesta2);
        

        if (probar_modelos){
            // añadir limite de uso de cpu o grafica demasiada tenperatura
            // limitar el pensamiento del sentimiento
            // probar modelo original sin cuantizar
            // Problema con lo de recordar respuestas tarda demasiado
            // Mistral model .gguf                          haciertos    tempo   tiempo-pregunta7                       usar
            // mistral-7b-instruct-v0.2.Q3_K_M                 3/5       08:15   01:16                                   NO
            // Mistral-7B-Instruct-v0.3-Q3_K_M                 3/5       08:51   01:21                                   NO
            // Mistral-7B-Instruct-v0.3-Q4_K_M                 3/5       01:30   00:18   //mejor domino del español       1
            // Mistral-7B-Instruct-v0.3-Q5_K_S                 2/5       03:26   00:57   //mas consumidora
            // mistralai_Magistral-Small-2506-IQ2_M            3/5       03:38   00:48   // lentisimo con mucho contexto NO
            // Mistral-Small-3.2-24B-Instruct-2506-UD-IQ2_XXS  4/5       08:01   01:14   // Mas lijera lentisnimo        NO
            // mistralai_Mistral-Small-3.1-24B-Instruct-2503-Q4_K_M  4/5 04:05   00:57   // Mejores tenperaturas          5
            // mistralai_Mistral-Small-3.1-24B-Instruct-2503-IQ2_XXS 2/5 09:40   01:34   // Poca precision               NO
            // mistralai_Mistral-Small-3.1-24B-Instruct-2503-Q4_K_S  4/5 03:08   00:44   // Velocidad inpecable           3
            // mistralai_Mistral-Small-3.1-24B-Instruct-2503-Q6_K    3/5 04:19   00:59
            // Ministral-3b-instruct.Q8_0                  error    /5
            // Ministral-3b-instruct.Q4_K_M                error    /5
            // Ministral-8B-Instruct-2410-Q4_K_M                   4/5   00:59   00:09  //  respuestas cortas             2
            // Ministral-8B-Instruct-2410-Q8_0                     4/5   01:19max 00:17  //  respuestas cortas            NO por tamño
            // Ministral-8B-Instruct-2410-f16                      4/5   01:56   00:22  //  ligermanete mas lista         4
            // Mistral-Nemo-12B-Instruct-2407-Q4_K_M                /5   00:36   no sabe                                  6

            // Ultimas pruebas
            // Mistral model .gguf                               haciertos    tempo
            // Ministral-8B-Instruct-2410-Q8_0                      4/7        01:38  02:18 con sentimientos      // solid fayo
            // Mistral-7B-Instruct-v0.3-Q4_K_M                      4/7        02:59
            // mistralai_Mistral-Small-3.1-24B-Instruct-2503-Q4_K_M 4/7        04:41
            // mistralai_Mistral-Small-3.1-24B-Instruct-2503-Q4_K_S 5/7        04:59

            // Probamos la calidad del bot con una pregunta difícil
            String respuesta3 = preguntarAlBot("Cual es la pregunta mas difícil que te han hecho?"); // respuesta larga
            System.out.println("Bot: "+" 1 " + respuesta3);

            String respuesta4 = preguntarAlBot("Cuantas e tien la palabra apache"); // tiene una e
            System.out.println("Bot: "+" 2 " + respuesta4);

            String respuesta5 = preguntarAlBot("Puedes decirme el resultado de esta operación: 7 - 7:1x1+3?"); //7 - 7 = 0 0 + 3 = 3
            System.out.println("Bot: "+" 3 " + respuesta5);

            String respuesta6 = preguntarAlBot("Puedes traducirme esto hal español: 'Hello, how are you?'"); //Hola, cómo estás
            System.out.println("Bot: "+" 4 " + respuesta6);

            String respuesta7 = preguntarAlBot("Creame un programa de Java que imprima 'Hola Mundo' en la consola"); // programa
            System.out.println("Bot: "+" 5 " + respuesta7);

            String respuesta8 = preguntarAlBot("Quién escribió los principios SOLID"); // Robert C. Martin
            System.out.println("Bot: "+" 6 " + respuesta8);

            String respuesta9 = preguntarAlBot("Eugenio murió después de una larga vida de 87 años, pero en su tumba escribieron el siguiente epitafio: “Eugenio vivió una buena y larga vida – Él amaba a sus hijo y a su bella esposa –Él era bueno, generoso y merecía lo mejor – Aunque solo tuviera 21 cumpleaños.”¿Cómo es posible esto?");
            System.out.println("Bot: "+" 7 " + respuesta9); //Respuesta: Eugenio nació el 29 de febrero en unaño bisiesto. Consecuentemente, a sus 87 años, solo tuvo 21 cumpleaños. En los demás años no hubo un 29 de febrero.>"""
        }

        timer.stop();
    }
}
