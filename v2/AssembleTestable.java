public class AssembleTestable extends Assemble {
    private String[] inputs;
    private int inputIndex;
    private StringBuilder out;

    public String run(String[] inputs) {
        this.inputs = inputs;
        this.inputIndex = 0;
        this.out = new StringBuilder();

        execute();

        return out.toString();
    }

    public String run(String input) {
        if (input == null || input.isEmpty()) {
            return run(new String[0]);
        }

        return run(input.split("\\R"));
    }

    @Override
    protected void print(String msg) {
        out.append(msg);
    }

    @Override
    protected void println(String msg) {
        out.append(msg).append("\n");
    }

    @Override
    protected String readLine() {
        if (inputIndex >= inputs.length) {
            return null;
        }

        return inputs[inputIndex++];
    }

    @Override
    protected void clear() {
        // UnitTest에서는 화면 지우기 안 함
    }

    @Override
    protected void delay(int ms) {
        // UnitTest에서는 delay 안 함
    }
}
