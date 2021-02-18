import os
import logging
import requests
import warnings
from threading import Thread
from oratio.Core import Core
from src.NetworkLabeling import NetworkLabeling
from src.AbsLogic import AbsLogic, default_core_callback
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


class Logic(AbsLogic):

    def __init__(self, out_path="", resources_path="", log_path="", debug=False):
        super().__init__(out_path, resources_path, log_path, debug)

    def download_face_model(self, url):
        self.__download_from_url(url, "face_detection.dat")

    def download_task_keywords(self, url):
        self.__download_from_url(url, "task_keywords.json")

    def __download_from_url(self, url, file_name):
        logging.info(f'downloading {file_name}....')
        model_file_path = os.path.join(self.resources_path, file_name)
        if not os.path.isfile(model_file_path):
            with open(model_file_path, 'wb') as f:
                model_data = requests.get(url).content
                f.write(model_data)
        logging.info("finished downloading")

    def run_core(self, request_label_func, core_end_callback=default_core_callback, num_sessions=0,
                 session_duration=1, ask_freq=1, use_camera=True, use_mouse=True, use_kb=True, use_metadata=True):
        if self.core_running():
            logging.warning("Can't run a working core")
            warnings.warn("Can't run a working core")
            return

        data_gatherers = {}
        if use_camera:
            camera_gatherer = {
                CameraCollector(fps=2, camera=0): {
                    CameraProcessor(self.resources_path): [CameraDataHandler(self.out_path)]}
            }
            data_gatherers.update(camera_gatherer)
        if use_mouse:
            mouse_gatherer = {
                MouseCollector(): {MouseProcessor(): [MouseDataHandler(self.out_path)],
                                   IdentityProcessor(): [RawDataHandler("MouseRawData", self.out_path)]}
            }
            data_gatherers.update(mouse_gatherer)
        if use_kb:
            kb_gatherer = {
                KeyboardCollector(): {KeyboardProcessor(): [KeyboardDataHandler(self.out_path)],
                                      IdentityProcessor(): [RawDataHandler("KeyboardRawData", self.out_path)]}
            }
            data_gatherers.update(kb_gatherer)
        if use_metadata:
            metadata_gatherer = {
                SessionMetaCollector(): {
                    SessionMetaProcessor(self.resources_path): [SessionMetaDataHandler(self.out_path)],
                    IdentityProcessor(): [RawDataHandler("MetaRawData", self.out_path)]}
            }
            data_gatherers.update(metadata_gatherer)

        self.labeler = NetworkLabeling(request_label_func)
        label_methods = [self.labeler]

        constant_labeler = ConstantLabelManager(labeling_methods=label_methods, ask_freq=ask_freq)
        database_managers = [SqliteManager(self.out_path)]

        core = Core(data_gatherers, self.out_path,
                    num_sessions=num_sessions, session_duration=session_duration,
                    database_managers=database_managers, label_manager=constant_labeler)

        self.core = core

        self.core_thread = Thread(target=self.__run_core, args=(core_end_callback,), name="core")
        self.core_thread.start()

    def __run_core(self, callback):
        self.core.run()
        if self.core.finished:
            callback()

    def stop_core(self):
        if self.core is None:
            logging.warning("In order to stop core you must first initialize core")
            warnings.warn("In order to stop core you must first initialize core")
        elif not self.core_running():
            logging.warning("Can't stop non-running core")
            warnings.warn("Can't stop non-running core")
        else:
            Thread(target=self.__stop_core, name="stop_core").start()

    def __stop_core(self):
        logging.info("stopping core....")
        self.labeler.stop_labeling()
        self.core.stop()
        self.core_thread.join()
        self.core_thread = None
        logging.info("core stopped")

    def set_label(self, label):
        if self.core_running():
            self.labeler.set_label(label)
        else:
            logging.error("Can't receive label before run the core")

    def core_running(self):
        return self.core is not None and self.core.running and \
               self.core_thread is not None and self.core_thread.is_alive()
