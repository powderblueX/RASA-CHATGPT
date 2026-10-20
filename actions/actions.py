"""Custom Rasa action backed by the OpenAI Responses API."""

import logging
import os
from typing import Any, Dict, List, Text

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

load_dotenv()
logger = logging.getLogger(__name__)


class GPTAction(Action):
    def name(self) -> Text:
        return "action_generate"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        prompt = (tracker.latest_message.get("text") or "").strip()
        api_key = os.getenv("OPENAI_API_KEY")
        model = os.getenv("OPENAI_MODEL")

        if not prompt:
            dispatcher.utter_message(text="Please enter a message first.")
            return []
        if not api_key or not model:
            dispatcher.utter_message(
                text="The OpenAI API is not configured. Check OPENAI_API_KEY "
                "and OPENAI_MODEL in your environment."
            )
            return []

        try:
            client = OpenAI(api_key=api_key)
            response = client.responses.create(model=model, input=prompt)
            dispatcher.utter_message(text=response.output_text)
        except OpenAIError:
            logger.exception("OpenAI request failed")
            dispatcher.utter_message(
                text="I could not generate a response. Please try again later."
            )

        return []

