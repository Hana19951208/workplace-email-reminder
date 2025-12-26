#!/usr/bin/env python3
"""
📧 上下班邮件提醒脚本
功能：通过 Gmail/163/QQ 等 SMTP 服务发送精美的 HTML 提醒邮件。
策略：采用“抢占式等待”方案，提前启动并精准延时，规避 GitHub Actions 的调度延迟。
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import pytz
import time
import chinese_calendar as calendar
from datetime import date
from dotenv import load_dotenv

# 🚀 自动加载环境变量逻辑
# 优先加载 .env.local (本地私密配置)，如果不存在则加载 .env
if os.path.exists('.env.local'):
    load_dotenv('.env.local')
else:
    load_dotenv()


def wait_for_target_time(target_hour: int, target_minute: int):
    """
    🎯 精准等待函数
    逻辑：计算当前北京时间与目标时刻的秒数差，进行阻塞式休眠。
    """
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)
    # 构造当日的目标时间对象
    target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)
    
    # 如果目标时间还在未来，则进入休眠逻辑
    if now < target_time:
        wait_seconds = (target_time - now).total_seconds()
        print(f"⏳ [北京时间] 当前: {now.strftime('%H:%M:%S')} -> 目标: {target_time.strftime('%H:%M:%S')}")
        print(f"😴 守护进程已启动，预计休眠 {wait_seconds:.1f} 秒...")
        
        # 每 60 秒苏醒一次并打印进度，防止 GitHub Actions 认为进程由于无输出而卡死
        while (target_time - datetime.now(beijing_tz)).total_seconds() > 0:
            remaining = (target_time - datetime.now(beijing_tz)).total_seconds()
            if remaining <= 0:
                break
            sleep_chunk = min(remaining, 60)
            time.sleep(sleep_chunk)
            if remaining > 60:
                 print(f"⏰ 正在精准倒计时... 剩余 {remaining:.0f} 秒")
        
        print(f"🚀 时间到！执行发送任务，当前时间: {datetime.now(beijing_tz).strftime('%H:%M:%S')}")
    else:
        # 如果启动时已经过了目标时间，则直接发送，不进行等待
        print(f"⏩ 当前时间 {now.strftime('%H:%M:%S')} 已超过目标时刻，跳过等待直接发送。")


def get_email_content(email_type: str) -> tuple[str, str]:
    """
    🎨 邮件内容模板引擎
    功能：根据 morning/evening 类型返回对应的 HTML 模板和主题。
    """
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)
    time_str = now.strftime('%H:%M')
    
    # 星期几的中文转换表
    weekday_map = {
        'Monday': '星期一', 'Tuesday': '星期二', 'Wednesday': '星期三',
        'Thursday': '星期四', 'Friday': '星期五', 'Saturday': '星期六', 'Sunday': '星期日'
    }
    weekday_cn = weekday_map.get(now.strftime('%A'), now.strftime('%A'))
    date_str_cn = now.strftime(f'%Y年%m月%d日 {weekday_cn}')
    
    if email_type == 'morning':
        subject = f"☀️ 早安打卡提醒 - {date_str_cn}"
        # 早晨模板使用暖色调渐变
        body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px;">
    <div style="max-width: 500px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 40px 30px; text-align: center;">
            <div style="font-size: 60px; margin-bottom: 10px;">🌅</div>
            <h1 style="color: white; margin: 0; font-size: 28px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">早安打卡提醒</h1>
        </div>
        <div style="padding: 40px 30px;">
            <p style="color: #333; font-size: 18px; line-height: 1.8; margin: 0 0 20px 0;">亲爱的小伙伴，新年的一天开始啦！ 🎉</p>
            <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); border-radius: 15px; padding: 25px; margin: 20px 0;">
                <p style="color: #555; font-size: 16px; margin: 0;">📅 <strong>{date_str_cn}</strong><br>⏰ 提醒时刻：<strong>{time_str}</strong></p>
            </div>
            <p style="color: #666; font-size: 16px; line-height: 1.8;">⏰ 请记得<strong style="color: #f5576c;">上班打卡</strong>哦！<br><br>💪 愿你今天工作顺利，心情愉快！</p>
        </div>
        <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #999; font-size: 12px; margin: 0;">🤖 此邮件由 GitHub Actions 抢占式系统自动发送</p>
        </div>
    </div>
</body>
</html>"""
    else:
        subject = f"🌙 下班打卡提醒 - {date_str_cn}"
        # 傍晚模板使用深蓝紫色调
        body = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); margin: 0; padding: 20px;">
    <div style="max-width: 500px; margin: 0 auto; background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
            <div style="font-size: 60px; margin-bottom: 10px;">🌙</div>
            <h1 style="color: white; margin: 0; font-size: 28px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">下班打卡提醒</h1>
        </div>
        <div style="padding: 40px 30px;">
            <p style="color: #333; font-size: 18px; line-height: 1.8; margin: 0 0 20px 0;">辛苦了一天，到下班时间啦！ 🎊</p>
            <div style="background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); border-radius: 15px; padding: 25px; margin: 20px 0;">
                <p style="color: #555; font-size: 16px; margin: 0;">📅 <strong>{date_str_cn}</strong><br>⏰ 提醒时刻：<strong>{time_str}</strong></p>
            </div>
            <p style="color: #666; font-size: 16px; line-height: 1.8;">⏰ 别忘了<strong style="color: #764ba2;">下班打卡</strong>哦！<br><br>🏠 收拾好心情，准备回家吧～</p>
        </div>
        <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #eee;">
            <p style="color: #999; font-size: 12px; margin: 0;">🤖 此邮件由 GitHub Actions 抢占式系统自动发送</p>
        </div>
    </div>
