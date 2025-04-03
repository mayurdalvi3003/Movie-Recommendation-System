import streamlit as st
import pandas as pd
import pickle
import requests
import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('pic.jpeg')


# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Please log in or sign up to access this page.")
    st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: white !important;
        color: black !important;
        border-radius: 5px;
        font-weight: bold;
        padding: 8px 16px;
    }
    </style>
    """,
    unsafe_allow_html=True)

    # Toggle between Login and Sign Up
    auth_choice = st.radio("Select an option:", ["Sign Up" ,"Login"])


    if auth_choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            from auth import validate_login  # Import inside to avoid circular import issues

            if validate_login(username, password):
                st.success(f"Welcome {username}!")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.rerun()  # Refresh page
            else:
                st.error("Invalid Username or Password!")

    elif auth_choice == "Sign Up":
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if st.button("Sign Up"):
            if new_password == confirm_password:
                from auth import register_user  # Ensure this function exists in auth.py

                if register_user(new_username, new_password):
                    st.success("Account created successfully! Please log in.")
                else:
                    st.error("Username already exists. Try another one.")
            else:
                st.error("Passwords do not match!")

    st.stop()  # Stop execution if user isn't logged in

# User is logged in, show recommendation system

def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=dfc88b60ef67ac3eadefe5547667ee5e&language=en-US")
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown('<p style="font-size:40px; color:white; font-weight:bold;">🎬 Movie Recommender System</p>', unsafe_allow_html=True)
st.markdown('<p style="font-weight:bold; font-size:30px;color:white;">Select a Movie:</p>', unsafe_allow_html=True)

selected_movie_name = st.selectbox('', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "username": None}))
