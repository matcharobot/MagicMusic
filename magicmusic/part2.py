import asyncio
from metagpt.actions import Action
from metagpt.actions.action_node import ActionNode
from metagpt.roles import Role
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import random

class GenerateMainMelody(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "GenerateMainMelody"
        self.desc = "Generate a main melody for a specific music style using the MusicGen model."

    async def run(self, chosen_style: str, *args, **kwargs):
        # 初始化 MusicGen 模型
        model = MusicGen.get_pretrained("facebook/musicgen-medium")

        # 构造描述，专注于钢琴且指定风格
        description = f"Single-voice {chosen_style} style piano melody"

        # 随机选择持续时间在 25 到 30 秒之间
        duration = random.randint(25, 30)  

        # 设置生成旋律的参数
        model.set_generation_params(duration)

        # 生成旋律
        wav = model.generate([description])  # 假设模型接受描述列表

        # 保存生成的音频文件
        audio_files = []
        for idx, one_wav in enumerate(wav):
            file_name = f"music/generated"
            audio_write(file_name, one_wav.cpu(), model.sample_rate, strategy="loudness")
            audio_files.append(f"{file_name}.wav")

        # 返回生成的音频文件名列表
        return audio_files

class MelodyGenerator(Role):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Liz"
        self.profile = "Generates melodies based on style."
        self.goal = "Generate a single piano melody matching the selected style."
        self.constraints = "The melody should be in piano and match the chosen style."

        # 初始化时添加动作
        self.set_actions([GenerateMainMelody()])

    async def run(self, chosen_style: str, *args, **kwargs):
        # 生成主旋律
        main_melody_action = self.actions[0]
        main_melody_files = await main_melody_action.run(chosen_style)

        return main_melody_files

async def test_melody_generation():
    melody_generator = MelodyGenerator()
    chosen_style = "Electronic" 
    main_melody_files = await melody_generator.run(chosen_style)

    print("Generated Melody Files:", main_melody_files)

if __name__ == "__main__":
    asyncio.run(test_melody_generation())