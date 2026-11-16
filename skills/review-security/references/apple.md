# Apple application security

Use [MASVS](https://mas.owasp.org/MASVS/) for relevant mobile controls and
[MASTG](https://mas.owasp.org/MASTG/) for platform test techniques. Select controls
for the app's data and threat model; resistance to device-owner reverse engineering
is not a substitute for server-side authorization. Consult the actual deployment
target and [Apple Platform Security](https://support.apple.com/guide/security/welcome/web).

Inspect source, signed entitlements, release configuration and the built artifact
when available. Simulator results do not establish physical-device key protection,
biometric behavior, distribution signing or production entitlements.

- Inventory credentials, personal data, downloaded files, shared containers, caches,
  backups, screenshots/app-switcher previews, pasteboards and exported diagnostics.
  Use [Keychain Services](https://developer.apple.com/documentation/security/keychain-services)
  for appropriate small secrets. Verify accessibility/access-control settings, access
  groups, device migration/synchronization and logout behavior against requirements.
  UserDefaults or an embedded app key is not a secret store.
- Review [ATS](https://developer.apple.com/documentation/security/preventing-insecure-network-connections),
  exceptions and custom certificate/trust callbacks. Apple documents that ATS does
  not cover lower-level Network/CFNetwork calls; inspect their TLS configuration
  independently. Pinning needs a concrete threat model and certificate-rotation plan;
  do not add it blindly or disable trust checks to make a test work.
- Follow universal links/custom schemes, document imports, URL handling, WebView
  navigation, JavaScript bridges, extensions and app-group communication. Verify
  origin, resource ownership and authorization where an external input reaches a
  privileged action. A successful biometric UI alone is not backend authorization.
- On macOS, inspect sandbox/hardened-runtime exceptions, XPC/privileged-helper client
  authorization, file access and update verification. Signing/notarization establishes
  an artifact property, not the absence of application vulnerabilities.
- Review Swift unsafe pointers, Objective-C/C bridges, lifetime/concurrency assumptions,
  archive decoding, arithmetic and attacker-sized allocations. Safe Swift syntax
  does not prevent authorization bugs, races across awaits or denial of service.
- Check privacy permissions against actual use; avoid unnecessary entitlements. Treat
  logs, MetricKit/crash uploads and analytics as data egress, with bounded fields,
  redaction, retention and environment separation.

Use existing Xcode static analysis and supported sanitizers where relevant; SwiftLint
alone is not a security scanner. Pick a few tests through real entry points: a wrong
user/resource, malformed import/link, expired session or denied permission as applicable.
Do not jailbreak a device, intercept unrelated traffic or change system trust to audit
an app. Report device-only checks that could not run.

Check [Apple security releases](https://support.apple.com/en-us/100100), Swift/package
upstream advisories and the exact OS/toolchain/binary dependency versions. Changes to
minimum OS versions or user-visible permission flows need a product decision.
