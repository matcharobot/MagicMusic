# MagicMusic

## DESCRIPTION
借助metagpt搭建多智能体平台进行歌曲生成，在原有基础上添加了4个role及6个action。
通过用户描述选择歌曲风格及乐器、生成歌词并合成最终歌曲
借助audio实现旋律生成，借助M4singer进行singing voice synises

## MENU
- [Get Started](#get-started)
- [贡献指南](#贡献指南)
- [许可](#许可)
- [作者](#作者)
- [致谢](#致谢)
- [版本历史](#版本历史)
- [FAQ](#faq)
- [附录](#附录)

## Get Started
### Installation
使用M4Singer作为人声合成器

M4Singer requires Python 3.8, torch 2.2.2. Please refer to [M4Singer](https://github.com/M4Singer/M4Singer) to install the M4Singer.

在3080上配置运行M4Singer的环境，执行`pip install -v -r requirementsforM4.txt`

借助MetaGPT进行多智能体的搭建，安装请参考[MetaGPT](https://github.com/geekan/MetaGPT)

完成安装后只需要保留`config,metagpt`两个子文件夹，并创建`magicmusic`子文件夹，将本代码放入其中

通过audiocraft为人声添加音乐，安装可以使用如下命令行
```shell
pip install git+https://github.com/facebookresearch/audiocraft.git
apt install ffmpeg
```

### Usage
在终端运行`python MetaGPT/magicmusic/run.py --description "对所需歌曲的描述"`

## 贡献指南
如何贡献代码或报告问题。

## 许可
项目的许可类型。

## 作者
主要贡献者及其联系方式。

## 致谢
感谢提供帮助和支持的人或组织。

## 版本历史
项目的版本变化和更新日志。

## FAQ
一些常见问题和解答。

## 附录
配置完成后部分主要路径
```shell
> code
    > infer_out
        > hunmanvoice.wav
    > inference
        > m4singer
            > base_svs_infer.py #有两处修改
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
