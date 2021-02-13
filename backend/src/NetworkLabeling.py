import time
import GuiRequests
from oratio.labeling.labeling_method.LabelMethod import LabelMethod


class NetworkLabeling(LabelMethod):

    def __init__(self, request_label):
        super().__init__()
        self.name = "GUI"
        self.request_label = request_label
        self.pending_for_label = False

    def set_label(self, label):
        self.label = label
        self.pending_for_label = False

    def get_label(self):
        self.pending_for_label = True
        self.request_label()
        while self.pending_for_label:
            time.sleep(0.001)
        self.pending_for_label = False
        # return super().get_label()
        return self.label
