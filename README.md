# 📦 ShopAI – Agentic AI Shopping Assistant

An AI-powered shopping assistant built with **Python, LangChain, LangGraph, Groq, SQLite, and Streamlit**.

ShopAI can search products, compare prices, check ratings and reviews, remember user preferences, access order history, place orders, and even find similar products from an uploaded image.

---

## 🚀 Features

### 🤖 Agentic AI

ShopAI uses an AI agent that decides which tool to use based on the user's request.

The agent can:

- Search for products
- Filter products by price
- Check product ratings
- Read customer reviews
- Remember shopping preferences
- Retrieve previous orders
- Place orders
- Analyze product images
- Find similar products
- Handle multiple users
- Reject unrelated queries using guardrails

---

### 🔎 Product Search

Users can search for products using natural language.

Example:

> Find organic honey under $20

The agent can identify the user's requirements and call the appropriate product-search tool.

---

### ⭐ Ratings & Reviews

Users can ask about product ratings and reviews.

Example:

> What is the rating of Organic Raw Honey?

The agent retrieves the relevant information from the database and presents it to the user.

---

### 🧠 Persistent User Memory

ShopAI remembers user-specific information such as:

- Previous orders
- Organic product preferences
- Maximum preferred price
- Current user session

Example:

> What are my shopping preferences?

The assistant can retrieve the user's saved preferences from SQLite.

---

### 🛒 Order Management

Users can place orders directly through the assistant.

Example:

> Order product 1

The system creates an order in the SQLite database and returns an order confirmation.

Example response:

