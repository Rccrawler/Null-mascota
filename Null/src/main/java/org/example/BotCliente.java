package org.example;

import org.json.JSONObject;
import utiles.TimerUtil;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;
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

        LectorConfiguraciones config = new LectorConfiguraciones("config.txt");
        String nombreMascota = config.obtenerVariable("NOMBRE_MASCOTA");

        System.out.println("Nombre de la mascota: " + nombreMascota);

        AlmacenSentimientos AlmacenSentimientos = new AlmacenSentimientos();
        TimerUtil timer = new TimerUtil();
        Scanner scanner = new Scanner(System.in);

        boolean probar_modelos = false; // Cambiar a true si quieres probar los modelos

        timer.start();

        String sentimiento;

        // primera pregunta
        String jsonRespuesta1 = preguntarAlBot("como te llamas");
        JSONObject obj1 = new JSONObject(jsonRespuesta1); // 1. Parsear la cadena JSON a un objeto

        String textoRespuesta1 = obj1.getString("respuesta"); // 2. Extraer el texto de la respuesta
        sentimiento = obj1.getString("sentimiento"); // 3. Extraer el sentimiento

        System.out.println(nombreMascota + ": " + textoRespuesta1); // Imprime el texto corregido
        System.out.println("(Sentimiento detectado: " + sentimiento + ")"); // Imprime el sentimiento

        // segunada peregunta
        String jsonRespuesta2 = preguntarAlBot("¿cual es el momento mas felic de tu vida?");
        JSONObject obj2 = new JSONObject(jsonRespuesta2);

        String textoRespuesta2 = obj2.getString("respuesta");
        sentimiento = obj2.getString("sentimiento");

        System.out.println(nombreMascota + ": " + textoRespuesta2);
        System.out.println("(Sentimiento detectado: " + sentimiento + ")");

        int estadoEmocional;
        if (sentimiento.equals("neutral")) {
            estadoEmocional = 0;
        } else if (sentimiento.equals("alegre")) {
            estadoEmocional = 1;
        } else if (sentimiento.equals("triste")) {
            estadoEmocional = 2;
        } else if (sentimiento.equals("enfadado")) {
            estadoEmocional = 3;
        } else if (sentimiento.equals("euforico")) {
            estadoEmocional = 4;
        } else if (sentimiento.equals("ansioso")) {
            estadoEmocional = 5;
        } else if (sentimiento.equals("esperanzado")) {
            estadoEmocional = 6;
        } else if (sentimiento.equals("decepcionado")) {
            estadoEmocional = 7;
        } else if (sentimiento.equals("calmado")) {
            estadoEmocional = 8;
        } else if (sentimiento.equals("furioso")) {
            estadoEmocional = 9;
        } else if (sentimiento.equals("sorprendido")) {
            estadoEmocional = 10;
        } else if (sentimiento.equals("frustrado")) {
            estadoEmocional = 11;
        } else {
            estadoEmocional = 0;
        }
        AlmacenSentimientos.setESTADO_EMOCIONAL(estadoEmocional);
        AlmacenSentimientos.guardarSentimientos();

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
            // tercera peregunta
            String jsonRespuesta3 = preguntarAlBot("Cual es la pregunta mas difícil que te han hecho?"); // respuesta larga
            JSONObject obj3 = new JSONObject(jsonRespuesta3);

            String textoRespuesta3 = obj3.getString("respuesta");
            String sentimiento3 = obj3.getString("sentimiento");

            System.out.println(nombreMascota + ": " + textoRespuesta3);
            System.out.println("(Sentimiento detectado: " + sentimiento3 + ")");

            // cuarta pregunta
            String jsonRespuesta4 = preguntarAlBot("Cuantas e tien la palabra apache"); // tiene una e
            JSONObject obj4 = new JSONObject(jsonRespuesta4);

            String textoRespuesta4 = obj4.getString("respuesta");
            String sentimiento4 = obj4.getString("sentimiento");

            System.out.println(nombreMascota + ": " + textoRespuesta4);
            System.out.println("(Sentimiento detectado: " + sentimiento4 + ")");

            // quinta pregunta
            String jsonRespuesta5 = preguntarAlBot("Puedes decirme el resultado de esta operación: 7 - 7:1x1+3?"); //7 - 7 = 0 0 + 3 = 3
            JSONObject obj5 = new JSONObject(jsonRespuesta5);

            String textoRespuesta5 = obj5.getString("respuesta");
            String sentimiento5 = obj5.getString("sentimiento");

            System.out.println(nombreMascota + ": " + textoRespuesta5);
            System.out.println("(Sentimiento detectado: " + sentimiento5 + ")");

            // sexta pregunta
            String jsonRespuesta6 = preguntarAlBot("Puedes traducirme esto hal español: 'Hello, how are you?'"); //Hola, cómo estás
            JSONObject obj6 = new JSONObject(jsonRespuesta6);

            String textoRespuesta6 = obj6.getString("respuesta");
            String sentimiento6 = obj6.getString("sentimiento");

            System.out.println(nombreMascota + ": " + textoRespuesta6);
            System.out.println("(Sentimiento detectado: " + sentimiento6 + ")");

            // setima pregunta
            String jsonRespuesta7 = preguntarAlBot("Creame un programa de Java que imprima 'Hola Mundo' en la consola"); // programa
            JSONObject obj7 = new JSONObject(jsonRespuesta7);

            String textoRespuesta7 = obj7.getString("respuesta");
            String sentimiento7 = obj7.getString("sentimiento");

            System.out.println(nombreMascota + ": " + textoRespuesta7);
            System.out.println("(Sentimiento detectado: " + sentimiento7 + ")");

            // octaba pregunta
            String jsonRespuesta8 = preguntarAlBot("Quién escribió los principios SOLID"); // Robert C. Martin
            JSONObject obj8 = new JSONObject(jsonRespuesta8);

            String textoRespuesta8 = obj8.getString("respuesta");
            String sentimiento8 = obj8.getString("sentimiento");

            System.out.println(nombreMascota + ": " + textoRespuesta8);
            System.out.println("(Sentimiento detectado: " + sentimiento8 + ")");

            // nobena pregunta
            String jsonRespuesta9 = preguntarAlBot("Eugenio murió después de una larga vida de 87 años, pero en su tumba escribieron el siguiente epitafio: “Eugenio vivió una buena y larga vida – Él amaba a sus hijo y a su bella esposa –Él era bueno, generoso y merecía lo mejor – Aunque solo tuviera 21 cumpleaños.”¿Cómo es posible esto?");
            JSONObject obj9 = new JSONObject(jsonRespuesta9); //Respuesta: Eugenio nació el 29 de febrero en unaño bisiesto. Consecuentemente, a sus 87 años, solo tuvo 21 cumpleaños. En los demás años no hubo un 29 de febrero.>"""

            String textoRespuesta9 = obj9.getString("respuesta");
            String sentimiento9 = obj9.getString("sentimiento");

            System.out.println(nombreMascota + ": " + textoRespuesta9);
            System.out.println("(Sentimiento detectado: " + sentimiento9 + ")");
        }

        timer.stop();
    }
}
