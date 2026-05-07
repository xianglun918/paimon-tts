# Training Notes

本文档记录使用 GPT-SoVITS v2 进行少样本语音微调的技术经验、踩过的坑以及解决方案。

> **项目路径**: `~/.openclaw/GPT-SoVITS`  
> **基础框架**: [RVC-Boss/GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) (MIT License)  
> **版本**: GPT-SoVITS v2

---

## 整体流程概览

```
原始音频样本
    ↓
质量筛选（单人说话、无背景噪音、2–10s 片段）
    ↓
重采样至 32 kHz
    ↓
自动分段
    ↓
ASR 识别 + 人工文本标注
    ↓
S2 微调（40 epochs）
    ↓
手动转换 checkpoint → 推理格式
    ↓
合成推理
```

### 时间线

| 阶段 | 耗时 | 状态 |
|------|------|------|
| 数据准备 | ~2h | ✅ |
| S1 微调尝试 (40 epochs) | ~12h | ❌ 失败 (top_3_acc 仅 1.15%) |
| S2 微调 (40 epochs) | ~17h | ✅ |
| 推理 bug 排查 | ~3h | ✅ |
| 模型对比测试 | ~1h | ✅ Epoch 40 锁定 |

---

## 数据准备

### 过滤策略

1. 只保留单人说话片段（排除多人对话、背景幺吓）
2. 排除 BGM 、音效声较重的片段
3. 保留 2–10 秒的片段
4. 音频质量过关

### 过滤结果

| 指标 | 数值 |
|------|------|
| 原始样本数 | ~25,000 |
| 过滤后样本数 | **937** |
| 过滤比例 | **96.2%** |
| 总音频时长 | ~60 分钟 |
| 平均片段长度 | 3.84 秒 |
| 2–5 秒占比 | 78% |

### 数据量反思

**官方说"1 分钟"，为什么我们用了 60 分钟？**

1. **"1 分钟"是 few-shot TTS 的宣传数字** — 指用 1 分钟高质量音频微调 S2，音色相似度就能明显提升
2. **实际生产级克隆通常需要 5–30 分钟** — 1 分钟只能做到"有点像"，要稳定、自然、跨文本泛化，需要更多数据
3. **S1 和 S2 对数据的需求不同**：
   - S2 (SoVITS): 学习音色特征，少量高质量数据即可
   - S1 (GPT): 学习语义映射，需要更多数据

**结论**: 60 分钟对 S2 来说充足，但 S1 失败不是因为数据量不够，而是超参数/训练配置有问题。

**最优策略**: 5–10 分钟极致高质量数据 > 60 分钟低质量数据

---

## S1 微调（已失败，作为经验记录）

### 训练配置

```yaml
learning_rate: 5e-4
batch_size: 6
epochs: 40
max_sec: 54
```

### 结果

| 指标 | 最终值 | 状态 |
|------|--------|------|
| total_loss | 2.8e+3 | ❌ 偏高 |
| top_3_acc | **1.15%** | ❌ 极低 |

### 失败分析

top_3_acc 仅 1.15% 意味着 GPT 几乎没学到任何东西。

可能原因：
1. 学习率偏高 (5e-4) — 对于已在 5000h 数据上预训练的模型，微调时学习率应该更低 (1e-4 ~ 2e-4)
2. batch_size 偏小 (6) — 导致梯度不稳定
3. 数据质量问题 — 即使经过过滤，仍可能有噪音、BGM 残留
4. 训练轮次不足 — 40 epochs 对于 937 条数据可能不够

### 修复建议

```yaml
learning_rate: 2e-4
batch_size: 12
epochs: 100
```

---

## S2 微调（成功）

### 训练配置

```json
{
  "train": {
    "epochs": 40,
    "batch_size": 4,
    "learning_rate": 1e-4,
    "save_every_epoch": 2,
    "if_save_every_weights": false
  }
}
```

### 训练结果

| Epoch | G_Loss | D_Loss | G+D 总和 |
|------|--------|--------|---------|
| 2 | 2.905 | 2.041 | 4.946 |
| 4 | 2.403 | 2.671 | 5.073 |
| 6 | 2.629 | 2.282 | 4.911 |
| 7 | 2.702 | **1.984** | **4.686** (optimal) |
| 12 | 2.482 | 2.386 | 4.869 |
| 27 | **2.171** | 2.655 | 4.826 (min G_loss) |
| 40 | 2.381 | 2.484 | 4.865 |

