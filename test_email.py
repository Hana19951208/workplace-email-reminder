import os
import sys
from send_email import send_email

def local_test():
    """
    本地验证脚本
    支持从 .env 文件或直接从环境变量读取
    """
    print("🚀 开始本地邮件发送验证...")
    
    # 尝试加载 python-dotenv (如果安装了)
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("💡 已加载 .env 文件配置")
    except ImportError:
        print("⚠️ 未安装 python-dotenv，将直接使用系统环境变量")

    # 检查必要变量
    required_vars = ['SENDER_EMAIL', 'SENDER_PASSWORD', 'RECEIVER_EMAIL']
    missing = [var for var in required_vars if not os.environ.get(var)]
    
    if missing:
        print(f"❌ 错误：缺少环境变量: {', '.join(missing)}")
        print("请创建 .env 文件并填入配置，或者直接设置系统环境变量。")
        sys.exit(1)

    try:
        # 默认测试早安邮件
        if not os.environ.get('EMAIL_TYPE'):
            os.environ['EMAIL_TYPE'] = 'morning'
            
        send_email()
        print("\n✅ 本地验证成功！请检查收件箱。")
    except Exception as e:
        print(f"\n❌ 验证失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    local_test()
