#写入文件，用到参数chosen_style, chord_sequence, key, output_file
def generate_runfile(chosen_style, output_file):

    content = f"""import wave
import contextlib
import IPython
import soundfile as sf
from mustango import Mustango

output_file = '/root/M4Singer/music/generated.wav'

model = Mustango("declare-lab/mustango")
prompt1 = " The song is {chosen_style}. This song has a relatively low pitch. The song is in middle tempo with human voice only. The key of this song is C major."
music1 = model.generate(prompt1)
sf.write(f'/root/M4Singer/music/1.wav', music1, samplerate=16000)
IPython.display.Audio(data=music1, rate=16000)

prompt2 = " The song is {chosen_style}. This song has a relatively low pitch. The song is in fast tempo with human voice only. The key of this song is A major."
music2 = model.generate(prompt2)
sf.write(f'/root/M4Singer/music/2.wav', music2, samplerate=16000)
IPython.display.Audio(data=music2, rate=16000)

def concatenate_wav_files(file1, file2, output_file):
    with wave.open(file1, 'rb') as wav1, wave.open(file2, 'rb') as wav2:
        # Check if parameters of both files match
        if (wav1.getnchannels(), wav1.getsampwidth(), wav1.getframerate()) != (wav2.getnchannels(), wav2.getsampwidth(), wav2.getframerate()):
            raise ValueError("WAV files must have the same number of channels, sample width, and frame rate")
        
        # Read frames from both files
        frames1 = wav1.readframes(wav1.getnframes())
        frames2 = wav2.readframes(wav2.getnframes())
        
        with wave.open(output_file, 'wb') as output_wav:
            # Set parameters for the output file
            output_wav.setnchannels(wav1.getnchannels())
            output_wav.setsampwidth(wav1.getsampwidth())
            output_wav.setframerate(wav1.getframerate())
            # Write frames from both files to the output file
            output_wav.writeframes(frames1)
            output_wav.writeframes(frames2)

concatenate_wav_files(f'/root/M4Singer/music/1.wav', f'/root/M4Singer/music/2.wav', output_file)"""

    # 将内容写入目标Python文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
