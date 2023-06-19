import disk
import sys
import socket


def main():
    host = socket.gethostname()
    port = 6666
    sock = socket.socket()
    sock.connect((host, port))
    storage_name = sock.recv(1024).decode()
    if storage_name:
        storage = disk.Disk(storage_name)
    res = "Storage: " + str(storage_name)
    print(res)
    sock.send(res.encode())
    while True:
        command = sock.recv(1024).decode()
        if not command:
            break
        if command == "exit":
            storage.exit()
            sock.close()
            sys.exit()
        command = command.split(' ')
        if command[0] == "add":
            result = storage.add_item(command[1], command[2])
        elif command[0] == "delete":
            result = storage.delete_item(command[1])
        elif command[0] == "get":
            result = storage.get_item(command[1])
        elif command[0] == "keys":
            result = storage.keys()
        elif command[0] == "values":
            result = storage.values()
        elif command[0] == "items":
            result = storage.items()
        else:
            break
        print(result)
        sock.send(result.encode())
    sock.close()


if __name__ == '__main__':
    main()
