import os
import logging
import pathlib
import requests
import warnings
from src.Com import Com
from threading import Thread
from oratio.Core import Core
from src.AbsBackend import AbsBackend
from src.NetworkLabeling import NetworkLabeling
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


class Backend(AbsBackend):

    def __init__(self, out_path="", resources_path="", log_path=""):
        super().__init__(out_path, resources_path, log_path)
        # self.labeler = NetworkLabeling(self.com.request_label)

    def download_face_model(self, url):
        logging.debug('downloading face model....')
        model_file_path = os.path.join(self.resources_path, "face_detection.dat")
        if not os.path.isfile(model_file_path):
            with open(model_file_path, 'wb') as f:
                model_data = requests.get(url).content
                f.write(model_data)
        logging.debug("finished downloading")

    def run_core(self, request_label_func, num_sessions=0, session_duration=1, ask_freq=1,
                 use_camera=True, use_mouse=True, use_kb=True, use_metadata=True):
        if self.core is not None and self.core.running and \
                self.core_thread is not None and self.core_thread.is_alive():
            logging.warning("Can't run a working core")
            warnings.warn("Can't run a working core")
            return

        camera_gatherer = {
            CameraCollector(fps=2, camera=0): {CameraProcessor(self.resources_path): [CameraDataHandler(self.out_path)]}
        }
        mouse_gatherer = {
            KeyboardCollector(): {KeyboardProcessor(): [KeyboardDataHandler(self.out_path)],
                                  IdentityProcessor(): [RawDataHandler("KeyboardRawData", self.out_path)]}
        }
        kb_gatherer = {
            MouseCollector(): {MouseProcessor(): [MouseDataHandler(self.out_path)],
                               IdentityProcessor(): [RawDataHandler("MouseRawData", self.out_path)]}
        }
        metadata_gatherer = {
            SessionMetaCollector(): {SessionMetaProcessor(self.resources_path): [SessionMetaDataHandler(self.out_path)],
                                     IdentityProcessor(): [RawDataHandler("MetaRawData", self.out_path)]}
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

        self.labeler = NetworkLabeling(request_label_func)
        label_methods = [self.labeler]

        constant_labeler = ConstantLabelManager(labeling_methods=label_methods, ask_freq=ask_freq)
        database_managers = [SqliteManager(self.out_path)]

        core = Core(data_gatherers, self.out_path,
                    num_sessions=num_sessions, session_duration=session_duration,
                    database_managers=database_managers, label_manager=constant_labeler)

        self.core = core

        self.core_thread = Thread(target=self.core.run)
        self.core_thread.start()

    def set_label(self, label):
        self.labeler.set_label(label)

    def stop_core(self):
        if self.core is None:
            logging.warning("In order to stop core you must first initialize core")
            warnings.warn("In order to stop core you must first initialize core")
        elif not self.core.running or self.core_thread is None or not self.core_thread.is_alive():
            logging.warning("Can't stop non-running core")
            warnings.warn("Can't stop non-running core")
        else:
            self.core.stop()
            self.core_thread.join()
            self.core_thread = None
