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
    /* Netflix-style dark theme */
    .stApp {{
        background: #141414;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.85);
        z-index: -1;
    }}
    /* Sidebar - Netflix black */
    section[data-testid="stSidebar"] {{
        background: #000000;
        border-right: 1px solid #333;
    }}
    section[data-testid="stSidebar"] .stButton button {{
        background: #E50914 !important;
        border: 2px solid #E50914;
        box-shadow: 0 2px 8px rgba(229,9,20,0.4);
    }}
    section[data-testid="stSidebar"] .stButton button:hover {{
        background: #f40612 !important;
        box-shadow: 0 4px 16px rgba(229,9,20,0.6);
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('pic.jpeg')


# Check if user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    # Netflix-style Auth Page CSS - Compact (no scroll)
    st.markdown("""
    <style>
    /* Reduce page padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }

    /* Auth page title */
    .auth-title {
        font-size: 32px;
        font-weight: 900 !important;
        text-align: center;
        color: #E50914;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
        font-family: 'Arial', sans-serif !important;
        text-shadow: 2px 2px 8px rgba(229,9,20,0.5);
    }

    /* Auth subtitle */
    .auth-subtitle {
        font-size: 13px;
        color: #808080;
        text-align: center;
        margin-bottom: 15px;
        font-weight: 700 !important;
        font-family: 'Arial', sans-serif !important;
    }

    /* Radio button styling */
    .stRadio label {
        color: #fff !important;
        font-weight: 700 !important;
        font-family: 'Arial', sans-serif !important;
        font-size: 13px;
    }

    .stRadio [role="radio"] {
        background-color: #E50914 !important;
        border-color: #E50914 !important;
    }

    .stRadio > div {
        margin-bottom: 10px;
    }

    /* Input fields - Netflix style, compact */
    .stInput {
        margin-bottom: 8px;
    }

    .stInput input {
        background: #181818 !important;
        border: 1px solid #333 !important;
        color: #fff !important;
        font-weight: 700 !important;
        font-family: 'Arial', sans-serif !important;
        height: 40px;
    }

    .stInput input:focus {
        border-color: #E50914 !important;
    }

    .stInput label {
        color: #fff !important;
        font-weight: 700 !important;
        font-family: 'Arial', sans-serif !important;
        font-size: 13px;
        margin-bottom: 4px;
    }

    /* Buttons - Netflix red, compact */
    .stButton button {
        background: #E50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px;
        padding: 10px 35px;
        font-size: 13px;
        font-weight: 900 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(229,9,20,0.3);
        font-family: 'Arial', sans-serif !important;
    }

    .stButton button:hover {
        background: #f40612 !important;
        box-shadow: 0 4px 20px rgba(229,9,20,0.5);
        letter-spacing: 1.5px;
    }

    /* Success/Error messages */
    .stAlert {
        background: #181818;
        border: 1px solid #333;
        color: #fff;
        font-weight: 700 !important;
        font-family: 'Arial', sans-serif !important;
        padding: 8px;
        margin: 5px 0;
    }

    /* Radio container */
    .stRadio {
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Auth Header - Compact
    st.markdown('<p class="auth-title">🎬 MOVIE RECOMMENDER</p>', unsafe_allow_html=True)
    st.markdown('<p class="auth-subtitle">LOGIN OR SIGN UP TO CONTINUE</p>', unsafe_allow_html=True)

    # Toggle between Login and Sign Up
    auth_choice = st.radio("", ["Sign Up", "Login"], label_visibility="collapsed", horizontal=True)


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
    recommended_movie_ids = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movie_ids.append(movie_id)

    return recommended_movies, recommended_movies_posters, recommended_movie_ids

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Custom CSS for Netflix-style UI with compact layout
st.markdown("""
<style>
    /* Apply Arial font globally with BOLD text */
    * {
        font-family: 'Arial', sans-serif !important;
        font-weight: 700 !important;
    }

    /* Main content - reduce padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    /* Main title - Netflix red, BOLD */
    .main-title {
        font-size: 40px;
        font-weight: 900 !important;
        text-align: center;
        color: #E50914;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
        font-family: 'Arial', sans-serif !important;
        text-shadow: 2px 2px 8px rgba(229,9,20,0.5);
    }

    /* Subtitle - BOLD */
    .subtitle {
        font-size: 14px;
        color: #808080;
        text-align: center;
        margin-bottom: 15px;
        font-weight: 700 !important;
        letter-spacing: 1px;
        font-family: 'Arial', sans-serif !important;
    }

    /* Select box container - removed background box */
    .select-container {
        margin-bottom: 15px;
    }

    .stSelectbox {
        background: transparent;
    }

    .stSelectbox > div {
        background: #181818;
        border: 2px solid #333;
        border-radius: 8px;
    }

    .stSelectbox label {
        font-size: 14px;
        font-weight: 900 !important;
        color: #fff;
        margin-bottom: 5px;
        font-family: 'Arial', sans-serif !important;
    }

    .stSelectbox [data-baseweb="select"] {
        height: 40px;
        font-size: 14px;
        font-family: 'Arial', sans-serif !important;
        font-weight: 700 !important;
    }

    /* Movie card - Netflix style */
    .movie-card {
        background: #181818;
        border-radius: 6px;
        padding: 6px;
        margin-bottom: 0;
        border: 1px solid #2a2a2a;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }

    .movie-card:hover {
        transform: scale(1.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        border-color: #404040;
        z-index: 10;
    }

    .movie-card::after {
        content: "▶";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0);
        font-size: 40px;
        color: white;
        transition: transform 0.3s ease;
        z-index: 5;
        text-shadow: 0 2px 10px rgba(0,0,0,0.8);
        font-family: 'Arial', sans-serif;
    }

    .movie-card:hover::after {
        transform: translate(-50%, -50%) scale(1);
    }

    /* Movie poster */
    .movie-poster {
        width: 100%;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.5);
        transition: opacity 0.3s ease;
    }

    .movie-card:hover .movie-poster {
        opacity: 0.4;
    }

    /* Movie title - BOLD */
    .movie-title {
        color: #ffffff;
        font-weight: 900 !important;
        font-size: 13px;
        text-align: center;
        margin-top: 8px;
        text-decoration: none;
        transition: color 0.3s ease;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        line-height: 1.3;
        font-family: 'Arial', sans-serif !important;
    }

    .movie-title:hover {
        color: #E50914;
    }

    /* Button - Netflix red with BOLD text */
    .stButton button {
        background: #E50914 !important;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 10px 35px;
        font-size: 14px;
        font-weight: 900 !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(229,9,20,0.3);
        font-family: 'Arial', sans-serif !important;
    }

    .stButton button:hover {
        background: #f40612 !important;
        box-shadow: 0 4px 20px rgba(229,9,20,0.5);
        letter-spacing: 1.5px;
    }

    /* Sidebar button */
    .stSidebar button {
        background: #E50914 !important;
        border: 1px solid #E50914;
        border-radius: 4px;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Arial', sans-serif !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Input fields */
    .stInput input {
        background: #181818;
        border: 1px solid #333;
        color: #fff;
        font-size: 14px;
        font-family: 'Arial', sans-serif !important;
    }
    .stInput input:focus {
        border-color: #E50914;
    }

    /* Columns - reduce gap */
    .stColumn {
        padding: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header Section - Compact
st.markdown('<p class="main-title">🎬 MOVIE RECOMMENDER</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">POWERED BY MACHINE LEARNING | MAYUR DALVI</p>', unsafe_allow_html=True)

st.markdown('<div class="select-container">', unsafe_allow_html=True)
selected_movie_name = st.selectbox('Select a movie:', movies['title'].values, label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

if st.button('Recommend'):
    names, posters, movie_ids = recommend(selected_movie_name)

    # Create 5 columns for movie cards
    cols = st.columns(5)

    for i, col in enumerate(cols):
        with col:
            tmdb_url = f"https://www.themoviedb.org/movie/{movie_ids[i]}"
            st.markdown(
                f"""
                <a href="{tmdb_url}" target="_blank" style="text-decoration: none;">
                    <div class="movie-card">
                        <img src="{posters[i]}" class="movie-poster">
                        <p class="movie-title">{names[i]}</p>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False, "username": None}))
