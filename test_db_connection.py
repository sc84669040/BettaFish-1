#!/usr/bin/env python3
"""
测试BettaFish应用与PostgreSQL数据库的连接
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import settings

def test_database_connection():
    """测试数据库连接"""
    
    print("=== BettaFish PostgreSQL数据库连接测试 ===")
    print(f"数据库类型: {settings.DB_DIALECT}")
    print(f"主机: {settings.DB_HOST}")
    print(f"端口: {settings.DB_PORT}")
    print(f"用户名: {settings.DB_USER}")
    print(f"数据库名: {settings.DB_NAME}")
    print(f"字符集: {settings.DB_CHARSET}")
    print("-" * 50)
    
    try:
        # 根据数据库类型选择不同的连接方式
        if settings.DB_DIALECT == "postgresql":
            import psycopg2
            
            conn_params = {
                'host': settings.DB_HOST,
                'port': settings.DB_PORT,
                'user': settings.DB_USER,
                'password': settings.DB_PASSWORD,
                'database': settings.DB_NAME
            }
            
            print("正在连接到PostgreSQL数据库...")
            conn = psycopg2.connect(**conn_params)
            cursor = conn.cursor()
            
            # 执行测试查询
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            
            # 检查数据库表
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            print(f"✅ 数据库连接成功!")
            print(f"PostgreSQL版本: {version.split(',')[0]}")
            print(f"数据库中的表数量: {len(tables)}")
            if tables:
                print("表列表:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("数据库为空，需要初始化表结构")
            
            return True
            
        else:
            print("❌ 不支持的数据库类型: {settings.DB_DIALECT}")
            return False
            
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("请检查:")
        print("1. PostgreSQL Docker容器是否正在运行")
        print("2. 数据库连接参数是否正确")
        print("3. 网络连接是否正常")
        return False

def test_application_models():
    """测试应用模型是否能正常加载"""
    
    print("\n=== 测试应用模型加载 ===")
    
    try:
        # 尝试导入数据库模型
        from MindSpider.DeepSentimentCrawling.MediaCrawler.database.models import Base
        print("✅ 数据库模型导入成功")
        
        # 检查是否有表定义
        print(f"模型中的表数量: {len(Base.metadata.tables)}")
        if Base.metadata.tables:
            print("表定义:")
            for table_name in Base.metadata.tables:
                print(f"  - {table_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 模型导入失败: {e}")
        return False

if __name__ == "__main__":
    print("正在加载配置...")
    
    # 测试数据库连接
    db_ok = test_database_connection()
    
    # 测试模型加载
    models_ok = test_application_models()
    
    print("\n" + "="*50)
    if db_ok and models_ok:
        print("✅ 所有测试通过! BettaFish应用可以正常使用PostgreSQL数据库")
        print("下一步: 重启Flask应用使新配置生效")
    else:
        print("❌ 部分测试失败，请检查配置和依赖")
    
    sys.exit(0 if (db_ok and models_ok) else 1)