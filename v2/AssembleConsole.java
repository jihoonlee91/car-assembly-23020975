import java.util.Scanner;

public class AssembleConsole extends Assemble {
    private final Scanner sc = new Scanner(System.in);

    public void run() {
        execute();
    }

    @Override
    protected void print(String msg) {
        System.out.print(msg);
    }

    @Override
    protected void println(String msg) {
        System.out.println(msg);
    }

    @Override
    protected String readLine() {
        return sc.nextLine();
    }

    @Override
    protected void clear() {
        System.out.print(CLEAR_SCREEN);
        System.out.flush();
    }

    @Override
    protected void delay(int ms) {
        try {
            Thread.sleep(ms);
        } catch (InterruptedException ignored) {
        }
    }
}
