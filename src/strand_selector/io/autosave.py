import json


def save_session(session, output_path):

    payload = {
        "pdf_path": session.pdf_path,
        "current_index": session.current_index,
        "annotations": session.annotations,
    }

    with open(output_path, "w") as handle:
        json.dump(payload, handle, indent=2)


def load_session(path):

    with open(path) as handle:
        return json.load(handle)
