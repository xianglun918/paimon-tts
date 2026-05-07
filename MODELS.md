# 🎞️ Model Zoo

> **Download**: [GitHub Releases](https://github.com/xianglun918/paimon-tts/releases)  
> **License**: MIT · **Usage**: Personal research & non-commercial only

---

## 🏷️ Model Cards

<div align="center">

<table>
<tr>
<td align="center" width="50%">

### 🎯 Model A — PM

`pm-v2-epoch40.pth`

| Spec | Value |
|------|-------|
| **Base** | GPT-SoVITS v2 |
| **S1** | Official pretrained (no finetuning) |
| **S2** | Finetuned · 40 epochs |
| **Language** | Chinese (中文) |
| **Size** | ~162 MB |
| **Ref Audio** | `ref_pm.wav` (6.5s) |
| **Ref Text** | "聊到炼金和研究的话题,砂糖就完全不怯场了,这就是研究者的气质吗?" |

</td>
<td align="center" width="50%">

### 🎭 Model B — TN

`tn-v2-epoch40.pth`

| Spec | Value |
|------|-------|
| **Base** | GPT-SoVITS v2 |
| **S1** | Official pretrained (no finetuning) |
| **S2** | Finetuned · 40 epochs |
| **Language** | Japanese (日本語) |
| **Size** | ~202 MB |
| **Ref Audio** | `ref_tn.wav` (3.0s) |
| **Ref Text** | "元気、元気の元気まるー" |

</td>
</tr>
</table>

</div>

---

## 🚀 Quick Start

### Prerequisites

```bash
# 1. Ensure submodule is initialized
git submodule update --init --depth 1

# 2. Install upstream dependencies (see upstream README)
#    You need: PyTorch, GPT-SoVITS requirements, and the official S1 pretrained model

# 3. Download model weights + reference audio from Releases
#    Place them in the project root directory
```

### One-liner Inference

```bash
# Model A — Chinese poetry
python infer_tangshi.py

# Model B — Long-form text
python infer_jiaran.py
```

### Custom Integration

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "GPT_SoVITS"))

import soundfile as sf
from GPT_SoVITS.inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav
from tools.i18n.i18n import I18nAuto

i18n = I18nAuto()

# 1. Load S1 (official pretrained — shared by all models)
change_gpt_weights(
    gpt_path="GPT_SoVITS/GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt"
)

# 2. Load S2 (pick one)
list(change_sovits_weights(sovits_path="pm-v2-epoch40.pth"))

# 3. Synthesize
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

> ⚠️ **Critical**: `prompt_text` must match the reference audio content as closely as possible. Mismatch degrades output quality significantly.

---

## 🎯 Tuning Guide

### Recommended Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `top_p` | **0.85** | Default 0.6 is too conservative; triggers premature EOS |
| `temperature` | **0.75** | Default 0.6 is too low; produces unnaturally short audio |
| `top_k` | **20** | Balanced diversity vs stability |
| `how_to_cut` | **No cut** | For texts < 50 chars; sentence slicing causes fragmentation |

### Parameter Impact

| Combo | Output Duration | Quality |
|-------|-----------------|---------|
| top_p=0.60, temp=0.60 | ~0.74s ❌ | Truncated, unusable |
| top_p=0.85, temp=0.75 | ~6.78s ✅ | Natural, full-length |

> 💡 **Rule of thumb**: If output is too short → raise top_p/temp. If output is garbled → lower them.

---

## 🔧 Troubleshooting

### `ModuleNotFoundError: No module named 'GPT_SoVITS'`

**Cause**: Submodule not initialized or Python path not set.  
**Fix**:
```bash
git submodule update --init --depth 1
# Scripts auto-add submodule to sys.path, but you can also:
export PYTHONPATH="${PYTHONPATH}:$(pwd)/GPT_SoVITS"
```

### `KeyError: 'config'` when loading .pth

**Cause**: Using a raw training checkpoint instead of the inference-format file.  
**Fix**: Download the `_infer.pth` files from our Releases — they are already converted.

### `UnboundLocalError` in inference_webui

**Cause**: Upstream bug when `prompt_language=None`.  
**Fix**: Always specify `prompt_language`. Our scripts already handle this.

### PyTorch 2.6+ `weights_only` error

**Fix**:
```python
import pathlib, torch
torch.serialization.add_safe_globals([pathlib.PosixPath])
```

---

## 📜 Data Pipeline

```
Raw voice samples
    ↓
Quality filter — single speaker, clean audio, 2–10s clips
    ↓
Resample to 32 kHz
    ↓
Auto-segmentation
    ↓
ASR + manual text annotation
    ↓
S2 finetune — 40 epochs, lr=1e-4, batch=4
    ↓
Checkpoint conversion → inference format
    ↓
🎙️ Deploy
```

### Key Stats

| Stage | Count / Value |
|-------|---------------|
| Raw samples | ~25,000 |
| After filtering | **937** (96.2% filtered) |
| Total audio | ~60 min |
| Avg clip length | 3.84s |
| 2–5s clips | 78% |

---

## 🙏 Disclaimer

These models are provided for **personal research, educational, and non-commercial purposes only**.

- Model weights are transformative derivative works.
- **Not affiliated with** any original content creators, voice actors, or rights holders.
- Users are responsible for complying with all applicable laws.
- Please use responsibly and respectfully.

No copyrighted training data, game assets, or original audio sources are distributed in this repository or its releases.
