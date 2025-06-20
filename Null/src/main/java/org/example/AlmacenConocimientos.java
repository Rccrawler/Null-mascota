package org.example;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.google.gson.GsonBuilder;

import java.io.*;
import java.lang.reflect.Type;
import java.util.*;

// java class AlmacenConocimientos
public class AlmacenConocimientos {
    private static final String ARCHIVO = "conocimiento.json";
    private final Gson gson = new GsonBuilder().setPrettyPrinting().create();
    private List<Entrada> conocimiento;

    public AlmacenConocimientos() {
        conocimiento = cargarConocimiento();
    }

    // Clase interna para representar una entrada de pregunta-respuesta
    private static class Entrada {
        String pregunta;
        String respuesta;
    }

    // Cargar desde el archivo JSON
    private List<Entrada> cargarConocimiento() {
        File file = new File(ARCHIVO);
        if (!file.exists()) return new ArrayList<>();

        try (Reader reader = new FileReader(file)) {
            Type listType = new TypeToken<List<Entrada>>() {}.getType();
            return gson.fromJson(reader, listType);
        } catch (IOException e) {
            e.printStackTrace();
            return new ArrayList<>();
        }
    }

    // Guardar toda la lista
    private void guardarConocimiento() {
        try (Writer writer = new FileWriter(ARCHIVO)) {
            gson.toJson(conocimiento, writer);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Agregar nueva pregunta-respuesta
    public void agregar(String pregunta, String respuesta) {
        Entrada nueva = new Entrada();
        nueva.pregunta = pregunta;
        nueva.respuesta = respuesta;
        conocimiento.add(nueva);
        guardarConocimiento();
    }

    // Buscar respuesta exacta
    public String buscarExacto(String pregunta) {
        for (Entrada e : conocimiento) {
            if (e.pregunta.equalsIgnoreCase(pregunta)) {
                return e.respuesta;
            }
        }
        return null;
    }

    // Buscar respuesta con coincidencia parcial
    public List<String> buscarRelativa(String fragmento) {
        List<String> respuestas = new ArrayList<>();
        for (Entrada e : conocimiento) {
            if (e.pregunta.toLowerCase().contains(fragmento.toLowerCase())) {
                respuestas.add(e.respuesta);
            }
        }
        return respuestas;
    }
}


/*
AlmacenConocimientos almacen = new AlmacenConocimientos();

// Agregar datos nuevos
almacen.agregar("¿Cuál es tu nombre?", "Me llamo Mascota AI");

// Buscar exacto
String respuesta1 = almacen.buscarExacto("¿Qué es Java?");
System.out.println(respuesta1);

// Buscar relativa
List<String> respuestasRelativas = almacen.buscarRelativa("java");
for (String r : respuestasRelativas) {
    System.out.println("Relativa: " + r);
}
 */