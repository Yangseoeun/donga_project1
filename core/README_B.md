# core 폴더 — 백엔드 B 담당 가이드

백엔드 핵심 로직을 모아둔 폴더입니다. 프론트 페이지에서 직접 계산이나 OpenAI 호출을 하지 않고, 이 폴더의 함수를 호출합니다.

---

## 파일 설명 및 담당자

| 파일 | 설명 | 담당 |
| --- | --- | --- |
| `__init__.py` | `core`를 Python 패키지로 인식시키는 파일입니다. | 공통 |
| `schemas.py` | `SajuResult`, `GeneralReport`, `ChatMessage` 등 공통 데이터 구조를 정의합니다. | **백엔드 A/B 공동 (합의 필요)** |
| `saju_calculator.py` | 생년월일시 기반 사주 계산, 오행 분포, 일간, 용신/기신 후보 계산을 담당합니다. | 백엔드 A 전담 |
| `result_builder.py` | `SajuResult`를 화면에 보여줄 일반 리포트 JSON으로 변환합니다. | 백엔드 A 전담 |
| `llm_client.py` | OpenAI API 키 로드, 모델 선택, 스트리밍/비스트리밍 응답 호출을 담당합니다. | **백엔드 B 전담** |
| `prompt_templates.py` | 상담 모드별 시스템 프롬프트와 메시지 조합 로직을 관리합니다. | **백엔드 B 전담** |
| `chat_engine.py` | 채팅 히스토리 정리, 사주 컨텍스트 결합, LLM 호출 흐름을 담당합니다. | **백엔드 B 전담** |

---

## 백엔드 B 수정 허용 파일 (이 파일들만 수정할 것)

```
core/llm_client.py
core/prompt_templates.py
core/chat_engine.py
tests/test_llm_client.py
tests/test_chat_engine.py
```

---

## 절대 수정 금지 파일 (다른 담당자 영역)

| 파일/폴더 | 이유 |
| --- | --- |
| `core/saju_calculator.py` | 백엔드 A 전담 — 사주 계산 로직 |
| `core/result_builder.py` | 백엔드 A 전담 — 리포트 변환 로직 |
| `tests/test_saju_calculator.py` | 백엔드 A 전담 테스트 |
| `tests/test_result_builder.py` | 백엔드 A 전담 테스트 |
| `ui/` | 프론트엔드 전담 |
| `utils/` | 공통 유틸 — 변경 필요 시 팀 전체 합의 |
| `docs/` | 공통 문서 — 변경 필요 시 팀 전체 합의 |

---

## 합의 후 수정 가능한 파일

| 파일 | 합의 상대 |
| --- | --- |
| `core/schemas.py` | 백엔드 A (공통 데이터 계약이므로 반드시 사전 동의) |
| `core/__init__.py` | 백엔드 A / 프론트 (패키지 노출 범위 영향) |

---

## 인터페이스 계약 (변경 금지 원칙)

백엔드 B가 외부로 노출하는 함수 시그니처는 **프론트엔드와 백엔드 A가 직접 호출**합니다.  
아래 함수의 이름·파라미터·반환 타입을 변경할 경우 반드시 팀 전체에 공지하고 합의하세요.

```python
# chat_engine.py
run_chat(saju: SajuResult, history: list, user_input: str, mode: ConsultationMode) -> str
run_chat_stream(saju: SajuResult, history: list, user_input: str, mode: ConsultationMode) -> Generator[str]
build_fallback_answer(saju: SajuResult, user_input: str) -> str

# llm_client.py
get_chat_response(messages: list[dict], stream: bool, temperature: float) -> str | Generator[str]
```

---

## 수정 전 체크리스트

- [ ] 수정 대상 파일이 위 **허용 목록** 안에 있는가?
- [ ] `schemas.py` 변경이 필요하다면 백엔드 A와 사전 합의했는가?
- [ ] 외부 인터페이스 시그니처를 변경했다면 팀 전체에 공지했는가?
- [ ] `tests/test_llm_client.py`, `tests/test_chat_engine.py`에 테스트를 함께 추가/수정했는가?


