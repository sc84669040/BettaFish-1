#!/usr/bin/env python3
"""
测试硅基流动支持的模型名称
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_model(model_name):
    """测试特定模型名称"""
    
    try:
        from config import settings
        from openai import OpenAI
        
        client = OpenAI(
            api_key=settings.FORUM_HOST_API_KEY,
            base_url="https://api.siliconflow.cn/v1"
        )
        
        # 创建一个简单的测试调用
        test_messages = [
            {"role": "system", "content": "你是一个测试助手"},
            {"role": "user", "content": "请回复'测试成功'"}
        ]
        
        response = client.chat.completions.create(
            model=model_name,
            messages=test_messages,
            max_tokens=50
        )
        
        print(f"✅ {model_name}: 测试成功")
        print(f"   响应: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ {model_name}: 测试失败 - {e}")
        return False

if __name__ == "__main__":
    print("=== 硅基流动模型名称测试 ===")
    
    # 尝试不同的模型名称格式
    models_to_test = [
        "Qwen2.5-72B-Instruct",  # 简化的模型名称
        "qwen2.5-72b-instruct",  # 小写格式
        "Qwen2.5-72B",  # 不带-Instruct后缀
        "deepseek-v3",  # DeepSeek模型
        "deepseek-chat",  # DeepSeek聊天模型
        "gpt-3.5-turbo",  # OpenAI兼容格式
        "gpt-4",  # OpenAI兼容格式
        "claude-3-sonnet",  # Anthropic兼容格式
    ]
    
    successful_models = []
    
    for model in models_to_test:
        success = test_model(model)
        if success:
            successful_models.append(model)
    
    print("\n" + "="*50)
    if successful_models:
        print(f"✅ 找到 {len(successful_models)} 个可用的模型:")
        for model in successful_models:
            print(f"   - {model}")
        print("\n请使用其中一个可用的模型名称更新配置")
    else:
        print("❌ 没有找到可用的模型名称")
        print("请检查:")
        print("1. API密钥是否正确")
        print("2. 网络连接是否正常")
        print("3. 硅基流动服务是否可用")
    
    sys.exit(0 if successful_models else 1)