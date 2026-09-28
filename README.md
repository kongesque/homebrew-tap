# Homebrew tap for LINE CLI

Install [LINE CLI](https://github.com/kongesque/line-cli) on macOS:

```sh
brew install kongesque/tap/line-cli
```

The formula installs the published macOS release for your Mac's architecture.
To upgrade:

```sh
brew upgrade line-cli
```

The [formula update workflow](.github/workflows/update-line-cli.yml) checks for
stable LINE CLI releases hourly and can also be run manually. When configured,
it verifies both macOS archives against the published SHA-256 manifest, then
opens a pull request for review. The tap changes only when that pull request is
merged.

To enable automatic pull requests, create a fine-grained GitHub personal access
token limited to `kongesque/homebrew-tap` with **Contents: Read and write** and
**Pull requests: Read and write**. Save it as the repository Actions secret
`TAP_PR_TOKEN`. The workflow's built-in GitHub token remains read-only. Until
the secret is set, scheduled runs succeed without proposing changes and explain
the missing setup in the run summary. Renew the secret before its token expires.
