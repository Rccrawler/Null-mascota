package org.example;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.net.URL;

class PanelPersonaje extends JPanel {

    /**
     * Un panel personalizado que carga y dibuja la imagen de la mascota.
     */

    private Image imagenPersonaje;

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
    }
}
