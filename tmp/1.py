import websocket
from websocket import ABNF
import json
import _thread
import time

url = "ws://192.168.7.103:19999/demo/imserver/a_1"   # 接口地址
wav_path="D:/audio_file/001/001M26_01_01_0001.pcm"   #音频文件地址

def on_message(ws, message):
   print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("close connection")

def on_open(ws):
    def run(*args):
        content = {
            "mid": "1508232047195",
            "version": "1.0",
            "request": {
                "timestamp": 1508232047195,
                "sessionId": "aaaadsfasdfkop"
            },
            "params": {
                "audio": {
                    "audioType": "wav",
                    "sampleRate": 16000,
                    "channel": 1,
                    "sampleBytes": 2
                }
            }
        }
        ws.send(json.dumps(content))
        step = 3200 
        with open(wav_path, 'rb') as f:
            while True:
                read_data = f.read(step)
                if read_data:
                    ws.send(read_data, ABNF.OPCODE_BINARY)
                if len(read_data) < step:
                    break
                time.sleep(0.1)

        ws.send('', ABNF.OPCODE_BINARY)
        time.sleep(1.5)
        ws.close()
    _thread.start_new_thread(run, ())

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(url,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
