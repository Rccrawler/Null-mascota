package org.example;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

// java class MascotaDesktop
public class MascotaDesktop {

    // --- 1. CONSTANTES PARA CONFIGURACIÓN ---
    // Definimos los "números mágicos" como constantes. Así es más fácil cambiarlos después.
    private static final int ANCHO_MASCOTA = 48;// 150 original
    private static final int ALTO_MASCOTA = 140;// 150 original
    private static String RUTA_IMAGEN = "/null-normal.png"; // Ruta relativa a la carpeta 'resources'
    private static String NOMBRE_MASCOTA = "NULL"; // Nombre por defecto de la mascota
    protected static AlmacenSentimientos sentimientos = new AlmacenSentimientos(); // Cargar la clase de los sentimientos de la mascota

    static PanelPersonaje panel = new PanelPersonaje(RUTA_IMAGEN);// defino la clase ha qui para poder haceder desde cualquier sitio ya que se necesita en barios metodos

    public static void main(String[] args) {
        // Ejecuta la creación de la GUI en el hilo de eventos de Swing para seguridad.
        SwingUtilities.invokeLater(MascotaDesktop::crearYMostrarGui);

        LectorConfiguraciones config = new LectorConfiguraciones("config.txt"); // Ruta del archivo de configuración
        NOMBRE_MASCOTA = config.obtenerVariable("NOMBRE_MASCOTA"); // Leer la variable 'usuario' del archivo de configuración
        LocalDate hoy = LocalDate.now();

        String fechaGuardadaTexto = config.obtenerVariable("ultimaEjecucion");

        if (fechaGuardadaTexto != null && !fechaGuardadaTexto.isBlank()) {

            LocalDate fechaGuardada = LocalDate.parse(fechaGuardadaTexto);

            if (fechaGuardada.isBefore(hoy)) {
                long diasPasados = ChronoUnit.DAYS.between(fechaGuardada, hoy) + 1;
                System.out.println("Han pasado " + diasPasados + " días desde la última ejecución.");

                // Guardar el total de días pasados
                config.guardarVariable("EDAD_MASCOTA_DIAS", String.valueOf(diasPasados));
            }
        }

        config.guardarVariable("ultimaEjecucion", hoy.toString());
        pensamiento();
    }

    private static boolean parpadeoActivo = false; // Variable para controlar el parpadeo
    private static void pensamiento() {
        parpadeoYrespiracion(true, true, true);
    }

