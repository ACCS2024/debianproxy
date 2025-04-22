import os
import subprocess
import netifaces
import time
import random  # 新增

def get_all_ips():
    ips = []
    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            for link in addrs[netifaces.AF_INET]:
                ip = link.get('addr')
                if ip and not ip.startswith('127.'):
                    ips.append(ip)
    return ips

def filter_ips(ips):
    filtered = []
    for ip in ips:
        if ip.startswith('37.') or ip.startswith('172.') or ip.startswith('216.'):
            filtered.append(ip)
    return filtered

def print_filtered_ips(ips):
    print("Filtered IPs (外网IP，37./172./216.开头):")
    for ip in ips:
        print(ip)

def curl_with_interface(ip, image_path):
    url = "https://api.trace.moe/search"
    cmd = [
        'curl',
        '--interface', ip,
        '-F', f'image=@{image_path}',
        url
    ]
    print(f"\nUsing IP: {ip}")
    result = subprocess.run(cmd, capture_output=True)
    print(result.stdout.decode('utf-8'))
    if result.returncode != 0:
        print(result.stderr.decode('utf-8'))

if __name__ == "__main__":
    all_ips = get_all_ips()
    filtered_ips = filter_ips(all_ips)
    print_filtered_ips(filtered_ips)
    image_path = 'demo.jpg'  # 确保demo.jpg在当前目录
    if filtered_ips:
        selected_ip = random.choice(filtered_ips)
        print(f"\n随机选择IP进行curl请求：{selected_ip}")
        curl_with_interface(selected_ip, image_path)
    else:
        print("No matching IP found for curl.")