# The Tutorial's Wrapper Helm Charts

This directory contains wrapper Helm charts for the tutorial.

## Deploying the basic initial configuration

To create a temporary Kubernetes cluster and install all wrapper charts with a minimal configuration to make them deployable, using only parmeters from `values.yaml` files:

```sh
hatch run tutorial up
```

## Deploying the final working configuration

To install all wrapper charts with their final working configuration for the purposes of this tutorial, using parmeters from both `values.yaml` and `values-production.yaml` files:

```sh
hatch run tutorial down
hatch run tutorial up --production
```

## Other `up` command usages

Invoke `up` with option `-h` to see the complete list of supported options and arguments:

```sh
hatch run tutorial up -h
```

## Tearing down the tutorial environment

Use the command:

```sh
hatch run tutorial down
```