import base64
import click
import subprocess

from tutorial.__about__ import __version__
from tutorial import kubernetes, kubectl, helm


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="tutorial")
def tutorial():
    pass


@tutorial.command(help=f'Setup "{kubernetes.cluster_name}" Kubernetes cluster.')
@click.argument("releases", nargs=-1)
@click.option(
    "--production",
    is_flag=True,
    help="Use values-production.yaml for each Helm chart, if it exists.",
)
@click.option(
    "--force",
    is_flag=True,
    help="Force re-deployment of Helm charts, even when the version has not changed.",
)
def up(releases, production, force):
    kubernetes.create_cluster()

    kubeconfig = kubernetes.kubeconfig

    if len(releases) == 0:
        for dep in dependencies:
            deploy_dependency(dep, production, kubeconfig, force)

    for release in releases:
        deploy_release(release, production, kubeconfig, force)


def deploy_release(release, production, kubeconfig, force):
    known_releases = []

    for dep in dependencies:
        if release in dep["release"]:
            return deploy_dependency(
                dep, production=production, kubeconfig=kubeconfig, force=force
            )

        known_releases.append(dep["release"])

    raise click.UsageError(f"Release must be one of: {', '.join(known_releases)}")


def deploy_dependency(dep, production, kubeconfig, force):
    release = helm.helm_install_or_upgrade(
        release_name=dep["release"],
        namespace=dep["namespace"],
        chart_name=dep["chart_name"],
        wait=True,
        create_namespace=True,
        production=production,
        kubeconfig=kubeconfig,
        force=force
    )


@tutorial.command(help=f"Forward a local port to a remote service.")
@click.argument("service")
@click.option(
    "--open",
    is_flag=True,
    help="Open the service in a browser.",
)
def port_forward(service, open):
    kubeconfig = kubernetes.kubeconfig

    known_services = []

    for dep in dependencies:
        if not "port_forward" in dep:
            continue

        if not service in dep["port_forward"]:
            known_services.extend(dep["port_forward"].keys())
            continue

        port_forward = dep["port_forward"][service]
        namespace = dep["namespace"]

        kubectl.port_forward(
            local_port=port_forward["local_port"],
            remote_port=port_forward["remote_port"],
            resource=port_forward["resource"],
            namespace=namespace,
            kubeconfig=kubeconfig,
        )

        url = f"http://localhost:{port_forward['local_port']}/"
        click.echo(f'{service} should now be accessible at {url}')

        if 'port_forward_hook' in dep:
            dep['port_forward_hook'](namespace, kubeconfig)

        if open:
            subprocess.run(["open", url], check=True)

        return

    raise click.UsageError(f"Service must be one of: {', '.join(known_services)}")


@tutorial.command(help=f'Teardown "{kubernetes.cluster_name}" Kubernetes cluster.')
def down():
    kubernetes.delete_cluster()


def argocd_print_admin_secret(namespace, kubeconfig):
    secret = kubectl.get(
        "secret/argocd-initial-admin-secret",
        namespace=namespace,
        kubeconfig=kubeconfig,
    )

    print(
        'Argo CD "admin" password:',
        base64.b64decode(secret["data"]["password"]).decode("utf-8"),
    )


dependencies = [
    {
        "title": "monitoring",
        "release": "monitoring",
        "namespace": "monitoring",
        "chart_name": "monitoring",
        "port_forward": {
            "prometheus": {
                "local_port": 9090,
                "remote_port": 9090,
                "resource": "service/monitoring-kube-prometheus-prometheus",
            }
        },
    },
    {
        "title": "Argo CD",
        "release": "argo-cd",
        "namespace": "argocd",
        "chart_name": "argo-cd",
        "port_forward_hook": argocd_print_admin_secret,
        "port_forward": {
            "argo-cd": {
                "local_port": 8080,
                "remote_port": 443,
                "resource": "service/argo-cd-argocd-server",
            }
        },
    },
    {
        "title": "Kyverno & Policies",
        "release": "kyverno",
        "namespace": "kyverno",
        "chart_name": "kyverno"
    },
    {
        "title": "Policy Reporter",
        "release": "policy-reporter",
        "namespace": "policy-reporter",
        "chart_name": "policy-reporter",
        "port_forward": {
            "policy-reporter": {
                "local_port": 8081,
                "remote_port": 8080,
                "resource": "service/policy-reporter-ui",
            }
        },
    },
    {
        "title": "Guestbook",
        "release": "guestbook",
        "namespace": "default",
        "chart_name": "guestbook",
    },
]
