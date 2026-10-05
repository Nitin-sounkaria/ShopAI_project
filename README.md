\# 🛍️ ShopAI – Agentic AI Shopping Assistant



ShopAI is an \*\*Agentic AI-powered shopping assistant\*\* built with Python, LangChain/LangGraph, Groq, SQLite, and Streamlit.



It allows users to interact with a store using natural language to \*\*search products, compare prices, check ratings, manage shopping preferences, view order history, place orders, and discover similar products using images\*\*.



The project demonstrates how an AI agent can combine an LLM with external tools, persistent user memory, databases, guardrails, and vision models to perform real-world tasks.



\---



\## 🚀 Features



\### 🤖 Agentic AI

\- Natural language shopping conversations

\- LLM-powered tool selection

\- Multi-step task execution

\- Database-backed actions



\### 🔎 Product Search

Search products using natural language and requirements such as price and organic preference.



Example:

```text

Find organic honey under $20

```



\### ⭐ Product Ratings \& Reviews

Ask the assistant to check product ratings before purchasing.



\### 🧠 Persistent User Memory

Stores user-specific information such as:

\- Previous orders

\- Organic product preference

\- Maximum preferred price

\- User account information



\### 🛒 Checkout \& Orders

Users can place orders directly through the AI assistant. Orders are associated with the current user.



\### 👤 Multi-User Support

Each user has a separate account, order history, and shopping preferences.



\### 🛡️ Shopping Guardrails

A shopping-focused guardrail keeps unrelated requests outside the shopping agent.



\### 🖼️ Image-Based Product Discovery

Users can upload a product image and ask the assistant to find similar products.



\### 📊 Agent Evaluation

Evaluation tests verify whether the agent selects the correct tool for different requests.



\---



\# 🏗️ System Architecture



```text

&#x20;                        ┌─────────────────────┐

&#x20;                        │      Streamlit      │

&#x20;                        │    Web Interface    │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │     Guardrails      │

&#x20;                        │  Shopping Request   │

&#x20;                        │      Filtering      │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │    ShopAI Agent     │

&#x20;                        │                     │

&#x20;                        │ LangChain /         │

&#x20;                        │ LangGraph           │

&#x20;                        └──────────┬──────────┘

&#x20;                                   │

&#x20;             ┌─────────────────────┼─────────────────────┐

&#x20;             │                     │                     │

&#x20;             ▼                     ▼                     ▼

&#x20;     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐

&#x20;     │    Product    │     │     User      │     │    Vision     │

&#x20;     │     Tools     │     │    Memory     │     │     Model     │

&#x20;     └───────┬───────┘     └───────┬───────┘     └───────┬───────┘

&#x20;             │                     │                     │

&#x20;             └─────────────────────┼─────────────────────┘

&#x20;                                   │

&#x20;                                   ▼

&#x20;                        ┌─────────────────────┐

&#x20;                        │       SQLite        │

&#x20;                        │      Database       │

&#x20;                        └─────────────────────┘

```



\---



\# 🧰 Tech Stack



| Technology | Purpose |

|---|---|

| Python | Core programming language |

| LangChain | LLM and tool orchestration |

| LangGraph | Agent runtime and workflow |

| Groq | LLM inference |

| GPT-OSS-120B | General-purpose shopping agent |

| Qwen3.8-27B | Vision-based product analysis |

| Streamlit | Web application interface |

| SQLite | Local database |

| SQL | Database queries |

| Python-dotenv | Environment variable management |

| Requests | API communication |

| Pillow | Image processing |



\---



\# 📁 Project Structure



```text

ShopAI\_project/

│

├── app.py

├── shopping\_agent.py

├── reviews\_api.py

├── setup\_db.py

├── migrate\_db.py

├── memory.py

├── guardrails.py

├── evals.py

├── requirements.txt

├── README.md

├── .gitignore

│

└── resources/

&#x20;   └── ...

```



\---



\# 📄 File Overview



\### `app.py`

Streamlit frontend responsible for the user interface, sessions, user selection, chat, image uploads, and agent interaction.



\### `shopping\_agent.py`

Core AI agent containing the LLM configuration, agent creation, shopping tools, checkout, memory tools, and image analysis.



\### `memory.py`

Handles user accounts, order history, shopping preferences, and current-user state.



\### `guardrails.py`

Contains the shopping-focused guardrail system.



\### `reviews\_api.py`

Handles product review and rating functionality.



\### `setup\_db.py`

Creates and initializes the SQLite database.



\### `migrate\_db.py`

Handles database changes and migrations.



\### `evals.py`

Contains evaluation logic for testing agent tool selection.



\---



\# 🗄️ Database



ShopAI uses \*\*SQLite\*\* for local data persistence.



Main tables include:



```text

products

reviews

orders

users

user\_preferences

```



\### Users



```text

id

name

```



\### User Preferences



```text

user\_id

prefers\_organic

max\_price

```



\### Orders



```text

id

product\_id

product\_name

price

ordered\_at

user\_id

```



\---



\# 🔧 Installation



\## 1. Clone the Repository



```bash

git clone https://github.com/Nitin-sounkaria/ShopAI\_project.git

cd ShopAI\_project

```



\## 2. Create a Virtual Environment



On Windows:



```powershell

python -m venv .venv

```



Activate it:



```powershell

.venv\\Scripts\\activate

```



\## 3. Install Dependencies



```powershell

pip install -r requirements.txt

```



\---



\# 🔐 Environment Variables



Create a `.env` file inside the project directory:



```env

GROQ\_API\_KEY=your\_groq\_api\_key\_here

```



