# proprietary_vendor_oneplus_sm8850-common — agent carrier

<!-- rom-ops:carrier
project = "proprietary_vendor_oneplus_sm8850-common"
seeded_at_ref = "oneplus/lineage-23.2"
seeded_at_oid = "af791f92595703f1c5d6a4236a98a5f1c821229f"
date = "2026-08-15"
-->

## Upstream distillation

This repository is generated proprietary output, not a source implementation. At the pinned commit it contains 1,634 tracked paths: 1,381 under `proprietary/vendor`, 116 under `proprietary/system_ext`, 113 under `proprietary/odm`, 15 under `proprietary/product`, four under `proprietary/system`, and the generated root metadata. Do not inspect or edit binary payload contents.

- `Android.bp`, `Android.mk`, `BoardConfigVendor.mk`, and `sm8850-common-vendor.mk` all identify themselves as automatically generated. `Android.mk` only establishes `LOCAL_PATH`, and `BoardConfigVendor.mk` is an empty generated stub; the substantive declarations are Soong modules in `Android.bp` and product assembly in `sm8850-common-vendor.mk`.
- The generator input is the corresponding source/device tree's `proprietary-files.txt`, processed by the LineageOS `extract-utils` setup/extraction scripts. That input is not stored in this pinned vendor tree. Change the source declaration, run its setup/extraction flow, and commit the regenerated metadata and payload sync here; do not hand-maintain generated output as an independent source of truth.
- `Android.bp` gives module-backed blobs a `name` and a payload path in `srcs` or `src`, plus an install class and partition property. For example, module `btaudio_offload_if` reads `proprietary/vendor/lib64/btaudio_offload_if.so` and is `soc_specific`. The file also declares prebuilt binaries, apps, JARs, APEX files, XML modules, scripts, RFSA files, symlinks, and their dependency closure.
- `sm8850-common-vendor.mk` exports the Soong namespace and packages the result. `PRODUCT_COPY_FILES` maps literal payloads to `$(TARGET_COPY_OUT_ODM)`, `PRODUCT`, `SYSTEM`, `SYSTEM_EXT`, or `VENDOR`; its first pinned rule maps `proprietary/odm/etc/camera/media_profiles.xml` into ODM. `PRODUCT_PACKAGES` names the modules generated in `Android.bp`, including libraries, services, apps, and XML fragments.
- The physical layout mirrors destination partitions: examples present at the pin are `proprietary/odm/etc/camera/media_profiles.xml`, `proprietary/product/app/uimremoteclient/uimremoteclient.apk`, `proprietary/system/etc/sysconfig/qti_whitelist.xml`, `proprietary/system_ext/bin/horae`, and `proprietary/vendor/lib64/btaudio_offload_if.so`. In Soong, these destinations appear chiefly as `device_specific`, `product_specific`, `system_ext_specific`, and `soc_specific` respectively.
- XML is part of the runtime contract, not proof that its implementation is packaged. VINTF fragments such as `proprietary/vendor/etc/vintf/manifest/manifest_audiocorehal_default.xml` and service/config files such as `proprietary/vendor/etc/audio/sku_canoe/plugin_manager.xml` must agree with the executable or library modules that the generated files actually install.

Treat each declared blob as a three-way invariant: the source-side `proprietary-files.txt` row, the generated packaging declaration (`Android.bp` module plus `PRODUCT_PACKAGES`, or a `PRODUCT_COPY_FILES` rule), and the payload under `proprietary/<partition>/...` must all agree. A missing payload normally appears during Soong/Ninja as a missing `src`/`srcs` or copy source; a missing generated module/package row appears as an undefined module or as a runtime component that is never installed. A manifest or audio configuration can still parse while its service/effect library is absent, producing a runtime registration failure instead of an early parse failure. Conversely, an undeclared payload is dead weight and is not evidence that the product ships it.

The source declaration change and its proprietary sync commit are one atomic change: land both together or land neither. Before merging, compare the declaration set, generated module/copy/package rows, and payload paths in both directions. Extraction should be section-scoped when the common list is a union of multiple donors; an unrelated full extraction can overwrite or delete valid blobs supplied by another variant.

Keep a payload here only when it is shared by SM8850 targets and its complete dependency/configuration contract is valid from the common namespace. Shared Qualcomm platform services and libraries (graphics, radio/IMS, GNSS, media, common audio infrastructure, security, performance, connectivity) and genuinely shared OnePlus interfaces/configuration belong here. Variant calibration, panel/camera/sensor data, device-only services, and any ODM library whose dependencies exist only in one device repository belong in that device's vendor tree. Partition alone does not decide ownership: shared ODM content may remain common, but a common module must not depend on private per-device modules.

## Our deltas

Against `af791f92595703f1c5d6a4236a98a5f1c821229f`, current HEAD `7c6481e2cb67854cc286a390f5044551bf75f17d` has 101 changed paths (54 added, 47 modified) across ODM, system_ext, and vendor, plus regenerated metadata. The post-base sync moves the aggregate to the OxygenOS 16.0.9 extraction state and adds or refreshes shared charger, display-brightness, FIDO/cryptoeng, Dolby Vision/DVS, sensor-policy, ShareBuffer, media, audio, display, and power payloads; later cleanup commits retire redundant or malformed pieces.

The post-base AudioX history records the concrete declaration/payload mismatch class. A six-row common device declaration initially landed without any matching vendor payload. A later sync added `proprietary/vendor/lib64/soundfx/libeffectproxy.so` and five ODM AudioX files plus generated declarations. The ODM engine then moved to the per-device `infiniti` repository because it depends on private `libMNN` and `libc++_shared` modules, but the shared vendor effect proxy was accidentally retired while its common declaration remained. That state left the configured spatializer UUID with no backing effect and `dumpsys audio` reported no spatializer. Current commit `f9a6285db336df106c0059797b1425b4322dbb00` restores only `libeffectproxy`, its `Android.bp` module, and its `PRODUCT_PACKAGES` row; the device-specific engine remains out of this common repository.

These deltas reinforce the pairing rule: source declaration commits and vendor extraction/sync commits must be reviewed and landed as a pair. Moving a blob between common and per-device ownership must move its declaration, generated packaging, payload, and dependency closure together; removing only one side recreates the AudioX failure.

## Known defects

### DEF-PAIR-01 — AudioX effect proxy declaration lacked its payload
The common device tree declared `vendor/lib64/soundfx/libeffectproxy.so`, but this repository lacked the file and generated package/module rows, so the configured spatializer had no backing effect. Done means all declaration, payload, module, and package sides agree and the pair gate passes. See `docs/history/DEFECTS-2026-08.md` for the full investigation.

## Owner rulings

### Altered payload repositories are forks (2026-08-13)
A repository fetched as-is is a sync source, but any 1vivy payload alteration makes this repository a fork. Manifest and contract composition must identify the 1vivy fork rather than continuing to classify the altered repository as an as-is sync source. See `docs/history/DIRECTIVES-2026-08.md`.
