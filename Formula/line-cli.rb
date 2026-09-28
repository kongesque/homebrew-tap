class LineCli < Formula
  desc "Unofficial LINE client for personal accounts"
  homepage "https://github.com/kongesque/line-cli"
  version "0.4.0"
  license "MIT"

  on_arm do
    url "https://github.com/kongesque/line-cli/releases/download/v0.4.0/line-darwin-arm64.tar.gz"
    sha256 "f19b2169822499502bd1d1628c7b541ff32edf423221a35dff3d6c484dd1b6e7"
  end

  on_intel do
    url "https://github.com/kongesque/line-cli/releases/download/v0.4.0/line-darwin-amd64.tar.gz"
    sha256 "2fe4a168a3152e71d0ffa3d5b81a2dc2ed0ab837191bc1cee23a99d6c8026a3a"
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