\*\*Never commit your real `.env` file or API keys to GitHub.\*\*



\---



\# 🗃️ Database Setup



Initialize the database:



```powershell

python setup\_db.py

```



If a migration is required:



```powershell

python migrate\_db.py

```



\---



\# ▶️ Run the Application



Start the Streamlit application:



```powershell

streamlit run app.py

```



\---



\# 💬 Example Conversations



\### Product Search



```text

Find organic honey under $20.

```



\### Price Search



```text

Show me honey under $15.

```



\### Product Rating



```text

What is the rating of Organic Raw Honey?

```



\### Order History



```text

Show me my previous orders.

```



\### Preferences



```text

What are my saved shopping preferences?

```



\### Save Preferences



```text

I prefer organic products and my maximum budget is $20.

```



\### Purchase



```text

I want to buy Organic Raw Honey.

```



\### Image Search



Upload an image and ask:



```text

Find products similar to this image.

```



\---



\# 🧠 Agent Tools



The ShopAI agent can use different tools depending on the user's request.



```text

&#x20;                   User Request

&#x20;                        │

&#x20;                        ▼

&#x20;                 ┌─────────────┐

&#x20;                 │  ShopAI     │

&#x20;                 │   Agent     │

&#x20;                 └──────┬──────┘

&#x20;                        │

&#x20;         ┌──────────────┼──────────────┐

&#x20;         │              │              │

&#x20;         ▼              ▼              ▼

&#x20;search\_products    get\_rating    order\_history

&#x20;         │              │              │

&#x20;         ▼              ▼              ▼

&#x20;     Products         Reviews        Orders



&#x20;         ┌──────────────┼──────────────┐

&#x20;         │              │              │

&#x20;         ▼              ▼              ▼

&#x20;get\_preferences  save\_preferences   checkout

&#x20;         │              │              │

&#x20;         ▼              ▼              ▼

&#x20;     User Data       User Data        Order

```



\### Available Tools



\- `search\_products` — Searches the store database.

\- `get\_rating` — Retrieves product rating information.

\- `order\_history` — Retrieves the current user's previous orders.

\- `get\_preferences` — Retrieves saved shopping preferences.

\- `save\_preferences` — Stores or updates user preferences.

\- `checkout` — Creates a new order for the current user.

\- `describe\_product\_image` — Analyzes an uploaded product image.



\---



\# 🛡️ Guardrails



The application uses a shopping-focused guardrail.



For example:



```text

Find organic honey under $20

```



is accepted.



An unrelated request such as:



```text

Write me a poem about space.

```



can be rejected with a shopping-focused response.



The purpose is to keep the agent aligned with its intended domain.



\---



\# 📊 Evaluation



The project contains basic evaluations for agent tool selection.



Example:



```text

Query:

"I want organic honey under $20"



Expected:

search\_products

```



```text

Query:

"Show me my previous orders"



Expected:

order\_history

```



```text

Query:

"What are my saved shopping preferences?"



Expected:

get\_preferences

```



These tests help verify that the agent chooses the appropriate tool for different requests.



\---



\# 🔒 Security



The project uses `.gitignore` to prevent sensitive and local files from being committed.



Examples:



```text

.env

\*.db

\_\_pycache\_\_/

.venv/

```



API keys should always be stored in environment variables.



\*\*Never commit your real API key to GitHub.\*\*



\---



\# 🧪 Development Workflow



```text

1\. Modify the agent/tools

&#x20;         ↓

2\. Test locally

&#x20;         ↓

3\. Run evaluation tests

&#x20;         ↓

4\. Test Streamlit application

&#x20;         ↓

5\. git add .

&#x20;         ↓

6\. git commit

&#x20;         ↓

7\. git push

```



\---



\# 🔮 Future Improvements



\- \[ ] RAG-based product knowledge

\- \[ ] Vector database integration

\- \[ ] Semantic product search

\- \[ ] Product embeddings

\- \[ ] Better conversational memory

\- \[ ] Personalized recommendation ranking

\- \[ ] Real-time inventory management

\- \[ ] Real payment gateway integration

\- \[ ] Production authentication

\- \[ ] Cloud database deployment

\- \[ ] Agent observability

\- \[ ] Advanced agent evaluation

\- \[ ] Automated evaluation pipelines

\- \[ ] Improved multimodal product understanding

\- \[ ] Cloud deployment



\---



\# 🎯 What This Project Demonstrates



This project demonstrates practical implementation of:



\- Agentic AI

\- LLM-powered agents

\- Tool calling

\- LangChain

\- LangGraph

\- Prompt engineering

\- AI application development

\- Persistent memory

\- User-specific state

\- SQL and database integration

\- SQLite

\- AI guardrails

\- Multimodal AI

\- Vision models

\- Agent evaluation

\- Streamlit

\- API integration

\- Environment variable management



\---



\# 📚 Key Learning Concept



The project explores how an LLM can move beyond simple question answering and interact with external systems.



The agent follows a workflow similar to:



```text

Understand User Request

&#x20;       ↓

Determine Required Action

&#x20;       ↓

Select Appropriate Tool

&#x20;       ↓

Interact with Database / API

&#x20;       ↓

Process Result

&#x20;       ↓

Generate Natural Language Response

```



This is the core idea behind building practical \*\*Agentic AI applications\*\*.



\---



\# 👨‍💻 Author



\## Nitin Sounkaria



\*\*B.Tech – Information Technology\*\*



GitHub:  

https://github.com/Nitin-sounkaria



\---



\# ⭐ Support



If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.



\---



\## 📌 Project Repository



https://github.com/Nitin-sounkaria/ShopAI\_project



