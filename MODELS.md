# Finetuned Voice Models

本项目维护两个基于 GPT-SoVITS v2 微调的 SoVITS S2 模型，用于语音合成研究与个人项目。

> **声明**: 本文档不含训练数据集或原始音频来源。仅提供最终模型权重及推理所需的最小参考音频片段。

---

## 模型概览

| 模型 | 文件 | 大小 | Epoch | S1 | S2 |
|-------|------|------|-------|----|----|
| Model A (PM) | `pm-v2-epoch40.pth` | ~162 MB | 40 | 官方预训练 | 微调 |
| Model B (TN) | `tn-v2-epoch40.pth` | ~202 MB | 40 | 官方预训练 | 微调 |

两个模型均使用官方 GPT-SoVITS v2 预训练 S1 （语义模型），未额外微调 S1。仅 S2 （声学/生成器）分支在筛选后的高质量语音样本上进行了微调。

### 下载

从 [Releases](../../releases) 页面下载最新版本。

---

## 使用方法

### 前提条件

- Python 3.10+
- 已通过子模块初始化上游 GPT-SoVITS 代码
- 官方预训练 S1: `GPT_SoVITS/GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt`

### 快速开始

本项目的推理脚本已自动处理子模块路径，可直接运行：

```bash
python infer_tangshi.py   # Model A
python infer_jiaran.py    # Model B
```

也可手动集成到自己的代码中：

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'GPT_SoVITS'))

import soundfile as sf
from GPT_SoVITS.inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav
from tools.i18n.i18n import I18nAuto

i18n = I18nAuto()

# 1. 加载 S1（官方预训练 — 所有模型通用）
change_gpt_weights(
    gpt_path="GPT_SoVITS/GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt"
)

# 2. 加载 S2（选择一个模型）
list(change_sovits_weights(sovits_path="pm-v2-epoch40.pth"))

# 3. 生成
result = get_tts_wav(
    ref_wav_path="ref_pm.wav",
    prompt_text="聊到炼金和研究的话题,砂糖就完全不怯场了,这就是研究者的气质吗?",
    prompt_language=i18n("中文"),
    text="你好，这是一段测试语音。",
    text_language=i18n("中文"),
    how_to_cut="不切",
    top_p=0.85,
    temperature=0.75,
    top_k=20,
)

sr, audio = list(result)[-1]
sf.write("output.wav", audio, sr)
```

### 参考音频与文本

| 模型 | 参考音频 | 时长 | 语言 | 参考文本 |
|-------|-----------------|--------|----------|----------------|
| PM | `ref_pm.wav` | ~6.5s | 中文 | `聊到炼金和研究的话题,砂糖就完全不怯场了,这就是研究者的气质吗?` |
| TN | `ref_tn.wav` | ~3.0s | 日语 | `元気、元気の元気まるー` |

> **重要**: `prompt_text` 必须与参考音频内容尽量匹配，否则会影响合成效果。

---

## 推荐推理参数

| 参数 | 值 | 说明 |
|-----------|-------|-------|
| `top_p` | 0.85 | 默认 0.6 太保守，可能导致提前 EOS |
| `temperature` | 0.75 | 默认 0.6 太低，会缩短输出 |
| `top_k` | 20 | 标准 |
| `how_to_cut` | `不切` | 短文本（< 50 字）推荐不切，避免碎片化 |

这些参数经验性确定，能够生成自然、完整的语句。

---

## 技术细节

### 数据流水线

```
原始语音样本
    ↓
质量筛选（单人说话、干净音频、2–10s 片段）
    ↓
重采样至 32 kHz
    ↓
自动分段
    ↓
ASR + 人工文本标注
    ↓
S2 微调（40 epochs, lr=1e-4, batch=4）
    ↓
手动 checkpoint 转换 → 推理格式
```

### 已知问题与修复

1. **Generator consumption bug**: `change_sovits_weights()` 返回一个 generator。必须用 `list()` 消费后才能正确加载模型权重。本项目提供的推理脚本已处理此问题。
2. **Checkpoint 格式不匹配**: 训练保存的格式是 `{"model": ...}`，推理期望 `{"weight": ..., "config": ..., "info": ...}`。Release 中的 `.pth` 文件已经转换为推理格式。
3. **PyTorch 2.6 兼容性**: 若使用 PyTorch ≥ 2.6，需在加载 checkpoint 前添加 `torch.serialization.add_safe_globals([pathlib.PosixPath])`。

---

## 免责声明

这些模型仅供 **个人研究、教育和非商业目的**。

- 模型权重是通过变换性训练得到的衍生作品。
- **不代表任何原始内容创作者、声优或版权所有者**。
- 用户需自行遵守所在地区的法律法规。
- 请合理、尊重地使用。

本仓库及其 Release 均不分发任何受版权保护的训练数据、游戏资源或原始音频来源。

---

## License

模型权重沿用与基础项目相同的 MIT License。详见 [LICENSE](LICENSE)。
