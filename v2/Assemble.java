import java.util.Arrays;

public abstract class Assemble {
    protected static final String CLEAR_SCREEN = "\033[H\033[2J";

    private static final int CarType_Q = 0;
    private static final int Engine_Q = 1;
    private static final int BrakeSystem_Q = 2;
    private static final int SteeringSystem_Q = 3;
    private static final int Run_Test = 4;

    private static final int SEDAN = 1, SUV = 2, TRUCK = 3;
    private static final int GM = 1, TOYOTA = 2, WIA = 3;
    private static final int MANDO = 1, CONTINENTAL = 2, BOSCH_B = 3;
    private static final int BOSCH_S = 1, MOBIS = 2;

    private final int[] stack = new int[5];
    private int step;

    protected final void execute() {
        reset();

        while (true) {
            clear();

            showMenu();

            print("INPUT > ");
            String buf = readLine();

            if (buf == null) {
                break;
            }

            buf = buf.trim();

            if (buf.equalsIgnoreCase("exit")) {
                println("바이바이");
                break;
            }

            int answer;

            try {
                answer = Integer.parseInt(buf);
            } catch (NumberFormatException e) {
                println("ERROR :: 숫자만 입력 가능");
                delay(800);
                continue;
            }

            if (!isValidRange(step, answer)) {
                delay(800);
                continue;
            }

            if (answer == 0) {
                if (step == Run_Test) {
                    step = CarType_Q;
                } else if (step > CarType_Q) {
                    step--;
                }
                continue;
            }

            switch (step) {
                case CarType_Q:
                    selectCarType(answer);
                    delay(800);
                    step = Engine_Q;
                    break;

                case Engine_Q:
                    selectEngine(answer);
                    delay(800);
                    step = BrakeSystem_Q;
                    break;

                case BrakeSystem_Q:
                    selectBrakeSystem(answer);
                    delay(800);
                    step = SteeringSystem_Q;
                    break;

                case SteeringSystem_Q:
                    selectSteeringSystem(answer);
                    delay(800);
                    step = Run_Test;
                    break;

                case Run_Test:
                    if (answer == 1) {
                        runProducedCar();
                        delay(2000);
                    } else if (answer == 2) {
                        println("Test...");
                        delay(1500);
                        testProducedCar();
                        delay(2000);
                    }
                    break;
            }
        }
    }

    private void reset() {
        step = CarType_Q;
        Arrays.fill(stack, 0);
    }

    private void showMenu() {
        switch (step) {
            case CarType_Q:
                showCarTypeMenu();
                break;
            case Engine_Q:
                showEngineMenu();
                break;
            case BrakeSystem_Q:
                showBrakeMenu();
                break;
            case SteeringSystem_Q:
                showSteeringMenu();
                break;
            case Run_Test:
                showRunTestMenu();
                break;
        }
    }

    private void showCarTypeMenu() {
        println("        ______________");
        println("       /|            |");
        println("  ____/_|_____________|____");
        println(" |                      O  |");
        println(" '-(@)----------------(@)--'");
        println("===============================");
        println("어떤 차량 타입을 선택할까요?");
        println("1. Sedan");
        println("2. SUV");
        println("3. Truck");
        println("===============================");
    }

    private void showEngineMenu() {
        println("어떤 엔진을 탑재할까요?");
        println("0. 뒤로가기");
        println("1. GM");
        println("2. TOYOTA");
        println("3. WIA");
        println("4. 고장난 엔진");
        println("===============================");
    }

    private void showBrakeMenu() {
        println("어떤 제동장치를 선택할까요?");
        println("0. 뒤로가기");
        println("1. MANDO");
        println("2. CONTINENTAL");
        println("3. BOSCH");
        println("===============================");
    }

    private void showSteeringMenu() {
        println("어떤 조향장치를 선택할까요?");
        println("0. 뒤로가기");
        println("1. BOSCH");
        println("2. MOBIS");
        println("===============================");
    }

    private void showRunTestMenu() {
        println("멋진 차량이 완성되었습니다.");
        println("어떤 동작을 할까요?");
        println("0. 처음 화면으로 돌아가기");
        println("1. RUN");
        println("2. Test");
        println("===============================");
    }

    private boolean isValidRange(int step, int ans) {
        switch (step) {
            case CarType_Q:
                if (ans < 1 || ans > 3) {
                    println("ERROR :: 차량 타입은 1 ~ 3 범위만 선택 가능");
                    return false;
                }
                break;

            case Engine_Q:
                if (ans < 0 || ans > 4) {
                    println("ERROR :: 엔진은 1 ~ 4 범위만 선택 가능");
                    return false;
                }
                break;

            case BrakeSystem_Q:
                if (ans < 0 || ans > 3) {
                    println("ERROR :: 제동장치는 1 ~ 3 범위만 선택 가능");
                    return false;
                }
                break;

            case SteeringSystem_Q:
                if (ans < 0 || ans > 2) {
                    println("ERROR :: 조향장치는 1 ~ 2 범위만 선택 가능");
                    return false;
                }
                break;

            case Run_Test:
                if (ans < 0 || ans > 2) {
                    println("ERROR :: Run 또는 Test 중 하나를 선택 필요");
                    return false;
                }
                break;
        }

        return true;
    }

