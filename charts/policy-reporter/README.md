# Policy Reporter Wrapper Chart

This chart wraps the official [Policy Reporter Helm chart](https://github.com/kyverno/policy-reporter/tree/main/charts/policy-reporter#readme).

## Why Policy Reporter?

While it is possible to interact with Kyverno policies using `kubectl`, a graphical user interface makes it easier for humans to review and filter the reports.

## Deploying Policy Reporter

```sh
hatch run tutorial up policy-reporter
```

## Accessing Policy Reporter

```sh
hatch run tutorial port-forward policy-reporter
```

This starts a port-forwarding process in the background. You should then be able to access the Policy Reporter UI at http://localhost:8081/.