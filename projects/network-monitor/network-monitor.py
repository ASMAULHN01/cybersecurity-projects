import socket
import os

def get_network_info():
    info = {}
    
    try:
        hostname = socket.gethostname()
        info['hostname'] = hostname
        
        ip_address = socket.gethostbyname(hostname)
        info['ip_address'] = ip_address
        
        if os.name == 'posix':
            os.system('ifconfig')
        else:
            os.system('ipconfig')
    except Exception as e:
        info['error'] = str(e)
    
    return info

if __name__ == "__main__":
    print("=== Network Information ===")
    info = get_network_info()
    for key, value in info.items():
        print(f"{key}: {value}")
