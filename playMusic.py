import threading
import pygame
from wypc import *
import queue
from multiprocessing  import Process


class playMusic():
    def __init__(self, instructionInput_conn,emotionOutput_conn):
        self.t = Process(target=self.run,args=[instructionInput_conn,emotionOutput_conn])
        self.musicRadio = music()
        self.currentEmotionIdx = 4
        self.currentInstruction = 0

    def run(self, instructionInput_conn,emotionOutput_conn):
        while True:
            try:
                newInstruction = instructionInput_conn.revc()
                self.currentEmotionIdx = newInstruction
                print("--newInstruction :{}".format(newInstruction))
            except queue.Empty:
                pass
            try:
                newEmotionIdx = emotionOutput_conn.revc()
                self.currentEmotionIdx = newEmotionIdx
            except queue.Empty:
                pass
            print("currentInstruction:   {},currentEmotionIdx:   {}".format(self.currentInstruction,self.currentEmotionIdx))
            # 修改音乐播放状态
            self.__radioEvent(self.currentInstruction, self.currentEmotionIdx)
            # 清空指令状态
            self.currentInstruction = 0

    def start(self):
        self.t.start()

    def __radioEvent(self, instruction, emotionIdx):
        # 开始播放音乐
        if instruction == 0:
            self.musicRadio.load(self.__chooseSong(emotionIdx))
            self.musicRadio.play()
        # 停止播放音乐
        elif instruction == 1:
            self.musicRadio.stop()
        # 播放下一首音乐
        elif instruction == 2:
            self.musicRadio.nextMusic(self.__chooseSong(emotionIdx))
        # 播放上一首音乐
        elif instruction == 3:
            self.musicRadio.preMusic()
        # 暂停播放音乐
        elif instruction == 4:
            self.musicRadio.pause()
        # 重新开始播放音乐
        elif instruction == 5:
            self.musicRadio.restart()

    def __chooseSong(self, emotionIdx):
        allEmotion = {0: ["安静", "放松"],
                      1: ["治愈", "孤独", "伤感"],
                      2: ["安静", "放松"],
                      3: ["快乐", "感动", "浪漫", "兴奋"],
                      4: ["清新", "放松", "安静"],
                      5: ["治愈", "孤独", "伤感"],
                      6: ["快乐", "感动", "浪漫", "兴奋"]}
        targetEmotion = allEmotion[emotionIdx]
        tar = random.randint(0, len(targetEmotion) - 1)
        targetType = targetEmotion[tar]
        # song是个列表，第一个参数是song[0]是name,song[1]是歌曲url
        song = loadMusic(targetType)
        print(song)  # ['大梦初醒 Awaken ', '[图片]http://music.163.com/song/media/outer/url?id=493283507.mp3']
        return song


class music:
    def __init__(self):
        self.pm = pygame.mixer
        self.pm.init()
        self.musicPos = 0.0
        self.stack1 = []  # 歌曲栈, 存当前和播放过的

    def load(self, music, musicPath=""):
        if len(music) != 0:
            self.download(music)
            print("song/" + music[0] + ".mp3")
            self.pm.music.load("song/" + music[0] + ".mp3")
            self.stack1.append("song/" + music[0] + ".mp3")
        elif musicPath != "":
            self.pm.music.load(musicPath)

    def play(self):
        self.pm.music.play(loops=1, start=0.0)
        self.pm.music.set_volume(0.5)  # ——  参数0-1设置音量
        # time.sleep(40)

    def stop(self):
        self.pm.music.stop()

    def pause(self):
        self.pm.music.get_pos()
        self.pm.music.pause()

    def restart(self):
        self.pm.music.play(start=self.musicPos)

    def preMusic(self):
        self.stop()
        # self.stack1.pop()
        musicPath = self.stack1[-1]
        self.load([], musicPath)
        self.play()

    def nextMusic(self, music):
        """
        :param music:
        :return:
        """
        self.stop()
        # self.stack1.append(musicPath)
        self.load(music)
        self.play()

    def download(self, music):
        import urllib.request
        print(music)
        urllib.request.urlretrieve(music[1], "song/" + music[0] + ".mp3")
        print("downss")


if __name__ == "__main__":
    m = music()
    m.load(choseSong("anger"))
    m.play()
    m.stop()
    print("finish1")
    m.preMusic()
    m.stop()
    print("finish2")
    m.nextMusic(['What If', '[图片]http://music.163.com/song/media/outer/url?id=1217607.mp3'])
    m.stop()
    print("finish3")
