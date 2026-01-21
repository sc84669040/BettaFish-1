#!/usr/bin/env python3
"""
创建PostgreSQL数据库脚本
用于为BettaFish项目创建数据库
"""

import psycopg2
from psycopg2 import sql
import sys

def create_database():
    """创建PostgreSQL数据库"""
    
    # 默认PostgreSQL连接参数
    db_params = {
        'host': 'localhost',
        'port': 5432,
        'user': 'postgres',
        'password': 'sc84669040',
        'database': 'postgres'  # 连接到默认数据库来创建新数据库
    }
    
    new_db_name = 'bettafish'
    
    try:
        # 连接到PostgreSQL服务器
        print("正在连接到PostgreSQL服务器...")
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True  # 设置自动提交，因为不能在有事务的情况下创建数据库
        
        cursor = conn.cursor()
        
        # 检查数据库是否已存在
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (new_db_name,))
        exists = cursor.fetchone()
        
        if exists:
            print(f"数据库 '{new_db_name}' 已存在")
        else:
            # 创建新数据库
            create_db_query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name))
            cursor.execute(create_db_query)
            print(f"数据库 '{new_db_name}' 创建成功")
        
        # 测试连接到新数据库
        test_params = db_params.copy()
        test_params['database'] = new_db_name
        
        try:
            test_conn = psycopg2.connect(**test_params)
            test_cursor = test_conn.cursor()
            test_cursor.execute("SELECT version();")
            version = test_cursor.fetchone()[0]
            print(f"数据库连接测试成功: {version.split(',')[0]}")
            
            # 创建必要的扩展
            test_cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
            print("UUID扩展已启用")
            
            test_cursor.close()
            test_conn.close()
            
        except Exception as e:
            print(f"数据库连接测试失败: {e}")
            
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"连接PostgreSQL服务器失败: {e}")
        print("请确保:")
        print("1. PostgreSQL服务正在运行")
        print("2. 连接参数正确 (用户名: postgres, 密码: sc84669040)")
        print("3. PostgreSQL服务监听在 localhost:5432")
        return False
    
    except Exception as e:
        print(f"创建数据库时出错: {e}")
        return False

if __name__ == "__main__":
    print("=== BettaFish PostgreSQL数据库创建工具 ===")
    print("目标数据库: bettafish")
    print("连接参数:")
    print("  主机: localhost")
    print("  端口: 5432") 
    print("  用户名: postgres")
    print("  密码: sc84669040")
    print("-" * 50)
    
    success = create_database()
    
    if success:
        print("\n✅ 数据库创建/验证完成!")
        print("接下来请更新.env配置文件中的数据库设置")
    else:
        print("\n❌ 数据库创建失败")
        print("请检查PostgreSQL服务状态和连接参数")
    
    sys.exit(0 if success else 1)