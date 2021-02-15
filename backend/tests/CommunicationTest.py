import os
import time
import logging
import pathlib
import unittest
from threading import Thread
from tests.stubs.GuiStub import GuiStub
from src.Communication import Communication
from tests.stubs.LogicStub import LogicStub


class CommunicationTest(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    def setUp(self):
        self.test_path = str(pathlib.Path(__file__).parent.absolute())
        self.res_path = os.path.join(self.test_path, 'resources')

        self.logic = LogicStub(self.res_path)
        self.com = Communication(self.logic)
        Thread(target=self.com.start_listen).start()  # com listener

        self.gui_stub = GuiStub()
        self.gui_stub.connect_to_backend()

    def test_close_connection(self):
        time.sleep(1)
        self.assertTrue(self.com.listening)
        self.gui_stub.close_gui()
        time.sleep(2)
        self.assertFalse(self.com.listening)
        self.assertFalse(self.com.logic.core_running())

    def test_download_face_model(self):
        self.assertFalse(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))
        self.gui_stub.download_face_model()
        time.sleep(2)
        self.assertTrue(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))
        self.gui_stub.close_gui()

    def test_download_task_keywords(self):
        self.assertFalse(os.path.isfile(os.path.join(self.res_path, 'task_keywords.json')))
        self.gui_stub.download_task_keywords()
        time.sleep(2)
        self.assertTrue(os.path.isfile(os.path.join(self.res_path, 'task_keywords.json')))
        self.gui_stub.close_gui()

    def test_run_core(self):
        self.assertFalse(self.logic.core_running())
        self.gui_stub.run_core(out_path=self.test_path, num_sessions=5, session_duration=1, ask_freq=10,
                               use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        time.sleep(1)
        self.assertTrue(self.logic.core_running())
        self.gui_stub.close_gui()

    def test_stop_core(self):
        self.gui_stub.run_core(out_path=self.test_path, num_sessions=10, session_duration=1, ask_freq=10,
                               use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        time.sleep(1)
        self.assertTrue(self.logic.core_running())
        self.gui_stub.stop_core()
        time.sleep(1)
        self.assertFalse(self.logic.core_running())
        self.gui_stub.close_gui()

    def test_receive_label(self):
        self.assertIsNone(self.logic.label)
        self.gui_stub.send_label({"test": 0})
        time.sleep(1)
        self.assertIsNotNone(self.logic.label)
        self.assertEqual(self.logic.label, {"test": 0})
        self.gui_stub.close_gui()

    def test_request_label(self):
        self.assertIsNone(self.logic.label)
        self.com.request_label()
        time.sleep(3)
        self.assertIsNotNone(self.logic.label)
        self.gui_stub.close_gui()


if __name__ == '__main__':
    unittest.main()
