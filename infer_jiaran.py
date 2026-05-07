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

# S2 微调模型：Model B (TN)
SOVITS_MODEL = "tn-v2-epoch40.pth"
REF_AUDIO = "ref_tn.wav"
REF_TEXT = "元気、元気の元気まるー"

# 示例文本
TARGET_TEXT = """我好想做嘉然小姐的狗啊。可是嘉然小姐说她喜欢的是猫，我哭了。我知道既不是狗也不是猫的我为什么要哭的。因为我其实是一只老鼠。我从没奢望嘉然小姐能喜欢自己。所有人都喜欢理解余裕上手天才打钱的萌萌的狗狗或者猫猫，没有人会喜欢阴湿带病的老鼠。但我还是问了嘉然小姐：“我能不能做你的狗？”我知道我是注定做不了狗的，但如果她喜欢狗，我就可以一直在身边看着她了，哪怕她怀里抱着的永远都是狗。
""".strip()

print("[*] Loading S1 pretrained model...")
change_gpt_weights(gpt_path=GPT_MODEL)

print(f"[*] Loading S2 model: {SOVITS_MODEL}...")
list(change_sovits_weights(sovits_path=SOVITS_MODEL))

print("[*] Generating...")
synthesis_result = get_tts_wav(
    ref_wav_path=REF_AUDIO,
    prompt_text=REF_TEXT,
    prompt_language=i18n("日文"),
    text=TARGET_TEXT,
    text_language=i18n("中文"),
    how_to_cut="按中文句号切",
    top_k=20,
    top_p=0.85,
    temperature=0.75,
)

result_list = list(synthesis_result)
if result_list:
    sr, audio = result_list[-1]
    out_path = "output_jiaran.wav"
    sf.write(out_path, audio, sr)
    print(f"[✓] Saved: {out_path} ({len(audio)/sr:.2f}s)")
else:
    print("✗ Generation failed!")
