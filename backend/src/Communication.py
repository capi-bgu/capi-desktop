import socket
import logging
import warnings
import GuiRequests
from src.AbsLogic import AbsLogic


class Communication:
    HOST = '127.0.0.1'
    PORT = 9867
    BUFFER = 1024

    def __init__(self, logic: AbsLogic):
        self.logic = logic
        self.listening = False

    def start_listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(1)
        logging.info("waiting for ui connection...")
        self.gui_sock, _ = self.sock.accept()
        logging.info("ui connected")

        self.listening = True
        logging.info("Communication thread initiated")
        self.listen()

    def request_label(self):
        logging.info("requesting label....")
        if self.listening:
            self.gui_sock.send(GuiRequests.build_pack_type(GuiRequests.REQUEST_LABEL))

    def listen(self):
        self.gui_sock.settimeout(1)
        logging.info("Communication started to listen")
        while self.listening:
            try:
                request = self.gui_sock.recv(self.BUFFER)
            except socket.timeout:
                continue
            if not request:
                logging.info("ui disconnected")
                break
            request = GuiRequests.read_msg(request)
            logging.info("Request received")
            if request["type"] == GuiRequests.DOWNLOAD_FACE_MODEL:
                logging.info("download face model request")
                self.logic.download_face_model(request["url"])
            elif request["type"] == GuiRequests.DOWNLOAD_TASK_KEYWORDS:
                logging.info("download task keywords request")
                self.logic.download_task_keywords(request["url"])
            elif request["type"] == GuiRequests.RUN_CORE:
                logging.info("run core request")
                self.logic.run_core(self.request_label, self.core_end_callback, request["num_sessions"],
                                    request["session_duration"],request["ask_freq"],
                                    request["use_camera"], request["use_mouse"],
                                    request["use_kb"], request["use_metadata"])
            elif request["type"] == GuiRequests.STOP_CORE:
                logging.info("stop core request")
                self.logic.stop_core()
            elif request["type"] == GuiRequests.LABEL:
                logging.info("label answer received")
                self.logic.set_label(request["label"])
            elif request["type"] == GuiRequests.CLOSE_CONN:
                break
            elif request["type"] == GuiRequests.UNKNOWN:
                logging.warning("unrecognized package received.")
                warnings.warn("unrecognized package received.")
            else:
                print(request)
                logging.warning("unrecognized package received.")
                warnings.warn("unrecognized package received.")
        self.close_communication()

    def core_end_callback(self):
        logging.info("core finished all it's sessions!")
        self.gui_sock.send(GuiRequests.build_pack_type(GuiRequests.CORE_FINISHED))

    def close_communication(self):
        logging.info("closing communications")
        self.listening = False
        self.gui_sock.close()
        self.sock.close()
        self.logic.stop_core()
        logging.info("communications closed")
