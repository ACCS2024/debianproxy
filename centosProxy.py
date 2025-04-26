import os
import subprocess
import netifaces
import time
import random
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# 缓存所有IP和额度信息
ip_cache = {}

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
        if ip.startswith('37.') or ip.startswith('156.') or ip.startswith('172.') or ip.startswith('216.'):
            filtered.append(ip)
    return filtered

def print_filtered_ips(ips):
    print("Filtered IPs (外网IP，37./172./216.开头):")
    for ip in ips:
        print(ip)

def curl_me_with_interface(ip):
    url = "https://api.trace.moe/me"
    cmd = [
        'curl',
        '--interface', ip,
        url
    ]
    print(f"\nUsing IP: {ip} for /me")
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = result.communicate()
    output = output.decode('utf-8')
    error = error.decode('utf-8')
    print(output)
    if result.returncode != 0:
        print(error)
    return output

def curl_with_interface(ip, image_path):
    url = "https://api.trace.moe/search"
    cmd = [
        'curl',
        '--interface', ip,
        '-F', f'image=@{image_path}',
        url
    ]
    print(f"\nUsing IP: {ip}")
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = result.communicate()
    output = output.decode('utf-8')
    print(output)
    if result.returncode != 0:
        print(error)
    return output

def update_ip_quota_cache():
    global ip_cache
    all_ips = get_all_ips()
    filtered_ips = filter_ips(all_ips)
    ip_cache.clear()
    print_filtered_ips(filtered_ips)
    print("\n初始化额度检查:")
    for ip in filtered_ips:
        try:
            quota_info = curl_me_with_interface(ip)
            data = json.loads(quota_info)
            quota = data.get("quota", 1000)
            quota_used = data.get("quotaUsed", 0)
            available = quota - quota_used
            ip_cache[ip] = {
                "quota": quota,
                "quotaUsed": quota_used,
                "available": available
            }
            print(f"{ip} 剩余 {available} 次")
        except Exception as e:
            print(f"{ip} 获取额度失败: {e}")

def get_available_ips():
    # 只返回还有额度的IP
    return [ip for ip, info in ip_cache.items() if info["available"] > 0]

def call_me():
    # 重新检查所有IP额度（可选，初始化时已检查）
    update_ip_quota_cache()
    return "IP额度已初始化完毕"

def check_image(image_path):
    available_ips = get_available_ips()
    if not available_ips:
        print("池内没有可用IP，程序终止。")
        os._exit(1)  # 直接终止程序
    # 随机选择一个可用IP
    selected_ip = random.choice(available_ips)
    print(f"\n随机选择可用IP进行curl请求：{selected_ip}")
    result = curl_with_interface(selected_ip, image_path)
    # 每次请求消耗一次额度
    ip_cache[selected_ip]["quotaUsed"] += 1
    ip_cache[selected_ip]["available"] -= 1
    return result

@app.route('/search', methods=['POST'])
def upload_file():
    upload_field = request.files.get('file') or request.files.get('image')
    if not upload_field:
        return jsonify({'error': 'No file part'}), 400
    file = upload_field
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    filename = f"upload_{int(time.time())}_{random.randint(1000,9999)}.jpg"
    filepath = os.path.join("/tmp", filename)
    file.save(filepath)
    print(f"Received file and saved as {filepath}")
    try:
        # 调用图片检查方法
        result = check_image(filepath)
        try:
            json_result = json.loads(result)
            return jsonify(json_result)
        except Exception as e:
            print(f"返回内容不是有效 JSON，内容为: {result}")
            return jsonify({'error': 'Invalid JSON from trace.moe centosProxy', 'raw': result}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Cache file {filepath} deleted.")

@app.route('/me', methods=['GET'])
def me():
    # 重新初始化额度池
    msg = call_me()
    return jsonify({'msg': msg, 'ip_cache': ip_cache})

if __name__ == "__main__":
    update_ip_quota_cache()  # 启动时初始化
    port = int(os.environ.get("PORT", 7755))
    app.run(host='0.0.0.0', port=port)
