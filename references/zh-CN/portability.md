# macOS 与 Windows 兼容

两个系统共用同一 Skill、规则和 Python 工具。路径来自使用者当前项目/Skill，不依赖作者 home、/tmp、Homebrew 或 Mac shell。

## 检查环境

- 先识别 OS/shell。Mac 查 python3；Windows PowerShell 用 `Get-Command python, py -ErrorAction SilentlyContinue`，再用 `python --version` 或 `py -3 --version` 核对解释器。Windows Store 别名不代表已装 Python。
- 辅助工具需 Python ≥3.9，仅标准库；图文与包体检查不需要 FFmpeg。盘点默认读取 PNG/JPEG/WebP 文件头，不探测音视频，--no-probe 进一步关闭图片元数据。只有选择音视频处理时才查 ffprobe/ffmpeg：--probe-av 开启盘点中的音视频检查，processing.video: true 开启物料视频检查；剪辑和完整视频测试再使用 ffmpeg。
- 仅所选工作确有需要时检查/安装媒体工具，优先已有/内置环境。缺失时按用户认可的包管理器或官方对应 OS/架构版本安装；Windows 不运行 brew 或 Unix curl-pipe-shell。平台 CLI 可能提供独立 exe/PowerShell 安装方式，以当前上游为准。
- 空格/中文路径必须引用；用 pathlib、参数数组，不拼 shell、不依赖 Unix 复制命令或符号链接。文本和进程 JSON 显式 UTF-8；Windows 产物名称避开保留字符和设备名。

## Windows PowerShell 示例

下面替换真实路径；若核实可用解释器是 python，就以 python 替换 py -3：

```powershell
py -3 "C:\Tools\h5-channel-adapter\scripts\inventory_project.py" "D:\Games\My Game" --output "D:\Evidence\inventory.json"
py -3 "C:\Tools\h5-channel-adapter\scripts\verify_materials.py" "D:\Materials\manifest.json" --report "D:\Evidence\materials-check.json"
py -3 "C:\Tools\h5-channel-adapter\scripts\verify_game_package.py" "D:\Builds\game-4399.zip" --channel 4399 --expected-public-id "<public-AppID>" --report "D:\Evidence\package-preflight.json"
```

Mac 使用 python3 和对应路径，完整示例见 [English](../portability.md)。manifest 内可用相对路径与 /；输出必须在 manifest 目录树内。Windows 反斜线由 JSON 序列化处理，不手工拼未转义 JSON。工具拒绝覆盖旧报告，使用新的证据文件名。

## 构建与验证

保留游戏原技术栈/锁文件，需要时才查 Node/npm。不能假定 Mac 专用开发工具在 Windows 存在；平台工具限制与本地可完成的工作分开报告。

使用可用的隔离浏览器或已授权宿主预览；不强依赖某桌面弹窗 API、浏览器驱动或原生自动化。能力缺失时退回文本选项并记录验证缺口。

`python3 tests/no_ffmpeg.py` 检查无媒体工具的图文路径，测试会清空子进程中的媒体工具 PATH；需要完整视频测试时才运行 `python3 tests/smoke.py` 并配置 FFmpeg。Windows 换成 py -3 或实际解释器。CI 模板包含两组检查，工具测试不能代替宿主或设备测试。
