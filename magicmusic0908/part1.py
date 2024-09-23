import asyncio
from metagpt.actions import Action
from metagpt.actions.action_node import ActionNode

class ChooseMusicStyle(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "ChooseMusicStyle"
        self.desc = "Choose the most suitable music style based on the description."

        self.node = ActionNode(
            key=self.name,
            expected_type=str,
            instruction="Based on the given description, choose the most suitable music style. Description: '{}'. Please return only one word in English.",
            example="Description: '充满活力，适合锻炼时听' -> Electronic",
            schema="raw"
        )

    async def run(self, msg: str, *args, **kwargs):
        prompt = self.node.instruction.format(msg)
        chosen_style = await self._aask(prompt)
        return chosen_style

class StyleSelector:
    def __init__(self, **kwargs):
        self.name = "Valenti"
        self.profile = "Style Selector"
        self.goal = "To select the most suitable music style based on the given description."
        self.desc = "A role dedicated to selecting music styles."

    async def run(self, description: str):
        chosen_style = await ChooseMusicStyle().run(description)
        print(f"Chosen music style: {chosen_style}")
        return chosen_style