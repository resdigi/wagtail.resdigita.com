# EliasellS – Virtual Sales Assistant for Django

**Eliasells** is an intelligent, multilingual virtual sales assistant built on top of LangChain and LangGraph frameworks. It integrates OpenAI's language models to provide real-time conversational capabilities tailored for e-commerce and customer support applications.

## ✨ Features

- **Conversational AI**: Uses `OpenAI` to simulate natural language dialogue with users.
- **Multilingual Support**: Automatically adapts system prompts to the current user's language using Django's i18n framework.
- **Stateful Conversations**: Each user session maintains a consistent context via `thread_id` and memory checkpointing.
- **Session-based Thread Management**: Unique thread ID per session ensures context is preserved across requests.
- **Custom Logging**: Logs interactions with the OpenAI API for debugging and monitoring purposes.
- **Token-efficient Prompting**: Integrates message trimming to fit token limits while maintaining conversation history.

## 🧠 How It Works

At the core of `eliasells` lies a **LangGraph workflow** that orchestrates the conversation logic.

### 1. `graph.py` – Conversation Engine

- **State Schema**: Uses a `TypedDict` with language and message history.
- **Prompting**: Combines system prompt with user messages, trimmed intelligently to stay within token limits.
- **Model Invocation**: Communicates with OpenAI’s chat models via LangChain’s `ChatOpenAI`.
- **Memory**: Uses `MemorySaver` for persistent, resumable conversations.

### 2. `views.py` – Django View Layer

- Provides an HTTP POST endpoint (`chat_view`) to receive user messages.
- Extracts the message and current language from the request.
- Initializes a session-bound `thread_id` to maintain context.
- Sends messages to the LangGraph `app` and returns the latest AI response.
- Handles errors and logs all request-response interactions with OpenAI.

## 🛠️ Installation

1. Add `eliasels` to your Django project.
2. Install required packages:

    ```bash
    pip install langchain langgraph openai django
    ```

3. Configure your OpenAI API key:

    ```python
    # settings.py
    OPENAI_API_KEY = 'your-key-here'
    ```

4. Set up language support (optional):

    ```python
    # settings.py
    USE_I18N = True
    LANGUAGES = [('en', 'English'), ('fr', 'French'), ...]
    ```

## 🧪 Usage

Make a `POST` request to the endpoint:

```http
POST /chat/
Content-Type: application/json

{
  "message": "Hi, I need help finding a product."
}










