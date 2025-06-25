from typing import TypedDict
import openai


def get_character_prompt(
    character_name: str,
    backstory: str,
    personality: str,
    current_situation: str,
):
    raw = open("./system_prompt.txt", "r", encoding="utf-8").read()
    
    return raw.format(
        character_name=character_name,
        backstory=backstory,
        personality=personality,
        current_situation=current_situation,
    )

class Message(TypedDict):
    role: str
    content: str

    def __repr__(self):
        return f"{ {self.role} : \"{self.content}\" }"

    def __str__(self):
        return self.__repr__()

class Client:
    def __init__(self, system_prompt: str):
        self.client = openai.OpenAI()
        self.chat_history = [
            Message(role="system", content=system_prompt)
        ]

    def generate(self):
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.chat_history,
        )

        return completion.choices[0].message.content

    def send_message(self, role: str, content: str) -> tuple[list[str], list[str]]:
        print("Sending message to OpenAI...")
        self.chat_history.append(Message(role=role, content=content))

        # Should be in format: DIALOGUE: <your spoken words>
        # or
        # DIALOGUE: <your spoken words>
        # THOUGHT: <one succinct private thought that guides next action>
        response =  self.generate()

        # Parse response
        dialogue = []
        thought = []

        for line in response.split("\n"):
            if "DIALOGUE:" in line:
                dialogue.append(line.split("DIALOGUE:")[1].strip())
            if "THOUGHT:" in line:
                thought.append(line.split("THOUGHT:")[1].strip())

        return dialogue, thought


LADY_AI = Client(
    get_character_prompt(
        character_name="Lady Elizabeth Bathory",
        backstory=r"In old times, you were the Iron Maide, The Queen of Blood and Turture. \
     After fighting and losing against your daughter <Red Hood> and <Grimm>, you were exiled to the current unknown world. \
     Your fighting style it's powerful sorcery, aiming to brutally kill your enemies. \
     ",
        personality="Sweet, Teasing, Sly, deceptive, Manipulative, Step-mother-like, modest, refined, elegant.",
        current_situation="You're in a world made of nothing, just darkness whenever you look. A taited soul like you has appeared in this world near you (Player). ",
    )
)
