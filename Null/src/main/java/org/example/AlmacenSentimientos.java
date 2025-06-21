package org.example;

// java class AlmacenSentimientos
public class AlmacenSentimientos {

    private int FELICIDAD;
    private int ENFADO;
    private int TRISTEZA;
    private int GANAS_DE_JUGAR; // 1 si 0 no
    private int SALUD;

    public AlmacenSentimientos() {
        LectorConfiguraciones config = new LectorConfiguraciones("config.txt");
        this.FELICIDAD = Integer.parseInt(config.obtenerVariable("FELICIDAD"));
        this.ENFADO = Integer.parseInt(config.obtenerVariable("ENFADO"));
        this.TRISTEZA = Integer.parseInt(config.obtenerVariable("TRISTEZA"));
        this.GANAS_DE_JUGAR = Integer.parseInt(config.obtenerVariable("GANAS_DE_JUGAR"));
        this.SALUD = Integer.parseInt(config.obtenerVariable("SALUD"));
    }

    public int guardarSentimientos() {
        LectorConfiguraciones config = new LectorConfiguraciones("config.txt");
        config.guardarVariable("FELICIDAD", String.valueOf(FELICIDAD));
        config.guardarVariable("ENFADO", String.valueOf(ENFADO));
        config.guardarVariable("TRISTEZA", String.valueOf(TRISTEZA));
        config.guardarVariable("GANAS_DE_JUGAR", String.valueOf(GANAS_DE_JUGAR));
        config.guardarVariable("SALUD", String.valueOf(SALUD));
        return 0; // Retorno de éxito
    }

    public int getFELICIDAD() {
        return FELICIDAD;
    }

    public void setFELICIDAD(int FELICIDAD) {
        this.FELICIDAD = FELICIDAD;
    }

    public int getENFADO() {
        return ENFADO;
    }

    public void setENFADO(int ENFADO) {
        this.ENFADO = ENFADO;
    }

    public int getTRISTEZA() {
        return TRISTEZA;
    }

    public void setTRISTEZA(int TRISTEZA) {
        this.TRISTEZA = TRISTEZA;
    }

    public int getGANAS_DE_JUGAR() {
        return GANAS_DE_JUGAR;
    }

    public void setGANAS_DE_JUGAR(int GANAS_DE_JUGAR) {
        this.GANAS_DE_JUGAR = GANAS_DE_JUGAR;
    }

    public int getSALUD() {
        return SALUD;
    }

    public void setSALUD(int SALUD) {
        this.SALUD = SALUD;
    }
}
