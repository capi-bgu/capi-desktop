import logging
import os

from src.Com import Com
from src.AbsBackend import AbsBackend
from src.NetworkLabeling import NetworkLabeling


class BackendStub(AbsBackend):

    def __init__(self, out_path="", resources_path="", log_path=""):
        super().__init__(out_path, resources_path, log_path)
        # self.com = Com(self)
        # self.labeler = NetworkLabeling(self.com.request_label)

    def set_label(self, label):
        self.labeler.set_label(label)  # use the com

    def download_face_model(self, url):
        logging.debug('downloading face model....')
        model_path = os.path.join(self.resources_path, "face_detection.dat")
        open(model_path, "w+")  # create empty file
        logging.debug("finished downloading")

    def run_core(self, request_label, num_sessions=0, session_duration=1, ask_freq=1,
                 use_camera=True, use_mouse=True, use_kb=True, use_metadata=True):
        logging.debug("Core is started")

    def stop_core(self):
        logging.debug("Core is stopped")
