apt install -y  python3 python3-pip python3-venv python3-dev build-essential curl git 
python3 -m venv venv
source venv/bin/activate

git clone https://github.com/ACCS2024/debianproxy.git
cd debianproxy

pip install -r requirements.txt
export PYTHONIOENCODING=utf-8
python3 debianProxy.py
```
[]: # 
[]: # ### 直接运行
[]: # 
[]: # 如果不想使用虚拟环境，可以直接运行：
[]: # 
[]: # ```bash
[]: # python3 debianproxy.py
[]: # ```
[]: # 
[]: # ## 注意事项
[]: # 
[]: # - 确保系统已连接到互联网。
[]: # - 如果在安装依赖时遇到问题，请检查网络连接或尝试手动安装缺失的包。