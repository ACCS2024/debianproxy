# Debian Trace.moe 代理服务

这是一个为trace.moe API设计的代理服务，可以自动轮换多个IP地址进行API请求，有效管理API使用配额。

## Debian 12安装步骤

### 1. 更新系统包

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. 安装必要的依赖

```bash
sudo apt install -y python3 python3-pip python3-venv curl git
```

### 3. 安装网络工具包（netifaces依赖）

```bash
sudo apt install -y python3-dev build-essential
```

### 4. 克隆项目代码

```bash
git clone https://your-repository-url/debianproxy.git
cd debianproxy
```

或者手动创建项目目录并添加必要的文件。

## 设置虚拟环境

### 1. 创建虚拟环境

```bash
python3 -m venv venv
```

### 2. 激活虚拟环境

```bash
source venv/bin/activate
```

激活后，命令行前面会出现`(venv)`的标识，表示当前处于虚拟环境中。

### 3. 安装项目依赖

```bash
pip install -r requirements.txt
```

## 运行程序

### 在虚拟环境中运行

确保虚拟环境已激活（命令行前有`(venv)`标识），然后执行：

```bash
python debianProxy.py
```

服务将在端口7755上启动，可通过`http://[服务器IP]:7755`访问。

### 设置开机自启（可选）

创建systemd服务文件：

```bash
sudo nano /etc/systemd/system/debianproxy.service
```

添加以下内容：

```
[Unit]
Description=Debian Trace.moe Proxy
After=network.target

[Service]
User=your_username
WorkingDirectory=/path/to/debianproxy
ExecStart=/path/to/debianproxy/venv/bin/python /path/to/debianproxy/debianProxy.py
Restart=always

[Install]
WantedBy=multi-user.target
```

启用并启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable debianproxy
sudo systemctl start debianproxy
```

## API使用方法

### 检查IP额度状态

```
GET /me
```

### 搜索图片

```
POST /search
```

请求体应为`multipart/form-data`格式，包含名为`file`或`image`的图片文件。

## 注意事项

- 确保服务器有多个可用IP地址（37.*, 172.*, 216.*开头）
- 程序会自动管理各IP的配额使用情况
