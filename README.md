# 📧 上下班打卡邮件提醒

> 使用 GitHub Actions 自动在工作日发送上下班打卡提醒邮件

![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ 功能特点

- 🕗 **定时发送**：每天自动运行，通过逻辑判断工作日
  - 早上 08:15 (北京时间) - 上班打卡提醒
  - 下午 17:35 (北京时间) - 下班打卡提醒
- 🏖️ **节假日识别**：自动跳过法定节假日，智能识别调休补班日
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
git commit -m "feat: 采用抢占式精准提醒方案"
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

## ⏰ 定时规则说明 (抢占式精准方案)

本项目采用了 **“提前抢占资源 + 进程内精准休眠”** 的方案，彻底规避了 GitHub Actions 的调度延迟问题：

1. **提前启动**：
   - 早上：于北京时间 **07:45** 启动（避开 08:00 的全球调度高峰）。
   - 下午：于北京时间 **17:00** 启动。
2. **精准倒计时**：
   - 脚本启动后，会计算与目标时间（早上 **08:15**，下午 **17:35**）的差值。
   - 使用 `time.sleep()` 在进程内进行阻塞式等待。
3. **秒级触发**：
   - 由于此时虚拟机已经分配并处于运行状态，到了目标时间会立即执行发送逻辑，不受 GitHub 队列影响。
4. **智能过滤**：
   - 脚本集成 `chinesecalendar`，启动后会先判断当天是否为大陆法定工作日。
   - 如果是周末但需要调休补班，邮件照常发送。
   - 如果是周一至周五但属于法定节假日，脚本自动休眠退出，不骚扰假期。

这种设计的优势在于：**极速启动，准时送达**。即使 GitHub Actions 的排队延迟长达 15 分钟，只要脚本在 08:15 前启动，您收到的邮件时间永远保持精准。

## 🎨 邮件效果预览

### 早安打卡提醒 ☀️
精美的渐变背景，配合温馨的问候语，让你每天都充满元气！

### 下班打卡提醒 🌙
舒缓的紫色调，提醒你收拾好心情，准备回家休息～

## 🔧 自定义配置

### 修改发送时间

1. 编辑 `.github/workflows/send-email.yml` 中的 cron 表达式，设置提前启动时间。
2. 编辑 `send_email.py` 中的 `auto_check_and_send` 函数，修改目标发送时刻。

### 修改邮件内容

编辑 `send_email.py` 中的 `get_email_content` 函数，自定义邮件模板。

## ❓ 常见问题

### Q: 邮件发送失败，提示认证错误？
A: 请确保使用的是 Gmail **应用专用密码**，而非账户密码。

### Q: 工作流没有按时运行？
A: 虽然 GitHub 有延迟，但通过目前的抢占式方案，只要在目标时间前启动了脚本，就能保证准时发送。

### Q: 如何停止定时发送？
A: 在 Actions 页面禁用该工作流，或删除 cron 触发器。

## 📄 License

MIT License © 2024

---

⭐ 如果这个项目对你有帮助，请给个 Star 支持一下！
