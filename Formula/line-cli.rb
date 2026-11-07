class LineCli < Formula
  desc "Unofficial LINE client for personal accounts"
  homepage "https://github.com/kongesque/line-cli"
  version "0.6.0"
  license "MIT"

  on_arm do
    url "https://github.com/kongesque/line-cli/releases/download/v0.6.0/line-darwin-arm64.tar.gz"
    sha256 "8aab9cbcef9f08184a4be26f36d02ef6509ee3529421ea1f2b671948a91afaf3"
  end

  on_intel do
    url "https://github.com/kongesque/line-cli/releases/download/v0.6.0/line-darwin-amd64.tar.gz"
    sha256 "03fea00dd6738e079c24283e5d3278fc87d6ac1b9fc5f86a4c265a19032bc14e"
  end

  livecheck do
    url "https://github.com/kongesque/line-cli/releases"
    regex(%r{href=.*?/releases/tag/v?(\d+(?:\.\d+)+)}i)
  end

  depends_on :macos

  def install
    bin.install "line"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/line version")
  end
end
