def generate_python_file_from_txt(input_txt_file, output_py_file):
    text = ""
    notes = ""
    notes_duration = ""

    with open(input_txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')  # 假设每行的元素用逗号分隔
            if len(parts) == 3:  # 确保行格式正确
                char, note, duration = parts
                if char == "。" or char == "，" or char == "！" or char == "？":  # 判断字符是否为指定的标点符号
                    text += "AP"
                    note = "rest"
                else:
                    text += char  # 直接添加字符
                
                if notes:
                    notes += f' | {note}'
                    notes_duration += f' | {duration}'
                else: 
                    notes += f'{note}'
                    notes_duration += f'{duration}'

    # 准备要写入Python文件的内容
    content = f"""import torch
from base_svs_infer import BaseSVSInfer
from utils import load_ckpt
from utils.hparams import hparams
from usr.diff.shallow_diffusion_tts import GaussianDiffusion
from usr.diffsinger_task import DIFF_DECODERS
from modules.fastspeech.pe import PitchExtractor
import utils


class DiffSingerE2EInfer(BaseSVSInfer):
    def build_model(self):
        model = GaussianDiffusion(
            phone_encoder=self.ph_encoder,
            out_dims=hparams['audio_num_mel_bins'], denoise_fn=DIFF_DECODERS[hparams['diff_decoder_type']](hparams),
            timesteps=hparams['timesteps'],
            K_step=hparams['K_step'],
            loss_type=hparams['diff_loss_type'],
            spec_min=hparams['spec_min'], spec_max=hparams['spec_max'],
        )
        model.eval()
        load_ckpt(model, hparams['work_dir'], 'model')

        if hparams.get('pe_enable') is not None and hparams['pe_enable']:
            self.pe = PitchExtractor().to(self.device)
            utils.load_ckpt(self.pe, hparams['pe_ckpt'], 'model', strict=True)
            self.pe.eval()
        return model

    def forward_model(self, inp):
        sample = self.input_to_batch(inp)
        txt_tokens = sample['txt_tokens']  # [B, T_t]
        spk_id = sample.get('spk_ids')
        with torch.no_grad():
            output = self.model(txt_tokens, spk_embed=spk_id, ref_mels=None, infer=True,
                                pitch_midi=sample['pitch_midi'], midi_dur=sample['midi_dur'],
                                is_slur=sample['is_slur'])
            mel_out = output['mel_out']  # [B, T,80]
            if hparams.get('pe_enable') is not None and hparams['pe_enable']:
                f0_pred = self.pe(mel_out)['f0_denorm_pred']  # pe predict from Pred mel
            else:
                f0_pred = output['f0_denorm']
            wav_out = self.run_vocoder(mel_out, f0=f0_pred)
        wav_out = wav_out.cpu().numpy()
        return wav_out[0]

if __name__ == '__main__':
    inp = {{
        'spk_name': 'Alto-1',
        'text': '{text}',
        'notes': '{notes}',
        'notes_duration': '{notes_duration}',
        'input_type': 'word',
    }}
    
    DiffSingerE2EInfer.example_run(inp)"""

    # 将内容写入目标Python文件
    with open(output_py_file, 'w', encoding='utf-8') as f:
        f.write(content)
