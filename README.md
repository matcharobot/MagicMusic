# MagicMusic

## DESCRIPTION
MagicMusic is a multi-agent platform built with MetaGPT for song generation, with the addition of 4 roles and 6 actions to the original setup. Users can choose the song style and instruments based on descriptions, generate lyrics, and synthesize the final song. Melody generation is achieved using audio, and singing voice synthesis is done using M4Singer.

## MENU
- [Get Started](#get-started)
- [Contribution Guide](#contribution-guide)
- [License](#license)
- [Authors](#authors)
- [Acknowledgments](#acknowledgments)
- [Version History](#version-history)
- [FAQ](#faq)
- [Appendix](#appendix)

## Get Started
### Installation
Using M4Singer as the voice synthesizer

M4Singer requires Python 3.8, torch 2.2.2. Please refer to [M4Singer](https://github.com/M4Singer/M4Singer) to install M4Singer.

Set up the environment to run M4Singer on a 3080 by executing `pip install -v -r requirementsforM4.txt`.

Build the multi-agent platform using MetaGPT. For installation, please refer to [MetaGPT](https://github.com/geekan/MetaGPT).

After completing the installation, keep only the `config` and `metagpt` subfolders, create a `magicmusic` subfolder, and place this code inside it.

Add music to the vocals using audiocraft, which can be installed using the following command line:
```shell
pip install git+https://github.com/facebookresearch/audiocraft.git
apt install ffmpeg
```

### Usage
Run `python MetaGPT/magicmusic/run.py --description "Description of the desired song"` in the terminal.

## Contribution Guide
How to contribute code or report issues.

## License
Type of project license.

## Authors
Main contributors and their contact information.

## Acknowledgments
Thanks to the people or organizations that provided help and support.

## Version History
Changes and updates log of the project versions.

## FAQ
Some frequently asked questions and answers.

## Appendix
Main paths after configuration
```shell
> code
    > infer_out
        > hunmanvoice.wav
    > inference
        > m4singer
            > base_svs_infer.py #Two modifications
> MetaGPT
    > config
    > logs
    > magicmusic
        > part1.py
        > part2.py
        > part3.py
        > part4.py
        > part5.py
        > run.py
        > sheet.txt
    > metagpt
    > workspace
> music
    > generated.wav
    > harmonic.wav
    > merged.wav
```
