# Prometheus Wrapper Chart

This Helm chart is a wrapper of the community-managed, semi-official [kube-prometheus-stack Helm chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack#readme). In the tutorial, we'll first deploy it with basic parameters from [values.yaml](values.yaml), and then with overrides from [values-production.yaml](values-production.yaml) for the final working configuration.

## Deploying Prometheus

Use the command:

```sh
hatch run tutorial up prometheus
```

This will deploy Prometheus with a basic initial configuration in the tutorial environment.

Use the `--production --force` options to upgrade the deployment to the final working configuration.

## Accessing the Prometheus UI

Start a port-forwarding process in the background with the following command:

```sh
hatch run tutorial port-forward prometheus
```

You can then access the Prometheus UI via http://localhost:9090/.