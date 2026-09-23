# AI 评测工程 Starter Kit — 面试讲述卡

## 60 秒

我做这个自建项目是为了解决“API 成功和夹具格式通过不能证明模型回答正确”。用 Python、JSONL、rubric/release gate 做了Baseline—Golden Set—Eval—错误归因—回归—发布门槛的离线模板和校验器。最难的是明确区分 fixture schema PASS 与 MODEL_QUALITY=NOT_RUN。目前证据是README 的 full selector 校验 5 个 synthetic_unverified 案例及单元测试。但没有接入生产模型，也没有人审业务标准答案；如果真实落地，下一步是接入 provider/trace，建立独立人审 Golden Set 和高风险回归门槛。

## 3 分钟

先演示核心路径：Baseline—Golden Set—Eval—错误归因—回归—发布门槛的离线模板和校验器。再打开仓库中的测试与案例页，解释为什么把状态/证据留在可检查的位置。重点讲一个取舍：明确区分 fixture schema PASS 与 MODEL_QUALITY=NOT_RUN。最后明确验证范围：README 的 full selector 校验 5 个 synthetic_unverified 案例及单元测试；本仓库演示评测流程，但不产出被测模型质量分数。不把演示、合成样本和生产效果混为一谈。

## 10 分钟技术深挖

1. 展示 README 的 Quick Start 与架构图/目录。
2. 从一个输入走到状态变化或输出，指出 Baseline—Golden Set—Eval—错误归因—回归—发布门槛的离线模板和校验器 对应的源代码。
3. 现场说明最难问题：明确区分 fixture schema PASS 与 MODEL_QUALITY=NOT_RUN；对照测试或复现步骤。
4. 解释失败路径及限制：没有接入生产模型，也没有人审业务标准答案。
5. 用 接入 provider/trace，建立独立人审 Golden Set 和高风险回归门槛 说明真正上线的优先级和验收证据。

## 九个常见追问

1. **为什么这样设计架构？** 为了把 Baseline—Golden Set—Eval—错误归因—回归—发布门槛的离线模板和校验器 的核心规则与展示/外部依赖分开，便于检查失败边界。
2. **最难的 bug/取舍？** 明确区分 fixture schema PASS 与 MODEL_QUALITY=NOT_RUN；请指向对应测试或演示复现，避免编造线上事故。
3. **用了什么框架？** Python、JSONL、rubric/release gate。选型服务于静态或离线演示，不等同生产选型结论。
4. **上线还差什么？** 接入 provider/trace，建立独立人审 Golden Set 和高风险回归门槛。
5. **如何防止误用？** 没有接入生产模型，也没有人审业务标准答案；任何不可逆外部动作需人工确认。
6. **怎么测试？** README 的 full selector 校验 5 个 synthetic_unverified 案例及单元测试。先跑 README 命令，再看具体断言，不把 200 或编译当成产品验收。
7. **AI 在哪里？** 本仓库演示评测流程，但不产出被测模型质量分数。不要把确定性规则、提示词或可选模型接口说成已验证的 AI 效果。
8. **哪些是 Mock？** 没有接入生产模型，也没有人审业务标准答案。
9. **模型怎么评测？个人贡献是什么？** 本仓库演示评测流程，但不产出被测模型质量分数。我负责公开仓库里可见的实现、测试和说明；未核验的业务结果与第三方工作不纳入我的贡献。
