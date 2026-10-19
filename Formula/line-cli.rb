class LineCli < Formula
  desc "Unofficial LINE client for personal accounts"
  homepage "https://github.com/kongesque/line-cli"
  version "0.5.0"
  license "MIT"

  on_arm do
    url "https://github.com/kongesque/line-cli/releases/download/v0.5.0/line-darwin-arm64.tar.gz"
    sha256 "8e554732556f2da27bf68046f4b695275a2f4bed44c63d0348e7fd2ebf96c2ee"
  end

  on_intel do
    url "https://github.com/kongesque/line-cli/releases/download/v0.5.0/line-darwin-amd64.tar.gz"
    sha256 "a3fae356d6afc4798f3217e6926e22f9371cfd28484f144eb87841bc8fe9bf17"
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
