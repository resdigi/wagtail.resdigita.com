import logging
import openai
from openai import OpenAI, OpenAIError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

# Configure a specific logger for OpenAI API calls
openai_logger = logging.getLogger("openai_logger")

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Log only OpenAI request
            openai_logger.info(f"Sending request to OpenAI: {user_message}")

            openai.api_key = settings.OPENAI_API_KEY

            # response = openai.chat.Completion.create(
            #     model="gpt-4",  # or any other model like "gpt-3.5-turbo"
            #     messages=[
            #         {"role": "system", "content": "You are a helpful assistant."},
            #         {"role": "user", "content": user_message},  # user input
            #     ],
            #     max_tokens=150,
            #     temperature=0.7,
            # )

            # chat_response = response['choices'][0]['message']['content'].strip() 

            client = OpenAI()

            response = client.responses.create(
                model="gpt-4o",
                input="Write a one-sentence bedtime story about a unicorn."
            )

            chat_response = response.output_text

            # Log only OpenAI response
            openai_logger.info(f"Received response from OpenAI: {chat_response}")

            return JsonResponse({"response": chat_response})

        # In the exception handling part
        except OpenAIError as e:
            openai_logger.error(f"OpenAI API error: {e}")
            return JsonResponse({"error": "OpenAI API issue"}, status=500)

        except Exception as e:
            openai_logger.exception(f"Unexpected error: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
