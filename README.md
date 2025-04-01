# `release-please` demo

Demo of a [`release-please`](https://github.com/googleapis/release-please) workflow in a Helm-based monorepo, with support for `uv`-based python packages and environment branches for GitOps Continuous Deployment.

There are currently just two components to this monorepo:

- `api/`: a Python FastAPI application, managed with `uv`, publishing a docker container to Github Packages
- `helm/`: a helm chart which uses the `api` container

When the `api` package is updated, the reference to it's docker container in `helm/values.yaml` is also updated, and the `helm` chart has it's patch version bumped.

This general approach should work for multiple components in various languages, but the workflows will need tweaks to build only what's needed, especially for development deployments.

> [!WARNING]
> This approach should work for multiple _artifacts_ produced by the non-helm package, but is not yet ready for multiple independent packages

## Release Workflow

This project, or a project using the same approach (see below for how to adapt elsewhere), follows this development process:

1. Changes begin in _feature branches_ which branch from `main`. Changes should be limited to just one component, i.e. `helm/` or `api/` but not both.
2. Developers can deploy their changes to the development environment with a manual Github Action Workflow, selecting their branch. This will build components with a post-release tag and update the `env/development` branch.
3. Pull requests target `main`, and must have a [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) _title_ indicating the depth of change. E.g. the PR title "fix: squash bug" translates to a minor version bump.
4. After review, the PR is squash-merged into `main`. This triggers the creation of a _release PR_ which bumps versions in various places (e.g. `pyproject.toml`, `uv.lock`, `Chart.yaml`, `values.yaml`) and updates changelogs.
5. The release PR builds pre-releases and updates an `env/staging` branch.
6. Before the release PR is merged, any number of additional feature-branch PRs can be merged into `main`. The release PR will update automatically, as will `env/staging`.
7. The release PR is approved and merged. This will create Github Releases, promote prerelease artifacts to release versions, create Github releases, and update `env/production`.

## Adopting in Other Projects

1. Configure your GitHub settings
   1. In General > Pull Requests, disable merge commits and rebase merging. Enable squash merging, with the title as the commit message.
   2. In Actions > General > Workflow permissions, give workflows "Read and write permissions", and check the box to "Allow Github Actions to create and approve pull requests".
   3. In Rules, create two rulesets: one for `main` and another for `env/*` branches (details TBD)
2. Create a fine-grained PAT with write access to repository contents. Add it as a secret in your repository
3. Prepare your repository by organizing your code into top-level folders, one for the helm chart (usually `helm/`) and one for each subcomponent (e.g. `api/`, `backend/`, etc.)
4. Add a `release-please-config.json` and `.release-please-manifest.json` to the root of the project.
5. Copy the actions and workflows from this repository's `.github/` folder into your repo, modifying as needed (all section starting with `## CUSTOMIZE ##`). Do not edit the `convention-commits` workflow nor any of the actions.
6. File the above changes as a PR and merge it.
7. Create branches `env/development`, `env/staging`, and `env/production` from `main`.
8. Update ArgoCD to use these new branches in matching environments.
9. Make your first new change, following the Release Workflow above

## FAQ

> Why version the helm chart? We aren't publishing it, and Argo is simply looking at the branch anyways.

If we didn't version the helm chart with release-please, helm-only changes wouldn't trigger a release PR, and we'd never update staging or prod until the next non-helm change was released.

> Why do we need an `env/production` branch? Why can't we use `main`?

If we sync our production environment from `main`, changes to the helm chart won't be gated by a release PR like other changes are. To properly delay release, we need a non-`main` branch we don't update until the release PR is merged.

> Why do we need build branches? Why not build from environment branches?

To avoid race conditions where ArgoCD is trying to pull an image that doesn't exist yet. By building from a build branch, we wait to update the environment branch until the build is fully complete, ensuring artifacts in the helm chart exist first.

## TODO

- Refactor into more actions
  - [ ] determine changed packages from manifest(s)
  - [ ] update tags in helm values
  - [ ] fix python version + `uv lock`
  - [ ] write helm changelog section
- Generalize
  - [ ] start using [pants](https://www.pantsbuild.org/) to push build, publish, etc. into each component
  - [ ] add a node-based component
  - [ ] add a non-docker artifact (model repository)
- Release
  - [ ] update helm Changelog when patch bumping
  - [ ] add docker image links to non-helm releases
