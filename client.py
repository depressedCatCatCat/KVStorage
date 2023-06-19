import socket
import threading

conns = []


def handle_conn_exception(index, e):
    if e.errno == 10053:
        conns.pop(index)
        print("users:", len(conns))
    else:
        raise


def send_message(message):
    for i, conn in enumerate(conns):
        try:
            conn.send(message.encode())
        except socket.error as e:
            handle_conn_exception(i, e)


def receive_message():
    responses = []
    for i, conn in enumerate(conns):
        try:
            data = conn.recv(1024)
            if data:
                responses.append(data.decode())
        except socket.error as e:
            handle_conn_exception(i, e)
    return responses


def main():
    host = socket.gethostname()
    port = 6666
    serv = socket.socket()
    serv.bind((host, port))
    serv.listen(100)
 
    def acceptor():
        while True:
            conn, address = serv.accept()
            conns.append(conn)
            print(f"connection: {address}")

    def sender():
        while True:
            message = input("~ ")
            if message == 'exit':
                for conn in conns:
                    conn.close()
                serv.close()
                break
            send_message(message)
            re_messages = receive_message()
            for re_message in re_messages:
                print(re_message)

    thread_acc = threading.Thread(target=acceptor)
    thread_acc.start()

    storage_name = input("name: ")
    if storage_name:
        send_message(storage_name)
        responses = receive_message()
        for response in responses:
            print(response)

    thread_snd = threading.Thread(target=sender)
    thread_snd.start()


if __name__ == '__main__':
    main()
