import os
import tempfile
import uuid

import streamlit as st

from guardrails import guardrail

from memory import (
    set_current_user,
    get_current_user,
    create_user,
    get_users,
    get_user_name
)

from shopping_agent import agent


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Shopping Assistant",
    page_icon="🛒",
    layout="wide"
)


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_image" not in st.session_state:
    st.session_state.pending_image = False

# NEW:
# Store the uploaded image path separately.
if "pending_image_path" not in st.session_state:
    st.session_state.pending_image_path = None

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "selected_user_name" not in st.session_state:
    st.session_state.selected_user_name = None


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:

    st.title("🛒 Shopping Assistant")

    st.divider()


    # -----------------------------------------------------------------------
    # USER ACCOUNT
    # -----------------------------------------------------------------------

    st.subheader("👤 Account")

    users = get_users()

    user_options = ["➕ Create New User"]

    for user in users:

        user_options.append(
            f"{user['name']} ({user['id']})"
        )


    # -----------------------------------------------------------------------
    # Determine current selection
    # -----------------------------------------------------------------------

    current_selection = "➕ Create New User"

    if st.session_state.user_id is not None:

        current_name = get_user_name(
            st.session_state.user_id
        )

        if current_name:

            current_selection = (
                f"{current_name} "
                f"({st.session_state.user_id})"
            )


    try:

        default_index = user_options.index(
            current_selection
        )

    except ValueError:

        default_index = 0


    selected_account = st.selectbox(
        "Select user",
        user_options,
        index=default_index
    )


    # -----------------------------------------------------------------------
    # CREATE NEW USER
    # -----------------------------------------------------------------------

    if selected_account == "➕ Create New User":

        st.markdown("### Create account")

        new_user_name = st.text_input(
            "Name",
            placeholder="Enter your name",
            key="new_user_name"
        )


        if st.button(
            "Create User",
            use_container_width=True
        ):

            name = new_user_name.strip()


            if not name:

                st.warning(
                    "Please enter your name."
                )


            else:

                # Generate unique user ID
                new_user_id = (
                    "user_"
                    + uuid.uuid4().hex[:8]
                )


                # Save user in database
                create_user(
                    new_user_id,
                    name
                )


                # Set Streamlit session
                st.session_state.user_id = (
                    new_user_id
                )

                st.session_state.selected_user_name = (
                    name
                )


                # Clear old conversation
                st.session_state.messages = []


                # Clear pending image
                st.session_state.pending_image = False

                st.session_state.pending_image_path = None


                # Set memory user
                set_current_user(
                    new_user_id
                )


                st.success(
                    f"Welcome, {name}!"
                )


                st.rerun()


    # -----------------------------------------------------------------------
    # EXISTING USER
    # -----------------------------------------------------------------------

    else:

        # Extract user ID
        #
        # Example:
        #
        # Nitin (user_12345678)
        #

        selected_user_id = (
            selected_account
            .split("(")[-1]
            .replace(")", "")
        )


        selected_user_name = (
            selected_account
            .split(" (")[0]
        )


        # ---------------------------------------------------------------
        # User changed
        # ---------------------------------------------------------------

        if (
            st.session_state.user_id
            != selected_user_id
        ):

            st.session_state.user_id = (
                selected_user_id
            )

            st.session_state.selected_user_name = (
                selected_user_name
            )


            # Start fresh conversation
            st.session_state.messages = []


            # Clear pending image
            st.session_state.pending_image = False

            st.session_state.pending_image_path = None


            st.rerun()


    # -----------------------------------------------------------------------
    # Set current user
    # -----------------------------------------------------------------------

    if st.session_state.user_id:

        set_current_user(
            st.session_state.user_id
        )


        user_name = get_user_name(
            st.session_state.user_id
        )


        if user_name:

            st.success(
                f"Logged in as **{user_name}**"
            )


    st.divider()


    # -----------------------------------------------------------------------
    # IMAGE SEARCH
    # -----------------------------------------------------------------------

    st.subheader("📷 Product Image")


    uploaded_file = st.file_uploader(
        "Upload a product image",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


    if uploaded_file is not None:

        if st.button(
            "🔍 Analyze Image",
            use_container_width=True
        ):

            if st.session_state.user_id is None:

                st.warning(
                    "Please create or select a user first."
                )


            else:

                # -------------------------------------------------------
                # Save image to temporary directory
                # -------------------------------------------------------

                temp_dir = tempfile.gettempdir()


                image_path = os.path.join(
                    temp_dir,
                    uploaded_file.name
                )


                with open(
                    image_path,
                    "wb"
                ) as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )


                # -------------------------------------------------------
                # IMPORTANT
                #
                # DO NOT put an image list inside messages.
                #
                # Groq expects messages[].content to be a string
                # for this agent.
                #
                # We store the path separately.
                # -------------------------------------------------------

                st.session_state.pending_image_path = (
                    image_path
                )


                st.session_state.pending_image = True


                st.rerun()


