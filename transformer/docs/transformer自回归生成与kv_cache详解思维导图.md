# Transformer 自回归生成与 KV Cache 思维导图

## 1. 总体目标

-   搞清楚：类 GPT（decoder-only）模型从输入 prompt → prefill → decode → 采样 → 下一个 token 的完整链路
-   搞清楚：Transformer 块内部的张量维度变化
-   搞清楚：KV Cache 在多层、多 token、自回归过程中的存储与复用
-   搞清楚：LM Head 输出的 (S, vocab_size) 每一行的语义
-   搞清楚：采样策略（temperature / top-k / top-p）的作用位置和顺序

## 2. Transformer 架构层级

-   Encoder-Decoder 原始架构（原论文）
    -   Encoder: 接收整段源序列，双向 Self-Attention
    -   Decoder: Masked Self-Attention + Cross-Attention
-   Decoder-only 架构（GPT, LLaMA, Qwen/Mistral 等）
    -   只有 Decoder 堆叠（N 层）
    -   每层：LN → Masked Self-Attn → 残差 → LN → FFN → 残差
    -   无 Cross-Attn，因此所有注意力都是基于已生成的上下文
    -   核心输出：对“下一个 token”做条件概率建模

## 3. 张量维度主线（不含 batch）

-   基本符号
    -   S / T：当前输入序列长度（prompt 长度或已生成序列长度）
    -   d_model (d)：隐藏维度
    -   h：多头数
    -   d_h = d_model / h：每个头的维度
-   输入
    -   token ids → embedding: 形状 [S, d]
    -   位置编码/旋转位置编码 RoPE：与 [S, d] 对齐
-   Q/K/V 线性映射（以 Self-Attention 为例）
    -   Q = X W_Q → [S, d]
    -   K = X W_K → [S, d]
    -   V = X W_V → [S, d]
    -   多头拆分后：
        -   Q → [S, h, d_h] 或 [h, S, d_h]
        -   K → [S, h, d_h]
        -   V → [S, h, d_h]
-   注意力打分
    -   scores = Q Kᵀ → 形状 [h, S_q, S_k]
    -   Self-Attn 时：S_q = S_k = S
    -   Cross-Attn 时：S_q = S_target, S_k = S_source
    -   Masked Self-Attn：在 scores 上加下三角 mask
-   注意力输出
    -   A = softmax(scores) → [h, S_q, S_k]
    -   O = A V → [h, S_q, d_h]
    -   多头拼接 → [S_q, d]
    -   线性映射回 d → [S_q, d]

## 4. LayerNorm 的位置与含义

-   Transformer 中使用 LayerNorm 而不是 BatchNorm
-   LayerNorm：对“每个 token 的特征维度”做归一化 → 行内归一化 → 对应 [S, d] 中的 d 维
-   计算公式：
    -   μ = mean(x, dim=-1)
    -   σ = std(x, dim=-1)
    -   y = (x - μ)/σ \* γ + β
-   作用：稳定训练、配合残差、使不同 token 的表示尺度统一

## 5. Prefill 阶段（关键）

-   定义
    -   一次性把用户输入的 prompt（长度 = S₀）喂给模型做完整前向
    -   计算出该序列上每一个位置的隐藏表示 + K/V → 用于后续 decode
    -   产物：
        -   hidden: [S₀, d]
        -   raw_logits: [S₀, vocab_size]
        -   每一层的 KV Cache: [h, S₀, d_h]（忽略 batch）
-   每一行 raw_logits 的语义
    -   raw*logits[i] ≈ 模型在训练时学到的：P(x*{i+1} | x\_{≤i})
    -   即：基于前 i 个 token 预测第 i+1 个 token 的分布
    -   所以：最后一行 raw_logits[-1] = 基于全部 prompt 预测“第一个要生成的 token”的分布
-   重要认识
    -   在推理时，我们只用最后一行
    -   前面的行在推理时不会拿来真正“生成”，但**它们仍然是模型在“尽最大可能预测下一个 token”**的产物（因为训练就是这么优化的）
    -   但它们不保证 100% 等于输入里的 ground truth（模型不是完美的，输入也可能不是训练分布中出现过的原句）

## 6. Decode 阶段（增量生成）

-   生成流程（带 KV Cache）：
    1. 取上一步生成的 token → embedding → 形状 [1, d]
    2. 逐层前向：
        - 计算当前步的 Q
        - 从 KV Cache 中读取历史 K/V（形状 [h, t, d_h]）
        - 只为当前这个 token 计算 K_t, V_t → 形状 [h, 1, d_h]
        - 追加到缓存 → [h, t+1, d_h]
        - 计算注意力：A_t = softmax(Q_t Kᵀ) → [1, t+1]
        - O_t = A_t V → [1, d]
    3. 最后一层输出 → LM Head → logits_t: [vocab_size]
    4. 采样/贪心 → 得到下一个 token
    5. 回到第 1 步直到结束
-   特点：
    -   每一层都要缓存自己的 K/V（因为每一层的 W_Q/W_K/W_V 都不同）
    -   缓存是“增量 append”，不是覆盖
    -   推理时的 S_q=1, S_k=已生成长度

## 7. KV Cache 的多层、多 token 存储机制

-   标准做法（无 vLLM）：
    -   每层各自一份 KV：
        -   K[l] ∈ [B, H, T, d_h]
        -   V[l] ∈ [B, H, T, d_h]
    -   T 随着生成步数 t 增长
    -   不保存 A（注意力矩阵），只保存 K/V
