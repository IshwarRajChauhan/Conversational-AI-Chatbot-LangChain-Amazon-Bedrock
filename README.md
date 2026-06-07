#  Conversational AI Chatbot — LangChain + Amazon Bedrock (DeepSeek V3)

A production-style conversational AI chatbot built with **LangChain**, **Amazon Bedrock (DeepSeek V3)**, and a **Streamlit** frontend. Features persistent in-session memory using `RunnableWithMessageHistory` and `InMemoryChatMessageHistory`.

---

##  Architecture

```
Frontend (Streamlit)
    └── User types message → chatbot_frontend.py

LangChain Layer
    ├── RunnableWithMessageHistory  ← Conversation chain
    ├── Prompt Builder              ← History + input text
    └── Amazon Bedrock (DeepSeek V3) ← LLM inference

Memory Layer
    ├── st.session_state            ← Streamlit session
    ├── InMemoryChatMessageHistory  ← LangChain memory
    └── Chat history                ← role + text list
```

Data flow: `input_text` → conversation chain → Bedrock → `chat_reply` → Streamlit UI → `reply.content` displayed to user. On each response, `st.rerun()` refreshes the UI.

---

##  Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Orchestration | LangChain (`RunnableWithMessageHistory`) |
| Memory | `InMemoryChatMessageHistory` |
| LLM | Amazon Bedrock — DeepSeek V3 (`deepseek.v3-v1:0`) |
| AWS Auth | boto3 (default credentials profile) |

---

##  Prerequisites

- Python 3.9+
- VS Code (recommended)
- AWS account with **Amazon Bedrock** access
- DeepSeek V3 model enabled in your AWS region
- AWS credentials configured locally (`aws configure`)

---

##  Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

Install all required libraries in VS Code terminal:

```bash
pip install boto3
pip install langchain
pip install -U langchain-aws
pip install streamlit
pip install transformers
pip install PyYAML
```

Or install from `requirements.txt` if provided:

```bash
pip install -r requirements.txt
```

### 4. Configure AWS credentials

```bash
aws configure
```

Enter your:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Output format: `json`

> **Note:** Make sure your IAM user/role has `bedrock:InvokeModel` permission and DeepSeek V3 is enabled in Amazon Bedrock Model Access for your region.

---

##  Running the Chatbot

### Step 1 — Open the project in VS Code

```
your-repo/
├── chatbot_backend.py
├── chatbot_frontend.py
└── requirements.txt
```

### Step 2 — Run the Streamlit app

In the VS Code integrated terminal:

```bash
streamlit run chatbot_frontend.py
```

### Step 3 — Use the chatbot

- The app opens at `http://localhost:8501` in your browser
- Type a message in the input box at the bottom
- The chatbot maintains full conversation memory within the session
- Each response is powered by DeepSeek V3 via Amazon Bedrock

---

##  Project Structure

```
├── chatbot_backend.py      # LangChain + Bedrock setup, memory, conversation chain
├── chatbot_frontend.py     # Streamlit UI with custom dark theme
└── requirements.txt        # Python dependencies
```

### `chatbot_backend.py` — Key Functions

| Function | Description |
|---|---|
| `demo_chatbot()` | Initializes `ChatBedrockConverse` with DeepSeek V3 |
| `demo_memory()` | Creates `InMemoryChatMessageHistory` instance |
| `demo_conversation()` | Wraps LLM in `RunnableWithMessageHistory`, invokes with session memory |

---

##  Configuration

You can adjust these parameters in `chatbot_backend.py`:

```python
demo_llm = ChatBedrockConverse(
    credentials_profile_name="default",  # Change if using a named AWS profile
    model="deepseek.v3-v1:0",            # Model ID
    temperature=0.1,                      # Lower = more deterministic
    max_tokens=1000,                      # Max response length
)
```

---

##  Troubleshooting

| Issue | Fix |
|---|---|
| `AccessDeniedException` from Bedrock | Enable DeepSeek V3 in Bedrock Model Access console |
| `botocore.exceptions.NoCredentialsError` | Run `aws configure` or check your credentials file |
| `ModuleNotFoundError` | Ensure virtual environment is activated and all packages installed |
| Streamlit blank page | Check terminal for errors; try `streamlit run chatbot_frontend.py --server.port 8502` |

---



##  How Memory Works

This chatbot uses LangChain's `RunnableWithMessageHistory` to maintain conversation context:

1. On first message, a new `InMemoryChatMessageHistory` object is created and stored in `st.session_state`
2. Every subsequent message appends to the same memory object
3. The full history is passed to Bedrock on each invocation, giving the model context of the entire conversation
4. Memory is **session-scoped** — refreshing the browser starts a new conversation

---


