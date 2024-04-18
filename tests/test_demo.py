import pytest
import os

from tutorial.cli import tutorial
from tutorial import kubernetes, helm


@pytest.fixture
def kubeconfig():
    teardown = True
    kubeconfig = kubernetes.kubeconfig

    try:
        if os.path.isfile(kubeconfig):
            teardown = False
        else:
            tutorial(["up"], standalone_mode=False)

        yield kubeconfig
    finally:
        if teardown:
            tutorial(["down"], standalone_mode=False)


@pytest.fixture
def argo_cd(kubeconfig):
    yield helm.setup_argo_cd(kubeconfig=kubeconfig)


@pytest.fixture
def kyverno(kubeconfig):
    yield helm.setup_kyverno(kubeconfig=kubeconfig)


def test_argo_cd(argo_cd):
    assert "namespace" in argo_cd


def test_kyverno(kyverno):
    assert "namespace" in kyverno
