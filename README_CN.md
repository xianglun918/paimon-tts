<div align="center">

<h1>🎙️ Paimon-TTS</h1>
<p><b>基于 GPT-SoVITS 的角色语音合成模型</b></p>

<a href="https://github.com/xianglun918/paimon-tts/releases"><img src="https://img.shields.io/github/v/release/xianglun918/paimon-tts?style=for-the-badge&logo=github&color=blue" /></a>
<a href="https://github.com/xianglun918/paimon-tts/blob/main/LICENSE"><img src="https://img.shields.io/badge/LICENSE-MIT-green.svg?style=for-the-badge&logo=opensourceinitiative" /></a>
<a href="#"><img src="https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge&logo=python" /></a>
<a href="https://github.com/RVC-Boss/GPT-SoVITS"><img src="https://img.shields.io/badge/上游-GPT--SoVITS-orange?style=for-the-badge" /></a>

<br>

<p>
  <a href="./MODELS.md">📋 模型档案</a> ·
  <a href="./docs/TRAINING_NOTES.md">🔬 训练笔记</a> ·
  <a href="https://github.com/xianglun918/paimon-tts/releases">📦 发行版</a> ·
  <a href="#quickstart">⚡ 快速开始</a>
</p>

</div>

---

## ✨ 亮点

<table>
<tr>
<td width="50%">

### 🎯 模型 A — PM
- **语言**: 中文
- **风格**: 活泼、富有表现力
- **适合场景**: 诗歌朗诵、对话、旁白
- **参考音频**: 6.5s 中文样本

</td>
<td width="50%">

### 🎭 模型 B — TN
- **语言**: 日语
- **风格**: 明快、元气满满
- **适合场景**: ACG 内容、短句合成、跨语言合成
- **参考音频**: 3.0s 日语样本

</td>
</tr>
</table>

### 🔑 核心特性

| 特性 | 状态 | 说明 |
|---------|--------|--------|
| 🎨 **少样本微调** | ✅ 可用 | S2 训练 40 epoch，基于筛选后的高质量样本 |
| 🌐 **跨语言合成** | ✅ 可用 | 中文目标文本配日语参考音频（或相反） |
| 🚀 **即开即用** | ✅ 可用 | 一行命令运行推理，自动处理路径 |
| 🔗 **上游同步** | ✅ 可用 | Git 子模块跟踪最新 GPT-SoVITS |
| 📦 **Release 分发** | ✅ 可用 | 模型权重 + 参考音频通过 GitHub Releases 发布 |

---

## 🚀 快速开始

### 1️⃣ 克隆项目（含子模块）

```bash
git clone --recurse-submodules https://github.com/xianglun918/paimon-tts.git
cd paimon-tts
```

> 💡 如果忘记带子模块：
> ```bash
> git submodule update --init --depth 1
> ```

### 2️⃣ 安装依赖

参照上游 [GPT-SoVITS 安装指南](https://github.com/RVC-Boss/GPT-SoVITS#installation) 配置 Python 环境。

**macOS 快捷方式**（Apple Silicon）：
```bash
conda create -n paimon-tts python=3.10
conda activate paimon-tts
pip install -r GPT_SoVITS/requirements.txt
```

### 3️⃣ 下载模型

从 [Releases](https://github.com/xianglun918/paimon-tts/releases) 下载模型文件，放到项目根目录：

```bash
# 下载后确认文件存在
ls *.pth *.wav
# pm-v2-epoch40.pth  tn-v2-epoch40.pth  ref_pm.wav  ref_tn.wav
```

### 4️⃣ 运行推理

```bash
# 模型 A — 唐诗朗诵示例
python infer_tangshi.py

# 模型 B — 长文本示例
python infer_jiaran.py
```

输出文件会生成在当前目录：`output_tangshi.wav` / `output_jiaran.wav`

---

## 🎛️ 推荐参数

经过大量测试，以下参数能够获得最自然的效果：

| 参数 | 推荐值 | 说明 |
|-----------|-------|-----|
| `top_p` | **0.85** | 默认 0.6 太保守，容易提前截断 |
| `temperature` | **0.75** | 默认 0.6 太低，输出会过短 |
| `top_k` | **20** | 标准值 |
| `how_to_cut` | **不切** | 短文本（< 50 字）推荐不切，避免句子碎片化 |

> ⚠️ **小贴士**: 如果输出被截断，调高 `top_p` 和 `temperature`；如果发音不稳，适当降低。

---

## 📦 模型档案

| 模型 | 权重文件 | 参考音频 | 语言 | Epoch | 大小 |
|-------|--------|-----------|------|-------|------|
| **PM** | `pm-v2-epoch40.pth` | `ref_pm.wav` (6.5s) | 中文 | 40 | ~162 MB |
| **TN** | `tn-v2-epoch40.pth` | `ref_tn.wav` (3.0s) | 日语 | 40 | ~202 MB |

📖 **完整文档**: [MODELS.md](./MODELS.md)

---

## 🏗️ 项目结构

```
paimon-tts/
├── 🎛️ GPT_SoVITS/              # [子模块] 上游核心代码
│   └── (跟踪 RVC-Boss/GPT-SoVITS)
│
├── 🎯 infer_tangshi.py         # 模型 A 推理脚本
├── 🎭 infer_jiaran.py          # 模型 B 推理脚本
│
├── 📋 MODELS.md                # 模型文档与使用说明
├── 🔬 docs/TRAINING_NOTES.md   # 训练经验与 bug 修复
│
├── 📄 README.md                # 英文文档
├── 📄 README_CN.md             # 中文文档
└── ⚖️  LICENSE                  # MIT
```

---

## 🔬 与上游的区别？

本仓库**不包含** GPT-SoVITS 引擎本身。它是一个**衍生项目**，提供：

1. **微调后的 S2 权重**，针对特定音色风格
2. **即开即用的推理脚本**，自动处理路径配置
3. **精心挑选的参考音频+文本对**，针对每个模型优化
4. **训练笔记**，记录坑点与解决方案

所有核心 TTS/NLP 能力、训练框架、WebUI 均来自上游项目。

---

## 🙏 致谢

本项目基于 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 构建，感谢 **RVC-Boss** 及所有上游贡献者。

| | |
|:---|:---|
| **上游仓库** | https://github.com/RVC-Boss/GPT-SoVITS |
| **开源协议** | MIT |
| **基础框架** | GPT-SoVITS v2 |

---

## ⚖️ 开源协议

本项目继承上游 GPT-SoVITS 的 **MIT License**。

模型权重仅供**个人研究与非商业使用**，请遵守所在地区法律法规。

本仓库及其 Release 均不分发任何受版权保护的训练数据、游戏资源或原始音频来源。
