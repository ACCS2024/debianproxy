import os
import sys
import platform
import subprocess
import argparse

def get_system_info():
    """获取系统信息"""
    system = platform.system()
    if system != "Linux":
        return system, None
    
    # 如果是Linux，判断具体发行版
    try:
        with open("/etc/os-release") as f:
            os_release = f.read()
        
        if "debian" in os_release.lower() or "ubuntu" in os_release.lower():
            return system, "debian"
        elif "centos" in os_release.lower() or "rhel" in os_release.lower() or "fedora" in os_release.lower():
            return system, "centos"
        else:
            # 尝试其他方法检测
            if os.path.exists("/etc/debian_version"):
                return system, "debian"
            elif os.path.exists("/etc/centos-release"):
                return system, "centos"
            elif os.path.exists("/etc/redhat-release"):
                return system, "centos"
    except Exception as e:
        print(f"获取Linux发行版信息失败: {e}")
    
    return system, None

def main():
    parser = argparse.ArgumentParser(description="启动适合当前系统的Trace.moe代理服务")
    parser.add_argument("--force", choices=["debian", "centos"], 
                        help="强制使用指定的代理脚本，忽略系统检测")
    parser.add_argument("--port", type=int, default=7755,
                        help="指定服务运行的端口号，默认7755")
    args = parser.parse_args()

    if args.force:
        system_type = args.force
        print(f"强制使用 {system_type} 代理脚本")
    else:
        system, distro = get_system_info()
        
        if system != "Linux":
            print(f"当前系统是 {system}，不是Linux系统，默认使用debian代理")
            system_type = "debian"
        elif distro == "debian":
            print(f"检测到Debian系Linux: {distro}")
            system_type = "debian"
        elif distro == "centos":
            print(f"检测到CentOS系Linux: {distro}")
            system_type = "centos"
        else:
            print(f"未能确定Linux发行版类型，默认使用debian代理")
            system_type = "debian"

    # 确定脚本路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    if system_type == "debian":
        script_path = os.path.join(current_dir, "debianProxy.py")
    else:
        script_path = os.path.join(current_dir, "centosProxy.py")

    print(f"启动代理脚本: {script_path}")
    
    # 设置环境变量，传递端口参数
    env = os.environ.copy()
    env["PORT"] = str(args.port)
    
    # 使用Python解释器启动脚本
    cmd = [sys.executable, script_path]
    try:
        subprocess.run(cmd, env=env)
    except KeyboardInterrupt:
        print("\n服务已停止")
    except Exception as e:
        print(f"启动失败: {e}")

if __name__ == "__main__":
    main()
