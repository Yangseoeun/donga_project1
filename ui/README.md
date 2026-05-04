# ui 폴더

화면에서 반복해서 쓰는 UI 컴포넌트와 CSS를 관리합니다. 디자인을 바꾸고 싶을 때 가장 먼저 확인할 폴더입니다.

## 파일 설명

| 파일 | 설명 | 담당 |
| --- | --- | --- |
| `__init__.py` | `ui`를 Python 패키지로 인식시키는 파일입니다. | 프론트 |
| `components.py` | 히어로 영역, 상태 카드, 사주 기둥, 리포트 카드, 채팅 말풍선 등 재사용 UI를 정의합니다. | 프론트, 디자인 |
| `styles.py` | 전체 CSS를 중앙 관리합니다. 카드, 배경, 채팅 메시지, 반응형 스타일이 들어 있습니다. | 디자인, 프론트 |

## 자주 수정하는 위치

| 바꾸고 싶은 것 | 수정할 곳 |
| --- | --- |
| 메인 화면 소개 문구 | `components.py`의 `render_intro_panel()` |
| 일반 리포트 카드 구성 | `components.py`의 `render_report_card()` |
| 채팅 말풍선 HTML 구조 | `components.py`의 `render_chat_message()` |
| 색상, 간격, 카드 모양 | `styles.py` |
| Streamlit 전체 테마 | `.streamlit/config.toml` |

## 수정 규칙

- 각 페이지에 인라인 CSS를 추가하지 말고 `styles.py`에서 관리합니다.
- 반복되는 UI는 페이지 파일에 직접 쓰지 말고 `components.py` 함수로 분리합니다.
- **코딩 완료 후 반드시 이 README.md 하단 "변경 이력" 섹션에 기록한다.**

---

## 함수 목록

### styles.py

| 함수 | 호출 페이지 | 설명 |
| --- | --- | --- |
| `apply_custom_styles()` | 채팅·리포트 페이지 | 채팅/리포트용 공통 CSS |
| `apply_landing_styles()` | `app.py` 전용 | 랜딩 페이지 Figma 디자인 CSS (Pretendard 폰트, 배경, 폼 카드, 완료 배너, 가이드 카드) |

### components.py

| 함수 | 설명 |
| --- | --- |
| `render_intro_panel()` | (구) 히어로 패널 — 현재 미사용 |
| `render_landing_hero()` | 랜딩 로고·태그라인·서브타이틀 영역 |
| `render_input_complete_banner(profile, saju)` | 정보 입력 완료 다크 네이비 배너 (4개 아이콘 인포) |
| `render_guide_section()` | 종합 분석 & 가이드 2-컬럼 카드 섹션 |
| `render_profile_balance_panel(saju, profile)` | 프로필 + Balance Status 바차트 패널 (공용) |
| `render_status_card(saju)` | (구) 상태 카드 |
| `render_quick_links()` | 페이지 링크 |
| `render_pillars(saju)` | 사주 4주 렌더링 |
| `render_saju_summary(saju)` | 일간·용신·기신 메트릭 |
| `render_report_card(report)` | 일반 리포트 카드 |
| `render_context_preview(saju)` | 채팅 페이지 사주 컨텍스트 미리보기 |
| `render_chat_message(role, content)` | 채팅 말풍선 |

---

## 변경 이력