# ---------------------------------------------------------------------------
# Main page
# ---------------------------------------------------------------------------

st.title(
    "🛍️ AI Shopping Assistant"
)


# ---------------------------------------------------------------------------
# No user selected
# ---------------------------------------------------------------------------

if st.session_state.user_id is None:

    st.info(
        "👈 Please create a new user or select an existing user "
        "from the sidebar to start shopping."
    )

    st.stop()


# ---------------------------------------------------------------------------
# Current user
# ---------------------------------------------------------------------------

current_user_name = get_user_name(
    st.session_state.user_id
)


if current_user_name:

    st.caption(
        f"Shopping as **{current_user_name}**"
    )


# ---------------------------------------------------------------------------
# Helper function
# ---------------------------------------------------------------------------

def get_final_response(result):

    messages = result.get(
        "messages",
        []
    )


    if not messages:

        return "I couldn't generate a response."


    return messages[-1].content


# ---------------------------------------------------------------------------
# Display previous messages
# ---------------------------------------------------------------------------

for message in st.session_state.messages:

    role = message.get("role")

    content = message.get("content")


    if role in [
        "user",
        "assistant"
    ]:

        with st.chat_message(role):

            st.markdown(
                content
                if isinstance(
                    content,
                    str
                )
                else str(content)
            )


# ---------------------------------------------------------------------------
# Pending image request
# ---------------------------------------------------------------------------

if st.session_state.pending_image:

    # Get image path
    image_path = (
        st.session_state.pending_image_path
    )


    # Reset pending state
    st.session_state.pending_image = False

    st.session_state.pending_image_path = None


    if image_path:

        # ---------------------------------------------------------------
        # IMPORTANT
        #
        # The message content is now a STRING.
        #
        # This fixes:
        #
        # messages[3].content must be a string
        # ---------------------------------------------------------------

        image_message = (
            "Find products similar to this image. "
            f"Image path: {image_path}"
        )


        # Save message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": image_message
            }
        )


        # Show friendly message in UI
        with st.chat_message("user"):

            st.markdown(
                "🖼️ Find products similar to this image."
            )


        # ---------------------------------------------------------------
        # Agent
        # ---------------------------------------------------------------

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing the image..."
            ):

                try:

                    # Make sure correct user is active
                    set_current_user(
                        st.session_state.user_id
                    )


                    result = agent.invoke(
                        {
                            "messages":
                            st.session_state.messages
                        }
                    )


                    response = get_final_response(
                        result
                    )


                except Exception as e:

                    response = (
                        "Sorry, something went wrong.\n\n"
                        f"`{str(e)}`"
                    )


            st.markdown(
                response
            )


        # Save assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


    st.rerun()


# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------

if prompt := st.chat_input(
    "What would you like to shop for?"
):

    # -----------------------------------------------------------------------
    # Make sure user exists
    # -----------------------------------------------------------------------

    if st.session_state.user_id is None:

        st.warning(
            "Please create or select a user first."
        )

        st.stop()


    # -----------------------------------------------------------------------
    # Guardrail
    # -----------------------------------------------------------------------

    allowed, guardrail_message = (
        guardrail(prompt)
    )


    # -----------------------------------------------------------------------
    # Add user message
    # -----------------------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    with st.chat_message("user"):

        st.markdown(
            prompt
        )


    # -----------------------------------------------------------------------
    # If not shopping related
    # -----------------------------------------------------------------------

    if not allowed:

        response = guardrail_message


        with st.chat_message("assistant"):

            st.markdown(
                response
            )


        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )


        st.rerun()


    # -----------------------------------------------------------------------
    # Agent response
    # -----------------------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner(
            "Thinking..."
        ):

            try:

                # Make sure correct user is active
                set_current_user(
                    st.session_state.user_id
                )


                result = agent.invoke(
                    {
                        "messages":
                        st.session_state.messages
                    }
                )


                response = get_final_response(
                    result
                )


            except Exception as e:

                response = (
                    "Sorry, something went wrong.\n\n"
                    f"`{str(e)}`"
                )


        st.markdown(
            response
        )


    # -----------------------------------------------------------------------
    # Save assistant message
    # -----------------------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


    st.rerun()