
# core 폴더

백엔드 핵심 로직을 모아둔 폴더입니다. 프론트 페이지에서 직접 계산이나 OpenAI 호출을 하지 않고, 이 폴더의 함수를 호출합니다.

## 파일 설명

| 파일 | 설명 | 담당 |
| --- | --- | --- |
| `__init__.py` | `core`를 Python 패키지로 인식시키는 파일입니다. | 공통 |
| `schemas.py` | `SajuResult`, `GeneralReport`, `ChatMessage` 등 공통 데이터 구조를 정의합니다. | 백엔드 A/B 공동 |
| `saju_calculator.py` | 생년월일시 기반 사주 계산, 오행 분포, 일간, 용신/기신 후보 계산을 담당합니다. | 백엔드 A |
| `result_builder.py` | `SajuResult`를 화면에 보여줄 일반 리포트 JSON으로 변환합니다. | 백엔드 A |
| `daily_report_builder.py` | 일간(day_master)과 강한 오행(dominant element)을 기반으로 데일리 리포트 JSON을 생성합니다. | 백엔드 A |
| `llm_client.py` | OpenAI API 키 로드, 모델 선택, 스트리밍/비스트리밍 응답 호출을 담당합니다. | 백엔드 B |
| `prompt_templates.py` | 상담 모드별 시스템 프롬프트와 메시지 조합 로직을 관리합니다. | 백엔드 B |
| `chat_engine.py` | 채팅 히스토리 정리, 사주 컨텍스트 결합, LLM 호출 흐름을 담당합니다. | 백엔드 B |

## 수정 규칙

- 백엔드 A는 주로 `saju_calculator.py`, `result_builder.py`, `daily_report_builder.py`를 수정합니다.
- 백엔드 B는 주로 `llm_client.py`, `prompt_templates.py`, `chat_engine.py`를 수정합니다.
- `schemas.py`는 A/B 공통 계약이므로 변경 전에 반드시 서로 합의합니다.
- 프론트는 OpenAI API를 직접 호출하지 않고 `chat_engine.py`를 통해 호출합니다.

---

## daily_report_builder.py 상세

> **추가일**: 2026-04-30  
> **담당**: 백엔드 A  
> **연결 페이지**: `pages/1_일반_사주.py`

### 역할

LLM 없이 순수 규칙 기반으로 데일리 리포트 JSON을 생성하는 **Backend A 데이터 생성기**입니다.  
`SajuResult.five_elements`에서 **가장 강한 오행(dominant element)** 을 추출한 뒤,  
오행별로 미리 작성된 운세·코칭 텍스트를 약속된 JSON 구조로 조립해 반환합니다.

### 출력 JSON 구조

```json
{
  "one_line_summary": "오늘의 핵심 기운을 담은 한 줄 요약",
  "detailed_fortune": {
    "총운":      "하루 전체 흐름과 조언",
    "재물운":    "금전 흐름 및 지출/저축 조언",
    "비즈니스운": "직장·사업·학업 성과 및 협업 조언",
    "애정운":    "연인·가족·대인관계 감정선 및 소통 조언",
    "건강운":    "오늘 신경 써야 할 신체 부위 및 컨디션 팁"
  },
  "coaching": {
    "outfit": {
      "추천 스타일":  "기운 보완 색상·재질·스타일",
      "행운의 아이템": "포인트 액세서리·소품",
      "주의 할 스타일": "오늘 피해야 할 옷차림"
    },
    "food": {
      "추천 식단":   "오늘 에너지를 채워줄 식재료·음식",
      "음료 페어링":  "식후·휴식 때 마시기 좋은 음료",
      "주의 할 음식": "소화 부담이 되거나 기운을 탁하게 하는 음식"
    },
    "environment": {
      "행운의 공간":  "능률이 오르는 장소의 특징",
      "에너지 방향":  "책상 배치·환기 방향 팁",
      "주의 할 장소": "기를 뺏기기 쉬운 공간"
    },
    "action": {
      "커뮤니케이션": "타인과 대화할 때의 태도·화법 전략",
      "네트워킹 전략": "오늘 사람을 만나는 방식에 대한 조언"
    }
  }
}
```

