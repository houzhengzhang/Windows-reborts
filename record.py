import random
import pyaudio
import wave
import threading

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
# 录音时间
RECORD_SECONDS = 5
p = pyaudio.PyAudio()


def recordWav(wavWrite_conn):
    """
    :param wavInputQueue: 存储录音文件的队列
    :return:
    """
    global timer

    WAVE_OUTPUT_FILENAME = "record/" + str(random.randint(0, 1000)) + ".wav"
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("* recording")
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    # print(type(frames[0]))
    print("* done recording")
    stream.stop_stream()
    stream.close()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    wavWrite_conn.send(WAVE_OUTPUT_FILENAME)
    timer = threading.Timer(5, recordWav, [wavWrite_conn])
    timer.start()


if __name__ == "__main__":
    # recordWav()
    pass