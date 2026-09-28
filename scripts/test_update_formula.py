import hashlib
import unittest

from update_formula import archive_checksums, release_assets, render_formula, verify_archives


TAG = "v0.4.0"
BASE = "https://github.com/kongesque/line-cli/releases/download/v0.4.0/"
ARM = "line-darwin-arm64.tar.gz"
INTEL = "line-darwin-amd64.tar.gz"


def release():
    return {
        "tag_name": TAG,
        "draft": False,
        "prerelease": False,
        "assets": [
            {"name": name, "browser_download_url": BASE + name, "size": 100}
            for name in (ARM, INTEL, "SHA256SUMS.txt")
        ],
    }


FORMULA = '''class LineCli < Formula
  version "0.3.1"
  on_arm do
    url "https://github.com/kongesque/line-cli/releases/download/v0.3.1/line-darwin-arm64.tar.gz"
    sha256 "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  end
  on_intel do
    url "https://github.com/kongesque/line-cli/releases/download/v0.3.1/line-darwin-amd64.tar.gz"
    sha256 "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
  end
end
'''


class FormulaUpdateTests(unittest.TestCase):
    def test_updates_both_architectures(self):
        checksums = {ARM: "c" * 64, INTEL: "d" * 64}
        updated = render_formula(FORMULA, TAG, checksums)
        self.assertIn('version "0.4.0"', updated)
        self.assertIn(BASE + ARM, updated)
        self.assertIn(BASE + INTEL, updated)
        self.assertIn('sha256 "' + "c" * 64 + '"', updated)
        self.assertIn('sha256 "' + "d" * 64 + '"', updated)
        self.assertEqual(updated.count("  on_arm do"), 1)
        self.assertEqual(updated.count("  on_intel do"), 1)

    def test_rejects_downgrade(self):
        with self.assertRaisesRegex(ValueError, "downgrade"):
            render_formula(FORMULA, "v0.2.0", {ARM: "c" * 64, INTEL: "d" * 64})

    def test_requires_canonical_complete_assets(self):
        self.assertEqual(release_assets(release())[0], TAG)
        bad = release()
        bad["assets"][0]["browser_download_url"] = "https://example.com/archive"
        with self.assertRaisesRegex(ValueError, "URL"):
            release_assets(bad)
        missing = release()
        missing["assets"].pop()
        with self.assertRaisesRegex(ValueError, "Missing"):
            release_assets(missing)

    def test_rejects_duplicate_or_missing_checksums(self):
        line = ("a" * 64 + "  " + ARM + "\n").encode()
        with self.assertRaisesRegex(ValueError, "Missing"):
            archive_checksums(line)
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            archive_checksums(line + line)

    def test_verifies_downloaded_archive_bytes_and_size(self):
        data = {ARM: b"arm archive", INTEL: b"intel archive"}
        assets = release_assets(release())[1]
        for name, body in data.items():
            assets[name]["size"] = len(body)
        digests = {name: hashlib.sha256(body).hexdigest() for name, body in data.items()}
        downloader = lambda url, limit: data[url.rsplit("/", 1)[-1]]
        verify_archives(assets, digests, downloader)
        with self.assertRaisesRegex(ValueError, "checksum mismatch"):
            verify_archives(assets, {**digests, ARM: "0" * 64}, downloader)
        assets[ARM]["size"] += 1
        with self.assertRaisesRegex(ValueError, "size mismatch"):
            verify_archives(assets, digests, downloader)


if __name__ == "__main__":
    unittest.main()
