import asyncio
from pydub import AudioSegment  
import torchaudio  
from metagpt.actions import Action
from metagpt.roles import Role
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

class GenerateHarmonicMelody(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "GenerateHarmonicMelody"

    async def run(self, singingvoice: str, descriptions: list[str], *args, **kwargs):
        model = MusicGen.get_pretrained('facebook/musicgen-melody')
        melody, sr = torchaudio.load(singingvoice)
        model.set_generation_params(duration=melody.shape[1] / float(sr))
        
        # 使用整合后的描述字符串进行条件生成
        wav = model.generate_with_chroma(descriptions, melody[None].expand(len(descriptions), -1, -1), sr)
        
        harmonic_files = []
        for idx, one_wav in enumerate(wav):
            file_name = f"music/harmonic"
            audio_write(file_name, one_wav.cpu(), model.sample_rate, strategy="loudness")
            harmonic_files.append(f"{file_name}.wav")
        
        return harmonic_files

class MusicGenerator(Role):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Karina"
        self.set_actions([GenerateHarmonicMelody()])

    async def merge_melodies(self, singing_voice_files, harmonic_melody_files):
        merged_files = []
        for singing_voice_file, harmonic_melody_file in zip(singing_voice_files, harmonic_melody_files):
            singing_voice = AudioSegment.from_file(singing_voice_file)
            harmonic_melody = AudioSegment.from_file(harmonic_melody_file)
            harmonic_melody = harmonic_melody - 12  # 降低音量
            merged_melody = singing_voice.overlay(harmonic_melody)
            merged_file_name = f"music/merged.wav"
            merged_melody.export(merged_file_name, format="wav")
            merged_files.append(merged_file_name)
        return merged_files

    async def run(self, style: str, recommended_instruments: list[str], singing_voice_file: str, *args, **kwargs):
        harmonic_melody_action = self.actions[0]
        singing_voice_files = [singing_voice_file]
        descriptions = [f'please use the{recommended_instruments[0]}to generate a {style} style harmonic melody']
        harmonic_melody_files = await harmonic_melody_action.run(singing_voice_file, descriptions)
        merged_files = await self.merge_melodies(singing_voice_files, harmonic_melody_files)
        return harmonic_melody_files, merged_files

async def test_melody_generation(singing_voice_path):
    melody_generator = MusicGenerator()
    style = "Pop"
    recommended_instruments = ["Guitar", "Drums", "Keybosrds"]   
    harmonic_melody_files, merged_files = await melody_generator.run(style, recommended_instruments, singing_voice_path)
    print("Harmonic Melody Files:", harmonic_melody_files)
    print("Merged Melody Files:", merged_files)

if __name__ == "__main__":
    # 这里请替换成您的人声文件路径
    singing_voice_path = "/root/M4Singer/code/infer_out/humanvoice.wav"
    asyncio.run(test_melody_generation(singing_voice_path))