### 내부 구성

| 상수/함수 | 설명 |
| --- | --- |
| `_EN_TO_HANJA` | `saju_calculator`의 영문 오행 키(`wood` 등)를 한자 키(`木` 등)로 변환하는 매핑 |
| `_ELEMENT_DATA` | 木·火·土·金·水 각 오행별 운세 텍스트·코칭 데이터 뱅크 |
| `_ONE_LINE_SUMMARY` | 오행별 한 줄 요약 문장 |
| `_get_dominant_hanja()` | `five_elements` 딕셔너리에서 가장 강한 오행을 한자 키로 반환 |
| `build_daily_report(saju)` | 공개 API — `SajuResult`를 받아 완성된 데일리 리포트 `dict`를 반환 |

### 호출 예시

```python
from core.daily_report_builder import build_daily_report

report = build_daily_report(saju)   # saju: SajuResult

print(report["one_line_summary"])
print(report["detailed_fortune"]["총운"])
print(report["coaching"]["outfit"]["추천 스타일"])
```

### 오행 키 규칙

# core 폴더

백엔드 핵심 로직을 모아둔 폴더입니다. 프론트 페이지에서 직접 계산이나 OpenAI 호출을 하지 않고, 이 폴더의 함수를 호출합니다.

## 파일 설명

| 파일 | 설명 | 담당 |
| --- | --- | --- |
| `__init__.py` | `core`를 Python 패키지로 인식시키는 파일입니다. | 공통 |
| `schemas.py` | `SajuResult`, `GeneralReport`, `ChatMessage` 등 공통 데이터 구조를 정의합니다. | 백엔드 A/B 공동 |
| `saju_calculator.py` | 생년월일시 기반 사주 계산, 오행 분포, 일간, 용신/기신 후보 계산을 담당합니다. | 백엔드 A |
| `result_builder.py` | `SajuResult`를 화면에 보여줄 일반 리포트 JSON으로 변환합니다. | 백엔드 A |
| `daily_report_builder.py` | 일간(day_master)과 강한 오행(dominant element)을 기반으로 데일리 리포트 JSON을 생성합니다. | 백엔드 A |
| `llm_client.py` | OpenAI API 키 로드, 모델 선택, 스트리밍/비스트리밍 응답 호출을 담당합니다. | 백엔드 B |
| `prompt_templates.py` | 상담 모드별 시스템 프롬프트와 메시지 조합 로직을 관리합니다. | 백엔드 B |
| `chat_engine.py` | 채팅 히스토리 정리, 사주 컨텍스트 결합, LLM 호출 흐름을 담당합니다. | 백엔드 B |

## 수정 규칙

- 백엔드 A는 주로 `saju_calculator.py`, `result_builder.py`, `daily_report_builder.py`를 수정합니다.
- 백엔드 B는 주로 `llm_client.py`, `prompt_templates.py`, `chat_engine.py`를 수정합니다.
- `schemas.py`는 A/B 공통 계약이므로 변경 전에 반드시 서로 합의합니다.
- 프론트는 OpenAI API를 직접 호출하지 않고 `chat_engine.py`를 통해 호출합니다.

---

## daily_report_builder.py 상세

> **추가일**: 2026-04-30  
> **담당**: 백엔드 A  
> **연결 페이지**: `pages/1_일반_사주.py`

### 역할

LLM 없이 순수 규칙 기반으로 데일리 리포트 JSON을 생성하는 **Backend A 데이터 생성기**입니다.  
`SajuResult.five_elements`에서 **가장 강한 오행(dominant element)** 을 추출한 뒤,  
오행별로 미리 작성된 운세·코칭 텍스트를 약속된 JSON 구조로 조립해 반환합니다.

### 출력 JSON 구조

