# AI 사주 상담 플랫폼

# 이것은 olive test

Streamlit + LLM 기반 사주 상담 웹 애플리케이션입니다.  
이 README는 프로젝트를 처음 실행하거나 폴더 구조를 빠르게 파악하기 위한 문서입니다.

## 실행 방법

### 1. 공통 준비

프론트엔드와 백엔드가 같은 Python 프로젝트 안에서 함께 실행됩니다. 먼저 패키지를 설치합니다.

```bash
python -m pip install -r requirements.txt
```

`.env.example`을 참고해서 `.env` 파일을 만들고 OpenAI API 키를 넣습니다.

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
MAX_HISTORY_TURNS=10
STREAM_ENABLED=true
```

`.env`는 Git에 올리지 않습니다.

### 2. 백엔드 실행 방법

백엔드는 따로 서버를 켜는 방식이 아닙니다.  
`core/` 폴더의 함수들이 Streamlit 화면에서 바로 호출됩니다.

백엔드 함수가 정상 동작하는지 확인하고 싶으면 테스트를 실행합니다.

```bash
python -m pytest tests -v
```

### 3. 프론트엔드 실행 방법

Streamlit 앱을 실행합니다.

```bash
python -m streamlit run app.py
```

실행 후 브라우저에서 접속합니다.

```text
http://localhost:8501
```

## 사용 흐름

1. `일반 사주 리포트` 페이지에서 생년월일시를 입력합니다.
2. 백엔드 A가 사주 결과와 일반 리포트를 생성합니다.
3. `AI 사주 채팅` 페이지에서 같은 사주 컨텍스트로 질문합니다.
4. 백엔드 B가 OpenAI API를 통해 사주 기반 답변을 생성합니다.

## 전체 폴더 구조

```text
donga_project1/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── core/
├── pages/
├── ui/
├── utils/
├── tests/
├── docs/
└── .streamlit/
```

## 폴더별 설명

| 폴더 | 설명 | 주요 담당 |
| --- | --- | --- |
| `core/` | 사주 계산, 일반 리포트 생성, LLM 연결, 채팅 엔진이 들어 있는 백엔드 폴더입니다. | 백엔드 A/B |
| `pages/` | Streamlit에서 실제로 보이는 페이지 화면을 관리합니다. | 프론트 |
| `ui/` | 재사용 UI 컴포넌트와 CSS 스타일을 관리합니다. | 프론트, 디자인 |
| `utils/` | 세션 상태 초기화, 로거 같은 공통 보조 기능을 관리합니다. | 공통 |
| `tests/` | 백엔드와 주요 로직이 정상 동작하는지 확인하는 테스트 코드를 관리합니다. | 각 담당자 |
| `docs/` | 설계, API 명세, 프롬프트 설계, 발표 참고 문서를 관리합니다. | 기획, 발표, 백엔드 |
| `.streamlit/` | Streamlit 테마 색상과 화면 기본 설정을 관리합니다. | 디자인, 프론트 |

## 루트 파일 설명

| 파일 | 설명 | 주요 담당 |
| --- | --- | --- |
| `app.py` | Streamlit 앱의 메인 진입점입니다. 첫 화면과 페이지 이동 흐름을 담당합니다. | 프론트 |
| `requirements.txt` | 프로젝트 실행에 필요한 Python 패키지 목록입니다. | 공통 |
| `.env.example` | 환경변수 예시 파일입니다. 실제 API 키는 `.env`에 넣고 Git에 올리지 않습니다. | 백엔드 B |
| `.gitignore` | Git에 올리지 않을 파일과 폴더를 정합니다. | 공통 |
| `README.md` | 프로젝트 실행 방법과 전체 폴더 구조를 설명하는 문서입니다. | 공통 |

## 폴더별 상세 문서

각 폴더 안에는 더 자세한 README가 있습니다.

- [`core/README.md`](core/README.md)
- [`pages/README.md`](pages/README.md)
- [`ui/README.md`](ui/README.md)
- [`utils/README.md`](utils/README.md)
- [`tests/README.md`](tests/README.md)
- [`docs/README.md`](docs/README.md)
- [`.streamlit/README.md`](.streamlit/README.md)

## 담당자별 추천 작업 위치

| 역할 | 주로 수정할 곳 |
| --- | --- |
| 기획 | `docs/` |
| 디자인 | `ui/`, `.streamlit/` |
| Streamlit 프론트 | `app.py`, `pages/`, `ui/` |
| 백엔드 A | `core/`, `tests/` |
| 백엔드 B | `core/`, `tests/`, `docs/` |
| 발표/PPT | `README.md`, `docs/` |

## 테스트란?

테스트는 “코드가 의도대로 동작하는지 자동으로 확인하는 코드”입니다.  
예를 들어 사주 계산 함수가 `SajuResult` 형식으로 결과를 반환하는지, 채팅 히스토리가 너무 길어졌을 때 잘 잘리는지 등을 확인합니다.

실행 명령어는 아래와 같습니다.

```bash
python -m pytest tests -v
```

현재 테스트는 실제 OpenAI API를 호출하지 않습니다. 그래서 API 비용 없이 실행할 수 있습니다.
