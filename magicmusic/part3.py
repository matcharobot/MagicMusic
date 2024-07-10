import asyncio
from metagpt.actions import Action
from metagpt.roles import Role
import librosa

class AnalyzeMelody(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "AnalyzeMelody"
        self.desc = "Analyze melody from an audio file and output each note's pitch and duration."

    @staticmethod
    def convert_note_to_pitch_class(note):
        """Convert note to pitch class number."""
        pitch_classes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
        pitch_class, octave = note[:-1], int(note[-1])
        return pitch_classes.get(pitch_class, 0) + (octave * 12)

    async def run(self, audio_file: str, output_file: str) -> list:
        sr = 2000  # Sample rate
        hop_length = 1  # Hop length

        y, _ = librosa.load(audio_file, sr=sr)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr, n_fft=4096, hop_length=hop_length, fmin=50.0, fmax=2000.0, threshold=0.1)

        prev_note = None
        total_duration = 0.0
        results = []

        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                note = librosa.hz_to_note(pitch)
                note = note.replace('♯', '#')
                if note == prev_note:
                    total_duration += hop_length / sr
                else:
                    if prev_note is not None:
                        results.append([prev_note, total_duration])
                    prev_note = note
                    total_duration = hop_length / sr
        if prev_note is not None:
            results.append([prev_note, total_duration])

        # 对前三个和后三个音高进行合并
        if len(results) >= 6:
            first_group = [" ".join([note for note, _ in results[:3]]), sum([duration for _, duration in results[:3]])]
            last_group = [" ".join([note for note, _ in results[-3:]]), sum([duration for _, duration in results[-3:]])]
            middle_results = results[3:-3]
            results = [first_group] + middle_results + [last_group]

        # 处理剩余音高的合并
        merged_results = []
        for note, duration in results:
            if merged_results and self.convert_note_to_pitch_class(note.split()[0]) - self.convert_note_to_pitch_class(merged_results[-1][0].split()[-1]) in range(-4, 5):
                merged_results[-1][0] += f" {note}"
                merged_results[-1][1] = f"{merged_results[-1][1]} {duration:.3f}"
            else:
                merged_results.append([note, f"{duration:.3f}"])

        # 将合并后的结果写入文件
        with open(output_file, 'w') as f:
            for note, duration in merged_results:
                f.write(f"{note},{duration}\n")
        return results  # results 是一个包含[音高, 持续时间]的列表

class GenerateLyrics(Action):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "GenerateLyrics"
        self.desc = "Generate lyrics based on the given description and melody analysis."

    async def run(self, description: str, num_lines: int) -> list:
        prompt = f"根据用户输入：{description}生成歌词。歌词需要包含标点符号，汉字与符号均算做长度中，歌词与符号的总长度为 {num_lines} ，请在一行内完成输出。"
        lyrics = '。'
        lyric = str(await self._aask(prompt))
        lyrics += lyric
        
        # 将生成的歌词拆分为单个字符，并返回列表
        return [char for char in lyrics]

class LyricsGenerator(Role):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "LyricsGenerator"
        self.profile = "Lyrics Generator"
        self.goal = "To generate lyrics based on an audio file and a description."
        self.audio_file = kwargs.get('audio_file', '')
        self.output_file = kwargs.get('output_file', '')

    async def run(self, description: str) -> None:
        analyze_melody_action = AnalyzeMelody()
        melody_results = await analyze_melody_action.run(audio_file=self.audio_file, output_file=self.output_file)

        generate_lyrics_action = GenerateLyrics()
        lyrics = await generate_lyrics_action.run(description=description, num_lines=len(melody_results))

        # 将歌词和音高分析的结果合并，并写入输出文件
        with open(self.output_file, 'w') as f:
            for (char, (pitch, duration)) in zip(lyrics, melody_results):
                f.write(f"{char},{pitch},{duration:.3f}\n")

# 测试代码
async def main():
    audio_file = "music/generated.wav"  # 替换为音频文件的路径
    description = "请写一首在体育比赛前的热场音乐"  # 替换为你的描述

    lyrics_generator = LyricsGenerator(audio_file=audio_file, output_file="MetaGPT/magicmusic/sheet.txt")
    lyrics = await lyrics_generator.run(description=description)
    

if __name__ == '__main__':
    asyncio.run(main())