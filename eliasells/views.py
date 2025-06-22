import logging
import openai
import uuid
from openai import OpenAI, OpenAIError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from django.utils import translation

from .graph import chatbotapp
from langchain_core.messages import HumanMessage

import calendar

from django.shortcuts import render
from django.utils import timezone


def index(request):
    current_year = timezone.now().year
    calendar_html = calendar.HTMLCalendar().formatyear(current_year)

    return render(request, 'eliasells/index.html', {
        'current_year': current_year,
        'calendar_html': calendar_html,
    })

# Configure a specific logger for OpenAI API calls
openai_logger = logging.getLogger("openai_logger")


@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Managing chat thread id through session
            if "thread_id" not in request.session:
                request.session["thread_id"] = str(uuid.uuid4())

            thread_id = request.session["thread_id"]

            # Log only OpenAI request
            openai_logger.info(f"Sending request to OpenAI: {user_message}, thread_id={thread_id}")

            input_messages = [HumanMessage(content=user_message)]
            config = {"configurable": {"thread_id": thread_id}}

            language = translation.get_language()

            output = chatbotapp.invoke({"messages": input_messages}, config)
            reply = output["messages"][-1].content

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
