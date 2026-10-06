# 🛍️ ShopAI – Agentic AI Shopping Assistant

An **Agentic AI-powered shopping assistant** built with Python, LangChain, LangGraph, Groq, SQLite, and Streamlit.

ShopAI can search products, compare prices, check ratings, remember user preferences, access order history, place orders, and understand products from uploaded images.

## 🏠 1. ShopAI Homepage

The ShopAI homepage provides a simple conversational interface where users can interact with the AI shopping assistant using natural language.

Users can describe what they are looking for, ask about products, check ratings, view their shopping preferences, access previous orders, and place orders through the assistant.

The sidebar also provides the option to upload a product image and search for similar products.
<img width="900" height="450" alt="image" src="https://github.com/user-attachments/assets/1bda0467-44b4-4a60-b60a-0804bfb0314a" />

## 🛡️ 2. Guardrail Example

ShopAI includes a guardrail mechanism that ensures the assistant stays focused on shopping-related tasks.

When a user asks an unrelated question, the guardrail prevents the request from being passed to the shopping agent and redirects the user toward supported shopping functionality.

This helps keep the AI assistant focused on its intended purpose.

<img width="900" height="450" alt="image" src="https://github.com/user-attachments/assets/e7b54d13-9e17-4b1a-ade8-7327fc9c6015" />

## 🖼️ 3. Find Products Using an Image

ShopAI also supports image-based product discovery.

Users can upload an image of a product through the **Shop by Image** option. The AI analyzes the uploaded image and generates relevant product information that can be used to search the product database for similar products.

This allows users to discover products without having to describe them manually using text.

<img width="900" height="450" alt="image" src="https://github.com/user-attachments/assets/faf6b018-7fdc-4c01-89d9-e502040cff99" />




---

## 🚀 Features

### 🤖 Agentic AI

Uses an LLM-powered agent that decides which tool to use based on the user's request.

The agent can:

- Search for products
- Check product ratings
- View previous orders
- Retrieve saved shopping preferences
- Save new preferences
- Complete product purchases
- Analyze product images
- Find products similar to an uploaded image

### 🔎 Product Search

Users can search products using natural language.

Example:

```text
Find organic honey under $20
```

The agent can identify the user's requirements and call the appropriate product-search tool.

### ⭐ Product Ratings & Reviews

Users can ask for product ratings and reviews.

Example:

```text
What is the rating of Organic Raw Honey?
```

### 🧠 User Memory

ShopAI maintains user-specific information such as:

- Order history
- Organic product preference
- Maximum preferred price

Example:

```text
What are my saved shopping preferences?
```

### 🛒 Checkout

Users can purchase products directly through the agent.

Example:

```text
Buy product 1
```

The order is stored in SQLite and associated with the current user.

### 🖼️ Image-Based Product Search

Users can upload an image of a product.

The vision model analyzes the image and extracts information that can be used to search for similar products.

Example:

```text
Find products similar to this image.
```

### 🛡️ Shopping Guardrails

The application prevents unrelated questions from being sent to the shopping agent.

For example:

```text
Who was Albert Einstein?
```

will be rejected because it is outside the shopping assistant's scope.

### 📊 Agent Evaluation

The project includes basic evaluation tests to verify whether the agent selects the correct tool for different user requests.

Example:

```text
I want organic honey under $20
```

Expected tool:

```text
search_products
```

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      Streamlit      │
                         │     Frontend        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     Guardrails      │
                         │ Shopping Validation │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Agentic AI Agent  │
                         │ LangChain/LangGraph │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
             ┌────────────┐  ┌────────────┐  ┌────────────┐
             │  Product   │  │  Memory    │  │  Vision    │
             │  Tools     │  │  Tools     │  │  Tool      │
             └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
                   │               │               │
                   └───────────────┼───────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │       SQLite        │
                         │      store.db       │
                         └─────────────────────┘
```

---

# 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web interface |
| LangChain | LLM and tool integration |
| LangGraph | Agent orchestration |
| Groq | LLM and vision inference |
| SQLite | Product, user, preference and order storage |
| Python-dotenv | Environment variable management |
| Requests | API requests |
| Pillow | Image processing |
| Git & GitHub | Version control |

---

# 📁 Project Structure

```text
store_agent/
│
├── app.py
│   └── Streamlit application
│
├── shopping_agent.py
│   └── Agent, tools and LLM integration
│
├── memory.py
│   └── User sessions, preferences and order history
│
├── guardrails.py
│   └── Shopping-related input validation
│
├── reviews_api.py
│   └── Product review functionality
│
├── setup_db.py
│   └── Initial database setup
│
├── migrate_db.py
│   └── Database migration scripts
│
├── evals.py
│   └── Agent tool-selection evaluation
│
├── resources/
│   └── Supporting resources
│
├── .env
│   └── API keys and environment variables
│
├── .gitignore
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/Nitin-sounkaria/ShopAI_project.git
```

Navigate into the project:

```bash
cd ShopAI_project
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file inside the project directory.

```env
GROQ_API_KEY=your_groq_api_key
```

Do **not** commit your `.env` file to GitHub.

The repository's `.gitignore` excludes `.env` files.

---

# 🗄️ Database Setup

Initialize the database:

```bash
python setup_db.py
```

