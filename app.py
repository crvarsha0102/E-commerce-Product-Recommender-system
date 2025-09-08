import streamlit as st
import pandas as pd
from db import create_users_table, add_user, authenticate_user
from recommendation import content_based_recommendation, collaborative_filtering_recommendation

# Create the users table if not already created
create_users_table()

# Load data from CSV files
@st.cache_data
def load_trending_products():
    return pd.read_csv("trending_products.csv")

@st.cache_data
def load_train_data():
    return pd.read_csv("clean_data.csv")

# Load datasets
trending_products = load_trending_products()
train_data = load_train_data()

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Function to handle the signup page
def signup():
    st.title("Signup Page")
    
    # Take user input
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if password == confirm_password:
        if st.button("Sign Up"):
            # Add user to database
            add_user(username, email, password)
            st.success("Account created successfully! You can now log in.")
    else:
        st.error("Passwords do not match.")

# Function to handle the login page
def login():
    st.title("Login Page")
    
    # Take user input for login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        # Authenticate user from the database
        if authenticate_user(username, password):
            st.session_state.username = username
            st.session_state.authenticated = True
            st.session_state.page = "homepage"  # Set the page to homepage directly after login
            st.success("Login successful!")
            st.rerun()  # Use st.rerun() to reload and redirect to homepage
        else:
            st.error("Invalid username or password.")

# Function to display the cart page with item details, quantity, and remove option
def cart_page():
    st.title("Your Cart")

    # Back button to go to the previous page (homepage)
    if st.button("Back to Homepage"):
        st.session_state.page = "homepage"
        st.rerun()  # Rerun to go back to homepage

    # Check if cart is empty
    if len(st.session_state.cart) == 0:
        st.write("Your cart is empty.")
    else:
        for idx, item in enumerate(st.session_state.cart):
            product_name = item['name']
            quantity = item['quantity']
            product = item  # Use the product data directly from the cart
            
            # Display product image, name, and details
            col1, col2, col3 = st.columns([1, 3, 1])

            # Display product image
            with col1:
                image_urls = product['ImageURL'].split(" | ")
                st.image(image_urls[0], width=100)  # Show the first image

            # Display product details
            with col2:
                st.subheader(product["name"])
                st.write(f"Brand: {product['Brand']}")
                st.write(f"Reviews: {product['ReviewCount']}")  # You can replace with actual review data if available
                st.write(f"Rating: {product['Rating']} ⭐")  # You can replace with actual rating if available

                # Display the quantity input field
                new_quantity = st.number_input(
                    f"Quantity for {product['name']}", 
                    min_value=1, 
                    value=quantity, 
                    key=f"qty_{idx}"
                )

                # Update the cart if quantity changes
                if new_quantity != quantity:
                    st.session_state.cart[idx]['quantity'] = new_quantity

            # Display Remove button
            with col3:
                if st.button(f"Remove {product_name}", key=f"remove_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.success(f"{product_name} removed from cart.")
                    st.rerun()  # Refresh the page after removing an item

        # Add Proceed to Buy button
        if st.button("Proceed to Buy"):
            st.success("Proceeding to checkout...")  # Replace with checkout process logic
            # Here you can redirect the user to a checkout page or show the next steps.

        # Display recommended products based on collaborative filtering
        st.header("Recommended Products Based on Your Cart")
        recommended_products = collaborative_filtering_recommendation(st.session_state.cart, train_data)
        for product in recommended_products:
            st.write(f"- {product}")

# Homepage logic after successful login
# Homepage logic after successful login
def homepage():
    st.title("E-commerce Platform: Your Shopping Destination")

    # Search Bar
    search_query = st.text_input("Search for Products...", "")

    if search_query:
        # Get the top 5 recommended products based on content-based filtering
        st.header(f"Recommended Products for '{search_query}'")

        # Perform content-based filtering
        recommended_products = content_based_recommendation(search_query, train_data)

        if recommended_products:
            for product_name in recommended_products:
                # Retrieve product details from the train_data DataFrame
                product = train_data[train_data["Name"] == product_name]

                if not product.empty:
                    product = product.iloc[0]  # Safely access the first matching product

                    # Display product details in a two-column layout
                    col1, col2 = st.columns([1, 3])

                    # Display product image
                    with col1:
                        image_urls = product['ImageURL'].split(" | ") if isinstance(product['ImageURL'], str) else []
                        if image_urls:
                            st.image(image_urls[0], width=100)  # Show the first image

                    # Display product details
                    with col2:
                        st.subheader(product["Name"])
                        st.write(f"Brand: {product['Brand']}")
                        st.write(f"Reviews: {product['ReviewCount']}")
                        st.write(f"Rating: {product['Rating']} ⭐")

                        # Add "Buy Now" button
                        if st.button(f"Buy Now - {product['Name']}"):
                            # Add product to cart with all necessary details
                            st.session_state.cart.append({
                                'name': product['Name'],
                                'quantity': 1,  # Default quantity
                                'Brand': product['Brand'],
                                'ImageURL': product['ImageURL'],
                                'ReviewCount': product['ReviewCount'],  # Add ReviewCount to cart
                                'Rating': product['Rating']  # Add Rating to cart
                            })
                            st.success(f"{product['Name']} added to cart!")
                else:
                    # Handle case where product details are missing
                    st.warning(f"Details for '{product_name}' are not available.")
        else:
            st.write("No products match your search query.")
    else:
        # Display trending products if no search query
        st.header("Trending Products")
        for i, product in trending_products.iterrows():
            col1, col2 = st.columns([1, 3])

            # Display product image
            with col1:
                image_urls = product['ImageURL'].split(" | ") if isinstance(product['ImageURL'], str) else []
                if image_urls:
                    st.image(image_urls[0], width=100)  # Show the first image

            # Display product details
            with col2:
                st.subheader(product["Name"])
                st.write(f"Brand: {product['Brand']}")
                st.write(f"Reviews: {product['ReviewCount']}")
                st.write(f"Rating: {product['Rating']} ⭐")

                # Add "Buy Now" button
                if st.button(f"Buy Now - {product['Name']}"):
                    # Add product to cart with all necessary details
                    st.session_state.cart.append({
                        'name': product['Name'],
                        'quantity': 1,  # Default quantity
                        'Brand': product['Brand'],
                        'ImageURL': product['ImageURL'],
                        'ReviewCount': product['ReviewCount'],  # Add ReviewCount to cart
                        'Rating': product['Rating']  # Add Rating to cart
                    })
                    st.success(f"{product['Name']} added to cart!")

# Sidebar to choose between Login and Signup
st.sidebar.title("Welcome to E-commerce Platform")

# Add a Cart option in the Sidebar
if "authenticated" in st.session_state and st.session_state.authenticated:
    # Cart Icon
    cart_count = len(st.session_state.cart)
    cart_button = st.sidebar.button(f"🛒 Cart ({cart_count})", key="cart_button")
    
    if cart_button:
        # Redirect to cart page
        st.session_state.page = "cart"
        st.rerun()

# Check if the user is authenticated
if "authenticated" in st.session_state and st.session_state.authenticated:
    # Check if page is set to 'cart'
    if "page" in st.session_state and st.session_state.page == "cart":
        cart_page()
    elif "page" in st.session_state and st.session_state.page == "homepage":
        homepage()
else:
    # Otherwise, show the login/signup options
    app_mode = st.sidebar.selectbox("Choose Action", ["Login", "Signup"])

    if app_mode == "Signup":
        signup()
    else:
        login()