import os
import socket
import logging
import pathlib
import requests
import GuiRequests
from threading import Thread
from oratio.Core import Core
from src.GuiLabeling import GuiLabeling
from oratio.processing.MouseProcessor import MouseProcessor
from oratio.collection.MouseCollector import MouseCollector
from oratio.collection.CameraCollector import CameraCollector
from oratio.processing.CameraProcessor import CameraProcessor
from oratio.database.sqlite_db.SqliteManager import SqliteManager
from oratio.collection.KeyboardCollector import KeyboardCollector
from oratio.processing.KeyboardProcessor import KeyboardProcessor
from oratio.processing.IdentityProcessor import IdentityProcessor
from oratio.database.sqlite_db.RawDataHandler import RawDataHandler
from oratio.labeling.ConstantLabelManager import ConstantLabelManager
from oratio.database.sqlite_db.MouseDataHandler import MouseDataHandler
from oratio.collection.SessionMetaCollector import SessionMetaCollector
from oratio.processing.SessionMetaProcessor import SessionMetaProcessor
from oratio.database.sqlite_db.CameraDataHandler import CameraDataHandler
from oratio.database.sqlite_db.KeyboardDataHandler import KeyboardDataHandler
from oratio.database.sqlite_db.SessionMetaDataHandler import SessionMetaDataHandler


class Backend:
    HOST = '127.0.0.1'
    PORT = 10000
    BUFFER = 1024

    def __init__(self, resources_path="", log_path=""):
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

        logging.basicConfig(level=logging.DEBUG,  # filename=os.path.join(self.log_path, "capi-run.log"),
                            format='%(asctime)s - %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, self.PORT))
        self.sock.listen(1)
        logging.debug("waiting for ui connection...")
        self.gui_sock, _ = self.sock.accept()
        logging.debug("ui connected")

        self.gui_sock.settimeout(1)
        self.listening = True
        self.listener = Thread(target=self.listen)
        self.listener.start()
        logging.debug("Backend thread initiated")

        self.labeler = GuiLabeling(self.gui_sock)

    def listen(self):
        logging.debug("backend started to listen")
        while self.listening:
            try:
                request = self.gui_sock.recv(self.BUFFER)
            except socket.timeout:
                continue
            request = GuiRequests.read_msg(request)
            logging.debug("I got a request")
            if request["type"] == GuiRequests.DOWNLOAD_MODEL:
                logging.debug("I need to download")
                self.download_face_model(request["url"])
            elif request["type"] == GuiRequests.INIT_CORE:
                self.init_core(request["out_path"], request["num_sessions"], request["session_duration"],
                               request["ask_freq"], request["use_camera"], request["use_mouse"],
                               request["use_kb"], request["use_metadata"])
            elif request["type"] == GuiRequests.RUN_CORE:
                self.run_core()
            elif request["type"] == GuiRequests.STOP_CORE:
                self.stop_core()
            elif request["type"] == GuiRequests.GET_LABEL:
                self.labeler.set_label(request["label"])
            elif request["type"] == GuiRequests.CLOSE_CONN:
                break
            else:
                logging.error("unrecognized package received.")

    def download_face_model(self, url):
        logging.debug('downloading face model....')
        model_file_path = os.path.join(self.resources_path, "face_detection.dat")
        if not os.path.isfile(model_file_path):
            with open(model_file_path, 'wb') as f:
                model_data = requests.get(url).content
                f.write(model_data)
        logging.debug("finished downloading")

    def init_core(self, out_path="", num_sessions=0, session_duration=1, ask_freq=1,
                  use_camera=True, use_mouse=True, use_kb=True, use_metadata=True):
        if out_path == "":
            out_path = self.curr_dir
        out_path = os.path.join(out_path, 'output')
        if not os.path.isdir(out_path):
            os.mkdir(out_path)

        camera_gatherer = {
            CameraCollector(fps=2, camera=0): {CameraProcessor(self.resources_path): [CameraDataHandler(out_path)]}
        }
        mouse_gatherer = {
            KeyboardCollector(): {KeyboardProcessor(): [KeyboardDataHandler(out_path)],
                                  IdentityProcessor(): [RawDataHandler("KeyboardRawData", out_path)]}
        }
        kb_gatherer = {
            MouseCollector(): {MouseProcessor(): [MouseDataHandler(out_path)],
                               IdentityProcessor(): [RawDataHandler("MouseRawData", out_path)]}
        }
        metadata_gatherer = {
            SessionMetaCollector(): {SessionMetaProcessor(self.resources_path): [SessionMetaDataHandler(out_path)],
                                     IdentityProcessor(): [RawDataHandler("MetaRawData", out_path)]}
        }

        data_gatherers = {}
        if use_camera:
            data_gatherers.update(camera_gatherer)
        if use_mouse:
            data_gatherers.update(mouse_gatherer)
        if use_kb:
            data_gatherers.update(kb_gatherer)
        if use_metadata:
            data_gatherers.update(metadata_gatherer)

        label_methods = [self.labeler]

        constant_labeler = ConstantLabelManager(label_methods, ask_freq=ask_freq)
        database_managers = [SqliteManager(out_path)]

        core = Core(data_gatherers, out_path,
                    num_sessions=num_sessions, session_duration=session_duration,
                    database_managers=database_managers, label_manager=constant_labeler)

        self.core = core

    def run_core(self):
        if self.core is None:
            logging.error("In order to run core you must first initialize core")
        elif self.core.running and self.core_thread is None:
            logging.error("Can't run a working core")
        else:
            self.core_thread = Thread(target=self.core.run)
            self.core_thread.start()

    def stop_core(self):
        if self.core is None:
            logging.error("In order to stop core you must first initialize core")
        elif not self.core.running or self.core_thread is None or not self.core_thread.is_alive():
            logging.error("Can't stop non-running core")
        else:
            self.core.stop()
            self.core_thread.join()
            self.core_thread = None

    def close_backend(self):
        logging.debug("closing backend")
        self.listening = False
        self.stop_core()
        self.listener.join()
        self.sock.close()
        logging.debug("backend closed")
