import base64
import json
import os
import sqlite3
from typing import Optional

from dotenv import load_dotenv
from groq import Groq

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

from reviews_api import get_product_rating

from memory import (
    get_order_history,
    get_user_preferences,
    save_user_preferences,
    get_current_user
)


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "store.db"
)


# ---------------------------------------------------------------------------
# Main LLM
# ---------------------------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ---------------------------------------------------------------------------
# Groq client for vision
# ---------------------------------------------------------------------------

groq_client = Groq(
    api_key=os.environ["GROQ_API_KEY"]
)


# ===========================================================================
# TOOLS
# ===========================================================================


# ---------------------------------------------------------------------------
# Search products
# ---------------------------------------------------------------------------

@tool
def search_products(
    query: str,
    max_price: Optional[float] = None,
    is_organic: Optional[bool] = None
) -> str:
    """
    Search the product database by keyword.

    Keyword is matched against:
    - product name
    - description
    - category

    Optional filters:
    - maximum price
    - organic status
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    sql = """
        SELECT
            id,
            name,
            category,
            price,
            description,
            is_organic
        FROM products
        WHERE 1=1
    """

    params = []

    # Keyword search
    if query:

        sql += """
            AND (
                name LIKE ?
                OR description LIKE ?
                OR category LIKE ?
            )
        """

        like = f"%{query}%"

        params.extend([
            like,
            like,
            like
        ])

    # Price filter
    if max_price is not None:

        sql += " AND price <= ?"

        params.append(max_price)

    # Organic filter
    if is_organic is not None:

        sql += " AND is_organic = ?"

        params.append(
            1 if is_organic else 0
        )

    cursor.execute(
        sql,
        params
    )

    rows = cursor.fetchall()

    conn.close()

    products = [
        {
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "price": row[3],
            "description": row[4],
            "is_organic": bool(row[5])
        }
        for row in rows
    ]

    return json.dumps(products)


# ---------------------------------------------------------------------------
# Get product rating
# ---------------------------------------------------------------------------

@tool
def get_rating(product_id: int) -> str:
    """
    Get the average customer rating and review count
    for a product.
    """

    result = get_product_rating(product_id)

    return json.dumps(result)


# ---------------------------------------------------------------------------
# Order history
# ---------------------------------------------------------------------------

@tool
def order_history() -> str:
    """
    Get the current user's previous orders.

    Use this when the user asks about:
    - previous purchases
    - past orders
    - order history
    - what they bought before
    """

    user_id = get_current_user()

    if user_id is None:
        return "No user session is active."

    orders = get_order_history()

    if not orders:
        return "The user has no previous orders."

    return json.dumps(
        orders,
        indent=2
    )


# ---------------------------------------------------------------------------
# Get preferences
# ---------------------------------------------------------------------------

@tool
def get_preferences() -> str:
    """
    Get the current user's saved shopping preferences.
    """

    user_id = get_current_user()

    if user_id is None:
        return "No user session is active."

    preferences = get_user_preferences()

    return json.dumps(
        preferences,
        indent=2
    )


# ---------------------------------------------------------------------------
# Save preferences
# ---------------------------------------------------------------------------

@tool
def save_preferences(
    prefers_organic: Optional[bool] = None,
    max_price: Optional[float] = None
) -> str:
    """
    Save the current user's long-term shopping preferences.

    Examples:
    - prefer organic products
    - maximum preferred price
    """

    user_id = get_current_user()

    if user_id is None:
        return "Error: No user session is active."

    try:

        preferences = save_user_preferences(
            prefers_organic=prefers_organic,
            max_price=max_price
        )

        return json.dumps(
            preferences,
            indent=2
        )

    except Exception as e:

        return f"Error saving preferences: {str(e)}"


# ---------------------------------------------------------------------------
# Checkout
# ---------------------------------------------------------------------------

@tool
def checkout(product_id: int) -> str:
    """
    Place an order for the given product ID.

    The order is saved for the current user.
    """

    # Get current user
    user_id = get_current_user()

    if user_id is None:
        return "Error: No user session is active."

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Find product
    cursor.execute(
        """
        SELECT
            name,
            price
        FROM products
        WHERE id = ?
        """,
        (product_id,)
    )

    row = cursor.fetchone()

    if not row:

        conn.close()

        return (
            f"Error: product with ID "
            f"{product_id} not found."
        )

    name, price = row

    # Save order with user ID
    cursor.execute(
        """
        INSERT INTO orders
        (
            product_id,
            product_name,
            price,
            ordered_at,
            user_id
        )
        VALUES (?, ?, ?, datetime('now'), ?)
        """,
        (
            product_id,
            name,
            price,
            user_id
        )
    )

    order_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return (
        f"Order #{order_id} confirmed! "
        f"'{name}' has been successfully ordered "
        f"for ${price:.2f}. "
        f"Your order will arrive in 3-5 business days. "
        f"Thank you for shopping with us!"
    )


# ---------------------------------------------------------------------------
# Product image analysis
# ---------------------------------------------------------------------------

@tool
def describe_product_image(
    image_path: str
) -> str:
    """
    Analyze a product image and return its key attributes as JSON.
    """

    print("VISION TOOL STARTED")
    print("Image path:", image_path)

    # Read image
    with open(
        image_path,
        "rb"
    ) as f:

        image_data = base64.b64encode(
            f.read()
        ).decode("utf-8")

    print("Image successfully encoded")

    # Determine MIME type
    ext = os.path.splitext(
        image_path
    )[1].lower().lstrip(".")

    mime = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp"
    }.get(
        ext,
        "image/jpeg"
    )

    print("MIME type:", mime)
    print("Sending image to Groq...")

    completion = groq_client.chat.completions.create(

        model="qwen/qwen3.8-27b",

        messages=[
            {
                "role": "user",

                "content": [

                    {
                        "type": "text",

                        "text": (
                            "Look at this product image "
                            "and identify the product.\n\n"

                            "Return ONLY a JSON object "
                            "with these fields:\n"

                            "product_type: what kind of "
                            "product it is\n"

                            "search_query: a short keyword "
                            "to search for it\n"

                            "is_organic: true if the label "
                            "says organic, false if not, "
                            "null if unclear\n"

                            "description: one sentence "
                            "describing the product"
                        )
                    },

                    {
                        "type": "image_url",

                        "image_url": {
                            "url": (
                                f"data:{mime};base64,"
                                f"{image_data}"
                            )
                        }
                    }
                ]
            }
        ],

        temperature=0,

        response_format={
            "type": "json_object"
        }
    )

    result = (
        completion
        .choices[0]
        .message
        .content
    )

    print("VISION RESULT:")
    print(result)

    return result


# ===========================================================================
# AGENT
# ===========================================================================

agent = create_agent(

    model=llm,

    tools=[
        search_products,
        get_rating,
        checkout,
        describe_product_image,
        order_history,
        get_preferences,
        save_preferences
    ],

    system_prompt=(

        "You are a helpful shopping assistant. "
        "Follow these rules strictly.\n\n"


        # ---------------------------------------------------------------
        # IMAGE SEARCH
        # ---------------------------------------------------------------

        "IMAGE SEARCH — when the user provides an image path:\n"

        "1. Call describe_product_image with the path "
        "to identify the product.\n"

        "2. Use the returned search_query and "
        "is_organic to call search_products.\n"

        "3. Continue with the BROWSING flow "
        "from step 2 onwards.\n\n"


        # ---------------------------------------------------------------
        # BROWSING
        # ---------------------------------------------------------------

        "BROWSING — when the user describes "
        "what they want to buy:\n"

        "1. Call search_products to find matching "
        "items. Apply any price or organic filters "
        "given by the user.\n"

        "2. For each candidate, call get_rating "
        "to retrieve its average rating.\n"

        "3. Filter by the user's minimum rating "
        "if specified.\n"

        "4. Present qualifying products as a "
        "numbered list. For each item use this "
        "exact format "
        "(plain text, no backticks, no code blocks, "
        "no bold, no italic):\n\n"

        "#<number>. <name> "
        "(ID:<product_id>) — "
        "$<price> ★<rating> — "
        "<organic or non-organic>\n\n"

        "Add a blank line between each product "
        "entry for readability.\n"

        "Always include (ID:X) so you can "
        "reference it later.\n"

        "5. If only one product qualifies, "
        "still show it in the list and ask:\n"

        "'Would you like to order it? "
        "Just say yes or give me the number.'\n"

        "6. Do NOT call checkout at this stage.\n\n"


        # ---------------------------------------------------------------
        # MEMORY
        # ---------------------------------------------------------------

        "MEMORY AND PERSONALIZATION — "
        "use memory when relevant:\n\n"

        "1. ORDER HISTORY:\n"

        "- If the user asks about previous purchases, "
        "past orders, or what they bought before, "
        "call order_history.\n"

        "- Never guess or invent previous orders.\n"

        "- Only report orders returned by the "
        "order_history tool.\n\n"


        "2. USER PREFERENCES:\n"

        "- If saved preferences may affect a "
        "product recommendation, call get_preferences.\n"

        "- Saved preferences may include a "
        "preference for organic products and "
        "a maximum preferred price.\n\n"


        "3. SAVING PREFERENCES:\n"

        "- If the user explicitly asks you to "
        "remember a long-term shopping preference, "
        "call save_preferences.\n"

        "- Examples include:\n"

        "'Remember that I prefer organic products.'\n"

        "'Always recommend organic products.'\n"

        "'Remember my budget is $20.'\n"

        "'Don't show me products above $20.'\n\n"


        "4. TEMPORARY REQUESTS:\n"

        "- Do not save temporary requests as "
        "permanent preferences.\n"

        "- For example, 'Find me something "
        "under $20 today' should not automatically "
        "change the user's saved maximum price.\n\n"


        "5. UPDATING PREFERENCES:\n"

        "- When the user explicitly provides "
        "a new preference, update the existing "
        "preference.\n"

        "- The most recent explicit preference "
        "takes priority.\n\n"


        "6. USING MEMORY:\n"

        "- Consider saved preferences when "
        "they are relevant to recommendations.\n"

        "- The user's current request always "
        "takes priority over saved preferences.\n"

        "- Do not force a saved preference when "
        "the user explicitly requests something different.\n\n"


        "7. MEMORY ACCURACY:\n"

        "- Never claim that something was remembered "
        "unless save_preferences succeeds.\n"

        "- Never claim an order exists unless it "
        "is returned by order_history.\n"

        "- Never invent or assume user preferences.\n\n"


        # ---------------------------------------------------------------
        # ORDERING
        # ---------------------------------------------------------------

        "ORDERING — when the user confirms they "
        "want to buy "
        "(e.g. 'yes', 'sure', 'go ahead', "
        "'order number 2', 'the first one', "
        "'get me #3'):\n"

        "1. Look at your previous message to find "
        "the (ID:X) for the chosen product.\n"

        "If only one product was listed and the "
        "user says 'yes', use that product's ID.\n"

        "2. Call checkout with that product_id, "
        "using the number from (ID:X).\n"

        "3. Confirm the order to the user "
        "in plain text.\n\n"

        "Never place an order unless the user "
        "explicitly confirms.\n"

        "Never guess a product_id. Always take "
        "it from the (ID:X) in your own "
        "previous message."
    )
)


# ===========================================================================
# TERMINAL TEST
# ===========================================================================

if __name__ == "__main__":

    # Set a test user for terminal testing
    from memory import set_current_user

    set_current_user("user_001")

    messages = []

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in [
            "exit",
            "quit"
        ]:
            break

        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        result = agent.invoke(
            {
                "messages": messages
            }
        )

        messages = result["messages"]

        print(
            "\nAssistant:",
            messages[-1].content
        )