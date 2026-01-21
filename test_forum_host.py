#!/usr/bin/env python3
"""
测试Forum Host配置和连接
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_forum_host_config():
    """测试Forum Host配置"""
    
    print("=== Forum Host配置测试 ===")
    
    try:
        from config import settings
        
        print(f"FORUM_HOST_API_KEY: {'已设置' if settings.FORUM_HOST_API_KEY else '未设置'}")
        print(f"FORUM_HOST_BASE_URL: {settings.FORUM_HOST_BASE_URL}")
        print(f"FORUM_HOST_MODEL_NAME: {settings.FORUM_HOST_MODEL_NAME}")
        
        if not settings.FORUM_HOST_API_KEY:
            print("❌ FORUM_HOST_API_KEY 未设置")
            return False
            
        if not settings.FORUM_HOST_BASE_URL:
            print("❌ FORUM_HOST_BASE_URL 未设置")
            return False
            
        if not settings.FORUM_HOST_MODEL_NAME:
            print("❌ FORUM_HOST_MODEL_NAME 未设置")
            return False
            
        print("✅ 配置检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置检查失败: {e}")
        return False

def test_forum_host_connection():
    """测试Forum Host连接"""
    
    print("\n=== Forum Host连接测试 ===")
    
    try:
        from config import settings
        from ForumEngine.llm_host import ForumHost
        
        print("正在初始化Forum Host...")
        
        # 测试Forum Host初始化
        host = ForumHost(
            api_key=settings.FORUM_HOST_API_KEY,
            base_url=settings.FORUM_HOST_BASE_URL,
            model_name=settings.FORUM_HOST_MODEL_NAME
        )
        
        print("✅ Forum Host初始化成功")
        print(f"模型: {host.model}")
        print(f"API地址: {host.base_url}")
        
        # 测试简单的API调用
        print("正在测试API连接...")
        
        # 创建一个简单的测试调用
        test_messages = [
            {"role": "system", "content": "你是一个测试助手"},
            {"role": "user", "content": "请回复'测试成功'"}
        ]
        
        try:
            response = host.client.chat.completions.create(
                model=host.model,
                messages=test_messages,
                max_tokens=50
            )
            
            print("✅ API连接测试成功")
            print(f"响应: {response.choices[0].message.content}")
            return True
            
        except Exception as e:
            print(f"❌ API连接测试失败: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Forum Host连接测试失败: {e}")
        return False

def test_forum_engine_monitor():
    """测试Forum Engine监控器"""
    
    print("\n=== Forum Engine监控器测试 ===")
    
    try:
        from ForumEngine.monitor import LogMonitor
        
        print("正在初始化日志监控器...")
        
        monitor = LogMonitor()
        
        print("✅ 日志监控器初始化成功")
        print(f"监控目录: {monitor.log_dir}")
        print(f"监控文件: {list(monitor.monitored_logs.keys())}")
        
        # 检查主持人模块是否可用
        try:
            from ForumEngine.llm_host import generate_host_speech
            print("✅ 主持人模块可用")
        except ImportError:
            print("❌ 主持人模块不可用")
        
        # 测试日志文件是否存在
        for app_name, log_file in monitor.monitored_logs.items():
            if log_file.exists():
                print(f"✅ {app_name}日志文件存在: {log_file}")
            else:
                print(f"⚠️ {app_name}日志文件不存在: {log_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Forum Engine监控器测试失败: {e}")
        return False

if __name__ == "__main__":
    print("正在测试Forum Host配置...")
    
    # 测试配置
    config_ok = test_forum_host_config()
    
    # 测试连接
    connection_ok = test_forum_host_connection()
    
    # 测试监控器
    monitor_ok = test_forum_engine_monitor()
    
    print("\n" + "="*50)
    if config_ok and connection_ok and monitor_ok:
        print("✅ 所有Forum Host测试通过!")
        print("Forum Engine应该可以正常工作")
    else:
        print("❌ 部分测试失败")
        print("请检查配置和依赖")
    
    sys.exit(0 if (config_ok and connection_ok and monitor_ok) else 1)