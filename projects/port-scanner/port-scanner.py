import socket
import sys

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ports(host, start_port, end_port):
    open_ports = []
    print(f"Scanning {host} from port {start_port} to {end_port}...")
    
    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            open_ports.append(port)
            print(f"Port {port}: OPEN")
    
    return open_ports

if __name__ == "__main__":
    host = "localhost"
    open_ports = scan_ports(host, 1, 1024)
    print(f"\nOpen ports: {open_ports}")
