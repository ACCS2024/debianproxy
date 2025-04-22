# Debian HTTP Proxy

本项目为在 Debian 12 环境下运行的 HTTP 反向代理服务，满足如下需求：

- 自动获取设备所有IP地址，筛选出以 `216.`、`37.`、`172.` 开头的外网IP
- 所有HTTP请求反向代理至 `https://api.trace.moe`
- 监听所有接口的 `7722` 端口
- 每次请求随机选择一个外网IP作为本地源IP，实现负载均衡
- 只需访问 `http://本机IP:7722` 即可实现代理请求

## 安装与运行

1. 安装 Python 3（Debian 12 默认自带或通过 apt 安装）  
2. 安装所需依赖
   ```
   pip install -r requirements.txt
   ```
3. 运行脚本
   ```
   python debianProxy.py
   ```
4. 若需后台运行，可使用 `start.sh` 脚本或进程管理工具

## 文件结构

```
- debianProxy.py
- requirements.txt
- README.md
- start.sh
```