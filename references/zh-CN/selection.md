# 来源、平台和功能选择

共用选项来自 `assets/capabilities.json`。选择表示本轮工作范围，不证明 SDK 支持或获得发布授权。在游戏已有交付目录保存 `channel-selection.json`，真实项目答案、账号信息不得进入此 Skill 仓库。

1. 检查真实源码目录、可运行入口／构建、Git 改动和已有 SDK。来源单选 `generic_h5`（普通 H5）、`taptap_h5`、`other_platform_h5`（已有其他平台 H5）。用户明确选定的其他平台版本可以作为来源，先固定基线再复制。Maker/UrhoX Lua 不是 H5，转换须另立范围。
2. 目标多选：TapTap H5、233、4399、小红书小工具、B 站 TOY、网易星匣。TapTap → TapTap 是该渠道增量维护，保留 namespace、ID、资源与旧包；不覆盖来源或重复建应用。
3. **逐个已选平台**选择功能：广告、身份、本地／云存档、排行榜、成就、礼包／兑换码、分享、振动、诊断反馈、多人联机、游戏内评价入口。展示该平台的已知能力与缺口。目录列的是可提出的需求，不承诺每个平台都支持所有项目。未验证与不支持的需求如实保留，不伪造实现。明确“无”可保存为空列表，缺回答不能视为“无”。
4. 离线收益、签到、音乐、音效、字号／性能设置另列为游戏逻辑；每个平台另选物料范围。它们不等于平台 API。未选择新增工作不意味着删除已有机制；未选物料视频不能删游戏音乐。
5. 可用工具支持真正多选时优先使用。当前建议答案弹窗为单选，改用编号列表让用户回复多个编号，再展示来源、目标、各平台功能及物料的简短汇总，取得明确确认。不得把单选伪称复选框。已明确且无歧义的范围直接沿用，不重复询问；默认和超时不是答案，缺必需选择时只读盘点。

文字示例：`目标：1 TapTap、2 233、3 4399、4 小红书、5 TOY、6 星匣。可回复多个编号；随后分别选择各平台功能，不新增接入请明确答“无”。` 最终汇总前说明未验证能力。

## 保存与恢复

答案结构和跨系统命令见[英文说明](../selection.md#persist-and-resume)，字段名与 JSON 共用，不维护第二份格式。`confirmed: true` 只能记录已收到的真实答案，示例不是授权。`source.inspection` 记录已核对入口、构建与接入的证据；脚本本身不验证源码目录内容。

```sh
python3 <skill-dir>/scripts/selection.py create <answers.json> --output <delivery-dir>/channel-selection.json
python3 <skill-dir>/scripts/selection.py validate <delivery-dir>/channel-selection.json
python3 <skill-dir>/scripts/selection.py plan <delivery-dir>/channel-selection.json
```

Windows 使用 `py -3` 或已核实 Python 路径。脚本只校验、保存范围，不建立游戏目录、不修改接入、不操作平台。拒绝缺项、重复或未知选项、未选功能启用，以及覆盖旧选择文件。后续目录、物料、SDK、出包均以 `plan` 输出为范围，只包含已选平台和功能。

| 状态 | 含义与下一步 |
| --- | --- |
| `not_selected` | 不做新增接入，保护已有游戏行为。 |
| `pending_verification` | 已选，接入前核对当前 H5 接口、配置与依赖。 |
| `unsupported` | 当前证据确认该产品／路线不可用；列缺口，不实现。 |
| `configured` | 已记录配置与实现证据；宿主、真机、发布仍需分别验证。 |

在同一文件更新所选功能的状态与 `evidence`，恢复前运行 `validate`。`configured` 和 `unsupported` 必须有带日期的依据或本地证据入口；H5 支持未知应为待核实，不能直接判不支持。`plan.next` 区分核实、报告缺口与验证配置。功能依赖不得隐式全选：说明缺少的依赖范围，沿用已有授权接入或询问缺项。单个远端功能待定不阻塞其他本地工作。
