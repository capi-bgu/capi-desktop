import os
import time
import shutil
import pathlib
import unittest
from src.Com import Com
from threading import Thread
from tests.stubs.GuiStub import GuiStub
from tests.stubs.BackendStub import BackendStub


class ComTest(unittest.TestCase):

    def setUp(self):
        self.test_path = str(pathlib.Path(__file__).parent.absolute())
        self.res_path = os.path.join(self.test_path, 'resources')

        self.backend = BackendStub(self.res_path)
        self.com = Com(self.backend)
        Thread(target=self.com.start_listen).start()  # com listener

        self.gui_stub = GuiStub()
        self.gui_stub.connect_to_backend()

    def tearDown(self):
        self.gui_stub.close_gui()
        self.com.close_com()

    def test_empty_run(self):
        time.sleep(5)

    def test_download_face_model(self):
        self.assertFalse(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))
        self.gui_stub.download_face_model()
        time.sleep(2)
        self.assertTrue(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))

    def test_download_face_model(self):
        self.assertFalse(os.path.isfile(os.path.join(self.res_path, 'task_keywords.json')))
        self.gui_stub.download_task_keywords()
        time.sleep(2)
        self.assertTrue(os.path.isfile(os.path.join(self.res_path, 'task_keywords.json')))

    def test_run_core(self):
        self.assertFalse(self.backend.core_running())
        self.gui_stub.run_core(out_path=self.test_path, num_sessions=10, session_duration=1, ask_freq=5,
                               use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        time.sleep(1)
        self.assertTrue(self.backend.core_running())

    def test_stop_core(self):
        self.gui_stub.run_core(out_path=self.test_path, num_sessions=10, session_duration=1, ask_freq=5,
                               use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        time.sleep(1)
        self.assertTrue(self.backend.core_running())
        self.gui_stub.stop_core()
        time.sleep(1)
        self.assertFalse(self.backend.core_running())

    def test_receive_label(self):
        self.assertIsNone(self.backend.label)
        self.gui_stub.send_label({"test": 0})
        time.sleep(1)
        self.assertIsNotNone(self.backend.label)
        self.assertEqual(self.backend.label, {"test": 0})

    def test_request_label(self):
        self.assertIsNone(self.backend.label)
        self.com.request_label()
        time.sleep(3)
        self.assertIsNotNone(self.backend.label)
        print(self.backend.label)

    def test_close_connection(self):
        self.assertTrue(self.com.listening)
        self.assertTrue(self.com.listener.is_alive())
        self.gui_stub.close_connection()
        time.sleep(2)
        self.assertFalse(self.com.listening)
        self.assertFalse(self.com.listener.is_alive())


if __name__ == '__main__':
    unittest.main()
