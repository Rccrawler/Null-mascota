package org.example;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.File; // CAMBIO: Importamos la clase File para manejar archivos externos.
import java.io.IOException;
// CAMBIO: Ya no necesitamos java.net.URL

/**
 * Un panel especializado que muestra la imagen de un personaje.
 * Esta versión está modificada para cargar imágenes desde una ruta de archivo
 * externa, permitiendo que las imágenes se cambien sin recompilar el programa.
 */
class PanelPersonaje extends JPanel {

    private Image imagenPersonaje;
    private Image iconoEstado; // Variable para la imagen del icono de estado

    /**
     * Constructor que carga la imagen inicial de la mascota desde una ruta de archivo.
     * @param rutaArchivo La ruta relativa o absoluta al archivo de imagen inicial.
     *                    (Ej: "imagenes/null-normal.png")
     */
    public PanelPersonaje(String rutaArchivo) {
        setOpaque(false); // Esencial para que el fondo del panel sea transparente

        // --- LÓGICA DE CARGA DESDE ARCHIVO EXTERNO ---
        File archivoImagen = new File(rutaArchivo);

        if (!archivoImagen.exists()) { // Comprobamos si el archivo existe en la ruta especificada
            System.err.println("Error: Archivo de imagen no encontrado en la ruta: " + rutaArchivo);
            // Muestra un error visual si la imagen no se encuentra, indicando la ruta completa.
            JOptionPane.showMessageDialog(this,
                    "No se pudo encontrar la imagen de la mascota en:\n" + archivoImagen.getAbsolutePath(),
                    "Error de Archivo",
                    JOptionPane.ERROR_MESSAGE);
        } else {
            try {
                // Leemos la imagen directamente desde el archivo
                imagenPersonaje = ImageIO.read(archivoImagen);
            } catch (IOException e) {
                e.printStackTrace();
                // Muestra un error si hay problemas al leer el archivo de imagen
                JOptionPane.showMessageDialog(this,
                        "Hubo un error al leer el archivo de imagen.",
                        "Error de Lectura (I/O)",
                        JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    /**
     * Este método se encarga de dibujar el componente en la pantalla.
     * Lo sobreescribimos para dibujar nuestra imagen de personaje.
     */
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        if (imagenPersonaje != null) {
            // Dibuja la imagen, escalándola para que ocupe todo el tamaño del panel
            g.drawImage(imagenPersonaje, 0, 0, this.getWidth(), this.getHeight(), this);
        }

        // Dibuja el icono de estado encima de la imagen principal, si existe
        if (iconoEstado != null) {
            // Posición: Arriba a la derecha.
            int iconoX = this.getWidth() - 28; // 24px de ancho del icono + 4px de margen
            int iconoY = 5; // 5px desde el borde superior
            g.drawImage(iconoEstado, iconoX, iconoY, 24, 24, this); // Dibuja el icono a 24x24px
        }
    }

    /**
     * Cambia la imagen actual del personaje por una nueva desde un archivo externo.
     * @param rutaArchivo La ruta al nuevo archivo de imagen.
     */
    public void cambiarImagen(String rutaArchivo) {
        File archivoImagen = new File(rutaArchivo);
        if (!archivoImagen.exists()) {
            System.err.println("Error al cambiar: Archivo de imagen no encontrado en " + rutaArchivo);
            return; // No hacemos nada si la nueva imagen no se encuentra
        }
        try {
            this.imagenPersonaje = ImageIO.read(archivoImagen);
            // ¡Muy importante! Llama a repaint() para que Swing redibuje el panel y se muestre la nueva imagen.
            this.repaint();
        } catch (IOException e) {
            e.printStackTrace();
            System.err.println("Error al leer el archivo de imagen: " + rutaArchivo);
        }
    }

    /**
     * Establece o elimina el icono de estado que se muestra sobre la mascota.
     * @param rutaArchivoIcono La ruta al archivo del icono, o null para quitar el icono.
     */
    public void setIconoEstado(String rutaArchivoIcono) {
        if (rutaArchivoIcono == null) {
            this.iconoEstado = null; // Si la ruta es nula, eliminamos el icono
        } else {
            File archivoIcono = new File(rutaArchivoIcono);
            if (archivoIcono.exists()) {
                try {
                    this.iconoEstado = ImageIO.read(archivoIcono);
                } catch (IOException e) {
                    e.printStackTrace();
                    this.iconoEstado = null; // Si hay error, no mostramos icono
                }
            } else {
                this.iconoEstado = null; // Si no existe el archivo, no mostramos icono
            }
        }
        this.repaint(); // Redibuja el panel para mostrar u ocultar el icono
    }
}



/*
package org.example;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.io.IOException;
import java.net.URL;

// java class PanelPersonaje
class PanelPersonaje extends JPanel {

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
*/