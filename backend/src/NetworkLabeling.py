import time
import logging
from oratio.labeling.labeling_method.LabelMethod import LabelMethod


class NetworkLabeling(LabelMethod):

    def __init__(self, request_label):
        super().__init__()
        self.name = "GUI"
        self.request_label = request_label
        self.pending_for_label = False
        self.label = {"label": "default"}
        self.labeling = True

    def set_label(self, label):
        self.label = label
        self.pending_for_label = False

    def get_label(self):
        if not self.labeling:
            return self.label
        self.pending_for_label = True
        self.request_label()
        while self.pending_for_label:
            time.sleep(0.001)
        self.pending_for_label = False
        return self.label

    def stop_labeling(self):
        self.labeling = False