</body>
</html>"""
    return subject, body


def get_smtp_config(email: str) -> tuple[str, int]:
    """自动获取 SMTP 配置：根据常用邮箱后缀分配对应服务器"""
    email = email.lower()
    if '@gmail.com' in email: return 'smtp.gmail.com', 465
    if '@163.com' in email: return 'smtp.163.com', 465
    if '@qq.com' in email: return 'smtp.qq.com', 465
    domain = email.split('@')[-1]
    return f'smtp.{domain}', 465


def send_email():
    """🚀 邮件发送核心逻辑"""
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    receiver_email = os.environ.get('RECEIVER_EMAIL')
    email_type = os.environ.get('EMAIL_TYPE', 'morning')
    
    if not all([sender_email, sender_password, receiver_email]):
        raise ValueError("❌ 错误：环境变量 SENDER_EMAIL, SENDER_PASSWORD 或 RECEIVER_EMAIL 缺失！")
    
    subject, body = get_email_content(email_type)
    
    # 构建多部分邮件对象
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = f"打卡提醒 <{sender_email}>"
    message['To'] = receiver_email
    message.attach(MIMEText(body, 'html', 'utf-8'))
    
    smtp_host, smtp_port = get_smtp_config(sender_email)

    try:
        # 优先使用 SSL (465端口)
        try:
            print(f"🔗 正在尝试 SSL 连接 {smtp_host}:{smtp_port}...")
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15)
        except Exception:
            print(f"⚠️ SSL 连接失败，正在回退至 STARTTLS (587端口)...")
            server = smtplib.SMTP(smtp_host, 587, timeout=15)
            server.starttls()
            
        with server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, [receiver_email], message.as_string())
        print(f"✅ 邮件已成功送达至 {receiver_email}！")
    except Exception as e:
        print(f"❌ 发送失败: {str(e)}")
        raise


def auto_check_and_send():
    """🕒 定时任务分发逻辑"""
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)
    h = now.hour
    
    print(f"🏠 定时守卫已就绪，当前北京时间: {now.strftime('%H:%M:%S')}")
    
    # 🕵️ 节假日过滤逻辑
    try:
        if not calendar.is_workday(now.date()):
            print(f"🏖️ 检测到今天 ({now.strftime('%Y-%m-%d')}) 是法定节假日或周末，且无需调休。")
            print("💤 脚本将自动退出，祝您假期愉快！")
            return
        else:
            print(f"💼 检测到今天 ({now.strftime('%Y-%m-%d')}) 是工作日（含调休），准备发送提醒...")
    except Exception as e:
        print(f"⚠️ 节假日检查失败 (可能是年份数据未更新): {e}，将默认继续执行。")

    # 根据启动的小时数判定是【早间启动】还是【晚间启动】
    if 7 <= h < 9:
        print("☀️ 检测到早间启动信号...")
        wait_for_target_time(8, 15) # 设定在 08:15 分发出提醒
        os.environ['EMAIL_TYPE'] = 'morning'
        send_email()
    elif 16 <= h < 18:
        print("🌙 检测到晚间启动信号...")
        wait_for_target_time(17, 35) # 设定在 17:35 分发出提醒
        os.environ['EMAIL_TYPE'] = 'evening'
        send_email()
    else:
        print(f"☕ 当前时间 ({now.strftime('%H:%M')}) 不在自动任务窗口内，将执行常规发送测试流程。")
        send_email()


if __name__ == '__main__':
    # 若设置了 AUTO_CHECK，则进入抢占式等待逻辑；否则直接发送（用于手动测试）
    if os.environ.get('AUTO_CHECK', 'False').lower() == 'true':
        auto_check_and_send()
    else:
        send_email()