```json
{
  "one_line_summary": "오늘의 핵심 기운을 담은 한 줄 요약",
  "detailed_fortune": {
    "총운":      "하루 전체 흐름과 조언",
    "재물운":    "금전 흐름 및 지출/저축 조언",
    "비즈니스운": "직장·사업·학업 성과 및 협업 조언",
    "애정운":    "연인·가족·대인관계 감정선 및 소통 조언",
    "건강운":    "오늘 신경 써야 할 신체 부위 및 컨디션 팁"
  },
  "coaching": {
    "outfit": {
      "추천 스타일":  "기운 보완 색상·재질·스타일",
      "행운의 아이템": "포인트 액세서리·소품",
      "주의 할 스타일": "오늘 피해야 할 옷차림"
    },
    "food": {
      "추천 식단":   "오늘 에너지를 채워줄 식재료·음식",
      "음료 페어링":  "식후·휴식 때 마시기 좋은 음료",
      "주의 할 음식": "소화 부담이 되거나 기운을 탁하게 하는 음식"
    },
    "environment": {
      "행운의 공간":  "능률이 오르는 장소의 특징",
      "에너지 방향":  "책상 배치·환기 방향 팁",
      "주의 할 장소": "기를 뺏기기 쉬운 공간"
    },
    "action": {
      "커뮤니케이션": "타인과 대화할 때의 태도·화법 전략",
      "네트워킹 전략": "오늘 사람을 만나는 방식에 대한 조언"
    }
  }
}
```

### 내부 구성

| 상수/함수 | 설명 |
| --- | --- |
| `_EN_TO_HANJA` | `saju_calculator`의 영문 오행 키(`wood` 등)를 한자 키(`木` 등)로 변환하는 매핑 |
| `_ELEMENT_DATA` | 木·火·土·金·水 각 오행별 운세 텍스트·코칭 데이터 뱅크 |
| `_ONE_LINE_SUMMARY` | 오행별 한 줄 요약 문장 |
| `_get_dominant_hanja()` | `five_elements` 딕셔너리에서 가장 강한 오행을 한자 키로 반환 |
| `build_daily_report(saju)` | 공개 API — `SajuResult`를 받아 완성된 데일리 리포트 `dict`를 반환 |

### 호출 예시

```python
from core.daily_report_builder import build_daily_report

report = build_daily_report(saju)   # saju: SajuResult

print(report["one_line_summary"])
print(report["detailed_fortune"]["총운"])
print(report["coaching"]["outfit"]["추천 스타일"])
```

### 오행 키 규칙

`SajuResult.five_elements`는 영문 키(`wood`, `fire`, `earth`, `metal`, `water`)로 저장되지만,  
`_ELEMENT_DATA` 및 `prompt_templates.py`의 `ELEMENT_PROFILE`은 한자 키(`木`, `火`, `土`, `金`, `水`)를 사용합니다.  
`_EN_TO_HANJA` 매핑을 통해 내부적으로 변환하므로, **외부에서는 영문/한자 키를 신경 쓰지 않아도 됩니다.**

### 텍스트 수정 방법

운세·코칭 문구를 바꾸려면 `_ELEMENT_DATA` 딕셔너리 안의 해당 오행 항목만 수정하면 됩니다.  
JSON Key 이름(`추천 스타일`, `행운의 아이템` 등)은 **UI와 약속된 계약**이므로 변경하지 않습니다.

---

## [Update: 2026-04-30] 데일리 리포트 UI 통합 내역

### 1. `pages/1_일반_사주.py` 개편
기존의 복잡했던 일반 사주 분석 페이지를 **데일리 리포트 전용 화면**으로 완전히 교체했습니다.
- **제거된 기능**: 사주 8글자 렌더링 카드, 오행 분포 바차트(기본형), 기존 방식의 단순 텍스트 운세.
- **새로운 UI 구조**: 
  - `MY ENERGY-UP COACH` 브랜딩이 적용된 헤더
  - 사용자의 기본 프로필과 오행 비율을 시각화한 **Balance Status 차트** 패널
  - `daily_report_builder.py`에서 생성한 오행 맞춤형 **한 줄 요약 Quote**
  - 가독성을 높인 카드 형태의 **운세 5종** (총운, 재물운, 비즈니스운, 애정운, 건강운)
  - 2×2 그리드로 깔끔하게 정돈된 **라이프 코칭 카드** (의상, 푸드, 환경, 행동 전략)
