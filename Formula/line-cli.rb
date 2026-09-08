class LineCli < Formula
  desc "Unofficial LINE client for personal accounts"
  homepage "https://github.com/kongesque/line-cli"
  version "0.1.0"
  license "MIT"

  depends_on :macos

  on_arm do
    url "https://github.com/kongesque/line-cli/releases/download/cli-v0.1.0/line-darwin-arm64.tar.gz"
    sha256 "add25c7bf9aa03b9c744b11e011ce52bd26aaba8ddd181ee9e0e425575f7b906"
  end

  on_intel do
    url "https://github.com/kongesque/line-cli/releases/download/cli-v0.1.0/line-darwin-amd64.tar.gz"
    sha256 "be0e1d27e7dbcf40b09285b796fb5dc8e399e35a2ac26cdee7179735a2b7c495"
  end

  def install
    bin.install "line"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/line version")
  end
end
