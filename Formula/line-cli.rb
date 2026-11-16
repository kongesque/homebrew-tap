class LineCli < Formula
  desc "Unofficial LINE client for personal accounts"
  homepage "https://github.com/kongesque/line-cli"
  version "0.7.0"
  license "MIT"

  on_arm do
    url "https://github.com/kongesque/line-cli/releases/download/v0.7.0/line-darwin-arm64.tar.gz"
    sha256 "e1c8cc932afc542e219d948f50008fb660058cd0e348b2a78a00e9451e6d6bf0"
  end

  on_intel do
    url "https://github.com/kongesque/line-cli/releases/download/v0.7.0/line-darwin-amd64.tar.gz"
    sha256 "9644029d2a04ef282118c1e50fef69e46ba6e4ed06d78fd32a614388ce7dae52"
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