**最低 G+D 总和在 Epoch 7，但 Epoch 2 就已能生成正常音频。**

### 改进建议

```json
{
  "train": {
    "if_save_every_weights": true,
    "save_every_epoch": 5
  }
}
```

---

## 推理生成

### 最终模型配置

| 组件 | 路径 |
|------|-------|
| S1 (GPT) | 官方预训练 `s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt` |
| S2 (SoVITS) | `pm-v2-epoch40.pth` (Epoch 40) |
| 参考音频 | `ref_pm.wav` (~6.5s) |
| 参考文本 | "聊到炼金和研究的话题,砂糖就完全不怯场了,这就是研究者的气质吗?" |

### 推理参数

```python
how_to_cut = "不切"        # 避免过度切割导致不连贯
top_p = 0.85                # 默认 0.6 太保守，导致提前 EOS
temperature = 0.75          # 默认 0.6 太低
top_k = 20
```

### 参数对比效果

| 参数组合 | 同一文本音频时长 |
|---------|----------------|
| top_p=0.6, temperature=0.6 | 0.74s ❌ |
| top_p=0.85, temperature=0.75 | 6.78s ✅ |

---

## 核心问题与解决方案

### Bug 1: inference_cli.py 未正确加载模型

**问题**: `change_sovits_weights()` 是 generator 函数，但 `inference_cli.py` 直接调用而不消费 generator，导致模型加载代码未执行。

**影响**: 无论传什么模型路径，实际使用的都是默认预训练模型。

**解决**:
```python
# 原代码
change_sovits_weights(sovits_path=SoVITS_model_path)

# 修复后
list(change_sovits_weights(sovits_path=SoVITS_model_path))
```

### Bug 2: 训练 checkpoint 格式不匹配

**问题**: 训练保存的格式是 `{'model': ..., 'iteration': ...}`，推理期望 `{'weight': ..., 'config': ..., 'info': ...}`。

**影响**: 直接加载会 KeyError: 'config'。

**解决**: 手动转换脚本：
```python
import torch
import json

config_path = "s2_config.json"
with open(config_path) as f:
    config = json.load(f)

ckpt = torch.load("G_9440.pth", map_location="cpu", weights_only=False)
weight = ckpt["model"]
weight_filtered = {k: v for k, v in weight.items() if "enc_q" not in k}

infer_ckpt = {
    "weight": weight_filtered,
    "config": config,
    "info": "GPT-SoVITS-v2-finetuned-epoch40",
}
torch.save(infer_ckpt, "G_9440_infer.pth")
```

### Bug 3: inference_webui.py 变量未初始化

**问题**: `change_sovits_weights()` 中 `prompt_text_update` 等变量在 `prompt_language=None` 时未定义，导致 UnboundLocalError。

**解决**: 在函数开头添加默认值初始化。

### Bug 4: PyTorch 2.6 weights_only 兼容性

**问题**: PyTorch 2.6 默认 `weights_only=True`，旧版 checkpoint 加载失败。

**解决**:
```python
import pathlib
import torch
torch.serialization.add_safe_globals([pathlib.PosixPath])
```

---

## 最佳实践总结

### 数据准备

- [ ] 原始数据不在乎多，在于精 — 尽可能筛选出 5–10 分钟极致高质量的单人说话音频
- [ ] 参考音频选择 3–10 秒典型音色片段
- [ ] 参考文本必须与音频内容完全匹配

### S1 训练

- [ ] 如果数据量 < 1000 条，建议直接使用预训练 S1 模型
- [ ] 如果必须微调 S1，降低学习率至 2e-4，增加 epochs 至 100+
- [ ] 每 10 epochs 做一次推理测试验证

### S2 训练

- [ ] 设置 `if_save_every_weights: true` 保存推理格式
- [ ] `save_every_epoch` 可设为 5 减少磁盘占用
- [ ] epoch 10 左右就可以开始测试，不需要等到 40

### 推理生成

- [ ] **训练前必须先验证推理链路**！
- [ ] 修复 inference_cli.py 的 generator 消费 bug
- [ ] 推荐参数: top_p=0.85, temperature=0.75
- [ ] 对于短文本，如果生成过短，尝试提高 top_p/temperature

### 模型选择

- [ ] 不要只看 loss 选模型 — 人耳听感比 loss 更重要
- [ ] 建议对比 3–5 个 epoch 的模型
- [ ] 综合考虑: 音色相似度、语调自然度、断句流畅度

---

*Last updated: 2026-05-07*
