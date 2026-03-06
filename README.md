# 🚀 uv Monorepo Copier Template

[![Python](https://img.shields.io/badge/Python-3.8%20%7C%20...%20%7C%203.14-blue.svg)](https://python.org)
[![uv](https://img.shields.io/badge/uv-Astral-purple)](https://github.com/astral-sh/uv)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Copier](https://img.shields.io/badge/Copier-Template-green)](https://copier.readthedocs.io/)
[![Actions status](https://github.com/dmitriypru/uv-monorepo-template/actions/workflows/ci.yml/badge.svg)](https://github.com/dmitriypru/uv-monorepo-template/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready [Copier](https://copier.readthedocs.io/) template for scaffolding a modern **monorepo**. Built aggressively around strict `uv` workspaces and BuildKit-optimized multi-stage Docker builds.

Provide a unified foundation for your microservices while seamlessly maintaining shared libraries with zero pathing headaches.

---

## ✨ Features

- **Base + Component Architecture**: Generate the exact directories you need. Scaffold the root monorepo, and iteratively generate services or shared libraries directly into it.
- **`uv` Workspace Native**: All components are instantly auto-discovered. No `sys.path` appending, no manual `pyproject.toml` references. Just drop in a component and `uv sync`.
- **Intelligent BuildKit Contexts**: Docker builds leverage `--mount=type=bind,source=shared,from=root` to selectively inject shared monorepo components into isolated service builds, preserving cache limits and eliminating daemon payload bloat.
- **Dynamic Compositions**: The root `docker-compose.yaml` and `README.md` automatically auto-wire to include new microservices and libraries as they are generated.
- **Customizable**: Choose your Python constraints (3.8-3.14) and explicitly opt-in/out of elements like exposed port mappings or postgres databases.

---

## ⚡ Quickstart

This template uses a modular approach. Generate the base monorepo first, then inject services or libraries as needed.

> ⚠️ **Note on `--trust`**: The runtime component generation (`service` and `library`) uses Copier tasks (Python scripts) to dynamically update the root `docker-compose.yaml` and `README.md` files upon exit. Copier requires the `--trust` flag to execute these post-generation automations.


### 1. Scaffold the Base Monorepo
Initialize the monorepo:
```bash
uvx copier copy --trust gh:dmitriypru/uv-monorepo-template my-monorepo
cd my-monorepo
```
When prompted `What do you want to scaffold?`, choose `Base`.

> 💡 **Tip:** Copier defaults to the latest Git tag (e.g., `v1.0.0`). If you want to scaffold using the bleeding-edge latest commit from the main branch instead, append `--vcs-ref=HEAD` to the command.

### 2. Add a Microservice
From the root of your newly generated monorepo, scaffold a new service:
```bash
uvx copier copy --trust gh:dmitriypru/uv-monorepo-template . 
```
When prompted, select `Service`. You will be asked for the service name (e.g., `api`) and port (optional). The service is placed in `projects/<service_name>`. The generation automatically appends a Docker Compose `include` directive and updates the repository documentation!

### 3. Add a Shared Library
From the root of your generated monorepo, scaffold a library:
```bash
uvx copier copy --trust gh:dmitriypru/uv-monorepo-template . 
```
When prompted, select `Library`. The library is placed in `shared/<library_name>` and is automatically discovered by `uv` via wildcards.

---

## 🏗️ Architecture & Tooling

### Workspace Glob Auto-Discovery
The root `pyproject.toml` defines `members = ["projects/*", "shared/*"]`. 
`uv` automatically traverses these directories to build a unified lockfile. No manual path registration is required when adding new services or libraries. Simply run `uv sync` from the monorepo root.

### Docker BuildKit `additional_contexts` Strategy
Monorepos traditionally struggle with Docker daemon payload sizes when building a single service that requires a sibling shared library at the repository root.

This template resolves the contextual bloat using Docker Compose's `additional_contexts` mapped to `root=../../`. `Dockerfile` within the project isolates its primary `context: .` strictly to the microservice itself. It selectively fetches the shared dependencies using BuildKit named bindings: `--mount=type=bind,source=shared,target=/app/shared,from=root`. This structural mapping mirrors the source layout natively within the builder image, allowing `uv sync --frozen` to execute perfectly without sending unnecessary folders to the Docker daemon.
