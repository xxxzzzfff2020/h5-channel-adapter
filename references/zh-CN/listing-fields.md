# 上架字段与 manifest 映射

上架要求记录于2026-09-22，来源为创作者后台表单。五平台物料机器规则共用 `assets/material-rules.json`，游戏上传体积另放 `assets/package-rules.json`；快照不是永久接口规范，执行时仍复核官方工具和最新表单。

| channel | text | metadata | files[].role |
| --- | --- | --- | --- |
| xiaohongshu | name、description、version 必填 | scene、permissions 必填 | icon 一个 |
| bilibili-toy | name、slug 必填 | 目前未记录其他项 | poster、icon 各一个 |
| xingxia | name、description 必填；about、controls 选填 | categories 1–2、tags 1–5；game_type/orientation 选填 | cover 一个；promo_media 图片/视频合计0–8个 |

assets 下的示例默认 `processing.video: false`；明确选择视频后才改为 true 并补视频/封面条目，报告含义见[物料范围](materials.md#范围与可选视频)。示例用于说明结构，需填当前游戏的真实文案、路径、标签与素材来源。移植现有 H5 使用适用的已有游戏上传入口；工坊管理是另一条发布路线。

小红书名称/简介各≤14，版本号格式未给，不猜 SemVer。场景标签按共用规则中的七类。permissions 的 album/camera/microphone/storage 是适配器内部标签，不是已确认的 SDK 权限名：只选实际使用能力，按当前官方流程映射，核实后台是否要求显式“无权限”，不能默认全部申请。

B 站封面4:3、图标1:1按表单比例检查，1200×900、500×500仅推荐导出尺寸。图片字节上限和名称字数未给；目前未记录简介/视频字段，不额外编必填项。已有 slug 保持原值。

星匣封面为 JPG/PNG、≤5 MB；800×450为推荐。选填宣传图/视频**合计**最多8个，不是各8个；图片 JPG/PNG/WebP ≤5 MB，视频 MP4/WebM/OGG ≤100 MB、≤60秒；1024×556为推荐比例。此表单不强制视频，也不强制宣传+实录拼接；纯音频 OGG 不能算视频。

硬尺寸/比例不合格才失败，推荐值偏差给提示。新字段按UTF-16单位保守计数（部分emoji计2），最终以后端计数器为准；选填缺失保持可选，数组拒绝重复项。文案来自当前游戏真实资料，不能虚构玩法/云档/广告等承诺。

输出均保留源路径/哈希；实机截图/录像注明版本，视频给 source_seconds/output_seconds。promo_media 可用真实宣传画或运行画面，插画不能标实机。233/4399合成视频规则只在相应平台选择视频处理时执行；未选时记录待补。

技术通过仅覆盖已编码规则；未知字段、权限、视觉、平台与真机仍分别记录。

Examples / 示例：[xiaohongshu](../../assets/material-manifest.xiaohongshu.example.json) · [bilibili-toy](../../assets/material-manifest.bilibili-toy.example.json) · [xingxia](../../assets/material-manifest.xingxia.example.json)
