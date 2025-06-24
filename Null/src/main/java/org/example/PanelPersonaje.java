package org.example;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.net.URL;

// java class PanelPersonaje
class PanelPersonaje extends JPanel {

    /**
     * Un panel personalizado que carga y dibuja la imagen de la mascota.
     */

    private Image imagenPersonaje;
    private Image iconoEstado; // Variable para la imagen del icono

    public PanelPersonaje(String rutaRecurso) {
        setOpaque(false); // Esencial para que el fondo del panel sea transparente

        // --- LÓGICA DE CARGA DE RECURSOS MEJORADA ---
        URL urlImagen = getClass().getResource(rutaRecurso);
        if (urlImagen == null) {
            System.err.println("Recurso no encontrado: " + rutaRecurso);
            // Muestra un error visual si la imagen no se encuentra
            JOptionPane.showMessageDialog(this,
                    "No se pudo encontrar la imagen de la mascota en: " + rutaRecurso,
                    "Error de Recurso",
                    JOptionPane.ERROR_MESSAGE);
        } else {
            try {
                imagenPersonaje = ImageIO.read(urlImagen);
            } catch (IOException e) {
                e.printStackTrace();
                // Muestra un error si hay problemas al leer el archivo de imagen
                JOptionPane.showMessageDialog(this,
                        "Error al leer el archivo de imagen.",
                        "Error de I/O",
                        JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (imagenPersonaje != null) {
            // Dibuja la imagen, escalándola para que ocupe todo el panel
            g.drawImage(imagenPersonaje, 0, 0, this.getWidth(), this.getHeight(), this);
        }

        // 2. Dibuja el icono de estado encima, si existe
        if (iconoEstado != null) {
            // Posición: Arriba a la derecha. Puedes cambiar los números para moverlo.
            int iconoX = this.getWidth() - 28; // 24px de ancho del icono + 4px de margen
            int iconoY = 5; // 5px desde el borde superior
            g.drawImage(iconoEstado, iconoX, iconoY, 24, 24, this); // Dibuja el icono a 24x24px
        }
    }

    public void cambiarImagen(String rutaRecurso) {
        URL urlImagen = getClass().getResource(rutaRecurso);
        if (urlImagen == null) {
            System.err.println("Recurso no encontrado: " + rutaRecurso);
            return;
        }
        try {
            this.imagenPersonaje = ImageIO.read(urlImagen);
            // ¡Muy importante! Llama a repaint() para que se muestre la nueva imagen.
            this.repaint();
        } catch (IOException e) {
            e.printStackTrace();
            // Opcional: mostrar un diálogo de error
        }
    }

    // Método para establecer el icono de estado
    public void setIconoEstado(String rutaRecursoIcono) {
        if (rutaRecursoIcono == null) {
            this.iconoEstado = null;
        } else {
            URL urlIcono = getClass().getResource(rutaRecursoIcono);
            if (urlIcono != null) {
                try {
                    this.iconoEstado = ImageIO.read(urlIcono);
                } catch (IOException e) {
                    e.printStackTrace();
                    this.iconoEstado = null;
                }
            }
        }
        this.repaint(); // Redibuja el panel para mostrar el cambio
    }

}
