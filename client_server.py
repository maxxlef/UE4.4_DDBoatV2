import socket
import threading
import time
import random
import sys
import signal

# DDBoat 17 (Server)
def handle_client(conn, addr, gps):
    print("Connection established with {}".format(addr))

    rmc_ok = False
    while not rmc_ok:
        rmc_ok, rmc_data = gps.read_rmc_non_blocking()
        if rmc_ok:
            gps_position = "%f;%s;%f;%s\0" % (rmc_data[0], rmc_data[1], rmc_data[2], rmc_data[3])
            break
        time.sleep(0.1)
    
    try:
        while True:
            rmc_ok = False
            while not rmc_ok:
                rmc_ok, rmc_data = gps.read_rmc_non_blocking()
                print ("RMC Data",rmc_data,rmc_ok)
                if rmc_ok:
                    gps_position = "%f;%s;%f;%s\0" % (rmc_data[0], rmc_data[1], rmc_data[2], rmc_data[3])
                    break
                time.sleep(0.1)            
            try:
                conn.sendall(gps_position.encode())
                print("Sent GPS Position to {}: {}".format(addr, gps_position))
            except (socket.error, BrokenPipeError):
                print("Client {} disconnected unexpectedly.".format(addr))
                break  # Exit loop when client disconnects
            time.sleep(0.01)  # save computations
    except Exception as e:
        print("Server error with {}: {}".format(addr, e))
    finally:
        conn.close()

def robot1_server():
    sys.path.append('../drivers-ddboat-v2')
    import gps_driver_v2 as gps_drv
    gps = gps_drv.GpsIO()
    gps.set_filter_speed("0")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))  # Listen on all available interfaces
    server_socket.listen(15)  # Allow up to 15 clients
    print("DDBoat 17 (Server) is waiting for connections...")
    
    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr, gps))
        client_thread.start()

# Robot 2 (Client)
def robot2_client_loop(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 5000))
    print("Connected to DDBoat 17 (Server)")

    # def signal_handler(sig, frame):
    #     print("Closing client connection gracefully...")
    #     client_socket.close()
    #     sys.exit(0)
    
    # signal.signal(signal.SIGINT, signal_handler)

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print("Received GPS Position from DDBoat 17: {}".format(data))
            time.sleep(0.01)
    except Exception as e:
        print("Client error: {}".format(e))
    finally:
        client_socket.close()

# Robot 2 (Client)
def robot2_client_onetime(server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 5000))
    print("Connected to DDBoat 17 (Server)")

    # def signal_handler(sig, frame):
    #     print("Closing client connection gracefully...")
    #     client_socket.close()
    #     sys.exit(0)
    
    # signal.signal(signal.SIGINT, signal_handler)

    data = ""
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print("Received GPS Position from DDBoat 17: {}".format(data))
            break
    except Exception as e:
        print("Client error: {}".format(e))
    finally:
        client_socket.close()
    return data

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "client":
        robot2_client_loop("172.20.25.217")  # Change IP if running on different machines
    elif  len(sys.argv) > 1 and sys.argv[1] == "single":
        gps_pos = robot2_client_onetime("172.20.25.217")
        print ("GPS Position",gps_pos)
    else:
        robot1_server()

