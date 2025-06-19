package org.example;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

public class MascotaDesktop {

    // --- 1. CONSTANTES PARA CONFIGURACIÓN ---
    // Definimos los "números mágicos" como constantes. Así es más fácil cambiarlos después.
    private static final int ANCHO_MASCOTA = 150;
    private static final int ALTO_MASCOTA = 150;
    private static final String RUTA_IMAGEN = "/Marshadow.png"; // Ruta relativa a la carpeta 'resources'
    private static final String NOMBRE_MASCOTA = "NULL";

    public static void main(String[] args) {
        // Ejecuta la creación de la GUI en el hilo de eventos de Swing para seguridad.
        SwingUtilities.invokeLater(MascotaDesktop::crearYMostrarGui);
    }

    private static void pensamiento() {

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
        PanelPersonaje panel = new PanelPersonaje(RUTA_IMAGEN);

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
        itemSalir.addActionListener(e -> System.exit(0));
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

