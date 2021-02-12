import os
import logging
import pathlib
from abc import ABC, abstractmethod


class AbsBackend(ABC):

    def __init__(self, out_path="", resources_path="", log_path=""):
        super().__init__()

        self.core = None
        self.core_thread = None

        self.curr_dir = pathlib.Path(__file__).parent.absolute()

        if log_path == "":
            log_path = self.curr_dir
        self.log_path = log_path
        if not os.path.isdir(self.log_path):
            os.mkdir(self.log_path)

        if resources_path == "":
            resources_path = self.curr_dir
        self.resources_path = resources_path
        if not os.path.isdir(self.resources_path):
            os.mkdir(self.resources_path)

        if out_path == "":
            out_path = self.curr_dir
        self.out_path = os.path.join(out_path, 'output')
        if not os.path.isdir(self.out_path):
            os.mkdir(self.out_path)

        logging.basicConfig(level=logging.DEBUG,  # filename=os.path.join(self.log_path, "capi-run.log"),
                            format='%(asctime)s - %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    @abstractmethod
    def download_face_model(self, url):
        pass

    @abstractmethod
    def set_label(self, label):
        pass

    @abstractmethod
    def run_core(self, request_label_func, num_sessions=0, session_duration=1, ask_freq=1,
                 use_camera=True, use_mouse=True, use_kb=True, use_metadata=True):
        pass

    @abstractmethod
    def stop_core(self):
        pass
