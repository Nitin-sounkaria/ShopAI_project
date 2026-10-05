import sqlite3
import os


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "store.db"
)


# ---------------------------------------------------------------------------
# Current user
# ---------------------------------------------------------------------------

CURRENT_USER_ID = None


def set_current_user(user_id):
    """
    Set the user ID for the current application session.
    """
    global CURRENT_USER_ID
    CURRENT_USER_ID = user_id


def get_current_user():
    """
    Return the current user's ID.
    """
    return CURRENT_USER_ID


# ---------------------------------------------------------------------------
# User management
# ---------------------------------------------------------------------------

def create_user(user_id, name):
    """
    Create a new user and an empty preferences row.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO users (id, name)
        VALUES (?, ?)
        """,
        (user_id, name)
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO user_preferences
        (
            user_id,
            prefers_organic,
            max_price
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            None,
            None
        )
    )

    conn.commit()
    conn.close()

    return {
        "user_id": user_id,
        "name": name
    }


def get_users():
    """
    Return all users.
    """

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name
        FROM users
        ORDER BY name
        """
    )

    users = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1]
        }
        for row in users
    ]


def get_user_name(user_id):
    """
    Get a user's name.
    """

    if user_id is None:
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return row[0]


# ---------------------------------------------------------------------------
# Order history
# ---------------------------------------------------------------------------

def get_order_history():
    """
    Get orders belonging to the current user.
    """

    if CURRENT_USER_ID is None:
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            product_name,
            price,
            ordered_at
        FROM orders
        WHERE user_id = ?
        ORDER BY ordered_at DESC
        """,
        (CURRENT_USER_ID,)
    )

    orders = cursor.fetchall()

    conn.close()

    return [
        {
            "order_id": row[0],
            "product_name": row[1],
            "price": row[2],
            "ordered_at": row[3]
        }
        for row in orders
    ]


# ---------------------------------------------------------------------------
# User preferences
# ---------------------------------------------------------------------------

def get_user_preferences():
    """
    Get preferences belonging to the current user.
    """

    if CURRENT_USER_ID is None:
        return {
            "user_id": None,
            "prefers_organic": None,
            "max_price": None
        }

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            prefers_organic,
            max_price
        FROM user_preferences
        WHERE user_id = ?
        """,
        (CURRENT_USER_ID,)
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return {
            "user_id": CURRENT_USER_ID,
            "prefers_organic": None,
            "max_price": None
        }

    return {
        "user_id": CURRENT_USER_ID,
        "prefers_organic": (
            bool(row[0])
            if row[0] is not None
            else None
        ),
        "max_price": row[1]
    }


# ---------------------------------------------------------------------------
# Save user preferences
# ---------------------------------------------------------------------------

def save_user_preferences(
    prefers_organic=None,
    max_price=None
):
    """
    Save or update preferences for the current user.
    """

    if CURRENT_USER_ID is None:
        raise ValueError("No current user is set.")

    current = get_user_preferences()

    # Keep existing value if not being changed
    if prefers_organic is None:
        prefers_organic = current["prefers_organic"]

    if max_price is None:
        max_price = current["max_price"]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create preference row if it doesn't exist
    cursor.execute(
        """
        INSERT OR IGNORE INTO user_preferences
        (
            user_id,
            prefers_organic,
            max_price
        )
        VALUES (?, ?, ?)
        """,
        (
            CURRENT_USER_ID,
            None,
            None
        )
    )

    # Update preferences
    cursor.execute(
        """
        UPDATE user_preferences
        SET
            prefers_organic = ?,
            max_price = ?
        WHERE user_id = ?
        """,
        (
            1 if prefers_organic is True else
            0 if prefers_organic is False else
            None,
            max_price,
            CURRENT_USER_ID
        )
    )

    conn.commit()
    conn.close()

    return {
        "user_id": CURRENT_USER_ID,
        "prefers_organic": prefers_organic,
        "max_price": max_price
    }