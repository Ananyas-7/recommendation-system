import ollama

def explain_recommendation(
    user_id,
    movie_title,
    overview
):

    prompt = f"""
    User ID: {user_id}

    Recommended Movie:
    {movie_title}

    Overview:
    {overview}

    Explain in 3-4 sentences
    why this movie may be a good recommendation.
    """

    response = ollama.chat(
        model="llama3.1",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]