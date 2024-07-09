#第一部分
'''
处理中文用户输入
保留英文传递消息的方式
输出为风格及乐器选择两个参数
'''
import asyncio
from metagpt.actions import Action
from metagpt.actions.action_node import ActionNode
from metagpt.roles import Role

class ChooseMusicStyle(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "ChooseMusicStyle"
        self.desc = "Choose the most suitable music style based on the description."

        self.node = ActionNode(
            key=self.name,
            expected_type=str,
            instruction="Based on the given description, choose the most suitable music style from the list: Pop, Rock, Jazz, Classical, Hip Hop, Electronic. Description: '{}'",
            example="Description: '充满活力，适合锻炼时听' -> Electronic",
            schema="raw"
        )

    async def run(self, msg: str, *args, **kwargs):
        prompt = self.node.instruction.format(msg)
        chosen_style = await self._aask(prompt)
        return chosen_style

class RecommendInstruments(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "RecommendInstruments"
        self.desc = "Recommend instruments for the chosen music style."

        self.node = ActionNode(
            key=self.name,
            expected_type=str,
            instruction="Given the chosen music style '{}', recommend typical instruments used in this style.",
            example="Music Style: 'Jazz' -> Recommended instruments: saxophone, piano, double bass, drums",
            schema="raw"
        )

    async def run(self, music_style: str, *args, **kwargs):
        prompt = self.node.instruction.format(music_style)
        recommended_instruments = await self._aask(prompt)
        return recommended_instruments

class StyleSelector(Role):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Valenti"
        self.profile = "Style Selector"
        self.goal = "To select the most suitable music style and recommend appropriate instruments based on the chosen style."
        self.desc = "A role dedicated to selecting music styles and recommending instruments."

        self.set_actions([ChooseMusicStyle, RecommendInstruments])

    async def run(self, description: str):
        chosen_style = await ChooseMusicStyle().run(description)
        print(f"Chosen music style: {chosen_style}")

        recommended_instruments = await RecommendInstruments().run(chosen_style)
        print(f"Recommended instruments for {chosen_style}: {recommended_instruments}")

        return chosen_style, recommended_instruments

async def main():
    role = StyleSelector()
    description = "请写一首在体育比赛前的热场音乐"
    chosen_style, recommended_instruments = await role.run(description)
    print("Test Result:")
    print(f"Chosen Music Style: {chosen_style}")
    print(f"Recommended Instruments: {recommended_instruments}")

asyncio.run(main())
