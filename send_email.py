#!/usr/bin/env python3
"""
上下班邮件提醒脚本
使用 Gmail SMTP 服务器发送邮件
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz


def get_email_content(email_type: str) -> tuple[str, str]:
    """
    根据邮件类型获取邮件主题和内容
    
    Args:
        email_type: 邮件类型，'morning' 或 'evening'
    
    Returns:
        (subject, body) 元组
    """
    # 获取北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)
    date_str = now.strftime('%Y年%m月%d日 %A')
    time_str = now.strftime('%H:%M')
    
    # 星期几的中文映射
    weekday_map = {
        'Monday': '星期一',
        'Tuesday': '星期二',
        'Wednesday': '星期三',
        'Thursday': '星期四',
        'Friday': '星期五',
        'Saturday': '星期六',
        'Sunday': '星期日'
    }
    weekday_cn = weekday_map.get(now.strftime('%A'), now.strftime('%A'))
    date_str_cn = now.strftime(f'%Y年%m月%d日 {weekday_cn}')
    
    if email_type == 'morning':
        subject = f"☀️ 早安打卡提醒 - {date_str_cn}"
        body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px;">
    <div style="max-width: 500px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 40px 30px; text-align: center;">
            <div style="font-size: 60px; margin-bottom: 10px;">🌅</div>
            <h1 style="color: white; margin: 0; font-size: 28px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">早安打卡提醒</h1>
        </div>
        <div style="padding: 40px 30px;">
            <p style="color: #333; font-size: 18px; line-height: 1.8; margin: 0 0 20px 0;">
                亲爱的小伙伴，新的一天开始啦！ 🎉
            </p>
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); border-radius: 15px; padding: 25px; margin: 20px 0;">
                <p style="color: #555; font-size: 16px; margin: 0;">
                    📅 <strong>{date_str_cn}</strong><br>
                    ⏰ 现在时间：<strong>{time_str}</strong>
                </p>
            </div>
            <p style="color: #666; font-size: 16px; line-height: 1.8;">
                ⏰ 请记得<strong style="color: #f5576c;">上班打卡</strong>哦！<br><br>
                💪 愿你今天工作顺利，心情愉快！<br>
                ☕ 先来杯咖啡开启元气满满的一天吧！
            </p>
        </div>
        <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #999; font-size: 12px; margin: 0;">
                🤖 此邮件由 GitHub Actions 自动发送
            </p>
        </div>
    </div>
</body>
</html>
"""
    else:
        subject = f"🌙 下班打卡提醒 - {date_str_cn}"
        body = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); margin: 0; padding: 20px;">
    <div style="max-width: 500px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
            <div style="font-size: 60px; margin-bottom: 10px;">🌙</div>
            <h1 style="color: white; margin: 0; font-size: 28px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">下班打卡提醒</h1>
        </div>
        <div style="padding: 40px 30px;">
            <p style="color: #333; font-size: 18px; line-height: 1.8; margin: 0 0 20px 0;">
                辛苦了一天，终于到下班时间啦！ 🎊
            </p>
            <div style="background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); border-radius: 15px; padding: 25px; margin: 20px 0;">
                <p style="color: #555; font-size: 16px; margin: 0;">
                    📅 <strong>{date_str_cn}</strong><br>
                    ⏰ 现在时间：<strong>{time_str}</strong>
                </p>
            </div>
            <p style="color: #666; font-size: 16px; line-height: 1.8;">
                ⏰ 别忘了<strong style="color: #764ba2;">下班打卡</strong>哦！<br><br>
                🏠 收拾好心情，准备回家吧～<br>
                🌟 好好休息，明天继续加油！
            </p>
        </div>
        <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #999; font-size: 12px; margin: 0;">
                🤖 此邮件由 GitHub Actions 自动发送
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    return subject, body


def get_smtp_config(email: str) -> tuple[str, int]:
    """根据邮箱地址自动获取 SMTP 配置"""
    email = email.lower()
    if '@gmail.com' in email:
        return 'smtp.gmail.com', 465
    elif '@163.com' in email:
        return 'smtp.163.com', 465
    elif '@qq.com' in email:
        return 'smtp.qq.com', 465
    else:
        # 默认尝试 465 SSL
        domain = email.split('@')[-1]
        return f'smtp.{domain}', 465


def send_email():
    """发送邮件的主函数"""
    # 从环境变量获取配置
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    email_type = os.environ.get('EMAIL_TYPE', 'morning')
    
    if not all([sender_email, sender_password, receiver_email]):
        raise ValueError("缺少必要的环境变量：SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL")
    
    # 获取邮件内容
    subject, body = get_email_content(email_type)
    
    # 创建邮件
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = f"打卡提醒 <{sender_email}>" # 163 有时要求这种格式
    message['To'] = receiver_email
    
    # 添加 HTML 内容
    html_part = MIMEText(body, 'html', 'utf-8')
    message.attach(html_part)
    
    # 调试模式
    debug_mode = os.environ.get('SMTP_DEBUG', 'False').lower() == 'true'
    
    # 自动获取 SMTP 地址
    smtp_host, smtp_port = get_smtp_config(sender_email)

    try:
        print(f"🚀 正在准备通过 {smtp_host} 发送邮件...")
        
        # 针对 163/QQ/Gmail 的统一处理逻辑
        try:
            print(f"尝试连接 {smtp_host}:{smtp_port} (SSL)...")
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15)
        except Exception as e:
            print(f"⚠️ SSL 连接失败 ({e})，尝试 587 端口 (STARTTLS)...")
            server = smtplib.SMTP(smtp_host, 587, timeout=15)
            server.starttls()

        if debug_mode:
            server.set_debuglevel(1)
            
        with server:
            print(f"正在登录 ({sender_email})...")
            server.login(sender_email, sender_password)
            
            print(f"正在推送给 {receiver_email}...")
            server.sendmail(sender_email, [receiver_email], message.as_string())
            
        print(f"✅ 邮件发送成功！")
        
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        if '163' in smtp_host:
            print("\n💡 163 邮箱排错提示:")
            print("1. 必须使用“授权码”而非登录密码（设置 -> POP3/SMTP/IMAP -> 新增授权码）。")
            print("2. 确认已开启 SMTP 服务。")
        raise


if __name__ == '__main__':
    send_email()
