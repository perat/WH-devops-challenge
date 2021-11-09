# Option 1

Simple python flask application serves API endpoint with API-KEY validation.
- Dockerfile uses non-root user to run application.
- Helm chart describes k8s deployment with 2 initial pod replicas and auto-scaling to 10 pods based on CPU/Memory load.
- Helm chart create service account inside k8s target namespace which is used to run pods.
- API Key is stored in k8s secret created as pre-requisite for deployment and mapped inside pods as environment variable.

Minikube local cluster was used to prepare those notes, so some steps (e.g. docker image publish to registry) are skipped.
[How to setup minikube on Mac](https://itnext.io/goodbye-docker-desktop-hello-minikube-3649f2a1c469)

## Deployment

### Pre-requisites

1. Create namespace
```bash
kubectl create namespace option1
```
2. Switch to the namespace
```bash
kubectl config set-context --current --namespace=option1

# Check your context
kubectl config get-contexts
```

3. Create secret
```bash
API_KEY=$( python -c 'import secrets; print(secrets.token_urlsafe(16))' )
kubectl create secret generic option1-app-secrets --from-literal=api-key="$API_KEY"
```

### Docker image
Build
```bash
docker build --pull --rm -f "option1/Dockerfile" -t whdevopschallenge_option1:latest "option1"
```
In order to deploy to external cluster this image needs to be published to docker registry accessible by cluster.

### Deployment of application with helm

Check resulting spec produced by helm

```bash
helm template option1/helm/sample-app
```

Install application into k8s namespace

```bash
helm upgrade --install --atomic sample-app option1/helm/sample-app

# Check pods status
kubectl get pods --selector app.kubernetes.io/name=sample-app

# Check logs
kubectl logs --selector app.kubernetes.io/name=sample-app
```

Get the application URL by running these commands:
in k8s cluster
```bash
export NODE_PORT=$(kubectl get --namespace option1 -o jsonpath="{.spec.ports[0].nodePort}" services sample-app)
export NODE_IP=$(kubectl get nodes --namespace option1 -o jsonpath="{.items[0].status.addresses[0].address}")
curl http://$NODE_IP:$NODE_PORT
```

Check that API_KEY variables is set inside container
```bash
kubectl get pods --selector app.kubernetes.io/name=sample-app
kubectl exec <pod_name> -- bash -c 'env|grep API'
```

Validate POST API 
```bash
curl \
-H "Content-Type: application/json" \
-H "x-api-key: $API_KEY" \
-X POST -d '{"username":"xyz","password":"xyz"}' http://localhost:$NODE_PORT/json/
```


# Horizontal Pod Autoscaler
references:
- [horizontal-pod-autoscale](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)
- [assign-memory-resource](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/)

for minikube it needs to be enabled like this:
```bash
minikube addons enable metrics-server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/metrics-server-helm-chart-3.6.0/components.yaml

# Check
kubectl top pods
```

## Test auto-scaling
Check initial count of pods
```bash
kubectl get pods --selector app.kubernetes.io/name=sample-app
```

It is expected to be only 2 pods according to values set for helm chart
```
# initial number of pods for deployment
replicaCount: 2 

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80
```

Run load test
```bash
option1/src/python/flask-api-key-package/tests/requests-spammer.sh
```

Check that new pods are created to process increasing load (up to maxReplicas: 10)
```bash
kubectl get pods --selector app.kubernetes.io/name=sample-app
```
