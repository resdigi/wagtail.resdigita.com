import logging
import openai
import uuid
from openai import OpenAI, OpenAIError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.utils import translation

from .graph import app
from langchain_core.messages import HumanMessage


# Configure a specific logger for OpenAI API calls
openai_logger = logging.getLogger("openai_logger")



@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Langchain implementation of chatbot

            # model = ChatOpenAI(model="gpt-4o-mini")
            # trimmer = trim_messages(
            #     max_tokens=65,
            #     strategy="last",
            #     token_counter=model,
            #     include_system=True,
            #     allow_partial=False,
            #     start_on="human",
            # )

            # openai.api_key = settings.OPENAI_API_KEY

            # prompt = str(_("localized_gpt_prompt"))

            # openai_logger.info(f"Sending prompt to OpenAI: {prompt}")

            # client = OpenAI()

            # response = client.responses.create(
            #     model="gpt-4o",
            #     instructions=prompt,
            #     input=user_message
            # )

            # Managing chat thread id through session
            if "thread_id" not in request.session:
                request.session["thread_id"] = str(uuid.uuid4())

            thread_id = request.session["thread_id"]

            # Log only OpenAI request
            openai_logger.info(f"Sending request to OpenAI: {user_message}, thread_id={thread_id}")

            input_messages = [HumanMessage(content=user_message)]
            config = {"configurable": {"thread_id": thread_id}}

            language = translation.get_language()

            output = app.invoke({"messages": input_messages}, config)
            reply = output["messages"][-1].content

            # chat_response = response.output_text

            # Log only OpenAI response
            openai_logger.info(f"Received response from OpenAI: {reply}")

            return JsonResponse({"response": reply})

        # In the exception handling part
        except OpenAIError as e:
            openai_logger.error(f"OpenAI API error: {e}")
            return JsonResponse({"error": "OpenAI API issue"}, status=500)

        except Exception as e:
            openai_logger.exception(f"Unexpected error: {e}")
            return JsonResponse({"error": "Internal server error"}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
