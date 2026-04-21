#!/usr/bin/env python3
import os
import sys
from collections import defaultdict


def format_size(size_bytes):
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    size = size_bytes
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"


def scan_directory(directory):
    if not os.path.isdir(directory):
        print(f"错误: {directory} 不是有效的目录路径", file=sys.stderr)
        sys.exit(1)

    extension_sizes = defaultdict(int)
    total_files = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            total_files += 1
            file_path = os.path.join(root, filename)
            
            try:
                file_size = os.path.getsize(file_path)
                name, ext = os.path.splitext(filename)
                ext = ext.lower() if ext else '(无后缀)'
                extension_sizes[ext] += file_size
            except (OSError, PermissionError):
                continue

    sorted_extensions = sorted(
        extension_sizes.items(),
        key=lambda x: x[1],
        reverse=True
    )

    total_size = sum(extension_sizes.values())
    
    print(f"\n扫描目录: {os.path.abspath(directory)}")
    print(f"文件总数: {total_files}")
    print(f"总大小: {format_size(total_size)}")
    print("\n" + "=" * 50)
    print(f"{'后缀名':<15} {'文件大小':<15} {'占比':>10}")
    print("=" * 50)

    for ext, size in sorted_extensions[:10]:
        percentage = (size / total_size * 100) if total_size > 0 else 0
        print(f"{ext:<15} {format_size(size):<15} {percentage:>8.1f}%")

    print("=" * 50)
    print(f"\n共计 {len(extension_sizes)} 种不同的文件类型\n")


def main():
    if len(sys.argv) != 2:
        print(f"使用方法: {sys.argv[0]} <目录路径>", file=sys.stderr)
        sys.exit(1)
    
    directory = sys.argv[1]
    scan_directory(directory)


if __name__ == "__main__":
    main()
