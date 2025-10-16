import os
import openai

def ai_recommendation(text: str) -> str:
    """
    Uses OpenAI's GPT model to generate recommendations based on the input text.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # Provide a clear error message in the UI instead of raising an exception
        return "错误：OPENAI_API_KEY 未在 .env 文件中配置。"
    
    openai.api_key = api_key

    try:
        # It's better to create a client instance
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一位提供市场营销建议的得力助手。"},
                {"role": "user", "content": text}
            ],
            max_tokens=400,
        )
        return response.choices[0].message.content
    except Exception as e:
        # Return a user-friendly error message
        return f"调用 OpenAI API 时出错: {e}"
