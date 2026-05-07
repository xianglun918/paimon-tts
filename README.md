<div align="center">

<h1>🎙️ Paimon-TTS</h1>
<p><b>Finetuned Character Voice Models · Powered by GPT-SoVITS</b></p>

<a href="https://github.com/xianglun918/paimon-tts/releases"><img src="https://img.shields.io/github/v/release/xianglun918/paimon-tts?style=for-the-badge&logo=github&color=blue" /></a>
<a href="https://github.com/xianglun918/paimon-tts/blob/main/LICENSE"><img src="https://img.shields.io/badge/LICENSE-MIT-green.svg?style=for-the-badge&logo=opensourceinitiative" /></a>
<a href="#"><img src="https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge&logo=python" /></a>
<a href="https://github.com/RVC-Boss/GPT-SoVITS"><img src="https://img.shields.io/badge/Upstream-GPT--SoVITS-orange?style=for-the-badge" /></a>

<br>

<p>
  <a href="./MODELS.md">📋 Models</a> ·
  <a href="./docs/TRAINING_NOTES.md">🔬 Training Notes</a> ·
  <a href="https://github.com/xianglun918/paimon-tts/releases">📦 Releases</a> ·
  <a href="#quickstart">⚡ Quick Start</a>
</p>

</div>

---

## ✨ Highlights

<table>
<tr>
<td width="50%">

### 🎯 Model A — PM
- **Language Focus**: Chinese (中文)
- **Style**: Energetic, expressive
- **Best For**: Poetry recitation, dialogue, narration
- **Reference**: 6.5s Chinese sample

</td>
<td width="50%">

### 🎭 Model B — TN
- **Language Focus**: Japanese (日本語)
- **Style**: Cheerful, animated
- **Best For**: ACG content, short phrases, cross-lingual synthesis
- **Reference**: 3.0s Japanese sample

</td>
</tr>
</table>

### 🔑 Key Features

| Feature | Status | Detail |
|---------|--------|--------|
| 🎨 **Few-shot Finetuning** | ✅ Ready | S2 trained 40 epochs on filtered high-quality samples |
| 🌐 **Cross-lingual** | ✅ Ready | Chinese target text with JP reference, or vice versa |
| 🚀 **Out-of-box Scripts** | ✅ Ready | One-command inference with auto path handling |
| 🔗 **Upstream Sync** | ✅ Active | Git submodule tracks latest GPT-SoVITS |
| 📦 **Release Distribution** | ✅ Ready | Models + reference audio via GitHub Releases |

---

## 🚀 Quick Start

### 1️⃣ Clone (with submodule)

```bash
git clone --recurse-submodules https://github.com/xianglun918/paimon-tts.git
cd paimon-tts
```

> 💡 If you forgot `--recurse-submodules`:
> ```bash
> git submodule update --init --depth 1
> ```

### 2️⃣ Install Dependencies

Follow the upstream [GPT-SoVITS installation guide](https://github.com/RVC-Boss/GPT-SoVITS#installation) to set up the Python environment.

**macOS shortcut** (Apple Silicon):
```bash
conda create -n paimon-tts python=3.10
conda activate paimon-tts
pip install -r GPT_SoVITS/requirements.txt
```

### 3️⃣ Download Models

Grab the latest release assets and place them in the project root:

```bash
# Download from Releases page, then:
ls *.pth *.wav
# pm-v2-epoch40.pth  tn-v2-epoch40.pth  ref_pm.wav  ref_tn.wav
```

### 4️⃣ Generate Speech

```bash
# Model A — Tang poetry demo
python infer_tangshi.py

# Model B — Long text demo
python infer_jiaran.py
```

Output files will appear as `output_tangshi.wav` / `output_jiaran.wav`.

---

## 🎛️ Recommended Settings

After extensive testing, these parameters deliver the most natural results:

| Parameter | Value | Why |
|-----------|-------|-----|
| `top_p` | **0.85** | Default 0.6 is too conservative; causes early cut-off |
| `temperature` | **0.75** | Default 0.6 is too low; output becomes unnaturally short |
| `top_k` | **20** | Standard value |
| `how_to_cut` | **No cut** | For texts < 50 chars; prevents sentence fragmentation |

> ⚠️ **Pro Tip**: If your output sounds truncated, raise `top_p` and `temperature`. If it sounds unstable, lower them slightly.

---

## 📦 Model Zoo

| Model | Weight | Ref Audio | Lang | Epoch | Size |
|-------|--------|-----------|------|-------|------|
| **PM** | `pm-v2-epoch40.pth` | `ref_pm.wav` (6.5s) | CN | 40 | ~162 MB |
| **TN** | `tn-v2-epoch40.pth` | `ref_tn.wav` (3.0s) | JP | 40 | ~202 MB |

📖 **Full documentation**: [MODELS.md](./MODELS.md)

---

## 🏗️ Project Structure

```
paimon-tts/
├── 🎛️ GPT_SoVITS/              # [Submodule] Upstream core code
│   └── (tracks RVC-Boss/GPT-SoVITS)
│
├── 🎯 infer_tangshi.py         # Model A inference demo
├── 🎭 infer_jiaran.py          # Model B inference demo
│
├── 📋 MODELS.md                # Model docs & usage guide
├── 🔬 docs/TRAINING_NOTES.md   # Training experience & bug fixes
│
├── 📄 README.md                # This file
└── ⚖️  LICENSE                  # MIT (from upstream)
```

---

## 🔬 What's Different from Upstream?

This repo does **not** contain the GPT-SoVITS engine. It is a **derivative project** that provides:

1. **Finetuned S2 weights** for specific voice styles
2. **Ready-to-use inference scripts** with path auto-configuration
3. **Curated reference audio + text pairs** optimized for each model
4. **Training notes** documenting pitfalls and solutions

All core TTS/NLP capabilities, training frameworks, and WebUI come from the upstream project.

---

## 🙏 Acknowledgments

This project stands on the shoulders of [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) by **RVC-Boss** and all its contributors.

| | |
|:---|:---|
| **Upstream** | https://github.com/RVC-Boss/GPT-SoVITS |
| **License** | MIT |
| **Base Model** | GPT-SoVITS v2 |

---

## ⚖️ License

This project inherits the **MIT License** from the upstream GPT-SoVITS project.

Model weights are provided for **personal research and non-commercial use only**. Please comply with applicable laws and regulations in your jurisdiction.

No training datasets, game assets, or original audio sources are distributed in this repository or its releases.
