class LineCli < Formula
  desc "Unofficial LINE client for personal accounts"
  homepage "https://github.com/kongesque/line-cli"
  version "0.3.0"
  license "MIT"

  on_arm do
    url "https://github.com/kongesque/line-cli/releases/download/v0.3.0/line-darwin-arm64.tar.gz"
    sha256 "1191964feec1f37198a8cf1504f82b68c56edcf12436727bf09542d204065e3c"
  end

  on_intel do
    url "https://github.com/kongesque/line-cli/releases/download/v0.3.0/line-darwin-amd64.tar.gz"
    sha256 "2defa1e1397dc95586318b3ab7925635a6f8a20874cbf0d192568c44a819c6fa"
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
