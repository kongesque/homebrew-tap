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
stable LINE CLI releases hourly and can also be run manually. It verifies both
macOS archives against the published SHA-256 manifest, then opens a pull request
for review. The tap changes only when that pull request is merged.
