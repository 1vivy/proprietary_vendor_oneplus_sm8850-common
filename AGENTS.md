# PROJECT KNOWLEDGE BASE
**Project:** proprietary_vendor_oneplus_sm8850-common
**Seeded-at-ref:** oneplus/lineage-23.2
**Seeded-at-oid:** af791f92595703f1c5d6a4236a98a5f1c821229f
**Seeded-at-date:** 2026-08-14
**Generated-policy-sha256:** 831fceec497e89cad3d18f57f71d7d9fbc2bf2498062efbc079821f326bd17f0

## UPSTREAM DISTILLATION

### Scope and ownership

This is generated proprietary payload shared by SM8850 OnePlus products. It packages vendor, ODM, system, system_ext, and product artifacts required by the common device graph. It is not the owner of open HAL contracts or policy; the source declarations and extraction logic live in `device/oneplus/sm8850-common/proprietary-files*.txt`.

### Build graph and layout

- `sm8850-common-vendor.mk` is the generated product mapping. `Android.mk`, `Android.bp`, and `BoardConfigVendor.mk` package generated prebuilts and board inputs.
- `proprietary/odm/` carries Oplus-specific init, charger, touch, sensor, and media configuration.
- `proprietary/vendor/` is the main QTI/Oplus HAL, library, firmware, display, audio, media, security, thermal, radio, and sensor payload surface.
- `proprietary/system/`, `system_ext/`, and `product/` carry their matching partition-scoped components and permissions.
- `.lfsconfig` marks large payload as Git LFS content. Validate hydration before interpreting a small file as the real artifact.

### Interface, init, and sepolicy boundaries

The generated tree contains rc files and prebuilt service implementations, but authors no open AIDL/HIDL contract or SELinux policy. Service ownership is established by the matching source interface, VINTF/init declaration, package selection, and sepolicy in open repositories. Treat a prebuilt rc or binary as an input to that join, not proof that the product should expose the service.

### Extension precedents

The base history removes vendor interfaces when open source takes ownership. Follow that deblob pattern: preserve only measured backend payload, update the common extraction declarations, regenerate this tree, and reconcile init, VINTF, dependencies, and policy in the owning source projects. Lineage/crDroid extensions must remain typed and must not publish opaque IDs or raw nodes.

### Conventions and verification

`sm8850-common-vendor.mk` is explicitly generated and must not be edited by hand. Upstream subjects use `sm8850-common: <imperative description>`; stock refreshes identify their OOS source. Every change is paired with extraction declarations and checked for undeclared/missing payload, exact partition placement, LFS hydration, ELF dependency closure, and stale service/config references. Never patch binary bytes to bypass the extraction workflow.

## OUR DELTAS

None at seed. Later entries must name topic commit OIDs and must not rewrite upstream truth.
