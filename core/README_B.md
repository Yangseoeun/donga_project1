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

## 코딩 완료 후 필수 기록 규칙

> **모든 코딩 작업이 끝난 즉시 이 README_B.md 하단 "변경 이력" 섹션에 기록한다.**

기록 항목:

| 항목 | 내용 |
| --- | --- |
| 날짜 | 작업 완료 날짜 |
| 수정 파일 | 변경된 파일 경로 목록 |
| 변경 유형 | 추가 / 수정 / 삭제 |
| 변경 요약 | 무엇을 왜 변경했는지 한 줄 설명 |
| 인터페이스 영향 | 외부(프론트·백엔드 A)에 영향을 주는 변경인지 여부 |

기록하지 않으면 팀원이 변경 이유를 알 수 없으므로 **코딩과 기록은 한 세트**로 처리한다.

---

## 전략 처방전 파이프라인 (prompt_templates.py 추가 구현)

### 개요

`prompt_templates.py` 하단에 **오행 부족 기운 보완형 전략 처방전** 파이프라인을 추가했습니다.  
백엔드 A 코드(`saju_calculator.py`, `result_builder.py`, `schemas.py`)는 **일절 수정하지 않았습니다.**  
`SajuResult.five_elements` 필드를 읽기 전용으로 참조합니다.

### 처리 흐름

```
SajuResult.five_elements (세션 스테이트)
    ↓
find_weakest_elements()   ← 수치 낮은 원소 2개 탐지
    ↓
generate_prescription(ohaeng, case)
    ↓
_PRESCRIPTION_MAP[case].build()   ← 카테고리 클래스 선택
    ↓
4대 영역 처방전 딕셔너리 반환 + 격려 메시지
```

### 공개 함수 (UI에서 호출 가능)

| 함수 | 인자 | 반환 |
| --- | --- | --- |
| `find_weakest_elements(ohaeng, top_n=2)` | `dict[str, int]` | 부족 원소 리스트 |
| `generate_prescription(ohaeng, case)` | `dict[str, int]`, `str` | 처방전 딕셔너리 |
| `build_encouragement_message(category_label)` | `str` | 격려 문구 문자열 |

### 지원 케이스(case) 목록

| case 값 | 카테고리 | 핵심 오행 |
| --- | --- | --- |
| `"business"` | 비즈니스 | 土 (신뢰) + 金 (냉철함) |
| `"love"` | 연애 | 火 (매력) + 水 (유연함) |
| `"wealth"` | 재물 | 木 (직관) + 金 (매듭) |
| `"study"` | 학업/업무 | 土 (지구력) + 木 (추진력) |
| `"health"` | 건강 | 水 (유연함) + 土 (기초 체력) |

### 처방전 출력 구조 (딕셔너리 키)

```python
{
    "category":            str,           # 카테고리 한글 레이블
    "weakest_elements":    list[str],      # 부족 원소 리스트
    "ohaeng_distribution": dict[str, int], # 전체 오행 분포 (표시용)
    "primary_boost":       str,            # 1순위 보완 원소
    "衣": {
        "보완_색상":      list[str],
        "행운_아이템":    list[str],
        "피해야_할_의상": list[str],
    },
    "食": {
        "에너지_상승_메뉴": list[str],
        "음료_페어링":      list[str],
        "피해야_할_음식":   list[str],
    },
    "宙": {
        "추천_공간":      list[str],
        "행운의_방향":    str,
        "피해야_할_장소": list[str],
    },
    "행동전략":   str,  # 카테고리·원소별 맞춤 커뮤니케이션 팁
    "격려_메시지": str,  # 대화 마무리 긍정 격려 문구
}
```

### 호출 예시

```python
from core.schemas import SajuResult
from core.prompt_templates import generate_prescription

# SajuResult.five_elements 를 세션 스테이트에서 전달
saju: SajuResult = ...  # 백엔드 A가 계산한 결과

result = generate_prescription(saju.five_elements, case="love")
print(result["primary_boost"])   # 예) "火"
print(result["행동전략"])
print(result["격려_메시지"])
```

### 클래스 구조 (확장 방법)

새 카테고리를 추가하려면 `_BasePrescription` 을 상속하고 `_PRESCRIPTION_MAP` 에 등록합니다.  
기존 클래스는 절대 수정하지 말고 새 클래스를 추가하세요.

```python
class NewCategoryPrescription(_BasePrescription):
    KEY_ELEMENTS = ("火", "木")
    CATEGORY_LABEL = "새 카테고리"
    ACTION_TIPS = {"火": "...", "木": "..."}

_PRESCRIPTION_MAP["new_case"] = NewCategoryPrescription()
```

---

## 변경 이력

### 2026-04-30

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `core/prompt_templates.py` |
| 변경 유형 | 추가 |
| 변경 요약 | `_RESPONSE_FORMAT_INSTRUCTION` 추가: 모든 전문 모드(general 제외)에서 衣食宙행동전략 구조 + 타 분야 질문 + 격려 마무리를 LLM에 지시 |
| 인터페이스 영향 | 없음 (내부 프롬프트 변경, 외부 함수 시그니처 유지) |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `core/prompt_templates.py` |
| 변경 유형 | 추가 |
| 변경 요약 | `MODE_GREETING` 딕셔너리 추가: 5개 모드별 인사말 텍스트 (pages 레이어에서 import하여 사용) |
| 인터페이스 영향 | 없음 (신규 export 상수, 기존 함수 영향 없음) |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `core/prompt_templates.py` |
| 변경 유형 | 수정 |
| 변경 요약 | `build_system_prompt()` 수정: general 모드는 자유 형식 유지, 나머지 모드는 `_RESPONSE_FORMAT_INSTRUCTION` 자동 추가 |
| 인터페이스 영향 | 없음 (함수 시그니처 동일, 반환 문자열 내용만 변경) |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `pages/2_채팅_사주.py` |
| 변경 유형 | 수정 |
| 변경 요약 | 모드 버튼 클릭 시 `prev_mode` 비교로 모드 변경을 감지하고 `MODE_GREETING`을 `chat_history`에 자동 주입하여 인사말 즉시 표시 |
| 인터페이스 영향 | 없음 (`ui/components.py`, `ui/styles.py` 미수정, core 인터페이스 유지) |
