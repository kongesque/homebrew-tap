class LineCli < Formula
  desc "Unofficial LINE client for personal accounts"
  homepage "https://github.com/kongesque/line-cli"
  url "https://github.com/kongesque/line-cli/archive/refs/tags/cli-v0.1.0.tar.gz"
  sha256 "4609031545743c4ab31a714c5ce09fe1e6d31cd9f43a178bbb1ec5a7f243d07e"
  license "MIT"

  depends_on "go" => :build
  depends_on :macos

  def install
    ENV["CGO_ENABLED"] = "1"
    system "go", "build", *std_go_args(output: bin/"line", ldflags: "-s -w -X main.version=cli-v#{version}"),
           "./cmd/line"
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/line version")
  end
end
