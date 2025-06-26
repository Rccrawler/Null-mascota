package org.example;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class MascotaDesktop {

    // --- 1. CONSTANTES Y VARIABLES DE LA CLASE ---
    private static final int ANCHO_MASCOTA = 48;
    private static final int ALTO_MASCOTA = 140;
    private static final String RUTA_BASE_IMAGENES = "resources/";

    // Las rutas ahora no llevan la barra "/" al principio.
    private static final String RUTA_IMAGEN_INICIAL = RUTA_BASE_IMAGENES + "null-normal.png";
    //private static final String RUTA_IMAGEN_INICIAL = "/null-normal.png";
    private static String NOMBRE_MASCOTA = "NULL";
    protected static AlmacenSentimientos sentimientos = new AlmacenSentimientos();

    // Solo necesitamos UNA instancia del panel de la mascota y UNA del bocadillo
    static PanelPersonaje panelMascota = new PanelPersonaje(RUTA_IMAGEN_INICIAL);
    static PanelBocadillo panelBocadillo = new PanelBocadillo();

    public static void main(String[] args) {
        // --- INICIALIZACIÓN ---
        LectorConfiguraciones config = new LectorConfiguraciones("config.txt");
        NOMBRE_MASCOTA = config.obtenerVariable("NOMBRE_MASCOTA");
        actualizarEdad(config);

        // --- ARRANQUE DE LA INTERFAZ Y LÓGICA ---
        SwingUtilities.invokeLater(MascotaDesktop::crearYMostrarGui);
        iniciarAnimacion();
        iniciarPensamientos();
    }

    private static void actualizarEdad(LectorConfiguraciones config) {
        LocalDate hoy = LocalDate.now();
        String fechaGuardadaTexto = config.obtenerVariable("ultimaEjecucion");

        if (fechaGuardadaTexto != null && !fechaGuardadaTexto.isBlank()) {
            LocalDate fechaGuardada = LocalDate.parse(fechaGuardadaTexto);
            if (fechaGuardada.isBefore(hoy)) {
                long diasPasados = ChronoUnit.DAYS.between(fechaGuardada, hoy);
                String edadActualStr = config.obtenerVariable("EDAD_MASCOTA_DIAS");
                long edadActual = 0;
                try {
                    edadActual = Long.parseLong(edadActualStr);
                } catch (NumberFormatException e) {
                    System.err.println("La edad guardada no era un número. Se reinicia a 0.");
                }
                long nuevaEdad = edadActual + diasPasados;
                System.out.println("Han pasado " + diasPasados + " días. La nueva edad es: " + nuevaEdad);
                config.guardarVariable("EDAD_MASCOTA_DIAS", String.valueOf(nuevaEdad));
            }
        } else {
            config.guardarVariable("EDAD_MASCOTA_DIAS", "0");
        }
        config.guardarVariable("ultimaEjecucion", hoy.toString());
    }

    private static void iniciarAnimacion() {
        // Ejecuta la animación en un hilo separado para no bloquear la interfaz
        new Thread(() -> estado(true, true, true, "contento")).start();
    }

    private static void estado(boolean parpadeoActivo, boolean dejarEsperaAntes, boolean respiracionActivo, String estado) {
        String estadoDefecto;
        switch (estado) {
            case "contento": estadoDefecto = RUTA_BASE_IMAGENES + "/null-contento.png"; break;
            // Añade más casos aquí...
            default: estadoDefecto = RUTA_BASE_IMAGENES + "/null-normal.png"; break;
        }

        if (dejarEsperaAntes) {
            try { Thread.sleep(6000); } catch (InterruptedException e) { e.printStackTrace(); }
        }

        while (parpadeoActivo) {
            // Animación de parpadeo
            panelMascota.cambiarImagen(estadoDefecto);
            try { Thread.sleep(80); } catch (InterruptedException e) { e.printStackTrace(); }
            panelMascota.cambiarImagen(RUTA_BASE_IMAGENES + "/null-normal-parpadeo-2.png");
            try { Thread.sleep(80); } catch (InterruptedException e) { e.printStackTrace(); }
            panelMascota.cambiarImagen(RUTA_BASE_IMAGENES + "/null-normal-parpadeo-3.png");
            try { Thread.sleep(80); } catch (InterruptedException e) { e.printStackTrace(); }
            panelMascota.cambiarImagen(RUTA_BASE_IMAGENES + "/null-normal-parpadeo-4.png");
            try { Thread.sleep(80); } catch (InterruptedException e) { e.printStackTrace(); }
            panelMascota.cambiarImagen(RUTA_BASE_IMAGENES + "/null-normal-parpadeo-5.png");
            try { Thread.sleep(80); } catch (InterruptedException e) { e.printStackTrace(); }

            // Animación de respiración
            if(respiracionActivo){
                panelMascota.cambiarImagen(estadoDefecto);
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(140);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                panelMascota.cambiarImagen(RUTA_BASE_IMAGENES + "/null-normal-respiracion-2.png");
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(140);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                panelMascota.cambiarImagen(RUTA_BASE_IMAGENES + "/null-normal-respiracion-3.png");
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(140);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                panelMascota.cambiarImagen(RUTA_BASE_IMAGENES + "/null-normal-respiracion-4.png");
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(140);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                panelMascota.cambiarImagen(estadoDefecto);
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(4080);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

        }
    }

    private static void iniciarPensamientos() {
        // Un Timer que se ejecuta una vez después de 5 segundos para mostrar el bocadillo
        Timer timerMostrar = new Timer(5000, e -> {
            mostrarBocadillo("¡Tengo una idea!");
            // Otro Timer para ocultar el bocadillo 4 segundos después
            Timer timerOcultar = new Timer(4000, ev -> ocultarBocadillo());
            timerOcultar.setRepeats(false);
            timerOcultar.start();
        });
        timerMostrar.setRepeats(false);
        timerMostrar.start();
    }

    public static void mostrarBocadillo(String mensaje) {
        panelBocadillo.setTexto(mensaje);
        panelBocadillo.setVisible(true);
    }

    public static void ocultarBocadillo() {
        panelBocadillo.setVisible(false);
    }

    private static void crearYMostrarGui() {
        // --- 1. CREACIÓN Y CONFIGURACIÓN DE LA VENTANA PRINCIPAL (JFrame) ---
        JFrame frame = new JFrame();
        frame.setSize(200, ALTO_MASCOTA + 50); // Tamaño total para mascota y bocadillo
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setUndecorated(true);
        frame.setAlwaysOnTop(true);
        frame.setBackground(new Color(0, 0, 0, 0));
        frame.getContentPane().setLayout(null); // Usamos layout nulo para posicionar a mano

        // --- 2. POSICIONAMIENTO DE LOS COMPONENTES ---
        // Se posicionan con setBounds(x, y, ancho, alto)
        panelMascota.setBounds(100, 40, ANCHO_MASCOTA, ALTO_MASCOTA);
        panelBocadillo.setBounds(10, 0, 150, 60);
        panelBocadillo.setVisible(false); // Oculto al inicio

        // --- 3. AÑADIR COMPONENTES A LA VENTANA ---
        frame.getContentPane().add(panelBocadillo);
        frame.getContentPane().add(panelMascota);

        // --- 4. CONFIGURAR INTERACCIONES ---
        JPopupMenu menuContextual = crearMenuContextual(frame);
        panelMascota.setComponentPopupMenu(menuContextual); // El menú va en el panel de la mascota
        configurarArrastreYMenu(frame, panelMascota, menuContextual);

        ToolTipManager.sharedInstance().registerComponent(panelMascota);

        // B. Establecemos el texto que queremos que aparezca.
        panelMascota.setToolTipText(NOMBRE_MASCOTA);

        // --- 5. HACER VISIBLE LA VENTANA ---
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }

    private static void configurarArrastreYMenu(JFrame frame, JPanel panel, JPopupMenu menu) {
        final Point[] initialClick = new Point[1];
        MouseAdapter adapter = new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                if (e.isPopupTrigger()) {
                    menu.show(e.getComponent(), e.getX(), e.getY());
                } else {
                    initialClick[0] = e.getPoint();
                }
            }

            @Override
            public void mouseDragged(MouseEvent e) {
                if (initialClick[0] == null) return;
                int xOnScreen = e.getXOnScreen();
                int yOnScreen = e.getYOnScreen();
                frame.setLocation(xOnScreen - initialClick[0].x, yOnScreen - initialClick[0].y);
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                if (e.isPopupTrigger()) {
                    menu.show(e.getComponent(), e.getX(), e.getY());
                }
                initialClick[0] = null;
            }
        };
        panel.addMouseListener(adapter);
        panel.addMouseMotionListener(adapter);
    }

    private static JPopupMenu crearMenuContextual(JFrame frame) {
        JPopupMenu menu = new JPopupMenu();

        JMenuItem tituloMenu = new JMenuItem(NOMBRE_MASCOTA);
        tituloMenu.setEnabled(false);
        tituloMenu.setFont(new Font("Segoe UI", Font.BOLD, 14));
        tituloMenu.setHorizontalAlignment(SwingConstants.CENTER);
        menu.add(tituloMenu);
        menu.addSeparator();

        menu.add("Jugar");

        menu.add("Ablar");

        menu.addSeparator();

        JMenuItem itemInfo = new JMenuItem("Info");
        itemInfo.addActionListener(e -> {
            LectorConfiguraciones infoConfig = new LectorConfiguraciones("config.txt");
            String edad = infoConfig.obtenerVariable("EDAD_MASCOTA_DIAS");

            String mensaje = "<html>" +
                    "<b>Tu mascota:</b> " + NOMBRE_MASCOTA + "<br>" +
                    "<b>es una mascota muy especial.</b><br>" +
                    "<b>Puedes comunicarte con ella</b><br>" +
                    "<b>no solo a través del chat,</b><br>" +
                    "<b>sino también mediante el sistema</b><br>" +
                    "<b>operativo o navegador.</b><br>" +
                    "<b>Puede enfadarse o ayudarte,</b><br>" +
                    "<b>dependiendo de cómo la trates.</b><br>" +
                    "<b>Edad de la mascota (en días):</b> " + edad + "<br>" +
                    "<b>Repositorio GitHub:</b> <a href='https://github.com/Rccrawler/Null-mascota.git'>Null Mascota</a><br>" +
                    "</html>";

            JOptionPane.showMessageDialog(frame, mensaje, "Información de la Mascota", JOptionPane.INFORMATION_MESSAGE);
        });
        menu.add(itemInfo);

        menu.add("Ajustes");
        menu.addSeparator();

        JMenuItem itemSalir = new JMenuItem("Salir");
        itemSalir.addActionListener(e -> {
            sentimientos.guardarSentimientos();
            // Animación de salida opcional
            new Thread(() -> {
                panelMascota.cambiarImagen(RUTA_BASE_IMAGENES + "/null-exit.png");
                try { Thread.sleep(1500); } catch (InterruptedException ex) {}
                System.exit(0);
            }).start();
        });
        menu.add(itemSalir);

        return menu;
    }
}