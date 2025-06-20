package org.example;
import java.io.*;
import java.util.HashMap;
import java.util.Map;

// java class LectorConfiguraciones
public class LectorConfiguraciones {
    private final File archivo;
    private final Map<String, String> configuraciones = new HashMap<>();

    public LectorConfiguraciones(String rutaArchivo) {
        this.archivo = new File(rutaArchivo);
        cargarDesdeArchivo(); // Carga automáticamente al crear la instancia
    }

    // Guarda una variable
    public void guardarVariable(String clave, String valor) {
        configuraciones.put(clave, valor);
        guardarEnArchivo();
    }

    // Leer una variable
    public String obtenerVariable(String clave) {
        return configuraciones.get(clave);
    }

    // Cargar todas las variables del archivo
    private void cargarDesdeArchivo() {
        if (!archivo.exists()) return;

        try (BufferedReader br = new BufferedReader(new FileReader(archivo))) {
            String linea;
            while ((linea = br.readLine()) != null) {
                if (linea.trim().isEmpty() || !linea.contains("=")) continue;
                String[] partes = linea.split("=", 2);
                configuraciones.put(partes[0].trim(), partes[1].trim());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Guardar todas las variables en el archivo
    private void guardarEnArchivo() {
        try (BufferedWriter bw = new BufferedWriter(new FileWriter(archivo))) {
            for (Map.Entry<String, String> entrada : configuraciones.entrySet()) {
                bw.write(entrada.getKey() + "=" + entrada.getValue());
                bw.newLine();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Mostrar todas las configuraciones por consola (opcional)
    public void mostrarConfiguraciones() {
        configuraciones.forEach((k, v) -> System.out.println(k + " = " + v));
    }
}


/*
public class Main {
    public static void main(String[] args) {
        LectorConfiguraciones config = new LectorConfiguraciones("config.txt");

        config.guardarVariable("usuario", "juan");
        config.guardarVariable("tema", "oscuro");

        String usuario = config.obtenerVariable("usuario");
        System.out.println("Usuario cargado: " + usuario);

        config.mostrarConfiguraciones(); // Opcional
    }
}
 */