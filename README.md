# Kyverno Tutorial

This tutorial demonstrates how [Kyverno](https://kyverno.io/) can be leveraged effectively to implement organization-specific policies within a running [Kubernetes](https://kubernetes.io/) cluster.

Our reference scenario for demonstration purposes will be an adaptation of the "[you build it, you run it](https://aws.amazon.com/blogs/enterprise-strategy/enterprise-devops-why-you-should-run-what-you-build/)" principle, where application development teams declare ownership of the Kubernetes resources that they manage via [Argo CD](https://argo-cd.readthedocs.io/en/stable/), and [Prometheus](https://prometheus.io/) is able to route alerts to the appropriate team using [custom labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) attached to the managed resources. In this scenario, a dedicated "platform operations" team will receive and handle *only* the alerts which pertain to infrastructure-level resources and are not application-specific.

Kyverno will play an essential role in ensuring that the [Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/) component of Prometheus can make informed routing decisions based on alert labels while minimizing the required effort for application development and platform operations teams to implement and maintain the solution.

> 💡 While this tutorial primarily relies on Argo CD and [Helm](https://helm.sh/) for Kubernetes resource management, the solution itself is not very specific to this particular combination of tools. In fact, you may notice that a wide range of resource management tools such as [Kustomize](https://kustomize.io/), [Jsonnet](https://jsonnet.org/), or [Flux CD](https://fluxcd.io/) will either work just as well out of the box, or can easily be supported with minimal changes to our Kyverno policies.

## Getting started

The easiest way to run this tutorial is to **[open the project](https://codespaces.new/growit-io/kyverno-tutorial)** in [GitHub Codespaces](https://github.com/features/codespaces) (using a cloud-based temporary environment). Alternatively, you can also open it locally in [Visual Studio Code](https://code.visualstudio.com/) with [Docker](https://www.docker.com/) installed, and recommended extensions enabled.

Use the following link from within Visual Studio Code to begin:

▶️ [Start the tutorial](vscode://vsls-contrib.codetour/startDefaultTour)

You may see an error while the recommended extensions are still being installed. In that case, just wait, and try again later.

## License

[Kyverno Tutorial](https://github.com/growit-io/kyverno-tutorial) &copy; 2024 by [Uwe Stuehler](https://github.com/ustuehler) is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
