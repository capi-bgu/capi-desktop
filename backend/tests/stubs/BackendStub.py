import os
import logging
import shutil

from src.AbsBackend import AbsBackend


class BackendStub(AbsBackend):
    def __init__(self, resources_path=""):
        shutil.rmtree(resources_path, ignore_errors=True)
        super().__init__("", resources_path, "")
        self.core_run = False
        self.label = None

    def download_face_model(self, url):
        logging.debug('downloading face_detection.dat....')

        model_path = os.path.join(self.resources_path, "face_detection.dat")
        with open(model_path, "w+") as f:
            pass  # create empty file
        logging.debug("finished downloading")

    def download_task_keywords(self, url):
        logging.debug('downloading face model....')
        model_path = os.path.join(self.resources_path, "task_keywords.json")
        with open(model_path, "w+") as f:
            pass  # create empty file
        logging.debug("finished downloading")

    def run_core(self, request_label_func, num_sessions=0, session_duration=1, ask_freq=1,
                 use_camera=True, use_mouse=True, use_kb=True, use_metadata=True):
        logging.debug("Core is started")
        self.core_run = True

    def stop_core(self):
        logging.debug("Core is stopped")
        self.core_run = False

    def set_label(self, label):
        self.label = label

    def core_running(self):
        return self.core_run
