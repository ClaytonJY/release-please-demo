# `release-please` demo

Demo of a [`release-please`](https://github.com/googleapis/release-please) workflow in a Helm-based monorepo, with support for `uv`-based python packages.

## TODO

- Release
  - [x] wrap release-please to update `uv.lock`
  - [x] wrap release-please to update component references in helm chart when component updates
  - [x] wrap release-please to patch bump chart when api updates
  - [ ] update helm Changelog when patch bumping
  - [ ] bump helm minor instead of patch?
  - [ ] open PR as draft, undraft after changes, trigger workflows on undraft
  - [ ] add docker image links to non-helm releases
- Staging
  - [ ] build/push pre-release artifacts from release PRs
  - [ ] update `staging` branch when release PR's opened/updated/merged
- Prod
  - [ ] promote artifacts when release PR merged
  - [ ] update `production` branch
- Dev
  - [ ] build/push pre-prerelease artifacts from PR? manual workflow?
  - [ ] update dev branch
- Process
  - [ ] enforce Conventional Commits
  - [ ] branch protection rules (once public)
- Refactor workflows/actions
  - [ ] determine changed packages from manifests
  - [ ] update tags in helm values
  - [ ] use `mise`?
- Generalize
  - [ ] add a node project
  - [ ] add a non-docker artifact (triton model repo)
- Test
  - [ ] merge conflicts

## Tips

- must allow Actions to file PRs!

## FAQ
