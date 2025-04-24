# CentOS 7 安装指南

## 安装必要的系统包

```bash
# 安装EPEL仓库（为了获取Python 3）
yum install -y epel-release

# 安装必要的系统包
yum install -y python3 python3-pip python3-devel gcc gcc-c++ make curl git

# 更新pip（推荐使用以下方式避免权限问题）
python3 -m pip install --upgrade pip --user

# 安装virtualenv
python3 -m pip install virtualenv --user
```

> **警告**: 直接以root用户运行pip命令可能导致权限问题和系统包冲突。建议使用`--user`标志或在虚拟环境中安装包。

## 设置环境并运行应用

### 使用虚拟环境（推荐）

```bash
# 创建一个非root用户来运行应用（如果尚未创建）
# useradd -m appuser
# su - appuser

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建新的虚拟环境..."
    python3 -m virtualenv venv
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
python -m pip install -r requirements.txt
export PYTHONIOENCODING=utf-8
python3 debianProxy.py
```

### 直接运行

如果不想使用虚拟环境，可以直接运行：

```bash
python3 debianproxy.py
```

## 注意事项

- 确保系统已连接到互联网。
- 如果在安装依赖时遇到问题，请检查网络连接或尝试手动安装缺失的包。
- CentOS 7 默认使用 Python 2.7，上述指令将安装并使用 Python 3。
- **建议使用虚拟环境**：这可以避免权限问题和系统包冲突。
- **避免以root用户运行pip**：如果必须使用root，请使用`python3 -m pip`代替直接调用`pip3`。
- 若在非虚拟环境中安装包，推荐添加`--user`标志以安装到用户目录。
