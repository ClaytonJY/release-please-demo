# `release-please` demo

Demo of a [`release-please`](https://github.com/googleapis/release-please) workflow in a Helm-based monorepo, with support for `uv`-based python packages.

## TODO

- [x] api-only release
- [x] helm-only release

- Release
  - [ ] use extra-files to bump api version reference in helm chart
  - [ ] wrap release-please to update `uv.lock`
  - [ ] wrap release-please to patch bump chart when api updates
- Staging
  - [ ] build/push pre-release artifacts from release PRs
  - [ ] update staging branch when release PR's opened/updated/merged
- Prod
  - [ ] promote artifacts when release PR merged
  - [ ] update production branch
- Dev
  - [ ] build/push pre-prerelease artifacts from PR? manual workflow?
  - [ ] update dev branch
- Process
  - [ ] enforce Conventional Commits
  - [ ] branch protection rules (once public)

## Tips

- must allow Actions to file PRs!
