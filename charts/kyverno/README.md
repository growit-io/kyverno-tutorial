# Kyverno & Policies Wrapper Chart

This Helm chart is a wrapper of the official [Kyverno Helm chart](https://github.com/kyverno/kyverno/tree/main/charts/kyverno#readme). In the tutorial, we'll first deploy it without policies from [values.yaml](values.yaml), and then with necessary policies enabled via [values-production.yaml](values-production.yaml) for the final working configuration.

## Why Kyverno?

With Kyverno's [mutating policies](https://kyverno.io/docs/writing-policies/mutate/), we can efficiently apply transformations to Kubernetes resources during creation or updates.

In the tutorial, [Kyverno](https://kyverno.io/)'s primary role will be to automate the propagation of our custom label `example.com/team` from the Argo CD `Application` resource to the application's managed resources. Kyverno will also be responsible for ensuring that Prometheus applies this label to all relevant scrape targets, so that Alertmanager can reliably make routing decisions based on this label.

💡 While other uses are outside the scope of this tutorial, as a general tool for policy management and enforcement, Kyverno can do a lot more than that for an organization. You can also use this tutorial's "sandbox" environment just to play around with Kyverno. 🤹