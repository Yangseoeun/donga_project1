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
