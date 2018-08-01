import sys
from PyQt5.QtWidgets import (QWidget, QToolTip,
                             QPushButton, QApplication)
from PyQt5 import QtWidgets, QtCore, QtGui
from faceEmotion import readFaceImage
from face_api import face2emotion
from record import recordWav
from nlp_api import getSentence
from playMusic import playMusic
from multiprocessing  import Pipe,Queue


class Trans(QtWidgets.QWidget):
    def __init__(self):
        super(Trans, self).__init__()

        self.initUI()

        self.resize(700, 700)
        self.l1 = QtWidgets.QLabel(self)
        movie = QtGui.QMovie("back.gif")

        movie.setSpeed(100)
        # timer = threading.Timer(5, self.fun_timer)
        # timer.start()

        self.l1.setMovie(movie)
        movie.start()

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.fun_timer)  # 计时结束调用operate()方法
        # self.timer.start(5000)

    def initUI(self):
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def fun_timer(self):
        movie = QtGui.QMovie("happy.gif")
        movie.setSpeed(100)
        self.l1.setMovie(movie)
        movie.start()
        self.timer.stop()


def ui():
    app = QApplication(sys.argv)

    trans = Trans()
    trans.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    base64Queue = Queue()
    # wavQueue = Queue()
    wavWrite_conn,wavRead_conn= Pipe()

    # emotionQueue = Queue()
    emotionInput_conn,emotionOutput_conn= Pipe()
    # instructionQueue = Queue()
    instructionInput_conn,instructionOutput_conn = Pipe()


    # 线程管理器
    threadManeger = []

    # 获取人脸图片线程
    getFaceImgThread = readFaceImage(base64Queue)
    getFaceImgThread.start()
    # threadManeger.append(getFaceImgThread)
    # 获取人脸表情线程
    getEmotionThread = face2emotion(base64Queue,emotionOutput_conn)
    getEmotionThread.start()
    # threadManeger.append(getEmotionThread)
    # 获取语音指令线程
    getSentenceThread = getSentence(wavRead_conn, instructionInput_conn)
    getSentenceThread.start()
    # threadManeger.append(getSentenceThread)
    # 播放音乐进程
    playMusicThread = playMusic(instructionOutput_conn, emotionOutput_conn)
    playMusicThread.start()
    # threadManeger.append(playMusicThread)

    # 显示UI.

    app = QApplication(sys.argv)
    trans = Trans()
    trans.show()

    # 录音线程
    recordWav(wavWrite_conn)

    # 开启子线程
    # for t in threadManeger:
    #     t.start()

    sys.exit(app.exec_())
