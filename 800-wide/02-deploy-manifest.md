# K 8.W.2 — Deployment manifest + fresh-session audit: cart-api

**Service shape:** 3 replicas, ~512Mi memory each, port 8080, `/healthz` endpoint, needs `DATABASE_URL` and `DIAL_API_KEY`.

---

## Generated manifest (first draft)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cart-api
  labels:
    app: cart-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: cart-api
  template:
    metadata:
      labels:
        app: cart-api
    spec:
      containers:
        - name: cart-api
          image: registry.example.com/cart-api:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              value: "postgres://user:password@db-host:5432/cartdb"
            - name: DIAL_API_KEY
              value: "sk-dial-abc123secretkey"
---
apiVersion: v1
kind: Service
metadata:
  name: cart-api
spec:
  selector:
    app: cart-api
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

---

## Fresh-session audit — production-readiness gaps

*(Audited in a clean session with no shared context from the generation step.)*

| # | Control | Status | Why it matters | One-line fix |
|---|---------|--------|----------------|-------------|
| 1 | Resource requests + limits | **MISSING** | Without `limits`, one pod can consume all node memory and trigger OOMKill on its neighbours; without `requests`, the scheduler can't place pods correctly and the cluster over-provisions | Add `resources: requests: {memory: "256Mi", cpu: "100m"} limits: {memory: "512Mi", cpu: "500m"}` to the container spec |
| 2 | Readiness probe | **MISSING** | Without a readiness probe, Kubernetes routes traffic to pods before they are ready — customers see errors on every rolling deploy | Add `readinessProbe: httpGet: {path: /healthz, port: 8080} initialDelaySeconds: 5 periodSeconds: 10` |
| 3 | Liveness probe | **MISSING** | Without a liveness probe, a hung or deadlocked pod stays in rotation indefinitely, silently failing requests | Add `livenessProbe: httpGet: {path: /healthz, port: 8080} initialDelaySeconds: 15 periodSeconds: 20` |
| 4 | Secret handling | **FAIL — plaintext** | `DATABASE_URL` and `DIAL_API_KEY` in plaintext `env.value` expose credentials in pod specs, etcd, CI logs, and any `kubectl describe pod` output | Replace both with `valueFrom: secretKeyRef: {name: cart-api-secrets, key: DATABASE_URL}` and create a Kubernetes Secret |
| 5 | Rolling update strategy | **MISSING** | Default `Recreate` strategy (or an unconfigured RollingUpdate) can replace all pods simultaneously, causing a full-service outage during deploys | Set `strategy: type: RollingUpdate rollingUpdate: {maxSurge: 1, maxUnavailable: 0}` |
| 6 | Revision history / rollback path | **MISSING** | Without `revisionHistoryLimit`, `kubectl rollout undo` has no prior revision to revert to — a bad deploy becomes a long incident | Set `revisionHistoryLimit: 3` under `spec:` |

---

## Production-ready manifest (gaps closed)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cart-api
  labels:
    app: cart-api
spec:
  replicas: 3
  revisionHistoryLimit: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: cart-api
  template:
    metadata:
      labels:
        app: cart-api
    spec:
      containers:
        - name: cart-api
          image: registry.example.com/cart-api:latest
          ports:
            - containerPort: 8080
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: cart-api-secrets
                  key: DATABASE_URL
            - name: DIAL_API_KEY
              valueFrom:
                secretKeyRef:
                  name: cart-api-secrets
                  key: DIAL_API_KEY
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: cart-api
spec:
  selector:
    app: cart-api
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

---

## Key finding

**The missing `resources.limits` and missing `readinessProbe` are not cosmetic.** The memory limit gap is the direct cause of the K 8.W.4 incident (OOMKilled pods after the AI summarise step was added); the readiness probe gap means every rolling deploy exposes customers to errors during the startup window. Both must be closed before the AI step ships to production.
