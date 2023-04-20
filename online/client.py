from PyQt5.QtCore import QObject, QDataStream
from PyQt5.QtNetwork import QTcpSocket, QHostAddress

from online.server import ServerThread


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

        # read message
        while self.socket.bytesAvailable() > 0:
            data = stream.readQString()
            print(f"Received: {data}.")

            # set nick
            if data.startswith("set_nick:"):
                self.player_nick = data.split(':')[1]
                if self.player_nick == 'dark':
                    self.player_nick = 'black'
                if self.player_nick == 'light':
                    self.player_nick = 'white'

                # permission for player
                if self.player_nick == 'black':
                    self.parent().scene.white_permission = False
                elif self.player_nick == 'white':
                    self.parent().scene.black_permission = False
                print(f"Your side: {self.player_nick}.")

            # Time synchronise
            elif data.startswith("time:"):
                time = map(int, data.split(":")[1:])
                if self.player_nick == 'white':
                    self.parent().scene.black_clock.timer.stop()
                    self.parent().scene.black_clock.setTime(time)
                if self.player_nick == 'black':
                    self.parent().scene.white_clock.timer.stop()
                    self.parent().scene.white_clock.setTime(time)

            # full server
            elif data == "server_full":
                self.socket.disconnectFromHost()
                print("The server is full!. Cannot join the game...")

            # start of the game
            elif data == 'start':
                pass

            # make move
            else:

                # Tomash's notation
                # start_col = int(data[0])
                # start_row = int(data[1])
                # stop_col = int(data[2])
                # stop_row = int(data[3])
                # My notation

                start_row = int(data[0])
                start_col = int(data[1])
                stop_row = int(data[2])
                stop_col = int(data[3])

                # send informations to functions
                self.parent().scene.chess_board.move(start_row, start_col, stop_row, stop_col)
                self.parent().scene.move_in_scene(start_row, start_col, stop_row, stop_col)

                # stop clock
                if self.player_nick == 'white':
                    self.parent().black_clock_scene.stop_black()
                else:
                    self.parent().white_clock_scene.stop_white()


    def sendData(self, data):
        stream = QDataStream(self.socket)
        stream.setVersion(QDataStream.Qt_5_0)
        stream.writeQString(data)
