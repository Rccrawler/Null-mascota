package org.example;

// java class AlmacenSentimientos
public class AlmacenSentimientos {

    private int ESTADO_EMOCIONAL; // 0 neutral, 1 alegre, 2 triste", 3 enfadado, 4 euforico, 5 ansioso, 6 esperanzado, 7 decepcionado, 8 calmado, 9 furioso, 10 sorprendido, 11 frustrado
    private int GANAS_DE_JUGAR; // 1 si 0 no
    private int SALUD; // 0 enfermo, 1 sano

    public AlmacenSentimientos() {
        LectorConfiguraciones config = new LectorConfiguraciones("config.txt");
        this.ESTADO_EMOCIONAL = Integer.parseInt(config.obtenerVariable("ESTADO_EMOCIONAL"));
        this.GANAS_DE_JUGAR = Integer.parseInt(config.obtenerVariable("GANAS_DE_JUGAR"));
        this.SALUD = Integer.parseInt(config.obtenerVariable("SALUD"));
    }

    public int guardarSentimientos() {
        LectorConfiguraciones config = new LectorConfiguraciones("config.txt");
        config.guardarVariable("ESTADO_EMOCIONAL", String.valueOf(ESTADO_EMOCIONAL));
        config.guardarVariable("GANAS_DE_JUGAR", String.valueOf(GANAS_DE_JUGAR));
        config.guardarVariable("SALUD", String.valueOf(SALUD));
        return 0; // Retorno de éxito
    }

    public int getESTADO_EMOCIONAL() {
        return ESTADO_EMOCIONAL;
    }

    public void setESTADO_EMOCIONAL(int ESTADO_EMOCIONAL) {
        this.ESTADO_EMOCIONAL = ESTADO_EMOCIONAL;
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
