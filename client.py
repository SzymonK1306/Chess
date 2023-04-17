from PyQt5.QtCore import QObject, QDataStream
from PyQt5.QtNetwork import QTcpSocket, QHostAddress

from server import ServerThread


class ChessClient(QObject):
    def __init__(self, ip, port, parent):
        super().__init__(parent)
        self.mainWindow = parent
        self.serverThread = None

        self.socket = QTcpSocket()
        self.socket.connected.connect(self.connected)
        self.socket.disconnected.connect(self.disconnected)
        self.socket.errorOccurred.connect(self.errorOccurred)
        self.socket.readyRead.connect(self.receiveData)

        self.ip, self.port = QHostAddress(ip), port
        self.socket.connectToHost(self.ip, self.port)

    @staticmethod
    def connected():
        print("Connected to server!")

    @staticmethod
    def disconnected():
        print("Disconnected from server...")

    def errorOccurred(self, error):
        if error == QTcpSocket.ConnectionRefusedError:
            print("The server is not running! Starting the server...")
            self.serverThread = ServerThread(self.ip, self.port)
            self.serverThread.start()
            self.socket.connectToHost(self.ip, self.port)
        else:
            print(f"Error: {error}")

    def receiveData(self):
        stream = QDataStream(self.socket)
        stream.setVersion(QDataStream.Qt_5_0)

        while self.socket.bytesAvailable() > 0:
            data = stream.readQString()
            print(f"Received: {data}.")

            if data.startswith("set_nick:"):
                player_nick = data.split(':')[1]
                print(f"Your side: {player_nick}.")
            elif data == "server_full":
                self.socket.disconnectFromHost()
                print("The server is full!. Cannot join the game...")

    def sendData(self, data):
        stream = QDataStream(self.socket)
        stream.setVersion(QDataStream.Qt_5_0)
        stream.writeQString(data)
