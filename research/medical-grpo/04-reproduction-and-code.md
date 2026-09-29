# 代码与复核：先读结果，再决定是否运行

[← 入口](00-project-overview.md) · [实验设计](01-experiment-design.md) · [主结果](02-main-results.md)

**复算已完成；训练没有为写笔记而重跑。**本地归档缺合并基座、LoRA 权重和完整优化器 checkpoint，不能只凭 notebook 与指标文件复现同一训练。主文件是medical_grpo2 (1).ipynb（原始文件仅存于本地）；当前代码可能经过修改，不能自动当成产生旧输出时的配置。

## 可复核什么

本地复算脚本和逐题 JSONL 没有公开，因此这份仓库**只能核查汇总值和协议说明，不能独立重跑逐题复算**。本地复算已执行成功：脚本检查题号唯一和主实验四份 `(id, gold)` 顺序一致，汇总 20 行历史与主实验记录；不加载模型、不用 GPU。两张图只取同协议的真实结果，不插值训练曲线：[主实验](assets/validation-accuracy.svg)、[V2 旧协议](assets/v2-greedy-accuracy.svg)。详细证据映射保留在本地。

## 如果将来重新运行

| 阶段 | 主 notebook 单元 / 函数 | 性质 |
| --- | --- | --- |
| 环境、配置、解析与评估定义 | A0～A3c；`extract_answer`、`evaluate_vllm` | 定义为主；A1 建目录 |
| 清洗与冻结题池 | B0～B2；`question_key`、`build_candidates` | B1c 写数据；不训练 |
| 初始 SFT 评估 | C0～C1 | GPU 推理；已有 JSONL 可直接复核 |
| 四答诊断 | D0～D2 | GPU 推理；不更新权重 |
| 纠错探索 | E0～E4 | **E1 训练**；与后续 RL 分支分开 |
| 直接 GRPO | F0～F3；`MixedOnlyGRPOTrainer` | **F2 训练**；从初始 SFT 启动 |
| GRPO 评估 | G0～G3 | 推理占 GPU；读既有汇总不训练 |
| DAPO 方案 | H0～H6；`build_dapo_command` | **H3 开启训练开关后会训练**；归档默认关闭 |

原始实现请读对应单元。本文不复制长代码；训练奖励插件（原始文件仅存于本地）和实际 DAPO 参数（原始文件仅存于本地）可用于核对配置，不代表已完成论文逐项复现。

## 环境与文件索引

Qwen3 主路线保存的环境为 RTX 4090、`torch 2.8.0+cu128`、`transformers 4.55.2`、`trl 0.21.0`、`peft 0.17.1`、`vllm 0.10.2`；DAPO 使用独立的 `ms-swift 4.5.3`、`trl 0.26.2`、`transformers 4.56.1`。具体以主协议（原始文件仅存于本地）和归档参数（原始文件仅存于本地）为准。Qwen2.5 的环境另见早期记录（原始文件仅存于本地），不要混装依赖。

| 文件 | 用途 |
| --- | --- |
| medical_grpo.ipynb（原始文件仅存于本地） | Qwen2.5 smoke、G=2/G=8、FP32 复评 |
| medical_grpo2.ipynb（原始文件仅存于本地） | Qwen3 V2：2千题 SFT 与三奖励 GRPO |
| medical_grpo3.ipynb（原始文件仅存于本地） | Qwen3 V3：1万题 SFT；第二轮逐题评估缺失 |
| medical_grpo2 (1).ipynb（原始文件仅存于本地） | 最终纠错探索、直接 GRPO、DAPO 配置对照 |
| 最终云端输出归档（原始文件仅存于本地） · 运行摘要（原始文件仅存于本地） | 输出、评估配置与耗时；不含权重 |
| [实验索引](data/experiment-index.csv) · [结果表](data/results-summary.csv) · 证据索引（仅存于本地） | 配置、协议、数字与原文件位置 |

公开笔记不附题目原文、模型权重或私有证据归档。无法复训的条件及未完成的 test、多种子和 V3 第二轮核验见待补清单（仅存于本地）。
