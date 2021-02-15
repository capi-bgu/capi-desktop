import os
import time
import pathlib
import unittest
import GuiRequests
from src.Logic import Logic


class LogicTest(unittest.TestCase):

    def setUp(self):
        self.test_path = str(pathlib.Path(__file__).parent.absolute())
        self.res_path = os.path.join(self.test_path, 'resources')
        self.output_path = os.path.join(self.test_path, 'output')
        self.log_path = self.output_path

        self.logic = Logic(self.output_path, self.res_path, self.log_path, debug=True)

    def tearDown(self):
        if self.logic.core_running():
            self.logic.stop_core()

        # shutil.rmtree(self.output_path, ignore_errors=True)
        # shutil.rmtree(self.res_path, ignore_errors=True)

    def __request_label(self):
        time.sleep(2)  # waiting for label
        self.logic.set_label({"label": 0})

    def test_download_face_model(self):
        self.assertFalse(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))
        self.logic.download_face_model(GuiRequests.DLIB_FACE_MODEL_URL)
        self.assertTrue(os.path.isfile(os.path.join(self.res_path, 'face_detection.dat')))

    def test_download_task_keywords(self):
        self.assertFalse(os.path.isfile(os.path.join(self.res_path, 'task_keywords.json')))
        self.logic.download_task_keywords(GuiRequests.TASK_KEYWORDS_URL)
        self.assertTrue(os.path.isfile(os.path.join(self.res_path, 'task_keywords.json')))

    def test_run_core(self):
        self.assertFalse(self.logic.core_running())
        self.logic.run_core(self.__request_label, num_sessions=5, session_duration=1, ask_freq=10,
                            use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        time.sleep(5)
        self.assertTrue(self.logic.core_running())

        self.assertWarns(UserWarning, self.logic.run_core, self.__request_label, 5, 1, 10, True, True, True, True)
        time.sleep(15)

        self.assertFalse(self.logic.core_running())
        self.logic.run_core(self.__request_label, num_sessions=10, session_duration=1, ask_freq=10,
                            use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        time.sleep(5)
        self.assertTrue(self.logic.core_running())
        time.sleep(15)

    def test_stop_core(self):
        self.assertWarns(UserWarning, self.logic.stop_core)
        self.logic.run_core(self.__request_label, num_sessions=20, session_duration=1, ask_freq=10,
                            use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        time.sleep(5)
        self.logic.stop_core()
        time.sleep(2)
        self.assertFalse(self.logic.core_running())
        self.assertWarns(UserWarning, self.logic.stop_core)

    def test_set_label(self):
        self.logic.run_core(self.__request_label, num_sessions=20, session_duration=1, ask_freq=10,
                            use_camera=True, use_mouse=True, use_kb=True, use_metadata=True)
        label = {"label": 0}
        self.logic.set_label(label)
        self.assertEqual(self.logic.labeler.label, label)
        self.logic.stop_core()


if __name__ == '__main__':
    unittest.main()
