import threading

import typer
from src.Logic import Logic
from src.Communication import Communication

app = typer.Typer()


@app.command()
def run(debug: bool = typer.Option(False, '--debug', '-d'),
        out_path: str = typer.Option("", "--out_path", "-op"),
        log_path: str = typer.Option("", '--log_path', '-lp'),
        resources_path: str = typer.Option("", '--resources_path', '-rp')):
    logic = Logic(out_path, resources_path, log_path, debug)
    com = Communication(logic)
    com.start_listen()


def run_backend(debug=False,
                out_path="",
                log_path="",
                resources_path=""):
    logic = Logic(out_path, resources_path, log_path, debug)
    com = Communication(logic)
    com.start_listen()


if __name__ == '__main__':
    app()
    # run_backend(debug=True, out_path=r"C:\Users\Hod\Desktop\bgu\Year4\project\CAPI_2.0\capi-desktop\backend\output",
    #             resources_path=r"C:\Users\Hod\Desktop\bgu\Year4\project\CAPI_2.0\capi-desktop\backend\resources")
