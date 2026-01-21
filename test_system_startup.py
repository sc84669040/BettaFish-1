#!/usr/bin/env python3
"""
测试系统启动功能
"""

import sys
import os
import requests
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_flask_server():
    """测试Flask服务器是否正常运行"""
    
    print("=== Flask服务器测试 ===")
    
    try:
        # 测试Flask服务器状态
        response = requests.get("http://127.0.0.1:5000/api/status", timeout=5)
        
        if response.status_code == 200:
            print("✅ Flask服务器正常运行")
            return True
        else:
            print(f"❌ Flask服务器返回错误状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Flask服务器连接失败: {e}")
        return False

def test_system_start():
    """测试系统启动API"""
    
    print("\n=== 系统启动API测试 ===")
    
    try:
        # 发送系统启动请求
        response = requests.post("http://127.0.0.1:5000/api/system/start", timeout=30)
        
        if response.status_code == 200:
            print("✅ 系统启动API调用成功")
            result = response.json()
            print(f"   状态: {result.get('status', 'unknown')}")
            print(f"   消息: {result.get('message', 'No message')}")
            return True
        else:
            print(f"❌ 系统启动API返回错误: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 系统启动API调用失败: {e}")
        return False

def test_components_status():
    """测试组件状态"""
    
    print("\n=== 组件状态测试 ===")
    
    components = ["insight", "media", "query", "forum"]
    
    for component in components:
        try:
            response = requests.get(f"http://127.0.0.1:5000/api/system/status", timeout=5)
            
            if response.status_code == 200:
                status_data = response.json()
                component_status = status_data.get(component, {})
                print(f"✅ {component}: {component_status.get('status', 'unknown')}")
            else:
                print(f"❌ {component}: 状态查询失败 ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {component}: 状态查询异常 - {e}")

def main():
    """主测试函数"""
    
    print("正在测试BettaFish系统启动...")
    
    # 等待Flask服务器启动
    print("等待Flask服务器启动...")
    time.sleep(5)
    
    # 测试Flask服务器
    flask_ok = test_flask_server()
    
    if not flask_ok:
        print("❌ Flask服务器未运行，无法继续测试")
        return False
    
    # 测试系统启动
    start_ok = test_system_start()
    
    # 等待系统组件启动
    if start_ok:
        print("\n等待组件启动...")
        time.sleep(10)
        
        # 测试组件状态
        test_components_status()
    
    print("\n" + "="*50)
    if flask_ok and start_ok:
        print("✅ 系统启动测试完成")
        print("所有组件应该可以正常工作")
    else:
        print("❌ 系统启动测试失败")
        print("请检查日志文件以获取详细信息")
    
    return flask_ok and start_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)