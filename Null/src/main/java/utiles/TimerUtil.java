/**
 * Program TimerUtil
 * Description measures the execution time of programs
 * @author Rccrawler
 * @version 2.0
 * @see References: https://github.com/Rccrawler
 */

package utiles;

import java.util.ArrayList;
import java.util.Scanner;

public class TimerUtil {
    private long inicio;
    private long pausado;
    private boolean isMeasuring;
    private boolean modificacion = false;
    private ArrayList<Integer> ListaTenposAñadir = new ArrayList<>();

    public void addTime(int nanosegundos){
        pause();
        ListaTenposAñadir.add(nanosegundos);
        this.modificacion = true;
        resume();
    }

    public TimerUtil() {
        this.isMeasuring = false;
        this.pausado = 0;
    }

    // Start the timer
    public void start() {
        if (!isMeasuring) {
            inicio = System.nanoTime() - pausado; // We adjust for when it has been paused
            isMeasuring = true;
            System.out.println("Timer started.");
        }
    }

    // Pause the timer
    public void pause() {
        if (isMeasuring) {
            pausado = System.nanoTime() - inicio; // We save the time elapsed before pausing
            isMeasuring = false;
            System.out.println("Timer paused.");
        }
    }

    // Restart the timer
    public void resume() {
        if (!isMeasuring) {
            start(); // Resumes the timer if it has been paused
            System.out.println("Timer resumed.");
        }
    }

    // Stops the timer and displays the elapsed time in digital clock format
    public void stop() {
        if (isMeasuring) {
            long fin = System.nanoTime();
            long tiempoTotal = fin - inicio; // time in nanoseconds

            // Add additional time (if any)
            if (modificacion) {
                for (int tiempo : ListaTenposAñadir) {
                    tiempoTotal += tiempo;  // Add each added time
                }
            }

            // We convert nanoseconds to milliseconds, then to seconds, minutes and hours
            long milisegundos = tiempoTotal / 1_000_000;
            long segundos = milisegundos / 1000;
            long minutos = segundos / 60;
            long horas = minutos / 60;

            // We calculate the remaining values ​​to obtain the correct format
            segundos = segundos % 60;
            minutos = minutos % 60;
            milisegundos = milisegundos % 1000;

            // Print the result in "HH:mm:ss:SSS" format
            System.out.println(" ");
            System.out.println("TimerUtil ----------- ho|mi|se|milliseconds");
            System.out.println(" Execution time: " + "(" + String.format("%02d:%02d:%02d:%03d", horas, minutos, segundos, milisegundos) + ")" + " weather modification: " + modificacion);
            isMeasuring = false; // We indicate that we have finished measuring
        } else {
            System.out.println("The timer has not started.");
        }
    }
}

/*
public static void main(String[] args) {
    TimerUtil timer = new TimerUtil();
    Scanner scanner = new Scanner(System.in);

    // Example of code execution without timing user input
    System.out.println("Antes de iniciar la medición...");
    System.out.print("Introduce un número (esto no será medido en el tiempo): ");
    int numero = scanner.nextInt(); // This reading will not be measured on the stopwatch.

    // Here we start measuring the time of a block of code
    timer.start();

    // We pause the measurement while the program waits for user interaction
    timer.pause(); // We pause the stopwatch before reading the entry

    // We simulate the user waiting for input
    System.out.println("Realiza alguna operación o espera...");
    scanner.nextLine(); // Simulates that the user is doing something

    // We resume measurement after the user has interacted
    timer.resume();

    // Here goes the code whose duration we want to measure
    for (int i = 0; i < 1_000_000; i++) {
        Math.sqrt(i); // Simulation of an expensive operation
    }

    // If we want to add time we can use this function
    timer.addTime(1000)// we put in milliseconds the time to add
    timer.addTime(500)// we put in milliseconds the time to add

    // We stop measuring time
    timer.stop();
}
*/