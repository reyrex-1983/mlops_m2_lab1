Quick Kubernetes deploy instructions

This folder contains manifest files to run the Iris API stack on Kubernetes (namespace `mlops`).

Files:
- `namespace.yaml` - creates the `mlops` namespace
- `api-deployment.yaml` - Deployment + Service for the FastAPI server (image: `mlops_m2_lab1-api:latest`)
- `mlflow-deployment.yaml` - Deployment + Service for MLFlow UI (image: `mlops_m2_lab1-api:latest`, runs `mlflow ui`)
- `prometheus-configmap.yaml` - Prometheus config (scrapes `iris-api` and `mlflow`)
- `prometheus-deployment.yaml` - Deployment + Service for Prometheus
- `grafana-deployment.yaml` - Deployment + Service for Grafana

Notes & Steps
1) Build the API image locally (from project root):

```bash
# build image
docker build -t mlops_m2_lab1-api:latest .
```

2) If you are using `kind` (local cluster), load the image into the cluster:

```bash
kind load docker-image mlops_m2_lab1-api:latest
```

If using `minikube`:

```bash
minikube image load mlops_m2_lab1-api:latest
```

Or push to a registry and update the image names in the manifests.

3) Apply the manifests:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/ --recursive
```

4) Expose services for local access (port-forwarding examples):

```bash
kubectl -n mlops port-forward svc/iris-api 8001:8000 &
kubectl -n mlops port-forward svc/mlflow 5001:5000 &
kubectl -n mlops port-forward svc/prometheus 9091:9090 &
kubectl -n mlops port-forward svc/grafana 3001:3000 &
```

5) Grafana: open http://localhost:3001 (admin/admin). Add Prometheus data source pointing to http://prometheus:9090 (or http://localhost:9091 when port-forwarded).

Caveats
- `mlruns` is stored in an `emptyDir` in these manifests; for persistence, replace with a `PersistentVolume` and `PersistentVolumeClaim`.
- The `mlflow` Deployment uses the API image and runs `mlflow ui` — you can create a dedicated MLFlow image if desired.
- If you want Grafana provisioning mounted automatically, create ConfigMaps from `grafana/provisioning` and mount them under `/etc/grafana/provisioning`.

If you want, I can:
- create PersistentVolumeClaims for `mlruns`, Prometheus, and Grafana
- create Grafana provisioning ConfigMaps so the dashboard and datasource are auto-provisioned
- push images to a registry if you provide credentials or a repo name

Which of these should I do next?