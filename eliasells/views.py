import openai
from django.conf import settings
from django.http import JsonResponse

openai.api_key = settings.OPENAI_API_KEY

def get_openai_response(user_message):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the model you prefer
            prompt=user_message,
            max_tokens=150,  # You can tweak this to control response length
            n=1,
            stop=None,
            temperature=0.9,  # Controls creativity: 0.0 is very deterministic, 1.0 is creative
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

