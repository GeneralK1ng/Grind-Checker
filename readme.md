# GitHub 内卷检测脚本

一个简单的 Python 脚本，用于分析 GitHub 用户的公开活动，检测是否存在“内卷”行为 —— 即在非正常工作时间、深夜或周末仍然活跃编码或贡献。

灵感来自于 [RimoChan/Pepin](https://github.com/RimoChan/Pepin) 仓库，但由于该项目使用的接口容易被墙，访问不稳定且存在一些小问题，所以对其进行了改进和优化。

## 功能特点

- 通过 GitHub API 获取指定用户的公开事件。
- 自动检测并使用当前电脑系统的本地时区，时间更准确。
- 统计一天中各小时的活跃情况。
- 统计工作时间外、午夜和周末的活动数量。
- 计算“内卷分数”，量化非工作时间的活跃强度。
- 输出清晰的文字报告，包括小时和日期的活跃分布。
- 支持同时分析多个用户。

## 依赖要求

- Python 3.7 及以上版本
- requests 库

非常推荐使用uv来创建虚拟环境

```bash
uv venv --python 3.12 .venv 
```
然后安装依赖

```bash
uv pip install -r requirements.txt
```
## 使用方法

1. 下载或克隆本仓库 `github_grind_checker.py`。
2. 在脚本中将 `github_token` 变量替换为你的 GitHub 个人访问令牌（token）。
    访问地址：https://github.com/settings/tokens （仅需读取公共数据权限，也就是什么都不用选）。
3. 修改脚本中 `usernames` 列表，添加你想监控的 GitHub 用户名。
4. 运行脚本：

```bash
python github_grind_checker.py
```

## 配置说明

- `usernames`：需要分析的 GitHub 用户列表。
- `work_start_hour`，`work_end_hour`：定义正常工作时间段（24小时制）。
- `lookback_days`：向前回溯分析的天数。

## 示例输出

```bash
--------------------------------------------------
👤 User: GeneralK1ng
📊 Total events: 49 | Off-hour events: 30
📅 Active days: 9 | Midnight events: 4 | Weekend events: 21
🔥 Grind Score: 3.51
🔧 Event type breakdown:
  PushEvent: 15
  ForkEvent: 9
  WatchEvent: 13
  IssueCommentEvent: 5
  IssuesEvent: 2
  PullRequestEvent: 2
  CreateEvent: 1
  PullRequestReviewCommentEvent: 1
  PullRequestReviewEvent: 1

⏰ Hourly activity (local time):
00:00 |  (0)
01:00 |  (0)
02:00 |  (0)
03:00 | ▇▇▇▇▇▇ (3)
04:00 |  (0)
05:00 | ▇▇ (1)
06:00 | ▇▇ (1)
07:00 |  (0)
08:00 |  (0)
09:00 |  (0)
10:00 |  (0)
11:00 | ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ (7)
12:00 |  (0)
13:00 | ▇▇▇▇▇▇▇▇▇▇▇ (5)
14:00 | ▇▇ (1)
15:00 | ▇▇▇▇▇▇▇▇ (4)
16:00 | ▇▇▇▇ (2)
17:00 |  (0)
18:00 | ▇▇▇▇▇▇▇▇ (4)
19:00 |  (0)
20:00 |  (0)
21:00 | ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ (9)
22:00 | ▇▇▇▇▇▇▇▇ (4)
23:00 | ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ (8)

📆 Daily activity breakdown:
 2025-06-07: 21h(8) 22h(2) 
 2025-06-08: 11h(1) 13h(1) 14h(1) 18h(1) 
 2025-06-09: 11h(1) 23h(5) 
 2025-06-10: 03h(3) 11h(1) 13h(4) 18h(2) 
 2025-06-11: 05h(1) 06h(1) 
 2025-06-12: 11h(1) 21h(1) 22h(1) 23h(1) 
 2025-06-13: 11h(1) 15h(2) 16h(2) 23h(1) 
 2025-06-14: 11h(1) 15h(2) 18h(1) 22h(1) 23h(1) 
 2025-06-15: 11h(1) 

==================================================
🏆 Grind Score Ranking:
GeneralK1ng          Grind Score: 3.51 | Off-hour: 30/49
```

------

欢迎反馈问题或提出改进建议！

------

