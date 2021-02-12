import os
import time
import shutil
import pathlib
import unittest
import GuiRequests
from src.Backend import Backend
from src.NetworkLabeling import NetworkLabeling


class BackendTest(unittest.TestCase):

    def setUp(self):
        self.test_path = str(pathlib.Path(__file__).parent.absolute())
        self.res_path = os.path.join(self.test_path, 'resources')
        self.output_path = os.path.join(self.test_path, 'output')
        self.log_path = self.output_path

        self.backend = Backend(self.output_path, self.res_path, self.log_path)

    def tearDown(self):
        self.backend.stop_core()

        # shutil.rmtree(self.res_path, ignore_errors=True)
        shutil.rmtree(self.output_path, ignore_errors=True)

    def __request_label(self):
        time.sleep(2)  # waiting for label
        self.backend.set_label({"label": 0})

    def test_set_label(self):
        self.backend.run_core(self.__request_label, num_sessions=10, session_duration=1, ask_freq=5,
                              use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        label = {"label": 0}
        self.backend.set_label(label)
        self.assertEqual(self.backend.labeler.label, label)

    def test_download_face_model(self):
        self.assertFalse(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))
        self.backend.download_face_model(GuiRequests.DLIB_FACE_MODEL_URL)
        self.assertTrue(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))

    def test_run_core(self):
        self.backend.run_core(self.__request_label, num_sessions=10, session_duration=1, ask_freq=5,
                              use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)  # suppose to be ok
        self.assertTrue(self.backend.core.running)
        self.assertTrue(self.backend.core_thread is not None)
        self.assertTrue(self.backend.core_thread.is_alive())
        time.sleep(10)

    def test_stop_core(self):
        self.backend.run_core(self.__request_label, num_sessions=10, session_duration=1, ask_freq=5,
                              use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)  # suppose to be ok
        time.sleep(1)
        self.backend.stop_core()
        self.assertFalse(self.backend.core.running)
        self.assertTrue(self.backend.core_thread is None)


if __name__ == '__main__':
    unittest.main()
