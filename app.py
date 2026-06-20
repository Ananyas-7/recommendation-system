import os
import requests
import streamlit as st

from dotenv import load_dotenv

from svd_recommender import recommend_for_user
from llm_explainer import explain_recommendation

# --------------------------
# CONFIG
# --------------------------

st.set_page_config(
    page_title="AI Movie Recommender",
    layout="wide"
)

st.title("🎬 Personalized Movie Recommender")

# --------------------------
# LOAD ENV
# --------------------------

load_dotenv()

TMDB_API_KEY = os.getenv(
    "TMDB_API_KEY"
)

# --------------------------
# SIDEBAR
# --------------------------

st.sidebar.header(
    "User Settings"
)

user_id = st.sidebar.number_input(
    "Enter User ID",
    min_value=1,
    max_value=671,
    value=1,
    step=1
)

# --------------------------
# FETCH POSTER
# --------------------------

@st.cache_data
def fetch_poster(movie_name):

    try:

        url = (
            "https://api.themoviedb.org/3/search/movie"
            f"?api_key={TMDB_API_KEY}"
            f"&query={movie_name}"
        )

        response = requests.get(url)

        data = response.json()

        results = data.get(
            "results",
            []
        )

        for movie in results:

            poster_path = movie.get(
                "poster_path"
            )

            if poster_path:

                return (
                    f"https://image.tmdb.org/t/p/w500{poster_path}"
                )

    except Exception as e:

        print("Poster Error:", e)

    return None

# --------------------------
# RECOMMEND BUTTON
# --------------------------

if st.sidebar.button(
    "Get Recommendations"
):

    with st.spinner(
        "Generating recommendations..."
    ):

        recommendations = recommend_for_user(
            user_id=user_id,
            top_n=10
        )

    st.subheader(
        f"🎯 Recommendations for User {user_id}"
    )

    for movie in recommendations:

        poster = fetch_poster(
            movie["title"]
        )

        col1, col2 = st.columns(
            [1, 3]
        )

        # --------------------------
        # POSTER
        # --------------------------

        with col1:

            if poster:

                st.image(
                    poster,
                    width=180
                )

            else:

                st.write(
                    "🎬 No Poster Available"
                )

        # --------------------------
        # MOVIE DETAILS
        # --------------------------

        with col2:

            st.markdown(
                f"### {movie['title']}"
            )

            st.write(
                f"⭐ Predicted Rating: {movie['predicted_rating']}/5"
            )

            st.write(
                f"🎯 Match Percentage: {movie['match_percent']}%"
            )

            st.progress(
                movie["match_percent"] / 100
            )

            if movie["overview"]:

                st.write(
                    movie["overview"]
                )

            # --------------------------
            # AI EXPLANATION
            # --------------------------

            with st.expander(
                "🤖 Why was this recommended?"
            ):

                try:

                    explanation = explain_recommendation(
                        user_id=user_id,
                        movie_title=movie["title"],
                        overview=movie["overview"]
                    )

                    st.write(
                        explanation
                    )

                except Exception as e:

                    st.error(
                        f"LLM Error: {e}"
                    )

        st.divider()