# Dynamic Assets

Dynamic Assets is a core Dynamic SS13 Modules integration module for non-DM,
non-TGUI assets such as icons, sounds, maps, JSON data, and other build inputs.
It keeps asset-aware prepare behavior updateable as a module instead of
hardcoded into the framework bootstrap.

The 1.0 slice is deliberately small:

- registers itself through the generic prepare plugin API
- reads every module's declared `build.assets` files
- writes `.dynamic_modules_build/assets/index.json`
- exposes the generated index through `.dynamic_modules_build/index.json`

The 1.0 scope indexes asset contributions. It does not copy or rewrite host
assets yet, but it gives modules and maintainer tools a stable place to
discover asset contributions before higher-level asset patching or bundling
behavior is added.

## Module Manifest

Modules that need Dynamic Assets indexing should depend on this module:

```toml
[load]
requires = ["dynamic-assets"]

[build]
assets = ["icons/**/*.dmi", "sound/**/*.ogg"]
```

## Generated Output

```text
.dynamic_modules_build/assets/index.json
```

The file is disposable build output and should not be committed.

## Local Development

Run the prepare plugin syntax check from this repo:

```bash
python3 -m py_compile prepare_plugin.py
```
