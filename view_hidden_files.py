#!/usr/bin/env python3
"""
Script to view hidden honeypot files
"""

import os
import sys
import platform
import sqlite3
from datetime import datetime

def find_hidden_files():
    """Find all hidden honeypot files"""
    hidden_files = []
    
    # Search in common locations
    search_paths = []
    
    if platform.system() == "Windows":
        search_paths = ["C:\\", "D:\\", "E:\\"]
    else:
        search_paths = ["/", "/root/", "/home/"]
    
    # Add current directory
    search_paths.append(os.getcwd())
    
    for path in search_paths:
        try:
            db_file = os.path.join(path, '.honeypot_enhanced.db')
            log_file = os.path.join(path, '.honeypot_enhanced.log')
            
            if os.path.exists(db_file):
                hidden_files.append(('Database', db_file))
            if os.path.exists(log_file):
                hidden_files.append(('Logs', log_file))
                
        except:
            continue
    
    return hidden_files

def view_database_content(db_path):
    """View content of the hidden database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"\n📊 Database Content ({db_path}):")
        print("=" * 60)
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Table: {table_name}")
            print("-" * 40)
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"Rows: {count}")
            
            # Show sample data (first 5 rows)
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
                rows = cursor.fetchall()
                print("Sample data:")
                for row in rows:
                    print(f"  {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading database {db_path}: {e}")

def view_log_content(log_path):
    """View content of the hidden log file"""
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n📄 Log File Content ({log_path}):")
        print("=" * 60)
        print(content)
        
    except Exception as e:
        print(f"❌ Error reading log file {log_path}: {e}")

def main():
    print("🔍 Hidden Honeypot Files Viewer")
    print("=" * 40)
    
    hidden_files = find_hidden_files()
    
    if not hidden_files:
        print("❌ No hidden honeypot files found!")
        print("\n💡 Make sure the honeypot has been run at least once.")
        return
    
    print(f"📁 Found {len(hidden_files)} hidden file(s):")
    print()
    
    for i, (file_type, file_path) in enumerate(hidden_files, 1):
        file_size = os.path.getsize(file_path)
        modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        
        print(f"{i}. {file_type} File:")
        print(f"   📍 Location: {file_path}")
        print(f"   📏 Size: {file_size} bytes")
        print(f"   🕒 Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    while True:
        try:
            choice = input("Enter file number to view (or 'q' to quit): ").strip()
            
            if choice.lower() == 'q':
                break
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(hidden_files):
                file_type, file_path = hidden_files[choice_num - 1]
                
                if file_type == 'Database':
                    view_database_content(file_path)
                else:
                    view_log_content(file_path)
                
                print("-" * 60)
                
            else:
                print("❌ Invalid choice!")
                
        except ValueError:
            print("❌ Please enter a valid number!")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main() 