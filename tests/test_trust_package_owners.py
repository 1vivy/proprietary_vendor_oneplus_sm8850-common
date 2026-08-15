# SPDX-License-Identifier: Apache-2.0

import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID_BP = (ROOT / "Android.bp").read_text(encoding="utf-8")
VENDOR_MK = (ROOT / "sm8850-common-vendor.mk").read_text(encoding="utf-8")

CAMERA_NAMESPACE_PACKAGES = {
    "manifest_oplus_cryptoeng.xml",
    "manifest_oplus_fido2.xml",
}

COMMON_PACKAGES = {
    "android.hardware.security.onekeymint-service-qti",
    "android.hardware.security.onekeymint-service-qti.xml",
    "android.hardware.security.secureclock-service-qti.xml",
    "android.hardware.security.sharedsecret-service-qti.xml",
    "manifest_oplus_fingerprint_aidl_v3.xml",
    "manifest_oplus_ifaa.xml",
    "vendor.oplus.hardware.biometrics.fingerprint@2.1-service_uff",
    "vendor.oplus.hardware.biometrics.fingerprintpay@1.0-service",
}

TRUST_MANIFESTS = {
    "proprietary/odm/etc/vintf/manifest/manifest_oplus_fingerprint_aidl_v3.xml",
    "proprietary/odm/etc/vintf/manifest/manifest_oplus_ifaa.xml",
    "proprietary/vendor/etc/vintf/manifest/android.hardware.security.onekeymint-service-qti.xml",
    "proprietary/vendor/etc/vintf/manifest/android.hardware.security.secureclock-service-qti.xml",
    "proprietary/vendor/etc/vintf/manifest/android.hardware.security.sharedsecret-service-qti.xml",
}

SYSTEM_EXT_PERMISSION_ROOT = Path("proprietary/system_ext/etc/permissions")
ODM_PERMISSION_ROOT = Path("proprietary/odm/etc/permissions")
COMMON_FIDO_LIBRARIES = {
    "vendor.oplus.hardware.fido.fidoca-V1-java": (
        SYSTEM_EXT_PERMISSION_ROOT / "vendor-oplus-hardware-biometrics-fido.xml",
        "vendor-oplus-hardware.fido.fidoca-V1.0",
    ),
    "vendor.oplus.hardware.fido.fido2ca-V1-java": (
        SYSTEM_EXT_PERMISSION_ROOT / "vendor-oplus-hardware-biometrics-fido2.xml",
        "vendor-oplus-hardware.fido.fido2ca-V1.0",
    ),
}
RETIRED_ODM_FIDO_REGISTRATIONS = {
    ODM_PERMISSION_ROOT / "vendor-oplus-hardware-biometrics-fido.xml",
    ODM_PERMISSION_ROOT / "vendor-oplus-hardware-biometrics-fido2.xml",
}
RETIRED_TA_PATHS = {
    ROOT / f"proprietary/odm/firmware/secure_ta/{family}.{suffix}"
    for family in ("cryptoeng", "fidoctap", "fidotap")
    for suffix in (*[f"b0{index}" for index in range(9)], "mdt")
}


def product_packages() -> list[str]:
    packages: list[str] = []
    collecting = False
    for raw_line in VENDOR_MK.splitlines():
        line = raw_line.strip()
        if line.startswith("PRODUCT_PACKAGES +="):
            collecting = True
            line = line.removeprefix("PRODUCT_PACKAGES +=").strip()
        elif not collecting:
            continue

        continued = line.endswith("\\")
        value = line.removesuffix("\\").strip()
        if value:
            packages.extend(value.split())
        collecting = continued
    return packages


class TrustPackageOwnersTest(unittest.TestCase):
    def test_camera_namespace_manifests_are_not_selected_by_common(self) -> None:
        selected = set(product_packages())
        self.assertEqual(set(), CAMERA_NAMESPACE_PACKAGES & selected)

    def test_common_trust_packages_have_one_module_and_selector(self) -> None:
        selected = product_packages()
        for package in COMMON_PACKAGES:
            self.assertEqual(1, selected.count(package), package)
            definitions = re.findall(
                rf'^\s*name:\s*"{re.escape(package)}"', ANDROID_BP, re.MULTILINE
            )
            self.assertEqual(1, len(definitions), package)

    def test_common_fido_libraries_have_one_system_ext_owner(self) -> None:
        selected = product_packages()
        for module, (relative_xml, library_name) in COMMON_FIDO_LIBRARIES.items():
            self.assertEqual(1, selected.count(module), module)
            definitions = re.findall(
                rf'^\s*name:\s*"{re.escape(module)}"', ANDROID_BP, re.MULTILINE
            )
            self.assertEqual(1, len(definitions), module)

            library = ET.parse(ROOT / relative_xml).getroot().find("library")
            self.assertIsNotNone(library, relative_xml)
            if library is None:
                raise AssertionError(f"missing library declaration: {relative_xml}")
            self.assertEqual(library_name, library.attrib.get("name"))
            self.assertEqual(
                f"/system/system_ext/framework/{module}.jar",
                library.attrib.get("file"),
            )

        for relative_xml in RETIRED_ODM_FIDO_REGISTRATIONS:
            self.assertFalse((ROOT / relative_xml).exists(), relative_xml)
        for path in RETIRED_TA_PATHS:
            self.assertFalse(path.exists(), str(path.relative_to(ROOT)))

    def test_common_trust_vintf_instances_are_singletons(self) -> None:
        owners: dict[tuple[str, str, str, str], list[str]] = {}
        for relative_path in TRUST_MANIFESTS:
            root = ET.parse(ROOT / relative_path).getroot()
            self.assertEqual("manifest", root.tag)
            self.assertEqual("device", root.attrib.get("type"))
            for hal in root.findall("hal"):
                hal_format = hal.attrib.get("format", "hidl")
                hal_name = hal.findtext("name")
                if hal_name is None:
                    raise AssertionError(f"missing HAL name in {relative_path}")
                for fqname in hal.findall("fqname"):
                    if fqname.text is None:
                        raise AssertionError(f"empty fqname in {relative_path}")
                    interface, instance = fqname.text.split("/", 1)
                    key = (hal_format, hal_name, interface, instance)
                    owners.setdefault(key, []).append(relative_path)
                for interface in hal.findall("interface"):
                    interface_name = interface.findtext("name")
                    if interface_name is None:
                        raise AssertionError(f"missing interface in {relative_path}")
                    for instance in interface.findall("instance"):
                        if instance.text is None:
                            raise AssertionError(f"empty instance in {relative_path}")
                        key = (hal_format, hal_name, interface_name, instance.text)
                        owners.setdefault(key, []).append(relative_path)

        self.assertTrue(owners)
        for key, providers in owners.items():
            self.assertEqual(1, len(providers), f"{key}: {providers}")


if __name__ == "__main__":
    _ = unittest.main()
