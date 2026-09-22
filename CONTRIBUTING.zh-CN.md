# 贡献指南

[English](CONTRIBUTING.md) · [返回 Skill 首页](README.zh-CN.md)

欢迎一起降低 H5 游戏多平台发布的重复工作。你可以补充平台、更新上架要求、改进通用接入方式、修复工具兼容问题，或完善使用示例。

仓库目前私有，受邀协作者可以参与；正式公开前会确定开源许可证并开放贡献入口。

## 从具体问题开始

提交 Issue 时，说明平台、希望完成的任务，以及当前缺失或不正确的行为。修改平台要求时，请附当前官方文档链接，或脱敏后的后台字段与日期。报告故障时，提供最小复现、操作系统和相关工具版本。

新增平台或较大依赖适合先讨论；小修复可以直接提交 Pull Request。

## 修改放在哪里

| 修改内容 | 位置 |
| --- | --- |
| Agent 定位与执行入口 | `SKILL.md` |
| 平台和流程说明 | `references/` 与 `references/zh-CN/` |
| 共用物料与包体限制 | `assets/material-rules.json`、`assets/package-rules.json` |
| 官方工具来源 | `assets/platform-sources.json` |
| 可复用命令 | `scripts/` |
| 工具行为测试 | `tests/` |

新增平台按[扩展说明](references/zh-CN/extending.md)进行。官方 Skill、CLI、MCP 保持为独立上游依赖，在这里贡献对接方式，不放修改过的官方 Skill 副本。

## 保持通用性

- 中英文一起更新；数值规则维护在共用 JSON 中，避免在代码里另存一份。
- 区分平台硬限制、推荐值与项目偏好；未知上限明确留空。
- 示例使用通用内容。不要提交游戏源码、商业素材、私有对话、账号 ID 或凭证。
- 路径和命令兼顾 macOS、Windows；单个游戏的选择放回游戏自身配置。
- 保留原游戏、已有存档和旧包；删减功能前沿用用户明确选择的方案。

## 检查修改

文档修改检查链接和对应翻译。涉及脚本或可执行规则时，在 Python 3.9+、`ffmpeg`、`ffprobe` 可用的环境运行：

```sh
python3 tests/smoke.py
```

Windows PowerShell 使用 `py -3 tests/smoke.py` 或已核实的 `python`。测试会生成临时合成素材。行为变化时补充相关用例，不为匹配文档措辞新增测试。

[CI 模板](ci/validate.github.yml)可由维护者启用到 `.github/workflows/validate.yml`，在 macOS 和 Windows 上执行相同检查。

## 提交 Pull Request

说明使用者遇到的问题、修改结果和检查方式。平台要求变化附官方来源；需要真实宿主或设备继续确认的部分写清楚。影响使用方式时更新 `CHANGELOG.md`，版本号由维护者统一发布。

复现问题请使用最小合成素材或脱敏示例，无需上传完整私人游戏。
