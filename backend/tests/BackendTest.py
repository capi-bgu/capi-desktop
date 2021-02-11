import os
import time
import shutil
import pathlib
import unittest
from threading import Thread
from src.Backend import Backend
from tests.GuiStub import GuiStub


class BackendTest(unittest.TestCase):

    def setUp(self):
        self.gui_stub = GuiStub()
        Thread(target=self.gui_stub.connect_to_backend).start()

        self.test_path = str(pathlib.Path(__file__).parent.absolute())
        self.res_path = os.path.join(self.test_path, 'resources')
        self.output_path = os.path.join(self.test_path, 'output')

        self.backend = Backend(resources_path=self.res_path)

    def tearDown(self):
        self.backend.close_backend()
        self.gui_stub.close_gui()

        # shutil.rmtree(self.res_path, ignore_errors=True)
        shutil.rmtree(self.output_path, ignore_errors=True)

    def test_empty_run(self):
        time.sleep(5)

    def test_download_face_model(self):
        self.assertFalse(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))
        self.gui_stub.download_face_model()
        time.sleep(15)
        self.assertTrue(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))

    def test_init_core(self):
        self.assertFalse(os.path.isdir(self.output_path))
        self.assertFalse(os.path.isfile(os.path.join(self.output_path, 'capi_client.db')))
        self.gui_stub.init_core(out_path=self.test_path, num_sessions=10, session_duration=1, ask_freq=5,
                                use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        time.sleep(10)
        self.assertTrue(os.path.isdir(self.output_path))
        self.assertTrue(os.path.isfile(os.path.join(self.output_path, 'capi_client.db')))

    def test_run_core(self):
        pass

    def test_stop_core(self):
        pass

    def test_get_label(self):
        pass

    def test_request_label(self):
        pass

    def test_close_connection(self):
        self.gui_stub.close_connection()


if __name__ == '__main__':
    unittest.main()
