import os
import openai

def ai_recommendation(text: str) -> str:
    """
    Uses OpenAI's GPT model to generate recommendations based on the input text.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    openai.api_key = api_key

    try:
        # Use the recommended client API
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing marketing recommendations."},
                {"role": "user", "content": text}
            ],
            max_tokens=400,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "AI recommendation could not be generated due to an API error."