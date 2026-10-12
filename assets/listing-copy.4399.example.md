# 4399 listing copy / 4399 上架文案模板

Fill each placeholder from the current game and form; this template is not a completed listing. Read [4399 guidance](../references/4399.md) / [4399 说明](../references/zh-CN/4399.md). Retain platform copy limits and per-role media rules in [the shared registry](material-rules.json).

按当前游戏与表单填写，不直接交付占位符。游戏建议尺寸逐游戏确定，不套用某一游戏的竖屏默认值；物料检查不验证游戏自适应。

## Copy / 文案

```text
Game name / 游戏名称：<current name>
Description / 游戏介绍：<truthful description within the current field limit>
Controls / 操作说明：<actual player controls within the current field limit>
```

## Recommended backend game resolution / 后台游戏推荐分辨率

```text
Game width / 游戏宽：<positive pixel width>
Game height / 游戏高：<positive pixel height>
Orientation / 游戏方向：<landscape 横屏 / portrait 竖屏>
Layout basis and current form check / 布局依据及当前表单核对：<actual basis, source/date>
Responsive test / 自适应验证：<tested viewport and result, or pending>
```

## Media specifications and actual results / 宣传物料规格及实际结果

Copy the current constraints for each role from the shared registry; record actual dimensions, byte count, SHA-256 and validation result. The video-cover K-to-byte conversion is conservative; other images keep their independently verified or unknown limits. Media sizes do not determine game resolution.

从机器表逐角色填入当前规格，并记录实际宽高、字节数、SHA-256 与结果。视频封面 K 转字节为保守换算，其他图片上限独立核实或保留未知；宣传物料尺寸不决定游戏分辨率。

| Role / 用途 | File / 文件 | Current dimensions and byte limit / 当前尺寸及字节限制 | Actual dimensions, bytes, SHA-256 / 实际尺寸、字节及哈希 | Check / 检查 |
| --- | --- | --- | --- | --- |
| icon / 图标 | <path> | <role rules> | <measurements> | <pass/fail/pending> |
| promo / 宣传图 | <path> | <role rules> | <measurements> | <pass/fail/pending> |
| video_cover / 视频封面 | <path or pending> | <role rules and conservative conversion basis> | <measurements> | <pass/fail/pending> |
| video / 视频 | <path or not selected> | <verified limits or unknown; working recommendations separate> | <measurements> | <pass/fail/deferred/pending> |
| detail / 详情图 | <paths or not selected> | <verified limits or unknown> | <measurements> | <pass/fail/pending> |

## Game package and platform state / 游戏包与平台状态

```text
Candidate / 候选包：<version, path, bytes, SHA-256>
Local static checks / 本地静态检查：<result and report>
Owner upload report / Owner 上传反馈：<reported state and source; independently verified or not>
Exact uploaded artifact / 实际上传制品：<uploaded version and SHA-256, or unknown; do not reuse the local candidate identity>
Platform result / 平台结果：<actual receipt, rejected, pending, or unknown>
Specific rejection reason / 具体拒绝原因：<actual message or unknown; do not infer>
Owner-handled replacement / Owner 自行修正：<not applicable / pending receipt and recheck / verified result>
```

Identical-byte renaming does not resolve rejection. Keep corrected files pending until received and rechecked; local pass is not platform acceptance. / 内容相同的改名不证明修复；未取得修正文件并复查前保持待验，本地通过不代表平台通过。
