# views 폴더

`app.py`의 세션 기반 라우터가 호출하는 화면 렌더러를 관리하는 폴더입니다.
Streamlit 기본 multipage 사이드바를 사용하지 않기 위해 `pages/` 대신 이 폴더에 화면 코드를 둡니다.

## 파일 설명

| 파일 | 설명 | 담당 |
| --- | --- | --- |
| `report_view.py` | 데일리 리포트 화면을 렌더링합니다. 입력 정보, 사주 구성, 오행 차트, 운세, 라이프스타일 코칭을 표시합니다. | Streamlit 프론트, 백엔드 A 연동 |
| `chat_view.py` | 1:1 코칭 화면을 렌더링합니다. 상담 분야 선택, 채팅 UI, 대화 기록을 관리합니다. | Streamlit 프론트, 백엔드 B 연동 |

## 연결 흐름

- `app.py`에서 기본 정보를 입력하고 `calculate_saju()` 결과를 `st.session_state["user_saju"]`에 저장합니다.
- `st.session_state["active_view"]` 값에 따라 `report_view.py` 또는 `chat_view.py`의 렌더 함수가 호출됩니다.
- 화면 이동은 `st.switch_page()`가 아니라 `active_view` 변경과 `st.rerun()`으로 처리합니다.