### 2026-05-01

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `ui/styles.py` |
| 변경 유형 | 추가 |
| 변경 요약 | `apply_landing_styles()` 신규 추가 — Figma 디자인 토큰 기반 랜딩 전용 CSS (Pretendard 폰트, conic 배경, 폼 카드, 완료 배너, 가이드 카드 스타일) |
| 인터페이스 영향 | 없음 (app.py 전용, 다른 페이지 CSS 미영향) |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `ui/components.py` |
| 변경 유형 | 추가 |
| 변경 요약 | `render_landing_hero()`, `render_input_complete_banner()`, `render_guide_section()` 3개 함수 신규 추가 |
| 인터페이스 영향 | 없음 (신규 export 함수, 기존 함수 영향 없음) |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `app.py` |
| 변경 유형 | 수정 |
| 변경 요약 | 랜딩 페이지 레이아웃 Figma 디자인으로 전면 재구성 — 히어로·폼 카드·완료 배너·가이드 섹션. 폼 데이터 처리 로직은 유지. |
| 인터페이스 영향 | 없음 (다른 페이지 미수정) |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `ui/styles.py`, `app.py` |
| 변경 유형 | 수정 |
| 변경 요약 | index.html 분석 기반 UI 개선 — (1) 입력 레이아웃 3행 구조로 변경: 이름(전체폭) → 성별+달력라디오 → 생년월일+출생시간 (2) 입력 컨테이너 글래스모피즘 카드 CSS 추가 `.st-key-birth_profile_panel` (3) 앱 배경 conic-gradient + linear-gradient 혼합으로 교체 |
| 인터페이스 영향 | 없음 (랜딩 페이지 전용, 다른 페이지 미영향) |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `views/report_view.py` |
| 변경 유형 | 수정 |
| 변경 요약 | Figma style.css 기반 데일리 리포트 UI 개선 — (1) 배경색 `#f5f6f8` → `#e9eff0` (2) 오행 색상 토큰 업데이트 (3) Balance 바 그라디언트 + % 바 내부 표시 + 높이 확대 (4) 운세 카테고리 배지 pill 스타일(총운=다크네이비, 나머지=연청) (5) 코칭 카드 아이콘 배경·텍스트 색상 Figma 토큰으로 교체 |
| 인터페이스 영향 | 없음 (페이지 내부 CSS/렌더링만 변경) |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `views/report_view.py` |
| 변경 유형 | 수정 |
| 변경 요약 | 데일리 리포트 디자인 토큰 2차 적용 — (1) 배경 `#e9eff0` → `#E9F1F6` (2) 오행 색상 새 팔레트(#A8C69F/#F8A1A4/#EBD9B4/#D1D1D1/#3E8EAB) (3) 포인트 컬러 `#072f48` → `#1A374D` (타이틀·프로필·배지·키 컬러 전체) (4) 본문 텍스트 `#3a4155` → `#333333` (5) 카드 border-radius `12px` → `20px` (6) 코칭 아이콘 파스텔 팔레트 적용 (7) 운세 배지 secondary 컬러 `#3E8EAB` 계열로 변경 |
| 인터페이스 영향 | 없음 (CSS·상수만 변경) |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `views/chat_view.py` |
| 변경 유형 | 전면 재작성 |
| 변경 요약 | Figma 채팅 페이지 디자인 기반 전면 개편 — (1) 배경 `#e9eff0` + 페이지 타이틀 "1:1 코칭" (2) `render_context_preview()` 제거 → 프로필 카드(좌) + Balance Status 차트(우) 상단 패널 추가 (3) 한줄 요약 배너(`saju.summary`) 추가 (4) 모드 선택 UI: teal 질문 배너 + 5개 카드(아이콘·제목·설명·선택버튼, 선택시 teal 테두리) (5) 오행 색상 Figma 토큰 적용 |
| 인터페이스 영향 | `render_context_preview` import 제거, MODE_OPTIONS 상수 제거 — 외부 인터페이스 영향 없음 |

| 항목 | 내용 |
| --- | --- |
| 수정 파일 | `views/chat_view.py` |
| 변경 유형 | 수정 |
| 변경 요약 | (1) 모드 카드 "선택" 버튼 제거 → CSS `:has()` + 투명 오버레이 버튼으로 카드 전체를 클릭 영역 전환 (2) 헤더 텍스트 → `img/proj1_report/로고.png` + `1_1 코칭.png` 이미지로 교체 (base64 인코딩) (3) 배경색 `#e9eff0` → `#E9F1F6` (4) `_img_b64()` 헬퍼 추가 (`@st.cache_data`) |
| 인터페이스 영향 | 없음 (렌더링·CSS 변경만) |
