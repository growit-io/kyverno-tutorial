# Argo CD Wrapper Chart

This Helm chart is a wrapper of the community-managed, semi-official [Argo CD Helm chart](https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd#readme). In the tutorial, we'll only deploy Argo CD once, with basic initial parameters from [values.yaml](values.yaml).

## Why Argo CD?

Argo CD deploys our [guestbook](../guestbook/) in the tutorial, or any other application defined in a Helm or Git repository. We use [Argo CD](https://argoproj.github.io/cd/) because its [Application](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/) resource provides a convenient "single source of truth" to declare ownership of a managed set of resources, but [Flux CD](https://fluxcd.io/) or another deployment tool would have worked as well.

Our ownership convention will be anchored in a custom `example.com/team` label on these `Application` resources. However, Argo CD cannot propagate this ownership label to managed resources on its own. We'll use the policies defined in our [Kyverno wrapper chart](../kyverno/) to propagate this ownership label, without changing how we deploy or use Argo CD, and without altering the applications we deploy!

## Deploying Argo CD

Use the command:

```sh
hatch run tutorial up argo-cd
```

This will deploy Argo CD in the tutorial environment.

## Accessing the Argo CD UI

Start a port-forwarding process in the background with the following command:

```sh
hatch run tutorial port-forward argo-cd
```

This command will also show you the password for the "admin" user.
You can then access the Argo CD UI via http://localhost:8080/.