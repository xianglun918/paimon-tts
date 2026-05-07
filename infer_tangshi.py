import os
import sys
import soundfile as sf

# 自动将子模块加入 Python 路径
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_PROJECT_ROOT, "GPT_SoVITS"))

from GPT_SoVITS.inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav
from tools.i18n.i18n import I18nAuto

i18n = I18nAuto()

# S1 官方预训练（通用）
GPT_MODEL = "GPT_SoVITS/GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt"

# S2 微调模型：Model A (PM)
SOVITS_MODEL = "pm-v2-epoch40.pth"
REF_AUDIO = "ref_pm.wav"
REF_TEXT = "聊到炼金和研究的话题,砂糖就完全不怯场了,这就是研究者的气质吗?"

# 唐诗：静夜思
TARGET_TEXT = "床前明月光，疑是地上霜。举头望明月，低头思故乡。"

print("[*] Loading S1 pretrained model...")
change_gpt_weights(gpt_path=GPT_MODEL)

print(f"[*] Loading S2 model: {SOVITS_MODEL}...")
list(change_sovits_weights(sovits_path=SOVITS_MODEL))

print("[*] Generating...")
synthesis_result = get_tts_wav(
    ref_wav_path=REF_AUDIO,
    prompt_text=REF_TEXT,
    prompt_language=i18n("中文"),
    text=TARGET_TEXT,
    text_language=i18n("中文"),
    how_to_cut="凑四句一切",
    top_k=20,
    top_p=0.85,
    temperature=0.75,
)

result_list = list(synthesis_result)
if result_list:
    sr, audio = result_list[-1]
    out_path = "output_tangshi.wav"
    sf.write(out_path, audio, sr)
    print(f"[✓] Saved: {out_path} ({len(audio)/sr:.2f}s)")
else:
    print("✗ Generation failed!")
