package org.example;

import org.json.JSONObject;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.List;

public class VentanaChat extends JFrame {

    private JTextArea areaConversacion;
    private JTextField campoMensaje;
    private JButton botonEnviar;

    private List<String> historial = new ArrayList<>();

    private String nombreMascota;
    private AlmacenSentimientos sentimientos;

    public VentanaChat(String nombreMascota) {
        this.nombreMascota = nombreMascota;

        // Cargar configuración y sentimientos
        LectorConfiguraciones config = new LectorConfiguraciones("config.txt");
        this.sentimientos = new AlmacenSentimientos();

        setTitle("Chat con " + nombreMascota);
        setSize(400, 500);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLayout(new BorderLayout());

        areaConversacion = new JTextArea();
        areaConversacion.setEditable(false);
        areaConversacion.setLineWrap(true);
        JScrollPane scroll = new JScrollPane(areaConversacion);

        campoMensaje = new JTextField();
        botonEnviar = new JButton("Enviar");

        JPanel panelInferior = new JPanel(new BorderLayout());
        panelInferior.add(campoMensaje, BorderLayout.CENTER);
        panelInferior.add(botonEnviar, BorderLayout.EAST);

        add(scroll, BorderLayout.CENTER);
        add(panelInferior, BorderLayout.SOUTH);

        // Eventos
        botonEnviar.addActionListener(e -> enviarMensaje());
        campoMensaje.addActionListener(e -> enviarMensaje());
    }

    private void enviarMensaje() {
        String mensajeUsuario = campoMensaje.getText().trim();
        if (mensajeUsuario.isEmpty()) return;

        agregarAlChat("Tú: " + mensajeUsuario);
        campoMensaje.setText("");

        new Thread(() -> {
            String respuestaJson = BotCliente.preguntarAlBot(mensajeUsuario);
            procesarRespuesta(respuestaJson);
        }).start();
    }

    private void procesarRespuesta(String json) {
        try {
            JSONObject obj = new JSONObject(json);
            String respuesta = obj.getString("respuesta");
            String sentimiento = obj.getString("sentimiento");

            agregarAlChat(nombreMascota + ": " + respuesta);

            int estadoEmocional = mapearSentimiento(sentimiento);
            sentimientos.setESTADO_EMOCIONAL(estadoEmocional);
            sentimientos.guardarSentimientos();

        } catch (Exception e) {
            agregarAlChat(nombreMascota + ": [Error al procesar respuesta]");
        }
    }

    private int mapearSentimiento(String sentimiento) {
        return switch (sentimiento.toLowerCase()) {
            case "alegre" -> 1;
            case "triste" -> 2;
            case "enfadado" -> 3;
            case "euforico" -> 4;
            case "ansioso" -> 5;
            case "esperanzado" -> 6;
            case "decepcionado" -> 7;
            case "calmado" -> 8;
            case "furioso" -> 9;
            case "sorprendido" -> 10;
            case "frustrado" -> 11;
            default -> 0;
        };
    }

    private void agregarAlChat(String mensaje) {
        historial.add(mensaje);
        SwingUtilities.invokeLater(() -> {
            areaConversacion.append(mensaje + "\n");
        });
    }
}



/*
package org.example;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;

public class VentanaChat extends JFrame {

    private JTextArea areaConversacion;
    private JTextField campoMensaje;
    private JButton botonEnviar;

    private java.util.List<String> historial = new ArrayList<>();

    public VentanaChat(String nombreMascota) {
        setTitle("Chat con " + nombreMascota);
        setSize(400, 500);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setLayout(new BorderLayout());

        areaConversacion = new JTextArea();
        areaConversacion.setEditable(false);
        areaConversacion.setLineWrap(true);
        JScrollPane scroll = new JScrollPane(areaConversacion);

        campoMensaje = new JTextField();
        botonEnviar = new JButton("Enviar");

        JPanel panelInferior = new JPanel(new BorderLayout());
        panelInferior.add(campoMensaje, BorderLayout.CENTER);
        panelInferior.add(botonEnviar, BorderLayout.EAST);

        add(scroll, BorderLayout.CENTER);
        add(panelInferior, BorderLayout.SOUTH);

        botonEnviar.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                enviarMensaje();
            }
        });

        campoMensaje.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                enviarMensaje();
            }
        });
    }

    private void enviarMensaje() {
        String mensajeUsuario = campoMensaje.getText().trim();
        if (mensajeUsuario.isEmpty()) return;

        agregarAlChat("Tú: " + mensajeUsuario);
        campoMensaje.setText("");

        new Thread(() -> {
            String respuestaJson = BotCliente.preguntarAlBot(mensajeUsuario);
            String respuestaFormateada = procesarRespuestaJson(respuestaJson);
            agregarAlChat("🐾 " + respuestaFormateada);
        }).start();
    }

    private String procesarRespuestaJson(String json) {
        try {
            org.json.JSONObject obj = new org.json.JSONObject(json);
            return obj.getString("respuesta"); // Asumimos que el JSON contiene {"respuesta": "..."}
        } catch (Exception e) {
            return "Error al procesar la respuesta.";
        }
    }

    private void agregarAlChat(String mensaje) {
        historial.add(mensaje);
        SwingUtilities.invokeLater(() -> {
            areaConversacion.append(mensaje + "\n");
        });
    }
}
*/