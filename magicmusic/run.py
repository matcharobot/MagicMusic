import asyncio
import subprocess
from part1 import StyleSelector
from part2 import MelodyGenerator
from part3 import LyricsGenerator
from part4 import generate_python_file_from_txt
from part5 import MusicGenerator
import os
import argparse


async def run_command(command):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        executable='/bin/bash'
    )
    stdout, stderr = await process.communicate()
    print(f"[stdout]\n{stdout.decode()}")
    if stderr:
        print(f"[stderr]\n{stderr.decode()}")

async def main(description):
    role1 = StyleSelector()    
    chosen_style, recommended_instruments = await role1.run(description)
    
    role2 = MelodyGenerator()
    main_melody_files = await role2.run(chosen_style)
    
    role3 = LyricsGenerator(audio_file="music/generated.wav", output_file="MetaGPT/magicmusic/sheet.txt")
    lyrics = await role3.run(description=description)
    
    generate_python_file_from_txt('/root/M4Singer/MetaGPT/magicmusic/sheet.txt', '/root/M4Singer/code/inference/m4singer/ds_e2e.py')
    
    # 创建一个临时脚本文件
    script_content = """
    source /root/venv38/bin/activate
    cd /root/M4Singer/code
    export PYTHONPATH=.
    python /root/M4Singer/code/inference/m4singer/ds_e2e.py --config usr/configs/m4singer/diff.yaml --exp_name m4singer_diff_e2e
    deactivate
    cd ~/M4Singer
    """

    script_path = "/tmp/temp_script.sh"
    with open(script_path, "w") as script_file:
        script_file.write(script_content)

    # 运行临时脚本
    await run_command(f"bash {script_path}")

    # 删除临时脚本文件
    os.remove(script_path)

    role4 = MusicGenerator()  
    harmonic_melody_files, merged_files = await role4.run(chosen_style, recommended_instruments, '/root/M4Singer/code/infer_out/humanvoice.wav')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run music generation process.')
    parser.add_argument('--description', type=str, required=True, help='Description for the music generation')
    args = parser.parse_args()

    asyncio.run(main(args.description))