    private void selectCarType(int a) {
        stack[CarType_Q] = a;

        String name;

        if (a == SEDAN) {
            name = "Sedan";
        } else if (a == SUV) {
            name = "SUV";
        } else {
            name = "Truck";
        }

        println("차량 타입으로 " + name + "을 선택하셨습니다.");
    }

    private void selectEngine(int a) {
        stack[Engine_Q] = a;

        String name;

        if (a == GM) {
            name = "GM";
        } else if (a == TOYOTA) {
            name = "TOYOTA";
        } else if (a == WIA) {
            name = "WIA";
        } else {
            name = "고장난 엔진";
        }

        println(name + " 엔진을 선택하셨습니다.");
    }

    private void selectBrakeSystem(int a) {
        stack[BrakeSystem_Q] = a;

        String name;

        if (a == MANDO) {
            name = "MANDO";
        } else if (a == CONTINENTAL) {
            name = "CONTINENTAL";
        } else {
            name = "BOSCH";
        }

        println(name + " 제동장치를 선택하셨습니다.");
    }

    private void selectSteeringSystem(int a) {
        stack[SteeringSystem_Q] = a;

        String name;

        if (a == BOSCH_S) {
            name = "BOSCH";
        } else {
            name = "MOBIS";
        }

        println(name + " 조향장치를 선택하셨습니다.");
    }

    private boolean isValidCheck() {
        if (stack[CarType_Q] == SEDAN && stack[BrakeSystem_Q] == CONTINENTAL) return false;
        if (stack[CarType_Q] == SUV && stack[Engine_Q] == TOYOTA) return false;
        if (stack[CarType_Q] == TRUCK && stack[Engine_Q] == WIA) return false;
        if (stack[CarType_Q] == TRUCK && stack[BrakeSystem_Q] == MANDO) return false;
        if (stack[BrakeSystem_Q] == BOSCH_B && stack[SteeringSystem_Q] != BOSCH_S) return false;

        return true;
    }

    private void runProducedCar() {
        if (!isValidCheck()) {
            println("자동차가 동작되지 않습니다");
            return;
        }

        if (stack[Engine_Q] == 4) {
            println("엔진이 고장나있습니다.");
            println("자동차가 움직이지 않습니다.");
            return;
        }

        String[] carNames = {"", "Sedan", "SUV", "Truck"};
        String[] engNames = {"", "GM", "TOYOTA", "WIA"};

        println("Car Type : " + carNames[stack[CarType_Q]]);
        println("Engine   : " + engNames[stack[Engine_Q]]);

        String brakeName;

        if (stack[BrakeSystem_Q] == MANDO) {
            brakeName = "Mando";
        } else if (stack[BrakeSystem_Q] == CONTINENTAL) {
            brakeName = "Continental";
        } else {
            brakeName = "Bosch";
        }

        String steeringName;

        if (stack[SteeringSystem_Q] == BOSCH_S) {
            steeringName = "Bosch";
        } else {
            steeringName = "Mobis";
        }

        println("Brake    : " + brakeName);
        println("Steering : " + steeringName);
        println("자동차가 동작됩니다.");
    }

    private void testProducedCar() {
        if (stack[CarType_Q] == SEDAN && stack[BrakeSystem_Q] == CONTINENTAL) {
            fail("Sedan에는 Continental제동장치 사용 불가");
        } else if (stack[CarType_Q] == SUV && stack[Engine_Q] == TOYOTA) {
            fail("SUV에는 TOYOTA엔진 사용 불가");
        } else if (stack[CarType_Q] == TRUCK && stack[Engine_Q] == WIA) {
            fail("Truck에는 WIA엔진 사용 불가");
        } else if (stack[CarType_Q] == TRUCK && stack[BrakeSystem_Q] == MANDO) {
            fail("Truck에는 Mando제동장치 사용 불가");
        } else if (stack[BrakeSystem_Q] == BOSCH_B && stack[SteeringSystem_Q] != BOSCH_S) {
            fail("Bosch제동장치에는 Bosch조향장치 이외 사용 불가");
        } else {
            println("자동차 부품 조합 테스트 결과 : PASS");
        }
    }

    private void fail(String msg) {
        println("자동차 부품 조합 테스트 결과 : FAIL");
        println(msg);
    }

    protected abstract void print(String msg);

    protected abstract void println(String msg);

    protected abstract String readLine();

    protected abstract void clear();

    protected abstract void delay(int ms);
}
