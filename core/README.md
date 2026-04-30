3기 서한진 입니다.
# core 폴더

백엔드 핵심 로직을 모아둔 폴더입니다. 프론트 페이지에서 직접 계산이나 OpenAI 호출을 하지 않고, 이 폴더의 함수를 호출합니다.

## 파일 설명

| 파일 | 설명 | 담당 |
| --- | --- | --- |
| `__init__.py` | `core`를 Python 패키지로 인식시키는 파일입니다. | 공통 |
| `schemas.py` | `SajuResult`, `GeneralReport`, `ChatMessage` 등 공통 데이터 구조를 정의합니다. | 백엔드 A/B 공동 |
| `saju_calculator.py` | 생년월일시 기반 사주 계산, 오행 분포, 일간, 용신/기신 후보 계산을 담당합니다. | 백엔드 A |
| `result_builder.py` | `SajuResult`를 화면에 보여줄 일반 리포트 JSON으로 변환합니다. | 백엔드 A |
| `llm_client.py` | OpenAI API 키 로드, 모델 선택, 스트리밍/비스트리밍 응답 호출을 담당합니다. | 백엔드 B |
| `prompt_templates.py` | 상담 모드별 시스템 프롬프트와 메시지 조합 로직을 관리합니다. | 백엔드 B |
| `chat_engine.py` | 채팅 히스토리 정리, 사주 컨텍스트 결합, LLM 호출 흐름을 담당합니다. | 백엔드 B |

## 수정 규칙

- 백엔드 A는 주로 `saju_calculator.py`, `result_builder.py`를 수정합니다.
- 백엔드 B는 주로 `llm_client.py`, `prompt_templates.py`, `chat_engine.py`를 수정합니다.
- `schemas.py`는 A/B 공통 계약이므로 변경 전에 반드시 서로 합의합니다.
- 프론트는 OpenAI API를 직접 호출하지 않고 `chat_engine.py`를 통해 호출합니다.

<<<<<<< HEAD

=======
##
>>>>>>> f288ef498395564470055b8e50ad22c218be5157
