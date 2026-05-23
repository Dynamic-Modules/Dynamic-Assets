# Dynamic Assets

Dynamic Assets is a core Dynamic SS13 Modules integration module for non-DM,
non-TGUI assets such as icons, sounds, maps, JSON data, and other build inputs.
It is where asset-aware prepare behavior can evolve without hardcoding asset
rules into the framework bootstrap.

The initial slice is deliberately small:

- registers itself through the generic prepare plugin API
- reads every module's declared `build.assets` files
- writes `.dynamic_modules_build/assets/index.json`
- exposes the generated index through `.dynamic_modules_build/index.json`

This does not yet copy or rewrite host assets. It gives modules and maintainer
tools a stable place to discover asset contributions before we add higher-level
asset patching or bundling behavior.

## Module Manifest

Modules that need future Dynamic Assets features should depend on this module:

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
