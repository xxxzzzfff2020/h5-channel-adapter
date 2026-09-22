# macOS 与 Windows 兼容

两个系统共用同一 Skill、规则和 Python 工具。路径来自使用者当前项目/Skill，不依赖作者 home、/tmp、Homebrew 或 Mac shell。

## 检查环境

- 先识别 OS/shell。Mac 查 python3/ffprobe/ffmpeg；Windows PowerShell 用 `Get-Command python, py, ffprobe, ffmpeg -ErrorAction SilentlyContinue`，再用 `python --version` 或 `py -3 --version` 核对解释器。Windows Store 别名不代表已装 Python。
- 两个 helper 需 Python ≥3.9，仅标准库；物料验证需 ffprobe 在 PATH。盘点可用 --no-probe，但不能据此称媒体通过。视频制作与合成夹具测试还需 ffmpeg。
- 优先已有/内置环境。缺失时按用户认可的包管理器或官方对应 OS/架构版本安装；Windows 不运行 brew 或 Unix curl-pipe-shell。平台 CLI 可能提供独立 exe/PowerShell 安装方式，以当前上游为准。
- 空格/中文路径必须引用；用 pathlib、参数数组，不拼 shell、不依赖 Unix 复制命令或符号链接。文本和进程 JSON 显式 UTF-8；Windows 产物名称避开保留字符和设备名。

## Windows PowerShell 示例

下面替换真实路径；若核实可用解释器是 python，就以 python 替换 py -3：

```powershell
py -3 "C:\Tools\h5-channel-adapter\scripts\inventory_project.py" "D:\Games\My Game" --output "D:\Evidence\inventory.json"
py -3 "C:\Tools\h5-channel-adapter\scripts\verify_materials.py" "D:\Materials\manifest.json" --report "D:\Evidence\materials-check.json"
```

Mac 使用 python3 和对应路径，完整示例见 [English](../portability.md)。manifest 内可用相对路径与 /；输出必须在 manifest 目录树内。Windows 反斜线由 JSON 序列化处理，不手工拼未转义 JSON。工具拒绝覆盖旧报告，使用新的证据文件名。

## 构建与验证

保留游戏原技术栈/锁文件，需要时才查 Node/npm。不能假定 Mac 专用开发工具在 Windows 存在；平台工具限制与本地可完成的工作分开报告。

使用可用的隔离浏览器或已授权宿主预览；不强依赖某桌面弹窗 API、浏览器驱动或原生自动化。能力缺失时退回文本选项并记录验证缺口。

仓库 CI 模板启用后以合成媒体在 macOS/Windows 执行 helper 测试，包含空格/中文路径；它只证明工具兼容，不代表 Windows 游戏构建、手机或平台 SDK 验收。
