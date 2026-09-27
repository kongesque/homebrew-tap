class LineCli < Formula
  desc "Unofficial LINE client for personal accounts"
  homepage "https://github.com/kongesque/line-cli"
  version "0.3.1"
  license "MIT"

  on_arm do
    url "https://github.com/kongesque/line-cli/releases/download/v0.3.1/line-darwin-arm64.tar.gz"
    sha256 "d60657ee45acf9fa5d112acc45c6c008e46345802e399e1b417f3f030a58a2fa"
  end

  on_intel do
    url "https://github.com/kongesque/line-cli/releases/download/v0.3.1/line-darwin-amd64.tar.gz"
    sha256 "51ed5e9b66f48ea700055d1a80639fcaaeee84adaada77c3f27c43a852af11bc"
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