    private static void parpadeoYrespiracion(boolean parpadeoActivo, boolean dejarEsperaAntes, boolean RespiracionActivo) {
        while (parpadeoActivo){

            if (dejarEsperaAntes) {
                try {
                    Thread.sleep(6000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                dejarEsperaAntes = false;
            }

            // Parpadeo de la mascota
            panel.cambiarImagen("/null-normal-parpadeo-1.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            panel.cambiarImagen("/null-normal-parpadeo-2.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            panel.cambiarImagen("/null-normal-parpadeo-3.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            panel.cambiarImagen("/null-normal-parpadeo-4.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            panel.cambiarImagen("/null-normal-parpadeo-5.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            // Respiración de la mascota
            if(RespiracionActivo){
                panel.cambiarImagen("/null-normal-respiracion-1.png");
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(140);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                panel.cambiarImagen("/null-normal-respiracion-2.png");
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(140);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                panel.cambiarImagen("/null-normal-respiracion-3.png");
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(140);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                panel.cambiarImagen("/null-normal-respiracion-4.png");
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(140);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                panel.cambiarImagen("/null-normal-respiracion-5.png");
                try {
                    // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                    Thread.sleep(4080);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }


            // Parpadeo de la mascota
            panel.cambiarImagen("/null-normal-parpadeo-1.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            panel.cambiarImagen("/null-normal-parpadeo-2.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            panel.cambiarImagen("/null-normal-parpadeo-3.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            panel.cambiarImagen("/null-normal-parpadeo-4.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            panel.cambiarImagen("/null-normal-parpadeo-5.png");
            try {
                // Pausa la ejecución durante 2 segundos (2000 milisegundos)
                Thread.sleep(80);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }


    private static void crearYMostrarGui() {
        // --- 2. CONFIGURACIÓN DE LA VENTANA (JFrame) ---
        JFrame frame = new JFrame();
        frame.setSize(ANCHO_MASCOTA, ALTO_MASCOTA);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        // Configuración para que sea una mascota de escritorio
        frame.setUndecorated(true);      // Sin bordes ni barra de título
        frame.setAlwaysOnTop(true);      // Siempre encima de otras ventanas
        frame.setBackground(new Color(0, 0, 0, 0)); // Fondo 100% transparente

        // --- 3. CREACIÓN DE COMPONENTES ---
        // El panel que contendrá y dibujará nuestra imagen
        //PanelPersonaje panel = new PanelPersonaje(RUTA_IMAGEN);

        // El menú que aparece al hacer clic derecho
        JPopupMenu menuContextual = crearMenuContextual(frame);
        panel.setComponentPopupMenu(menuContextual);

        // --- 4. LÓGICA DE INTERACCIÓN (ARRASTRE) ---
        configurarArrastreYMenu(frame, panel, menuContextual);

        // --- 5. ENSAMBLAJE Y VISUALIZACIÓN ---
        frame.add(panel);
        frame.setLocationRelativeTo(null); // Centra la ventana al iniciar
        frame.setVisible(true);
    }

    /**
     * Configura los listeners para permitir que la ventana se arrastre con el ratón.
     */
    private static void configurarArrastreYMenu(JFrame frame, JPanel panel, JPopupMenu menu) {
        final Point[] initialClick = new Point[1];

        // Se crea un único "escuchador" (Adapter) para todos los eventos de ratón.
        MouseAdapter adapter = new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                // Comprueba si el clic es el que debe mostrar el menú (normalmente clic derecho)
                if (e.isPopupTrigger()) {
                    menu.show(e.getComponent(), e.getX(), e.getY());
                } else {
                    // Si es cualquier otro clic, lo usamos para empezar a arrastrar.
                    initialClick[0] = e.getPoint();
                }
            }

            @Override
            public void mouseDragged(MouseEvent e) {
                // Solo arrastra si el clic inicial no es nulo (es decir, se empezó con un clic izquierdo)
                if (initialClick[0] == null) {
                    return;
                }

                // Lógica de arrastre correcta usando coordenadas de la pantalla
                int xOnScreen = e.getXOnScreen();
                int yOnScreen = e.getYOnScreen();

                int nuevaX = xOnScreen - initialClick[0].x;
                int nuevaY = yOnScreen - initialClick[0].y;

                frame.setLocation(nuevaX, nuevaY);
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                // Se comprueba también al soltar el clic, por compatibilidad con Windows y otros SO
                if (e.isPopupTrigger()) {
                    menu.show(e.getComponent(), e.getX(), e.getY());
                }
                // Al soltar el botón, se reinicia el punto de clic para el próximo arrastre.
                initialClick[0] = null;
            }
        };

        // Se añade el mismo "escuchador" al panel para ambos tipos de evento.
        panel.addMouseListener(adapter);
        panel.addMouseMotionListener(adapter);
    }

    /**
     * Crea y devuelve el JPopupMenu con las opciones para la mascota.
     * CAMBIO: Ya no necesita el parámetro 'frame'.
     */
    private static JPopupMenu crearMenuContextual() {
        JPopupMenu menu = new JPopupMenu();
        menu.add("Hablar"); // Desplegar un chat
        menu.add("Jugar");

        menu.addSeparator();

        JMenuItem itemSalir = new JMenuItem("Salir");
        itemSalir.addActionListener(e -> {
            sentimientos.guardarSentimientos(); // Llama a la función antes de salir
            System.exit(0);
        });
        menu.add(itemSalir);

        return menu;
    }

    /**
     * Crea y devuelve el JPopupMenu con las opciones para la mascota.
     */
    private static JPopupMenu crearMenuContextual(JFrame frame) {

        JPopupMenu menu = new JPopupMenu();

        JMenuItem tituloMenu = new JMenuItem(NOMBRE_MASCOTA);
        tituloMenu.setEnabled(false);
        tituloMenu.setFont(new Font("Segoe UI", Font.BOLD, 14));
        tituloMenu.setHorizontalAlignment(SwingConstants.CENTER);
        menu.add(tituloMenu);
        menu.addSeparator();

        menu.add("Hablar"); // Desplegar un chat
        menu.add("Jugar");
        menu.addSeparator(); // Línea separadora
        menu.add("info");
        menu.add("ajustes"); // Desplegar un diálogo de configuración
        // indicador de comida y que ponga la bateria del ordenador

        menu.addSeparator(); // Línea separadora

        JMenuItem itemSalir = new JMenuItem("Salir");
        itemSalir.addActionListener(e -> System.exit(0));
        menu.add(itemSalir);

        return menu;
    }
}

