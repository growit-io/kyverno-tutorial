import json
import socket
import subprocess

from time import monotonic, sleep


def kubectl(args: list[str], kubeconfig: str, **kwargs):
    kwargs["check"] = True

    return subprocess.run(("kubectl", f"--kubeconfig={kubeconfig}", *args), **kwargs)


def apply(obj: dict, kubeconfig: str, namespace: str = None, **kwargs):
    kwargs["check"] = True

    subprocess.run(
        ("kubectl", f"--kubeconfig={kubeconfig}", "apply", "-f", "-"),
        input=json.dumps(obj),
        text=True,
        **kwargs
    )


def get(resource: str, kubeconfig: str, namespace: str = None):
    args = ["-o", "json"]

    if namespace:
        args.extend(("-n", namespace))

    pipe = kubectl(
        ["get", *args, resource], kubeconfig=kubeconfig, stdout=subprocess.PIPE
    )

    return json.loads(pipe.stdout)


def port_forward(
    resource: str,
    local_port: int,
    remote_port: int,
    kubeconfig: str,
    namespace: str = None,
):
    args = []

    if namespace:
        args.extend(("-n", namespace))

    subprocess.Popen(
        [
            "kubectl",
            "--kubeconfig",
            kubeconfig,
            "port-forward",
            *args,
            resource,
            f"{local_port}:{remote_port}",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    wait_port(local_port)


# https://dev.to/farcellier/wait-for-a-server-to-respond-in-python-488e
def wait_port(
    port: int, host: str = "localhost", timeout: int = None, attempt_every: int = 100
) -> None:
    """
    wait until a port would be open, for example the port 5432 for postgresql
    before going further

    >>> fixtup.helper.wait_port(5432, timeout=5000)

    :param port: port that has to be open
    :param remote_ip: host on which the port has to be open. It will be localhost by default
    :param timeout: timeout in ms before raising TimeoutError.
    :param attempt_every: time in ms between each attempt to check if the port is responding
    """
    start = monotonic()
    connected = False
    while not connected:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, port))
                connected = True
            except ConnectionRefusedError:
                if timeout is not None and monotonic() - start > (timeout / 1000):
                    raise TimeoutError()

        sleep(attempt_every / 1000)
