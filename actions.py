# -------------------------------------------------------------
# MindSense – FINAL ACTIONS FILE (Clean, Stable, Error-Free)
# -------------------------------------------------------------

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType
import joblib

# -------------------------------------------------------------
# 1. REMINDER ACTION
# -------------------------------------------------------------

class AddEventSimple(Action):
    def name(self) -> Text:
        return "action_add_event"

    def run(self, dispatcher, tracker, domain) -> List[EventType]:
        event_name = tracker.get_slot("event")
        time_value = tracker.get_slot("time")

        if not event_name or not time_value:
            dispatcher.utter_message(text="Sorry, I couldn't understand the event details.")
            return []

        dispatcher.utter_message(text=f"Okay! I will remind you about **{event_name}** at **{time_value}**.")

        return [
            SlotSet("event", None),
            SlotSet("time", None),
        ]

# -------------------------------------------------------------
# 2. VIDEO ACTIONS (Breathing / Grounding)
# -------------------------------------------------------------

class RedirectBreathing(Action):
    def name(self) -> Text:
        return "action_breathing_video"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print("🔥🔥🔥 Breathing Video Triggered! 🔥🔥🔥")

        # video_link = "https://youtu.be/odADwWzHR24"

        # ⭐ FIX: send only what your frontend expects (clean JSON)
        dispatcher.utter_message(
            text="Starting your breathing video...",
            custom={
                "data": {
                    "video_url": "https://youtu.be/odADwWzHR24"
                }
            }
        )

        return []


class RedirectGrounding(Action):
    def name(self) -> Text:
        return "action_grounding_video"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("🔥🔥🔥 Grounding Video Triggered! 🔥🔥🔥")

        # video_link = "https://youtu.be/30VMIEmA114"

        dispatcher.utter_message(
            text="Opening a grounding technique video for you...",
            custom={
                "data": {
                    "video_url": "https://youtu.be/30VMIEmA114"
                }
            }
        )

        return []


class SpotifyAnxietyPlaylist(Action):
    def name(self) -> Text:
        return "action_play_spotify_anxiety"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print("🔥🔥🔥 Spotify Action Triggered! 🔥🔥🔥")

        # playlist_url = "https://open.spotify.com/embed/playlist/37i9dQZF1DWVlYsZJXqym0"

        dispatcher.utter_message(
            text="Playing calming music...",
            custom={
                "data": {
                    "external_url": "https://open.spotify.com/playlist/3l6b0zuXjgyPxLK6PIAqED?si=db58a30a7f17489c"
                }
            }
        )

        return []

# -------------------------------------------------------------
# 4. PERSONALITY QUESTION ACTIONS
# -------------------------------------------------------------

Talkative_opt = ['Talkative', 'Reserved']
pref_list = ['Yes', 'No']
energ_drain_list = ['Energized', 'Drained']
persuasion_list = [
    'I like persuasion',
    'Am not fond but ok with persuasion',
    'I don’t like persuasion'
]
personal_invo_list = ['Low', 'Medium', 'High']


class AskForTalkativeAction(Action):
    def name(self): return "action_ask_talk_or_resv"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            text="Are you a talkative or reserved person?",
            buttons=[{"title": p, "payload": p} for p in Talkative_opt]
        )
        return []


class AskForPrefListAction(Action):
    def name(self): return "action_ask_list_or_obsv"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            text="Do you prefer listening/observing more than talking?",
            buttons=[{"title": p, "payload": p} for p in pref_list]
        )
        return []


class AskForEnergisedOrDrainedAction(Action):
    def name(self): return "action_ask_energ_or_drain"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            text="Do you feel energized or drained after long conversations?",
            buttons=[{"title": p, "payload": p} for p in energ_drain_list]
        )
        return []


class AskForPersuationAction(Action):
    def name(self): return "action_ask_persuasion"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            text="Do you like being persuaded to do things?",
            buttons=[{"title": p, "payload": p} for p in persuasion_list]
        )
        return []


class AskForPrsnlInvolvAction(Action):
    def name(self): return "action_ask_prsnl_invol"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            text="How much personal involvement do you prefer from friends?",
            buttons=[{"title": p, "payload": p} for p in personal_invo_list]
        )
        return []

# -------------------------------------------------------------
# 5. FORM VALIDATION
# -------------------------------------------------------------

class ValidateUserProfileForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_user_profile_info_form"

    def validate_talk_or_resv(self, slot_value, dispatcher, tracker, domain):
        return {"talk_or_resv": slot_value}

    def validate_list_or_obsv(self, slot_value, dispatcher, tracker, domain):
        return {"list_or_obsv": slot_value}

    def validate_energ_or_drain(self, slot_value, dispatcher, tracker, domain):
        return {"energ_or_drain": slot_value}

    def validate_persuasion(self, slot_value, dispatcher, tracker, domain):
        return {"persuasion": slot_value}

    def validate_prsnl_invol(self, slot_value, dispatcher, tracker, domain):
        return {"prsnl_invol": slot_value}

# -------------------------------------------------------------
# 6. PERSONALITY CLASSIFIER
# -------------------------------------------------------------

class ClassifyUser(Action):
    def name(self) -> Text:
        return "action_classify_user"

    def run(self, dispatcher, tracker, domain):

        # Load model safely
        try:
            clf = joblib.load("PERSONALITY_MODEL.joblib")
        except:
            dispatcher.utter_message(text="Personality model is missing.")
            return []

        talk = tracker.get_slot("talk_or_resv")
        list_obsv = tracker.get_slot("list_or_obsv")
        energy = tracker.get_slot("energ_or_drain")
        persuasion = tracker.get_slot("persuasion")
        involvement = tracker.get_slot("prsnl_invol")

        if not all([talk, list_obsv, energy, persuasion, involvement]):
            dispatcher.utter_message(text="Missing personality form inputs.")
            return []

        talk_map = {'Talkative': 0, 'Reserved': 1}
        list_map = {'Yes': 1, 'No': 0}
        energy_map = {'Drained': 0, 'Energized': 1}
        persuasion_map = {
            "I don’t like persuasion": 0,
            "Am not fond but ok with persuasion": 1,
            "I like persuasion": 2
        }
        involvement_map = {'Low': 0, 'Medium': 1, 'High': 2}

        features = [[
            talk_map[talk],
            list_map[list_obsv],
            energy_map[energy],
            persuasion_map[persuasion],
            involvement_map[involvement]
        ]]

        prediction = clf.predict(features)[0]
        label_map = {0: "Formal", 1: "Personal", 2: "Moderate"}

        personality = label_map[prediction]

        dispatcher.utter_message(text=f"Your personality type: **{personality}**.")

        return [
            SlotSet("personality", personality),
            SlotSet("talk_or_resv", None),
            SlotSet("list_or_obsv", None),
            SlotSet("energ_or_drain", None),
            SlotSet("persuasion", None),
            SlotSet("prsnl_invol", None)
        ]
