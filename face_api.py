import requests
from json import JSONDecoder
import threading
import queue
from multiprocessing import Process

key = "PGtYXqZJGBqtV_hUNnlrb2snrL_pC2aF"
secret = "KV7_d2dq08SxtxWzgfeyY6LV2LWtRXUy"
url = "https://api-cn.faceplusplus.com/facepp/v3/detect"


def maxEmotion(emotion):
    """
    anger：愤怒
    disgust：厌恶
    fear：恐惧
    happiness：高兴
    neutral：平静
    sadness：伤心
    surprise：惊讶
    :param emotion:
    :return:返回可能性最大的表情
    """
    i = "neutral"
    for k in emotion.keys():
        if emotion[i] < emotion[k]:
            i = k
    # print(emotion[i])
    return i


def eyestatus(eye):
    """
    眼睛状态信息。返回值包含以下属性：
    left_eye_status：左眼的状态
    right_eye_status：右眼的状态
    每个属性都包含以下字段。每个字段的值都是一个浮点数，范围 [0,100]，小数点后 3 位有效数字。字段值的总和等于 100。

    occlusion：眼睛被遮挡
    no_glass_eye_open：不戴眼镜且睁眼
    normal_glass_eye_close：佩戴普通眼镜且闭眼
    normal_glass_eye_open：佩戴普通眼镜且睁眼
    dark_glasses：佩戴墨镜
    no_glass_eye_close：不戴眼镜且闭眼
    :param eye:
    :return:status[0]是左眼状态，status[1]是右眼状态
    """
    stauts = []
    for k in eye.keys():
        i = "no_glass_eye_open"
        for j in eye[k].keys():
            if eye[k][j] > eye[k][i]:
                i = j
        # print("III: ",i)
        stauts.append(i)
    return stauts


def face(imgBase64):
    """

    :param imgPath:
    :return:可以通过len(faces)得到几个人
    """
    data = {"api_key": key, "api_secret": secret, "image_base64": imgBase64,
            "return_attributes": "gender,age,smiling,ethnicity,eyegaze,eyestatus,emotion"}
    # print (type(file))
    response = requests.post(url=url, data=data)
    req_con = response.content.decode('utf-8')

    req_dict = JSONDecoder().decode(req_con)
    # print("Req_dict: ", req_dict)
    emotion = []
    try:
        for i in range(len(req_dict["faces"])):
            emotion.append(maxEmotion(req_dict["faces"][i]["attributes"]["emotion"]))
        return emotion
    except:
        emotion = []
        return emotion


class face2emotion():
    def __init__(self, base64OutputQueue, emotionInput_conn):
        self.running = True
        self.t = Process(target=self.run, args=[base64OutputQueue, emotionInput_conn])
        # 计数器  每 30 次向 playMusic 发送一次请求
        self.count = 0
        self.emotionRecord = {'anger': 0, 'disgust': 0, 'fear': 0, 'happiness': 0,
                              'neutral': 0, 'sadness': 0, 'surprise': 0}
        self.faceEmotiontuple = {'anger': 0,
                'disgust': 1,
                'fear': 2,
                'happiness': 3,
                'neutral': 4,
                'sadness': 5,
                'surprise': 6}

    def start(self ):
        self.t.start()
    def run(self, base64OutputQueue, emotionInput_conn):
        while self.running:
            try:
                # get data
                base64Img,evt = base64OutputQueue.get()
                # process the data
                emotionLabel = face(base64Img)
                if len(emotionLabel) != 0:
                    self.emotionRecord[emotionLabel[0]]+=1
                    self.count+=1
                    print("Emotion Label:{}".format(emotionLabel[0]))
                    print("count:{}".format(self.count))
                if self.count == 30 :
                    # 获取 60 个时间周期内 出现次数最多的表情的index
                    curEmotionIdx = max(self.emotionRecord,key=self.emotionRecord.get)
                    # 清空 重新统计
                    self.count = 0
                    self.emotionRecord = {'anger': 0, 'disgust': 0, 'fear': 0, 'happiness': 0,
                                          'neutral': 0, 'sadness': 0, 'surprise': 0}
                    # 向playMusic 发送当前 emotion
                    print("********self.faceEmotiontuple[curEmotionIdx]:{}".format(self.faceEmotiontuple[curEmotionIdx]))
                    emotionInput_conn.send(self.faceEmotiontuple[curEmotionIdx])
                    # inputEmotionQueue.put(self.faceEmotiontuple[curEmotionIdx])

                evt.set()

            except queue.Empty:
                pass


if __name__ == "__main__":
    print(face("11.jpg"))
