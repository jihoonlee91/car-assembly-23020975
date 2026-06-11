import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

public class UnitTest {

    @Test
    void 정상_조합이면_PASS() {
        AssembleTestable app = new AssembleTestable();

        String[] input = {
                "1", // Sedan
                "1", // GM
                "1", // MANDO
                "1", // BOSCH
                "2"  // Test
        };

        String output = app.run(input);

        assertTrue(output.contains("자동차 부품 조합 테스트 결과 : PASS"));
    }

    @Test
    void Sedan에_Continental이면_FAIL() {
        AssembleTestable app = new AssembleTestable();

        String[] input = {
                "1", // Sedan
                "1", // GM
                "2", // CONTINENTAL
                "1", // BOSCH
                "2"  // Test
        };

        String output = app.run(input);

        assertTrue(output.contains("자동차 부품 조합 테스트 결과 : FAIL"));
        assertTrue(output.contains("Sedan에는 Continental제동장치 사용 불가"));
    }

    @Test
    void 고장난_엔진이면_RUN_실패() {
        AssembleTestable app = new AssembleTestable();

        String[] input = {
                "1", // Sedan
                "4", // 고장난 엔진
                "1", // MANDO
                "1", // BOSCH
                "1"  // RUN
        };

        String output = app.run(input);

        assertTrue(output.contains("엔진이 고장나있습니다."));
        assertTrue(output.contains("자동차가 움직이지 않습니다."));
    }
}
