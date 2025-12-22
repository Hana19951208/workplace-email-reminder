# 📧 上下班打卡邮件提醒

> 使用 GitHub Actions 自动在工作日发送上下班打卡提醒邮件

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ 功能特点

- 🕗 **定时发送**：每周一至周五自动发送
  - 早上 8:20 - 上班打卡提醒
  - 下午 5:30 - 下班打卡提醒
- 🎨 **精美模板**：使用现代化的 HTML 邮件模板
- 🔐 **安全存储**：使用 GitHub Secrets 存储敏感信息
- 🧪 **手动测试**：支持手动触发工作流进行测试

## 🚀 快速开始

### 1. Fork 或 Clone 仓库

```bash
git clone https://github.com/Hana19951208/workplace-email-reminder.git
cd workplace-email-reminder
```

### 2. 配置 Gmail 应用专用密码

> ⚠️ **重要**：Gmail 不允许直接使用账户密码进行 SMTP 登录，需要创建**应用专用密码**。

1. 访问 [Google 账户安全设置](https://myaccount.google.com/security)
2. 确保已开启 **两步验证**
3. 在"两步验证"页面底部，点击 **应用专用密码**
4. 选择"邮件"和"其他"，输入名称如 "GitHub Actions"
5. 点击生成，**复制生成的 16 位密码**

### 3. 配置 GitHub Secrets

在你的 GitHub 仓库中：

1. 进入 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**，添加以下三个 Secret：

| Secret 名称 | 值 |
|------------|-----|
| `SENDER_EMAIL` | `wfe19951208@gmail.com` |
| `SENDER_PASSWORD` | `你的应用专用密码` |
| `RECEIVER_EMAIL` | `1948978861@qq.com` |

### 4. 推送代码到 GitHub

```bash
git add .
git commit -m "feat: 初始化上下班打卡邮件提醒项目"
git push origin main
```

### 5. 测试工作流

1. 进入仓库的 **Actions** 页面
2. 选择 **定时上下班邮件提醒** 工作流
3. 点击 **Run workflow**
4. 选择邮件类型（morning/evening）进行测试

## 📁 项目结构

```
workplace-email-reminder/
├── .github/
│   └── workflows/
│       └── send-email.yml    # GitHub Actions 工作流
├── .env.example              # 本地环境配置文件模板
├── .gitignore                # Git 忽略配置
├── README.md                 # 项目说明文档
├── requirements.txt          # Python 依赖
├── send_email.py             # 核心邮件发送逻辑
└── test_email.py             # ✅ 本地验证脚本
```

## 🧪 本地验证

在将代码推送到 GitHub 之前，你可以在本地进行测试：

1. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   ```

2. **配置本地环境**：
   复制模板并填写你的配置信息（`.env` 文件已被 git 忽略，不会被提交）：
   ```bash
   cp .env.example .env
   ```
   编辑 `.env` 文件，填入你的邮箱 and **应用专用密码**。

3. **运行测试**：
   ```bash
   python test_email.py
   ```

---

## ⏰ 定时规则说明

本项目采用了 **“高频检测 + 脚本判断”** 的方案，以解决 GitHub Actions 原生 Cron 触发延迟严重的问题：

1. **触发频率**：GitHub Actions 设定为每 5 分钟运行一次。
2. **逻辑判断**：
   - 脚本会自动获取北京时间。
   - 判断当前是否处于 **08:20 - 08:25**（早安提醒）或 **17:30 - 17:35**（下班提醒）。
   - 只有在上述窗口期内，脚本才会执行发送动作，其余时间将自动跳过。

这种方式确保了即使 GitHub 调度器延迟了 1-3 分钟，你依然能准时收到邮件。

## 🎨 邮件效果预览

### 早安打卡提醒 ☀️
精美的渐变背景，配合温馨的问候语，让你每天都充满元气！

### 下班打卡提醒 🌙
舒缓的紫色调，提醒你收拾好心情，准备回家休息～

## 🔧 自定义配置

### 修改发送时间

编辑 `.github/workflows/send-email.yml` 中的 cron 表达式：

```yaml
on:
  schedule:
    - cron: '分钟 小时 * * 1-5'  # UTC 时间
```

### 修改邮件内容

编辑 `send_email.py` 中的 `get_email_content` 函数，自定义邮件模板。

## ❓ 常见问题

### Q: 邮件发送失败，提示认证错误？
A: 请确保使用的是 Gmail **应用专用密码**，而非账户密码。

### Q: 工作流没有按时运行？
A: GitHub Actions 的定时任务可能会有几分钟的延迟，这是正常现象。

### Q: 如何停止定时发送？
A: 在 Actions 页面禁用该工作流，或删除 cron 触发器。

## 📄 License

MIT License © 2024

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！
