# Soundboard themes

Original **Daylight** theme, media, standalone package, and authoring tools for Soundboard.

## Import Daylight

1. Open **Themes** in Soundboard.
2. Paste this manifest link:

```text
https://raw.githubusercontent.com/sproch/SoundboardThemes/main/Daylight/theme.json
```

3. Tap **Preview theme**, then **Install and apply**.

A normal [GitHub file link](https://github.com/sproch/SoundboardThemes/blob/main/Daylight/theme.json) also works. Once installed, the theme works offline.

You can also download [Daylight.soundboardtheme](https://github.com/sproch/SoundboardThemes/raw/refs/heads/main/Daylight.soundboardtheme) and import it through Files or AirDrop without a server. Use this route for private repositories; never put a GitHub personal access token into a theme or app bundle.

## Make your own

Copy `Daylight/`, then change its `id`, `name`, `author`, labels, colors, and media references in `theme.json`. Theme identifiers must be unique; `studio` belongs to the app's built-in theme. Choose distribution terms for your own content and describe them in `license` before publishing.

Theme images are PNG or JPEG. Audio may be WAV, M4A, MP3, or CAF. Keep media below 8 MB per image and 12 MB per audio file, 50 MB in total, and sounds below two minutes. Grid themes support 1–24 buttons. Radial themes support 2–8 buttons.

Run these standard-library Python tools from this folder:

```sh
python3 build_package.py Daylight
python3 validate_themes.py
```

The package builder recalculates byte sizes and SHA-256 hashes and writes `Daylight.soundboardtheme`. Commit the updated `theme.json` together with the media. Increase the integer `version` for updates, then import the link again in the app to apply the new version. Already-installed themes continue to work offline.

Themes contain JSON settings and media only. They cannot contain executable code, web pages, scripts, arbitrary actions, or remote assets outside the manifest's folder. Use only content you created or have permission to distribute.
