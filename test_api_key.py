#!/usr/bin/env python3
"""
测试硅基流动API密钥有效性
"""

import requests
import sys

def test_api_key():
    """测试API密钥是否有效"""
    
    api_key = "sk-qgppasedcphauznagkiaicnflumblxhjhfqjyunkajrjxdpd"
    base_url = "https://api.siliconflow.cn/v1"
    
    print("=== 硅基流动API密钥测试 ===")
    print(f"API密钥: {api_key[:10]}...{api_key[-10:]}")
    print(f"API地址: {base_url}")
    
    # 测试1: 检查网络连接
    print("\n1. 测试网络连接...")
    try:
        response = requests.get("https://api.siliconflow.cn", timeout=10)
        print("✅ 网络连接正常")
    except Exception as e:
        print(f"❌ 网络连接失败: {e}")
        return False
    
    # 测试2: 检查API端点
    print("\n2. 测试API端点...")
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 尝试列出模型
        response = requests.get(f"{base_url}/models", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ API端点访问成功")
            models = response.json()
            print(f"   可用模型数量: {len(models.get('data', []))}")
            
            # 显示前几个模型
            for i, model in enumerate(models.get('data', [])[:5]):
                print(f"   - {model.get('id', 'Unknown')}")
            
            return True
            
        elif response.status_code == 401:
            print("❌ API密钥无效 (401 Unauthorized)")
            print("   请检查API密钥是否正确")
            return False
            
        else:
            print(f"❌ API端点访问失败: {response.status_code}")
            print(f"   响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API端点测试失败: {e}")
        return False

if __name__ == "__main__":
    success = test_api_key()
    
    print("\n" + "="*50)
    if success:
        print("✅ API密钥测试通过")
        print("下一步: 请检查模型名称格式")
    else:
        print("❌ API密钥测试失败")
        print("请检查:")
        print("1. API密钥是否正确")
        print("2. 网络连接是否正常")
        print("3. 硅基流动服务状态")
    
    sys.exit(0 if success else 1)