import requests
import json
import uuid
import base64
import urllib
from requests import HTTPError
from record_and_recognize import get_instruction
import queue
from multiprocessing import Process


class getSentence():
    def __init__(self, wavRead_conn, instructionInput_conn):
        self.getSentence = self.getWords()
        self.t = Process(target=self.run, args=[wavRead_conn, instructionInput_conn])

    def start(self):
        self.t.start()

    def run(self, wavRead_conn, instructionInput_conn):
        while True:
            try:
                wavPath = wavRead_conn.recv()

                sentence = self.getSentence(wavPath)
                print("cur sentence is {}".format(sentence))
                if sentence["state"] == True:
                    instruction = get_instruction(sentence['words'][0])
                    print("instruction is {}".format(instruction))
                    instructionInput_conn.send(instruction)
                # else:
                #     instructionInputQueue.put(0)


            except queue.Empty:
                print("wavOutputQueue is empty  timeout")
                pass

    def getWords(self):
        """
        获取token
        :return: 一串token，例如：token: 24.4800f01a96a885cc741bc6e79e2b61d3.2592000.1535162577.282335-11588713
        """
        baidu_server = "https://openapi.baidu.com/oauth/2.0/token?"
        grant_type = "client_credentials"
        client_id = "VBnqrZLfXB6BzY3O4iqn6Wvl"  # 填写API Key
        client_secret = "LwzMzMBcIZPBYb95tqVBjej7onm8oPp4"  # 填写Secret Key
        # 合成请求token的URL
        url = baidu_server + "grant_type=" + grant_type + "&client_id=" + client_id + "&client_secret=" + client_secret

        # 获取token
        res = urllib.request.urlopen(url).read()
        # print(res)
        data = json.loads(res.decode('utf-8'))
        token = data["access_token"]
        # return token
        url = "http://vop.baidu.com/server_api"
        rate = 16000

        def recognize(fileName):

            sig = open(fileName, "rb").read()

            speech_length = len(sig)
            # print(speech_length)
            speech = base64.b64encode(sig).decode("utf-8")
            mac_address = uuid.UUID(int=uuid.getnode()).hex[-12:]
            data = {
                "format": "wav",
                "rate": rate,
                "channel": 1,
                "cuid": mac_address,
                "token": token,
                # "lan": "zh",
                "len": speech_length,
                "speech": speech,
            }
            data_length = len(json.dumps(data).encode("utf-8"))
            headers = {"Content-Type": "application/json",
                       "Content-Length": str(data_length)}
            result = {}
            try:

                r = requests.post(url, data=json.dumps(data), headers=headers)

                r = r.json()

                if r["err_no"] == 0:
                    result["state"] = True
                    result["words"] = r["result"]
                else:

                    result["words"] = " "
                    result["state"] = False
                    print("nlp_api错误：:", r)

                # print(r)
            except HTTPError:
                r = requests.post(url, data=json.dumps(data), headers=headers)

                r = r.json()
                print("r: ", r)
                result["state"] = False
                result["words"] = ""

            return result

        return recognize
