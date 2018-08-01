import base64
import cv2
import threading
from multiprocessing import Process,Manager

def cvimg2base64(cvimg):
    """
    :param cvimg:  opencv 的 mat 格式的图片
    :return:  base64 encode
    """
    retval, buffer = cv2.imencode('.jpg', cvimg)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text

class readFaceImage():
    def __init__(self, base64InputQueue):
        self.t = Process(target=self.run,args=[base64InputQueue])
    def start(self):
        self.t.start()
    def run(self, base64InputQueue):
        cap = cv2.VideoCapture(0)
        while True:
            # cap.read() 返回 bool值，每一帧的图像
            ret, img = cap.read()
            # 成功获取图像
            if ret:
                evt = Manager().Event()
                # cv2.cvtColor ( ) 颜色空间转换
                # start_time = time.time()
                rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # 将拍摄到的照片使用base64编码
                faceBase64 = cvimg2base64(rgb)
                base64InputQueue.put((faceBase64, evt))
                # wait for faceAPI
                evt.wait()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()