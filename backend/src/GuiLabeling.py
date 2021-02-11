import time
import GuiRequests
from oratio.labeling.labeling_method.LabelMethod import LabelMethod


class GuiLabeling(LabelMethod):

    def __init__(self, gui_sock):
        super().__init__()
        self.name = "GUI"
        self.gui_sock = gui_sock
        self.pending_for_label = False

    def set_label(self, label):
        self.label = label
        self.pending_for_label = False

    def get_label(self):
        self.gui_sock.send(GuiRequests.build_pack_type(GuiRequests.REQUEST_LABEL))
        self.pending_for_label = True
        while self.pending_for_label:
            time.sleep(0.001)
        self.pending_for_label = False
        return super().get_label()
