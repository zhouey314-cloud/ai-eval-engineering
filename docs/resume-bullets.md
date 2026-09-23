# AI 评测工程 Starter Kit — 中文简历项目要点

仅描述公开仓库内可核查的自建演示；按岗位挑选，勿三版叠加。证据与边界以 README、测试和 [case study](case-study.md) 为准。

## AI Engineer / FDE

- 围绕“API 成功和夹具格式通过不能证明模型回答正确”，用 Python、JSONL、rubric/release gate 实现Baseline—Golden Set—Eval—错误归因—回归—发布门槛的离线模板和校验器。
- 验证：README 的 full selector 校验 5 个 synthetic_unverified 案例及单元测试；本仓库演示评测流程，但不产出被测模型质量分数。
- 明确边界：没有接入生产模型，也没有人审业务标准答案。

## AI Product / Solution

- 将“API 成功和夹具格式通过不能证明模型回答正确”拆成可点击的用户流程，交付Baseline—Golden Set—Eval—错误归因—回归—发布门槛的离线模板和校验器。
- 用可运行 Demo、测试和案例页说明实现与限制；README 的 full selector 校验 5 个 synthetic_unverified 案例及单元测试。
- 为客户化落地列出前置条件：接入 provider/trace，建立独立人审 Golden Set 和高风险回归门槛。

## 实习 / 校招

- 独立完成AI 评测工程 Starter Kit的公开演示、代码、测试和文档，技术栈为 Python、JSONL、rubric/release gate。
- 解决“明确区分 fixture schema PASS 与 MODEL_QUALITY=NOT_RUN”，保留可复核的验证：README 的 full selector 校验 5 个 synthetic_unverified 案例及单元测试。
- 不把演示包装成上线业务：没有接入生产模型，也没有人审业务标准答案。
