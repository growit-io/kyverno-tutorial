import json
import os
import subprocess
import yaml


charts_dir = os.path.join(os.path.dirname(__file__), "../../charts")


def helm(args, kubeconfig=None, **kwargs):
    if kubeconfig:
        args = (f"--kubeconfig={kubeconfig}", *args)

    if not "check" in kwargs:
        kwargs["check"] = True

    return subprocess.run(("helm", *args), **kwargs)


def helm_show_chart(chart_dir):
    args = ["show", "chart"]

    process = helm((*args, chart_dir), stdout=subprocess.PIPE, check=True)

    return yaml.full_load(process.stdout)


def helm_get_metadata(release_name, namespace=None, kubeconfig=None, **kwargs):
    args = ["get", "metadata", "--output=json"]

    if namespace:
        args.append(f"--namespace={namespace}")

    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.DEVNULL
    kwargs["check"] = False

    metadata = helm((*args, release_name), kubeconfig=kubeconfig, **kwargs)

    return json.loads(metadata.stdout) if metadata.returncode == 0 else None


def helm_install(
    release_name,
    chart_dir,
    namespace=None,
    create_namespace=False,
    production=False,
    wait=False,
    kubeconfig=None,
    **kwargs,
):
    args = ["install", "--dependency-update", "--atomic"]

    if namespace:
        args.append(f"--namespace={namespace}")

    if create_namespace:
        args.append("--create-namespace")

    if production and os.path.isfile(f"{chart_dir}/values-production.yaml"):
        args.extend([f"-f", f"{chart_dir}/values-production.yaml"])

    if wait:
        args.append("--wait")

    return helm((*args, release_name, chart_dir), kubeconfig=kubeconfig, **kwargs)


def helm_upgrade(
    release_name,
    chart_dir,
    namespace=None,
    production=False,
    wait=False,
    kubeconfig=None,
    **kwargs,
):
    args = ["upgrade", "--dependency-update", "--atomic"]

    args.append("--reset-values")

    if namespace:
        args.append(f"--namespace={namespace}")

    if production and os.path.isfile(f"{chart_dir}/values-production.yaml"):
        args.extend([f"-f", f"{chart_dir}/values-production.yaml"])

    if wait:
        args.append("--wait")

    return helm((*args, release_name, chart_dir), kubeconfig=kubeconfig, **kwargs)


def helm_install_or_upgrade(
    release_name,
    chart_name,
    create_namespace=False,
    namespace=None,
    production=False,
    wait=False,
    kubeconfig=None,
    force=None,
    **kwargs,
):
    chart_metadata = helm_show_chart(f"{charts_dir}/{chart_name}")

    release_metadata = helm_get_metadata(
        release_name, namespace=namespace, kubeconfig=kubeconfig
    )

    up_to_date = release_metadata and all(
        [release_metadata[k] == chart_metadata[k] for k in ("name", "version")]
    )

    if up_to_date and not force and release_metadata['status'] == 'deployed':
        print("Skipping", chart_metadata['name'], chart_metadata['version'], f"({release_metadata['status']})")
        return release_metadata

    kwargs = {
        "release_name": release_name,
        "chart_dir": f"{charts_dir}/{chart_name}",
        "namespace": namespace,
        "production": production,
        "wait": wait,
        "kubeconfig": kubeconfig,
        "stdout": subprocess.DEVNULL,
        **kwargs,
    }

    if release_metadata:
        fn = helm_upgrade
        print("Upgrading", chart_metadata['name'], release_metadata['version'], "->", chart_metadata['version'])
    else:
        fn = helm_install
        kwargs["create_namespace"] = create_namespace
        print("Installing", chart_metadata['name'], chart_metadata['version'])

    fn(**kwargs)

    return helm_get_metadata(release_name, namespace=namespace, kubeconfig=kubeconfig)
