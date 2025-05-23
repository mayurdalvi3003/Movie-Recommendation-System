import streamlit as st
import pandas as pd
import pickle 
import requests 


# this code is for the upload the background image in streamlit
#import base64
#def add_bg_from_local(image_file):
 #   with open(image_file, "rb") as image_file:
  #      encoded_string = base64.b64encode(image_file.read())
   # st.markdown(
    #f"""
    #<style>
    #.stApp {{
     #   background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
      #  background-size: cover
    #}}
    #</style>
    #""",
    #unsafe_allow_html=True
    #)
#add_bg_from_local('pic.png')   # path of my backgrouun image  





def fetch_poster(movie_id):
     response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=dfc88b60ef67ac3eadefe5547667ee5e&language=en-US".format(movie_id))
     data = response.json()

     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title']== movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)) , reverse =True , key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
            #here i will fetch the movie poster by using the movie id 
            movie_id = movies.iloc[i[0]].movie_id
            
            recommended_movies.append(movies.iloc[i[0]].title)

            #fetch poster from the API
            recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_posters


    
movies_dict =pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


#st.write("Movie Recommender System")
st.write('<p style="font-size:30px; color:pink;">Movie Recommender System </p>',
unsafe_allow_html=True) # for change the font size and colour of the text 

selected_movie_name = st.selectbox(
'How would you like to be contacted?',
movies['title'].values)

# make one button for the recommend 
if st.button('Recommend'):
    names , posters= recommend(selected_movie_name)
    
    col1 ,col2 , col3 ,col4 ,col5  =st.columns(5)
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
         
    