If database migrations are required:

```bash
python migrate_db.py
```

The application uses SQLite for storing:

- Products
- Reviews
- Users
- User preferences
- Orders

---

# ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Streamlit will provide a local URL similar to:

```text
http://localhost:8501
```

Open that URL in your browser.

---

# 💬 Example Conversations

## Product Search

```text
User:
Find organic honey under $20
```

The agent searches the product database and returns matching products.

---

## Product Rating

```text
User:
What is the rating of Organic Raw Honey?
```

The agent uses the rating tool to retrieve the product rating.

---

## Order History

```text
User:
Show me my previous orders
```

The agent retrieves the current user's order history.

---

## Preferences

```text
User:
What are my saved shopping preferences?
```

The agent retrieves stored preferences.

---

## Saving Preferences

```text
User:
I prefer organic products under $20.
```

The agent can save these preferences for future shopping interactions.

---

## Checkout

```text
User:
Buy product 1
```

The checkout tool:

1. Identifies the current user
2. Finds the selected product
3. Creates the order
4. Stores the order in SQLite
5. Returns an order confirmation

---

# 🧠 Agent Tools

The agent has access to multiple tools.

| Tool | Purpose |
|---|---|
| `search_products` | Search products using filters |
| `get_rating` | Retrieve product ratings |
| `order_history` | Retrieve user's previous orders |
| `get_preferences` | Retrieve saved preferences |
| `save_preferences` | Save user shopping preferences |
| `checkout` | Place a product order |
| `describe_product_image` | Analyze an uploaded product image |

The LLM decides which tool should be called based on the user's request.

---

# 🖼️ Vision-Based Search

The application also supports image-based product discovery.

The uploaded image is passed to a vision-capable Groq model.

The vision tool attempts to determine:

- Product type
- Product characteristics
- Search keywords
- Whether the product appears organic

The resulting information can then be used to search the product database.

Example workflow:

```text
User uploads image
        ↓
Vision Model
        ↓
Product Description
        ↓
Search Query
        ↓
Product Database
        ↓
Similar Products
```

---

# 🛡️ Guardrails

ShopAI is designed specifically for shopping-related tasks.

The guardrail checks incoming user messages for shopping-related keywords.

Examples of accepted requests:

```text
Find organic honey
```

```text
Show products under $20
```

```text
What are my previous orders?
```

Examples of rejected requests:

```text
Explain quantum physics
```

```text
Write me a poem
```

```text
Who is the president of the United States?
```

The user is redirected back toward shopping-related functionality.

---

# 🧪 Evaluation

The project includes `evals.py` to test whether the agent selects the appropriate tool.

Example test cases:

| User Request | Expected Tool |
|---|---|
| I want organic honey under $20 | `search_products` |
| Find honey under $15 | `search_products` |
| Show me my previous orders | `order_history` |
| What are my saved shopping preferences? | `get_preferences` |

Run the evaluations with:

```bash
python evals.py
```

---

# 🔐 Security

Sensitive credentials should never be committed to GitHub.

The project uses environment variables for API keys:

```env
GROQ_API_KEY=your_api_key
```

The `.gitignore` file excludes:

```text
.env
.env.*
*.db
.venv/
__pycache__/
uploads/
temp/
```

---

# 🔄 Application Workflow

The overall application flow is:

```text
User
  │
  ▼
Streamlit UI
  │
  ▼
Guardrail
  │
  ├── Not Shopping Related ──► Rejection Message
  │
  ▼
Agent
  │
  ├── Product Search
  │
  ├── Product Rating
  │
  ├── Order History
  │
  ├── User Preferences
  │
  ├── Save Preferences
  │
  ├── Checkout
  │
  └── Image Search
  │
  ▼
SQLite Database / External API / Vision Model
  │
  ▼
Agent Response
  │
  ▼
User
```

---

# 🎯 Learning Objectives

This project demonstrates practical implementation of:

- Large Language Model applications
- Agentic AI
- Tool calling
- LangChain
- LangGraph
- Prompt engineering
- Structured tool execution
- SQLite database integration
- User memory
- Preference storage
- Order management
- Vision-language models
- Image-based product search
- Guardrails
- Agent evaluation
- Streamlit application development
- Environment variable management
- Git and GitHub

---

# 🚀 Future Improvements

Potential improvements include:

- Real payment gateway integration
- Real product inventory management
- Shopping cart functionality
- Product recommendations
- Better semantic product search using embeddings
- Vector database integration
- RAG-based product knowledge
- Multi-agent architecture
- Better image similarity search
- Conversation persistence
- Production-grade authentication
- Cloud database integration
- Deployment on Streamlit Cloud or another cloud platform
- Automated testing
- Better evaluation datasets
- Human-in-the-loop order confirmation

---

# 📌 Project Highlights

ShopAI combines several important Agentic AI concepts into one practical application:

**LLM + Tools + Memory + Database + Vision + Guardrails + Evaluation**

Instead of simply generating text, the AI agent can interact with external tools and take actions based on the user's request.

---

# 👨‍💻 Author

**Nitin Sounkaria**

B.Tech Information Technology

GitHub:  
https://github.com/Nitin-sounkaria

Project Repository:  
https://github.com/Nitin-sounkaria/ShopAI_project
