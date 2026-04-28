# tests 폴더

자동 테스트 코드를 관리합니다. 기능을 수정한 뒤 기존 동작이 깨지지 않았는지 확인합니다.

## 실행 방법

```bash
python -m pytest tests -v
```

## 파일 설명

| 파일 | 설명 | 담당 |
| --- | --- | --- |
| `test_saju_calculator.py` | 사주 계산 결과가 `SajuResult` 형식인지, 오행 합계와 입춘 기준이 동작하는지 테스트합니다. | 백엔드 A |
| `test_result_builder.py` | 일반 리포트 JSON에 필요한 화면 표시 항목이 들어 있는지 테스트합니다. | 백엔드 A |
| `test_llm_client.py` | API 키가 없을 때 LLM 클라이언트가 명확한 오류를 내는지 테스트합니다. | 백엔드 B |
| `test_chat_engine.py` | 채팅 히스토리 정리, 프롬프트 메시지 생성, fallback 답변을 테스트합니다. | 백엔드 B |

## 주의

- 현재 테스트는 실제 OpenAI API를 호출하지 않습니다.
- 새 기능을 추가하면 담당 파일에 맞는 테스트도 함께 추가하는 것을 권장합니다.
