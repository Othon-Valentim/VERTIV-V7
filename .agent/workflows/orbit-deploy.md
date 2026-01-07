---
description: orbit-deploy
---

# ORBIT DEPLOYMENT PROTOCOL

description: Builds and Deploys the full stack to Google Cloud Run.

steps:
  - step: "Verify Infrastructure"
    instruction: "Check if `scripts/orbit_deploy.sh` exists and has execution permissions (`chmod +x`)."

  - step: "Execute Deploy"
    instruction: "Run `./scripts/orbit_deploy.sh` in the terminal. Monitor for errors."

  - step: "Validation"
    instruction: "After deploy, verify if the returned Backend URL and Frontend URL are reachable."