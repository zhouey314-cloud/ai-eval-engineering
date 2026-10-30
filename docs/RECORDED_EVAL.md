# 对已记录的回答和工具轨迹执行机械评测

现在除了验证数据集格式，也可以输入响应记录，执行字面约束、工具允许/禁止清单、拒答理由、人工门禁、升级与决策标志的检查，并比较两个版本。

```sh
python runners/evaluate.py --cases evals/golden_set.example.jsonl evals/regression_set.example.jsonl evals/high_risk_set.example.jsonl --responses examples/recorded-responses.jsonl --output output/baseline.json
# 换成候选版本的响应文件，再加：
# --baseline output/baseline.json
```

响应 JSONL 必须提供 case_id、text、tools_called（字符串数组），并按各 case 的 expected 提供 escalated、decision_performed、human_review_requested 或 refusal_reason。布尔值不能用字符串代替。缺失响应/轨迹、未支持的规则会 BLOCKED；重复/未知 ID、删除 baseline case 或无效契约会非零退出。禁止工具或字面条件不符会 FAIL。每个报告保存输入文件哈希、Python 版本、case 失败原因及 improved/regressed/unchanged/new。

退出码：0=机械契约通过，1=失败/回归，2=缺少依赖证据或输入契约无效。原始轨迹由接入方负责完整记录；手写 tools_called 并不能证明真实系统没有执行其他动作。

这些公开响应是手写 synthetic_unverified 示例，不是模型调用结果。字面匹配不判断语义、引用支撑或文本中的否定；拒答/升级标志也不证明真实业务动作。报告始终单列 MODEL_QUALITY/semantic_correctness=NOT_EVALUATED 和 production_acceptance=BLOCKED。需要语义质量时，接入真实记录、业务事实、经确认的金标和独立人工审阅，不能用这 5 个机械示例代替。

12 条测试覆盖原格式校验，以及规则执行、工具违规、遗漏、重复、未知规则、错误类型、人工门禁与跨版本回归。
