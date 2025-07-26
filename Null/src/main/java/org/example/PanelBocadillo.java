package org.example;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.net.URL;

public class PanelBocadillo extends JPanel {

    private Image imagenFondo;
    private String texto = "";

    public PanelBocadillo() {
        setOpaque(false); // Hacemos el panel transparente

        // Cargamos la imagen del bocadillo
        URL urlImagen = getClass().getResource("/iconos/bocadillo-comic.png");
        if (urlImagen != null) {
            try {
                imagenFondo = ImageIO.read(urlImagen);
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    // Método para cambiar el texto que se muestra
    public void setTexto(String nuevoTexto) {
        this.texto = nuevoTexto;
        this.repaint(); // Pedimos que se redibuje el panel para mostrar el nuevo texto
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);

        // 1. Dibujamos la imagen de fondo del bocadillo
        if (imagenFondo != null) {
            g.drawImage(imagenFondo, 0, 0, this.getWidth(), this.getHeight(), this);
        }

        // 2. Dibujamos el texto encima de la imagen
        if (texto != null && !texto.isEmpty()) {
            Graphics2D g2d = (Graphics2D) g;

            // Hacemos que el texto se vea más suave
            g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

            // Configuramos la fuente y el color
            g2d.setColor(Color.BLACK);
            g2d.setFont(new Font("Arial", Font.BOLD, 12));

            // Calculamos la posición para centrar el texto (aproximado)
            FontMetrics fm = g2d.getFontMetrics();
            int x = (this.getWidth() - fm.stringWidth(texto)) / 2;
            int y = (this.getHeight() - fm.getHeight()) / 2 + fm.getAscent() - 5; // Pequeño ajuste hacia arriba

            g2d.drawString(texto, x, y);
        }
    }
}