#!/usr/bin/env python3
import argparse
import json
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


def collect_stats(directory):
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

    total_size = sum(extension_sizes.values())
    sorted_extensions = sorted(
        extension_sizes.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return {
        'directory': os.path.abspath(directory),
        'total_files': total_files,
        'total_size': total_size,
        'extensions': [
            {
                'ext': ext,
                'bytes': size,
                'percentage': (size / total_size * 100) if total_size > 0 else 0
            }
            for ext, size in sorted_extensions
        ],
        'extension_count': len(extension_sizes)
    }


def print_human_readable(stats):
    print(f"\n扫描目录: {stats['directory']}")
    print(f"文件总数: {stats['total_files']}")
    print(f"总大小: {format_size(stats['total_size'])}")
    print("\n" + "=" * 50)
    print(f"{'后缀名':<15} {'文件大小':<15} {'占比':>10}")
    print("=" * 50)

    for ext_info in stats['extensions'][:10]:
        print(f"{ext_info['ext']:<15} {format_size(ext_info['bytes']):<15} {ext_info['percentage']:>8.1f}%")

    print("=" * 50)
    print(f"\n共计 {stats['extension_count']} 种不同的文件类型\n")


def print_json(stats):
    json_stats = stats.copy()
    json_stats['extensions'] = [
        {
            'ext': ext_info['ext'],
            'bytes': ext_info['bytes'],
            'percentage': round(ext_info['percentage'], 2)
        }
        for ext_info in stats['extensions']
    ]
    print(json.dumps(json_stats, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description='递归扫描目录，按后缀名汇总磁盘占用大小')
    parser.add_argument('directory', help='要扫描的目录路径')
    parser.add_argument('-j', '--json', action='store_true', help='输出JSON格式结果')
    
    args = parser.parse_args()
    
    stats = collect_stats(args.directory)
    
    if args.json:
        print_json(stats)
    else:
        print_human_readable(stats)


if __name__ == "__main__":
    main()
