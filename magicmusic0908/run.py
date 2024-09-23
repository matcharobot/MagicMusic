import asyncio
import subprocess
from part1 import StyleSelector
from part2 import generate_runfile
from part3 import LyricsGenerator
from part4 import generate_python_file_from_txt
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
    chosen_style = await role1.run(description)
    
    generate_runfile(chosen_style, output_file = f'/root/M4Singer/mustango/run.py')
    script_content1 = """
    source /root/mus/bin/activate 
    cd /root/M4Singer/mustango
    python run.py
    deactivate
    cd /root/M4Singer
    """
    script_path1 = "/tmp/temp_script1.sh"
    with open(script_path1, "w") as script_file:
        script_file.write(script_content1)
    await run_command(f"bash {script_path1}")
    os.remove(script_path1)
   
    role3 = LyricsGenerator(audio_file="/root/M4Singer/music/generated.wav", output_file="/root/M4Singer/music/sheet.txt")
    lyrics = await role3.run(description=description)
    
    generate_python_file_from_txt('/root/M4Singer/music/sheet.txt', '/root/M4Singer/code/inference/m4singer/ds_e2e.py')
    
    script_content2 = """
    source /root/venv38/bin/activate
    cd /root/M4Singer/code
    export PYTHONPATH=.
    python /root/M4Singer/code/inference/m4singer/ds_e2e.py --config usr/configs/m4singer/diff.yaml --exp_name m4singer_diff_e2e
    deactivate
    cd /root/M4Singer
    """
    script_path2 = "/tmp/temp_script2.sh"
    with open(script_path2, "w") as script_file:
        script_file.write(script_content2)
    await run_command(f"bash {script_path2}")
    os.remove(script_path2)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run music generation process.')
    parser.add_argument('--description', type=str, required=True, help='Description for the music generation')
    args = parser.parse_args()

    asyncio.run(main(args.description))