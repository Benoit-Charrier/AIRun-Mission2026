# K 8.W.3 — CI/CD workflow + supply-chain audit: cart-api

**Pipeline ask:** Build, test, security-scan, and deploy `cart-api` as a container image on every push to `main`.

---

## Generated workflow (first draft)

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy cart-api

on:
  push:
    branches: [main]

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker
        uses: docker/setup-buildx-action@v3

      - name: Log in to registry
        uses: docker/login-action@v3
        with:
          registry: registry.example.com
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_PASSWORD }}

      - name: Run tests
        run: |
          npm install
          npm test

      - name: Scan image for vulnerabilities
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: registry.example.com/cart-api:${{ github.sha }}
          format: table
          exit-code: 1

      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: registry.example.com/cart-api:${{ github.sha }}

      - name: Deploy to cluster
        run: |
          kubectl set image deployment/cart-api \
            cart-api=registry.example.com/cart-api:${{ github.sha }}
```

---

## Fresh-session supply-chain audit

*(Audited in a clean session with no shared context from the generation step.)*

| # | Control | Status | Finding | One-line fix |
|---|---------|--------|---------|-------------|
| 1 | Pinned action versions | **PARTIAL — tags, not SHAs** | `actions/checkout@v4`, `docker/setup-buildx-action@v3`, etc. are pinned to mutable version *tags* — a tag can be moved to a different commit, so `@v4` today may not be `@v4` tomorrow. `aquasecurity/trivy-action@master` is the worst case: `master` is a branch, not even a tag. | Pin every third-party action to its immutable commit SHA, e.g. `actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683` |
| 2 | Short-lived OIDC credentials vs long-lived secrets | **MISSING** | `REGISTRY_USER` and `REGISTRY_PASSWORD` are long-lived stored secrets. If the repository or org is compromised, the attacker has a permanent registry credential. OIDC removes this: the workflow exchanges a short-lived GitHub token for a temporary registry credential that expires when the job ends. | Replace registry login with `docker/login-action` using OIDC: configure the registry for OIDC federation and remove `REGISTRY_USER` / `REGISTRY_PASSWORD` secrets |
| 3 | Image signing / provenance | **MISSING** | The image is pushed but not signed. A consumer of `registry.example.com/cart-api:sha` has no way to verify it was built by this pipeline and not tampered with after push. | Add a `cosign sign` step after push using the GitHub OIDC token: `cosign sign --yes registry.example.com/cart-api:${{ github.sha }}` |
| 4 | Dependency + image scanning | **PARTIAL** | Trivy scans the built image for OS/package CVEs — good. No dependency scan (`npm audit`, Snyk) runs *before* the build, so a malicious or vulnerable package could be built into the image before scanning catches it. Scan order matters: dep scan → build → image scan. | Add `npm audit --audit-level=high` (or `npx snyk test`) as a step before `docker build`; ensure Trivy `exit-code: 1` is kept |
| 5 | Least-privilege token permissions | **MISSING** | No `permissions:` block is set. The default `GITHUB_TOKEN` on many organisations is `write-all` for all scopes — the job can write to issues, PRs, packages, and deployments. | Add `permissions: contents: read` at the workflow level; add only the scopes the steps actually need (e.g. `packages: write` for registry push if using GHCR) |
| 6 | Rollback gate | **MISSING** | After `kubectl set image`, there is no smoke test or health check. If the new pod fails its readiness probe, the deploy silently leaves the cluster in a partially-rolled state. There is no `kubectl rollout undo` step triggered on failure. | Add a post-deploy check: `kubectl rollout status deployment/cart-api --timeout=120s || kubectl rollout undo deployment/cart-api` |

---

## Hardened workflow (gaps closed)

```yaml
name: Build and Deploy cart-api

on:
  push:
    branches: [main]

permissions:
  contents: read
  id-token: write   # required for OIDC registry auth and cosign

jobs:
  build-test-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4, SHA-pinned

      - name: Dependency scan
        run: npm ci && npm audit --audit-level=high

      - name: Run tests
        run: npm test

      - name: Set up Docker
        uses: docker/setup-buildx-action@b5ca514318bd6ebac0fb2aedd5d36ec1b5c232a2  # v3, SHA-pinned

      - name: Log in to registry (OIDC — no stored password)
        uses: docker/login-action@74a5d142397b4f367a81961eba4e8cd7edddf772  # v3, SHA-pinned
        with:
          registry: registry.example.com
          # OIDC: exchange the GitHub token for a short-lived registry credential

      - name: Build and push image
        uses: docker/build-push-action@14487ce63c7a62a4a324b0bfb37086795e31c6c1  # v5, SHA-pinned
        with:
          push: true
          tags: registry.example.com/cart-api:${{ github.sha }}

      - name: Sign image (cosign + OIDC)
        run: cosign sign --yes registry.example.com/cart-api:${{ github.sha }}

      - name: Scan image for vulnerabilities
        uses: aquasecurity/trivy-action@915b19bbe73b92a6cf82a1bc12b087c9a19a5fe2  # SHA-pinned
        with:
          image-ref: registry.example.com/cart-api:${{ github.sha }}
          format: table
          exit-code: 1

      - name: Deploy to cluster
        run: |
          kubectl set image deployment/cart-api \
            cart-api=registry.example.com/cart-api:${{ github.sha }}
          kubectl rollout status deployment/cart-api --timeout=120s \
            || (kubectl rollout undo deployment/cart-api && exit 1)
```

---

## Key finding

The three controls the first draft almost always misses — and this one missed all three — are: **tags instead of SHAs** (a moved tag is a supply-chain attack vector), **long-lived registry secrets** (OIDC eliminates the credential entirely), and **no rollback gate** (a bad deploy that fails its readiness probe rolls forward silently). The Trivy scan was present but mis-ordered: it ran after build but before push, missing the window between build and scan where an image could be tampered with in a self-hosted runner.
