import time
import socket
import logging
import GuiRequests
from threading import Thread


class GuiStub:

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 9867
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(1)
        self.listener = Thread(target=self.listen)
        self.running = True
        self.core_finished = False

    def connect_to_backend(self):
        self.sock.connect((self.host, self.port))
        logging.debug("connected to Communication")
        self.listener.start()

    def listen(self):
        logging.debug("ui started to listen")
        while self.running:
            try:
                request = self.sock.recv(1024)
            except socket.timeout:
                continue
            if not request:
                logging.debug("backend disconnected")
                break
            request = GuiRequests.read_msg(request)
            if request["type"] == GuiRequests.REQUEST_LABEL:
                time.sleep(2)
                label = {"categorical": 5, "VAD": {"Valance": 2, "Arousal": -3, "Dominance": 4}}
                self.send_label(label)
            if request["type"] == GuiRequests.CORE_FINISHED:
                self.core_finished = True

    def close_gui(self):
        logging.debug("closing gui")
        self.sock.send(GuiRequests.build_pack_type(GuiRequests.CLOSE_CONN))
        self.running = False
        self.listener.join()
        self.sock.close()

    def download_face_model(self, url=GuiRequests.DLIB_FACE_MODEL_URL):
        self.sock.send(GuiRequests.build_download_model_msg(url))
        logging.debug("I sent download model msg")

    def download_task_keywords(self, url=GuiRequests.TASK_KEYWORDS_URL):
        self.sock.send(GuiRequests.build_download_task_keywords_msg(url))
        logging.debug("I sent download model msg")

    def run_core(self, out_path, num_sessions, session_duration, ask_freq,
                 use_camera, use_mouse, use_kb, use_metadata):
        self.sock.send(GuiRequests.build_run_core_msg(out_path, num_sessions,
                                                      session_duration, ask_freq,
                                                      use_camera, use_mouse, use_kb, use_metadata))

    def stop_core(self):
        self.sock.send(GuiRequests.build_pack_type(GuiRequests.STOP_CORE))

    def send_label(self, label):
        self.sock.send(GuiRequests.build_label_msg(label))