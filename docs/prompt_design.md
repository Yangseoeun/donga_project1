# Prompt Design

백엔드 B 프롬프트는 `core/prompt_templates.py`에서만 관리합니다.

- `GENERAL_SYSTEM_PROMPT`: 일반 상담
- `BUSINESS_SYSTEM_PROMPT`: 사업/커리어 상담
- `LOVE_SYSTEM_PROMPT`: 연애/관계 상담
- `HEALTH_SYSTEM_PROMPT`: 건강/컨디션 상담

모든 프롬프트는 `SajuResult`의 사주 컨텍스트를 포함합니다. 답변은 단정적인 예언보다 해석, 자기 이해, 실행 가능한 조언을 중심으로 구성합니다.
