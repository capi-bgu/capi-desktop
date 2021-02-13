import socket
import logging
import warnings
import GuiRequests
from threading import Thread
from src.AbsBackend import AbsBackend


class Com:
    HOST = '127.0.0.1'
    PORT = 10000
    BUFFER = 1024

    def __init__(self, backend: AbsBackend):
        self.backend = backend
        self.listening = False

    def start_listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(1)
        logging.debug("waiting for ui connection...")
        self.gui_sock, _ = self.sock.accept()
        logging.debug("ui connected")

        self.listening = True
        self.listener = Thread(target=self.listen)
        self.listener.start()
        logging.debug("Com thread initiated")

    def request_label(self):
        self.gui_sock.send(GuiRequests.build_pack_type(GuiRequests.REQUEST_LABEL))

    def listen(self):
        self.gui_sock.settimeout(1)
        logging.debug("Com started to listen")
        while self.listening:
            try:
                request = self.gui_sock.recv(self.BUFFER)
            except socket.timeout:
                continue
            request = GuiRequests.read_msg(request)
            logging.debug("I got a request")
            if request["type"] == GuiRequests.DOWNLOAD_FACE_MODEL:
                logging.debug("download face model request")
                self.backend.download_face_model(request["url"])
            elif request["type"] == GuiRequests.DOWNLOAD_TASK_KEYWORDS:
                logging.debug("download task keywords request")
                self.backend.download_task_keywords(request["url"])
            elif request["type"] == GuiRequests.RUN_CORE:
                logging.debug("run core request")
                self.backend.run_core(self.request_label, request["num_sessions"], request["session_duration"],
                                      request["ask_freq"], request["use_camera"], request["use_mouse"],
                                      request["use_kb"], request["use_metadata"])
            elif request["type"] == GuiRequests.STOP_CORE:
                logging.debug("stop core request")
                self.backend.stop_core()
            elif request["type"] == GuiRequests.LABEL:
                logging.debug("label answer received")
                self.backend.set_label(request["label"])
            elif request["type"] == GuiRequests.CLOSE_CONN:
                self.close_com()
            elif request["type"] == GuiRequests.UNKNOWN:
                logging.warning("unrecognized package received.")
                warnings.warn("unrecognized package received.")
            else:
                logging.warning("unrecognized package received.")
                warnings.warn("unrecognized package received.")

    def close_com(self):
        logging.debug("closing communications")
        self.listening = False
        # self.listener.join()
        self.gui_sock.close()
        self.sock.close()
        self.backend.stop_core()
        logging.debug("communications closed")
