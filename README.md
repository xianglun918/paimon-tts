# Paimon-TTS

基于 [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) 的语音合成衍生项目，专注于角色语音模型的微调、推理与归档。

> **声明**: 本项目不包含 GPT-SoVITS 核心代码。所有基础 TTS 能力来自上游 [RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS)。

---

## 项目定位

本项目仅维护以下内容：

- 微调后的 SoVITS v2 模型权重与参考音频
- 面向具体角色的推理脚本与配置
- 模型使用文档与最佳实践
- 训练过程中的技术经验与问题解决方案

---

## 快速开始

### 1. 克隆本项目（含子模块）

```bash
git clone --recurse-submodules https://github.com/xianglun918/paimon-tts.git
cd paimon-tts
```

如果已克隆但忘带子模块：

```bash
git submodule update --init --depth 1
```

### 2. 安装依赖

参照上游 [GPT-SoVITS 安装文档](https://github.com/RVC-Boss/GPT-SoVITS#installation)安装环境依赖。本项目的推理脚本会自动将子模块加入 Python 路径，无需手动设置 `PYTHONPATH`。

### 3. 下载模型

从 [Releases](https://github.com/xianglun918/paimon-tts/releases) 下载模型权重（`.pth`）和参考音频（`.wav`），放置在项目根目录。

### 4. 推理示例

```bash
# 模型 A （中文重点）
python infer_tangshi.py

# 模型 B （日语重点）
python infer_jiaran.py
```

---

## 模型档案

详见 [MODELS.md](./MODELS.md)。

---

## 目录结构

```
paimon-tts/
├── GPT_SoVITS/              # 【子模块】上游 GPT-SoVITS 核心代码
├── docs/
│   └── TRAINING_NOTES.md   # 训练技术经验与问题解决方案
├── infer_tangshi.py         # 模型 A 推理脚本（示例：唐诗）
├── infer_jiaran.py          # 模型 B 推理脚本（示例：中文长文本）
├── MODELS.md                # 模型文档与使用说明
├── README.md                # 本文件
└── LICENSE                  # MIT
```

---

## 上游项目

| 项目 | 链接 |
|------|-------|
| **Repository** | https://github.com/RVC-Boss/GPT-SoVITS |
| **License** | MIT |
| **说明** | 本项目所有基础 TTS/NLP 能力、训练框架、WebUI 均来自上游。感谢 RVC-Boss 及所有上游贡献者。 |

---

## License

本项目沿用上游 GPT-SoVITS 的 MIT License。模型权重仅供个人研究与非商业使用，请遵守相关法律法规。
