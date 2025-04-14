# 📦 moddb-addon-manager

A GitHub Action to upload or update addons on [moddb.com](https://moddb.com).
It logs in to your ModDB account, uploads a .zip addon file with a thumbnail, and handles optional metadata like tags, platforms, licence, and more.

## 🚀 Features
* Upload new addons to a ModDB mod page
* Update existing addons by URL
* Secure login via GitHub secrets
* Works in CI/CD pipelines

## 📥 Inputs

| Name             | Required | Description                                                  |
|------------------|----------|--------------------------------------------------------------|
| `mode`           | ✅       | `upload` or `update`                                         |
| `moddb_username` | ✅       | Your ModDB username                                          |
| `moddb_password` | ✅       | Your ModDB password                                          |
| `mod_url`        | ❌       | Required only for `upload` mode                              |
| `addon_url`      | ❌       | Required only for `update` mode                              |
| `addon_path`     | ❌       | Path to `.zip` file for upload                               |
| `thumbnail_path` | ❌       | Path to thumbnail image for upload                           |
| `name`           | ❌       | Addon name/title                                             |
| `summary`        | ❌       | Addon summary (min 50, max 1000 chars)                       |
| `description`    | ❌       | Addon description (min 100, max 100000 chars, HTML allowed)  |
| `category`       | ❌       | Addon category (e.g. `player_skin`)                          |
| `platforms`      | ❌       | Comma-separated platform list (e.g. `windows,linux`)         |
| `credits`        | ❌       | Optional credit line                                         |
| `tags`           | ❌       | Comma-separated tags (e.g. `patch,release`)                  |
| `licence`        | ❌       | Licence enum (e.g. `mit`, `proprietary`, `gpl`)              |
| `file_url`       | ❌       | Only useable in `update` mode                                |

## 🧪 Example Usage

```yaml
jobs:
  deploy-addon:
    runs-on: ubuntu-latest
    steps:
      - uses: Tosox/moddb-addon-manager@v1
        with:
          mode: upload
          moddb_username: ${{ secrets.MODDB_USER }}
          moddb_password: ${{ secrets.MODDB_PASS }}
          mod_url: https://www.moddb.com/mods/my-mod
          addon_path: ./dist/my-addon.zip
          thumbnail_path: ./media/thumb.jpg
          name: Cool Addon
          summary: Adds cool stuff to the mod.
          description: >
            This update adds <b>explosive</b> new features!
          category: player_skin
          platforms: windows,linux
          tags: patch,release
          licence: mit
```

## 📤 Outputs

| Name          | Description                 |
|---------------|-----------------------------|
| `result`      | Either uploaded or updated  |

## 🧱 Available Enum Values

`category` (AddonCategory)
```
maps, skins, models, audio, graphics, hud, gui, effects_gfx, ...
```

`platforms` (PlatformCategory)
```
windows, linux, mac, ps5, switch, steamdeck, web, android, ...
```

`licence` (Licence)
```
mit, gpl, lgpl, proprietary, commercial, public_domain, ...
```

(See [moddb.enums](https://github.com/Tosox/moddb/blob/develop/moddb/enums.py) for full lists)

## 🔐 Security

You must store your ModDB credentials as GitHub secrets:
* MODDB_USERNAME
* MODDB_PASSWORD

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
