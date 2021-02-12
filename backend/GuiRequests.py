import json


DLIB_FACE_MODEL_URL = "https://drive.google.com/uc?export=download&id=1AilalzxfrUbFYxK-CbN5AGzZntQ5y9mR"

CLOSE_CONN = "close_connection"
DOWNLOAD_MODEL = "download_face_model"
RUN_CORE = "run_core"
STOP_CORE = "stop_core"
GET_LABEL = "get_label"
REQUEST_LABEL = "request_label"


def get_msg_from_type(msg):
    return {"type": msg}


def build_download_model_msg(url=DLIB_FACE_MODEL_URL):
    msg = get_msg_from_type(DOWNLOAD_MODEL)
    msg["url"] = url
    return build_pack(msg)


def build_run_core_msg(out_path="", num_sessions=0, session_duration=1, ask_freq=1,
                       use_camera=True, use_mouse=True, use_kb=True, use_metadata=True):
    msg = get_msg_from_type(RUN_CORE)
    msg["out_path"] = out_path
    msg["num_sessions"] = num_sessions
    msg["session_duration"] = session_duration
    msg["ask_freq"] = ask_freq
    msg["use_camera"] = use_camera
    msg["use_mouse"] = use_mouse
    msg["use_kb"] = use_kb
    msg["use_metadata"] = use_metadata
    return build_pack(msg)


def build_get_label_msg(label):
    msg = get_msg_from_type(GET_LABEL)
    msg["label"] = label
    return build_pack(msg)


def build_pack(msg):
    msg = json.dumps(msg)
    return msg.encode('utf-8')


def build_pack_type(msg):
    return build_pack(get_msg_from_type(msg))


def read_msg(msg):
    msg = msg.decode('utf-8')
    return json.loads(msg)