```text
Order #12 confirmed!
'Organic Raw Honey' has been successfully ordered for $14.99.
Your order will arrive in 3-5 business days.
👤 Multi-User Support

ShopAI supports separate user accounts.

Each user can have their own:

User ID
Name
Preferences
Order history

This prevents one user's shopping history from being mixed with another user's data.

🛡️ Guardrails

The application includes a shopping-focused guardrail system.

If a user asks an unrelated question, the assistant responds with a message explaining that it is designed for shopping-related tasks.

Example:

User:
Who invented the telephone?

ShopAI:
I'm your shopping assistant, so I can help you find products,
compare prices, check ratings, remember your preferences,
and place orders. What would you like to shop for?
🖼️ Image-Based Product Discovery

Users can upload a product image and ask the assistant to find similar products.

The system:

Receives the uploaded image
Sends the image to a vision model
Extracts product characteristics
Generates a search query
Searches the product database
Returns similar products

This allows users to search for products using images instead of only text.

📊 Agent Evaluation

ShopAI includes an evaluation system to verify whether the agent selects the correct tools for different queries.

Example evaluation cases:

"I want organic honey under $20"
→ search_products

"Find honey under $15"
→ search_products

"Show me my previous orders"
→ order_history

"What are my saved shopping preferences?"
→ get_preferences
🏗️ Architecture
                    ┌─────────────────────┐
                    │      User           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Streamlit       │
                    │       App           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Guardrails      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    AI Shopping      │
                    │       Agent         │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
      ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
      │   Product    │ │   Memory &   │ │    Image     │
      │   Search     │ │    Orders    │ │   Analysis   │
      └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                     ┌─────────────────┐
                     │     SQLite      │
                     │    Database     │
                     └─────────────────┘
🧰 Tech Stack
Technology	Purpose
Python	Core programming language
Streamlit	Web application interface
LangChain	LLM and tool integration
LangGraph	Agent orchestration
Groq	LLM and vision inference
GPT-OSS-120B	General-purpose agent reasoning
Qwen3.8-27B	Image/product analysis
SQLite	Database
SQL	Data querying
Python-dotenv	Environment variable management
Requests	API requests
Pillow	Image processing
📁 Project Structure
store_agent/
│
├── app.py
├── shopping_agent.py
├── reviews_api.py
├── setup_db.py
├── store.db
├── memory.py
├── migrate_db.py
├── evals.py
├── guardrails.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── resources/
│
└── .env
📄 File Overview
app.py

Streamlit frontend responsible for:

User interface
Chat interface
User selection
New user creation
Image uploads
Agent interaction
Session management
shopping_agent.py

Contains the main AI shopping agent and its tools.

Tools include:

search_products
get_rating
order_history
get_preferences
save_preferences
checkout
describe_product_image
memory.py

Handles user-specific persistent information.

It manages:

Current user
Order history
User preferences
Preference updates
guardrails.py

Controls whether incoming requests are shopping-related.

It prevents the assistant from being used as a general-purpose chatbot.

reviews_api.py

Handles product review-related functionality.

setup_db.py

Creates and initializes the SQLite database.

migrate_db.py

Handles database migrations such as adding:

Users
User preferences
User IDs to orders
evals.py

Contains evaluation cases used to test whether the agent chooses the correct tool.

requirements.txt

Contains the Python dependencies required to run the project.

🗄️ Database

ShopAI uses SQLite for persistent storage.

Main tables include:

products
reviews
orders
users
user_preferences
Products

Stores product information such as:

Product ID
Product name
Price
Organic status
Reviews

Stores product reviews and ratings.

Orders

Stores:

Order ID
Product ID
Product name
Price
Order date
User ID
Users

Stores:

User ID
User name
User Preferences

Stores:

User ID
Organic preference
Maximum preferred price
⚙️ Installation
1. Clone the Repository
git clone https://github.com/Nitin-sounkaria/ShopAI_project.git

Move into the project directory:

cd ShopAI_project
2. Create a Virtual Environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
🔑 Environment Variables

Create a .env file in the project root.

GROQ_API_KEY=your_groq_api_key

Never commit your actual API key to GitHub.

The .gitignore file is configured to prevent .env from being uploaded.

🗃️ Initialize the Database

Run:

python setup_db.py

If database migrations are required:

python migrate_db.py
▶️ Run the Application

Start Streamlit:

streamlit run app.py

The application will open in your browser.

💬 Example Conversations
Product Search
User:
Find organic honey under $20

ShopAI searches the available products and returns matching products.

Product Rating
User:
What is the rating of Organic Raw Honey?

ShopAI retrieves the product rating.

Order History
User:
Show me my previous orders

ShopAI retrieves the current user's order history.

Preferences
User:
What are my saved shopping preferences?

ShopAI retrieves the user's saved preferences.

Saving Preferences
User:
I prefer organic products and I don't want to spend more than $20.

ShopAI can save these preferences for future shopping interactions.

Checkout
User:
Order Organic Raw Honey

The agent identifies the product and uses the checkout tool to create the order.

Image Search
User:
Find products similar to this image.

The user uploads an image and ShopAI uses the vision model to analyze it and search for similar products.

🧠 Agent Tools

The AI agent has access to multiple tools.

Tool	Purpose
search_products	Search products
get_rating	Retrieve ratings/reviews
order_history	Retrieve user's orders
get_preferences	Retrieve saved preferences
save_preferences	Save user preferences
checkout	Create a new order
describe_product_image	Analyze an uploaded product image

The agent decides which tool to use based on the user's request.

🛡️ Security

The project follows several basic security practices.

API Keys

API keys are stored in .env rather than directly inside source code.

Git Protection

.gitignore prevents sensitive files from being committed.

Ignored files include:

.env
*.db
.venv/
__pycache__/
uploads/
Database

User-specific information is associated with a user ID to keep orders and preferences separated.

🧪 Evaluation

The project includes an evaluation script:

python evals.py

The evaluation checks whether the agent selects the expected tool for different shopping requests.

Example:

Input:
I want organic honey under $20

Expected tool:
search_products
🔄 Development Workflow

Typical development workflow:

1. Modify code
      ↓
2. Run application
      ↓
3. Test agent
      ↓
4. Run evaluations
      ↓
5. Fix issues
      ↓
6. Git commit
      ↓
7. Git push
🚧 Future Improvements

Potential improvements for ShopAI include:

Real e-commerce API integration
Real payment gateway integration
Delivery tracking
Product recommendations
Semantic/vector search
RAG-based product knowledge
Conversation summarization
Better image similarity search
Advanced user profiles
Product inventory management
Admin dashboard
Production authentication
Cloud database deployment
Deployment on a cloud platform
Better agent observability and tracing
More comprehensive agent evaluations
🎯 Learning Outcomes

This project demonstrates practical experience with:

Agentic AI
LLM tool calling
LangChain
LangGraph
Prompt engineering
Function/tool design
AI agents
Vision models
SQLite
SQL
Persistent memory
Multi-user sessions
Guardrails
Streamlit
API integration
Agent evaluation
Git and GitHub
Environment variable management
📌 Why This Project?

ShopAI was built to explore how Agentic AI can be used in real-world applications rather than simply creating a basic chatbot.

The system combines:

LLM
+
Tools
+
Memory
+
Database
+
Guardrails
+
Vision
+
Evaluation

to create a practical AI shopping assistant capable of taking actions based on user requests.

👨‍💻 Author

Nitin Sounkaria

B.Tech – Information Technology

GitHub:

https://github.com/Nitin-sounkaria

Project:

https://github.com/Nitin-sounkaria/ShopAI_project

⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.

📜 License

This project is intended for educational and portfolio purposes.
