# Architecture

## Conflict-Minimized Ownership

- Frontend: `app.py`, `pages/`, `ui/`
- Backend A: `core/saju_calculator.py`, `core/result_builder.py`
- Backend B: `core/llm_client.py`, `core/chat_engine.py`, `core/prompt_templates.py`
- Shared: `core/schemas.py`

현재 스캐폴드는 백엔드 A의 계산 파일을 생성하지 않습니다. 프론트는 임시 데모 `SajuResult`로 동작하고, 백엔드 A 구현이 완료되면 `user_saju`에 실제 계산 결과를 저장하도록 연결하면 됩니다.
