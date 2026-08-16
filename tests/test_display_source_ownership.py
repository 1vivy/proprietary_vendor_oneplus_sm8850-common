# SPDX-License-Identifier: Apache-2.0

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DisplaySourceOwnershipTest(unittest.TestCase):
    def test_mapper_fragment_is_source_owned(self) -> None:
        android_bp = (ROOT / "Android.bp").read_text(encoding="utf-8")
        vendor_mk = (ROOT / "sm8850-common-vendor.mk").read_text(encoding="utf-8")

        module = re.compile(
            r'prebuilt_etc_xml\s*\{[^}]*name:\s*"mapper\.qti\.xml"',
            re.DOTALL,
        )
        package = re.compile(r"^\s+mapper\.qti\.xml\s+\\$", re.MULTILINE)

        self.assertIsNone(module.search(android_bp))
        self.assertIsNone(package.search(vendor_mk))
        self.assertFalse(
            (
                ROOT
                / "proprietary/vendor/etc/vintf/manifest/mapper.qti.xml"
            ).exists()
        )


if __name__ == "__main__":
    _ = unittest.main()
