import subprocess
import os

cluster_name = "kyverno-tutorial"

kubeconfig = os.path.join(os.getcwd(), "kubeconfig")


def kind(*args, **kwargs):
    return subprocess.run(["kind", *args], check=True, **kwargs)


def create_cluster():
    clusters = kind('get', 'clusters', capture_output=True, text=True).stdout.split()

    if cluster_name in clusters:
        with open(kubeconfig, 'w') as f:
            process = kind(
                "get",
                "kubeconfig",
                "--name",
                cluster_name,
                stdout=subprocess.PIPE,
                text=True
            )
            f.write(process.stdout)
            return

    _ = kind(
        "create",
        "cluster",
        "--name",
        cluster_name,
        "--kubeconfig",
        kubeconfig,
    )


def delete_cluster():
    clusters = kind('get', 'clusters', capture_output=True, text=True).stdout.split()

    if cluster_name in clusters:
        kind("delete", "clusters", cluster_name)

    if os.path.isfile(kubeconfig):
        os.unlink(kubeconfig)