-   vLLM 的 PagedAttention 的做法：
    -   逻辑：仍然是“我要一个连续的时间轴上的 K/V”
    -   物理：不一定是连续内存，拆成 block/page 存
    -   好处：
        -   动态分配
        -   多请求共享前缀
        -   避免大块连续显存浪费
    -   前缀缓存（prefix caching）：
        -   如果请求 B 的开头 token 序列与请求 A 的某些 block 完全一致 → 可以直接复用这些 block 的 KV
        -   粒度是 block，而不是任意 token
        -   所以：如果“France?”和“Germany?”落在同一个 block 里 → 这一整个 block 都不能复用，只能复用到上一个 block

## 8. 前缀缓存（prefix caching）你我的统一版理解

-   判断前缀是否可复用的关键不是“有一部分 token 一样”，而是“这些 token 在分页后的 block 边界上也一样”
-   所以前缀缓存是：**按块重用的前缀缓存**，不是按 token 粒度的
-   请求 B 在 prefill 时：
    -   直接拿请求 A 的 block0, block1……
    -   从第一个不匹配的 block 开始重新算 → 新生成的 KV 存到新的 block 里

## 9. LM Head 与 (S, vocab_size) 的语义

-   计算：logits = X @ W_Eᵀ
    -   X: [S, d]
    -   W_E: [vocab_size, d]
    -   logits: [S, vocab_size]
-   第 i 行 logits[i]:
    -   语义：基于“前 i 个 token”预测“第 i+1 个 token”的分布
    -   来源：训练目标是自回归 LM：P(x*t | x*{<t})
-   推理时只取最后一行：
    -   logits[-1] → 基于“全部上下文”预测“下一个 token”
    -   这一行再进入采样策略

## 10. 采样阶段的细化

-   步骤拆解：
    1. 得到 logits[-1] → [vocab_size]
    2. temperature 缩放（可选）：logits /= T
    3. softmax → 得到基础概率分布 p
    4. top-k（可选）：保留概率最高的 k 个，其他置 0
    5. top-p（可选）：在 top-k 之后再做累计概率裁剪，得到概率质量在 p 内的最小集合
    6. 重新归一化 → p'
    7. 采样（或贪心 argmax） → 得到下一个 token
-   顺序问题：
    -   一般是：**先 top-k，后 top-p**
    -   你的推导理由：如果先 top-p（是动态的），可能得到的集合大小 < k，此时再 top-k 就没有意义；所以先用 top-k 固定上限，再用 top-p 做动态裁剪 → 两者都能生效
-   不设置 top-k/top-p 时：
    -   直接在全词表上采样，理论上会采到极小概率的 token → 实际系统一般都会设一个默认的 top-p 或者直接用贪心

## 11. Prefill 阶段的 logits 能力的再解释

-   你提出的补充视角：
    -   “既然模型是按自回归方式训练的，那么对于已有的输入序列，它在 prefill 阶段对每一行做的预测，其实都是‘尽最大可能去还原真实下一个 token’的行为” —— ✅ 这个说法成立
    -   预训练结束后的大模型，面对符合训练分布的输入时：
        -   前几个位置的 logits 基本都会把真实下一个 token 排在前列
        -   只是我们在推理时不需要用这些位置的预测
    -   所以可以认为：prefill 阶段输出的 (S, vocab_size) 在“训练语义”上全部都有意义，在“推理语义”上我们只取最后一行

## 12. 为什么 Transformer 用 LayerNorm 而 CNN 用 BatchNorm

-   Transformer：
    -   输入是序列，每一行就是一个 token 的语义向量
    -   不同 token 之间语义差异大，不适合跨样本做统计
    -   所以用 LayerNorm：对每一行内部 across feature 做归一化
-   CNN：
    -   输入是图像，通道有空间一致性
    -   同一通道在不同样本、位置上统计一致，因此适合 BatchNorm：对 (B, H, W) 上同一通道做归一化

## 13. 生成模型的“通用模板”

-   前端：token embedding + 位置编码（或 RoPE）
-   中间：N × DecoderBlock（LN → Masked Self-Attn → 残差 → LN → FFN → 残差）
-   末端：Final LayerNorm → LM Head (weight tying) → logits → 采样策略 → token
-   理解了这个核心块，就可以在前后加：
    -   prefix encoder / adapter / LoRA
    -   多模态 encoder（图文对齐）
    -   控制模块（prefix prompt, system prompt, SFT head）
    -   量化 / KV Cache 压缩 / paged attention / prefix caching

## 14. 关键结论回顾

-   raw_logits 的每一行都有“基于前 i 个 token 预测第 i+1 个”的含义
-   推理时只取最后一行，是因为我们只需要“基于全部上下文的下一个 token 的分布”
-   KV Cache 会在**每个 decoder 层**中缓存 K/V，并且是增量追加
-   vLLM 的 prefix caching 是**按 block**粒度的，只有完全对齐的 block 才能复用
-   采样策略是 **softmax 之后的事**，不影响 Transformer 内部计算
-   top-k 和 top-p 同时用时，通常是 **先 k 后 p**，你的推理“否则 top-k 失效”是对的
-   Prefill 阶段虽然输出了 S 行 logits，但只有最后一行被用于真正生成，前面各行只是“训练语义上的预测”
