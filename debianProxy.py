import os
import subprocess
import netifaces
import time
import random
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

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
    return result.stdout.decode('utf-8')

def curl_me_with_interface(ip):
    url = "https://api.trace.moe/me"
    cmd = [
        'curl',
        '--interface', ip,
        url
    ]
    print(f"\nUsing IP: {ip} for /me")
    result = subprocess.run(cmd, capture_output=True)
    output = result.stdout.decode('utf-8')
    print(output)
    if result.returncode != 0:
        print(result.stderr.decode('utf-8'))
    return output

def check_image(image_path):
    all_ips = get_all_ips()
    filtered_ips = filter_ips(all_ips)
    print_filtered_ips(filtered_ips)
    if filtered_ips:
        selected_ip = random.choice(filtered_ips)
        print(f"\n随机选择IP进行curl请求：{selected_ip}")
        result = curl_with_interface(selected_ip, image_path)
        return result
    else:
        print("No matching IP found for curl.")
        return "No matching IP found for curl."

def call_me():
    all_ips = get_all_ips()
    filtered_ips = filter_ips(all_ips)
    print_filtered_ips(filtered_ips)
    if filtered_ips:
        selected_ip = random.choice(filtered_ips)
        print(f"\n随机选择IP进行curl请求(me)：{selected_ip}")
        result = curl_me_with_interface(selected_ip)
        return result
    else:
        print("No matching IP found for curl.")
        return "No matching IP found for curl."

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
        return jsonify({'result': result})
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Cache file {filepath} deleted.")

@app.route('/me', methods=['GET'])
def me():
    result = call_me()
    try:
        # 如果trace.moe返回的是JSON，尝试直接转发
        return jsonify(**json.loads(result))
    except Exception:
        # 如果不是合法JSON则直接返回文本
        return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7755)

