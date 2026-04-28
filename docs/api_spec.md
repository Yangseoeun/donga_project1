# Backend B API Spec

## `core.chat_engine.run_chat`

```python
run_chat(
    saju: SajuResult,
    history: list[dict[str, str]],
    user_input: str,
    mode: ConsultationMode = "general",
) -> str
```

비스트리밍 채팅 응답을 반환합니다.

## `core.chat_engine.run_chat_stream`

```python
run_chat_stream(
    saju: SajuResult,
    history: list[dict[str, str]],
    user_input: str,
    mode: ConsultationMode = "general",
) -> Generator[str, None, None]
```

Streamlit `st.write_stream()`에 바로 전달할 수 있는 토큰 제너레이터를 반환합니다.

## History Format

```python
chat_history = [
    {"role": "user", "content": "올해 사업운은 어떤가요?"},
    {"role": "assistant", "content": "귀하의 일간은 무토(戊土)로..."},
]
```
