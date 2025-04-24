# 安装必要的系统包
apt install -y python3 python3-pip python3-venv python3-dev build-essential curl git 

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建新的虚拟环境..."
    python3 -m venv venv
else
    echo "虚拟环境已存在，跳过创建步骤"
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate

# 检查仓库是否已克隆
if [ ! -d "debianproxy" ]; then
    git clone https://github.com/ACCS2024/debianproxy.git
else
    echo "仓库已存在，跳过克隆步骤"
fi

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