- **개발자 도구 제거**: 사용자 경험 개선을 위해 페이지 하단에 있던 원본 JSON 확인용 Expander를 최종 삭제했습니다.

### 2. `app.py` 라우팅 간소화
- 기존 상담 시작 메뉴에 있던 3개의 버튼(일반모드, 채팅모드, 데일리 리포트)을 **2개**로 줄였습니다.
- `1_일반_사주.py`가 데일리 리포트 화면으로 통합되었기 때문에, `일반모드로 보기` 버튼 클릭 시 바로 **데일리 리포트 전용 페이지**로 이동하도록 직관적으로 수정했습니다.

---

## [Update: 2026-04-30] 비즈니스 전략 코치 페르소나 적용 및 UI 고도화 (Backend A 리포트)

### 1. `daily_report_builder.py` 데이터 모델 전면 개편 (라이프스타일 에이전트 페르소나)
프론트엔드의 데일리 리포트에 표출되는 정적 데이터 뱅크(`_ELEMENT_DATA`)를 **'비즈니스 전략 코치'** 페르소나에 맞추어 완전히 새롭게 작성했습니다. 
- **톤앤매너 변경**: 고리타분한 점술 어조를 버리고, 즉시 실행할 수 있는 실질적인 액션 플랜을 제안하는 세련된 전문가의 평어체를 적용했습니다.
- **분야별 3줄 요약**: 총운, 재물운, 비즈니스운, 애정운, 건강운을 각각 명확한 3줄 풀이로 정리했습니다.
- **Energy-up 솔루션 (정적 처방) 카테고리 재편**:
  - `의상(衣)`: 돋보이는 코디 및 색상, 행운의 아이템 & 액세서리, 피해야 할 의상
  - `푸드(食)`: 점심/회식 추천 메뉴, 주류 및 음료, 피해야 할 음식/주류/음료
  - `공간(宙)`: 업무 효율용 공간 제안, 행운의 방향, 피해야 할 장소
  - `행동전략`: 커뮤니케이션 팁, 네트워킹 팁

### 2. `pages/1_일반_사주.py` UI/UX 고도화
새롭게 정의된 데이터 규격에 맞추어 프론트엔드 UI를 세밀하게 조정했습니다.
- **JSON Key 매핑 업데이트**: 백엔드에서 변경된 새로운 카테고리명(예: `돋보이는 코디 및 색상`)을 정상적으로 파싱하여 화면에 뿌려지도록 `_COACHING_META` 리스트를 갱신했습니다.
- **Balance Status 그래프 개선**:
  - 기존의 막대그래프가 너무 작아 정보 전달력이 떨어진다는 피드백에 따라, 컨테이너 높이를 키우고 바의 배율(`height` 계산식)을 상향 조정하여 시원하게 보이도록 수정했습니다.
  - 상단 패널 레이아웃의 `align-items`를 조정하여 그래프가 바닥선에 안정적으로 정렬되도록 했습니다.
  - 불필요하게 공간을 차지하던 "Balance Status" 텍스트 타이틀을 삭제하여 더욱 깔끔한 뷰를 완성했습니다.
- **코칭 카드 그리드 정렬**: 서로 다른 항목 개수로 인해 카드 높이가 들쭉날쭉해지는 현상을 방지하기 위해, Streamlit의 내장 column 대신 순수 HTML/CSS `Grid` 레이아웃(`display: grid`)을 도입하여 모든 코칭 카드가 균일한 높이(`height: 100%`)를 가지도록 레이아웃을 최적화했습니다.
