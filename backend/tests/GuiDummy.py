import os
import time
import logging
import pathlib
import unittest
from tests.stubs.GuiStub import GuiStub


class GuiDummy(unittest.TestCase):
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S')

    def setUp(self):
        self.test_path = str(pathlib.Path(__file__).parent.absolute())
        self.res_path = os.path.join(self.test_path, 'resources')

        self.gui_stub = GuiStub()
        self.gui_stub.connect_to_backend()
        time.sleep(2)

    def test_close_connection(self):
        time.sleep(1)
        self.gui_stub.close_gui()
        time.sleep(2)

    def test_download_face_model(self):
        self.gui_stub.download_face_model()
        time.sleep(2)
        self.gui_stub.close_gui()

    def test_download_task_keywords(self):
        self.gui_stub.download_task_keywords()
        time.sleep(2)
        self.gui_stub.close_gui()

    def test_run_core(self):
        self.gui_stub.run_core(out_path=self.test_path, num_sessions=5, session_duration=1, ask_freq=20,
                               use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        while not self.gui_stub.core_finished:
            time.sleep(0.001)
        self.gui_stub.close_gui()

    def test_stop_core(self):
        self.gui_stub.run_core(out_path=self.test_path, num_sessions=10, session_duration=1, ask_freq=20,
                               use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        time.sleep(2)
        self.gui_stub.stop_core()
        time.sleep(2)
        self.gui_stub.close_gui()

    def test_receive_label(self):
        self.gui_stub.send_label({"test": 0})
        time.sleep(1)
        self.gui_stub.close_gui()


if __name__ == '__main__':
    unittest.main()
