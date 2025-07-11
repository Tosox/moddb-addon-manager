import os
import sys
import moddb
from moddb import AddonCategory, PlatformCategory, Licence


def set_output(name, value):
    with open(os.getenv("GITHUB_OUTPUT"), 'a') as f:
        print(f"{name}={value}", file=f)

def assert_required(var, msg):
    if not var:
        print(f"::error title=Missing input::{msg}")
        sys.exit(1)

def parse_platforms(platform_str):
    if not platform_str:
        return []

    platforms = []
    for p in platform_str.split(","):
        p = p.strip()
        try:
            platforms.append(PlatformCategory[p])
        except KeyError:
            print(f"::error title=Invalid platform::'{p}' is not a valid platform")
            print(f"Valid options: {', '.join([e.name for e in PlatformCategory])}")
            sys.exit(1)
    return platforms


def parse_tags(tag_str):
    return [t.strip() for t in tag_str.split(",")] if tag_str else []


def parse_enum(enum_cls, value, default=None):
    if not value:
        return default
    try:
        return enum_cls[value]
    except KeyError:
        print(f"::error title=Invalid enum::{value} is not valid for {enum_cls.__name__}")
        print(f"Valid options: {', '.join([e.name for e in enum_cls])}")
        sys.exit(1)


def main():
    mode = os.getenv("MODE")
    assert_required(mode, "Missing required input: MODE")

    username = os.getenv("MODDB_USERNAME")
    password = os.getenv("MODDB_PASSWORD")
    assert_required(username, "Missing required input: MODDB_USERNAME")
    assert_required(password, "Missing required input: MODDB_PASSWORD")

    mod_url = os.getenv("MOD_URL")
    addon_url = os.getenv("ADDON_URL")
    addon_path = os.getenv("ADDON_PATH")
    thumbnail_path = os.getenv("THUMBNAIL_PATH")
    name = os.getenv("NAME")
    summary = os.getenv("SUMMARY")
    description = os.getenv("DESCRIPTION")
    category = os.getenv("CATEGORY")
    platforms = os.getenv("PLATFORMS")
    credits = os.getenv("CREDITS")
    tags = os.getenv("TAGS")
    license = os.getenv("LICENSE")
    file_url = os.getenv("FILE_URL")

    try:
        client = moddb.Client(username, password)
    except ValueError:
        print(f"::error title=Authentication Failed::Login failed for user '{username}'")
        sys.exit(1)

    print(f"✅ Successfully logged in as {username}")

    category_enum = parse_enum(AddonCategory, category)
    license_enum = parse_enum(Licence, license, Licence.proprietary)
    platform_list = parse_platforms(platforms)
    tag_list = parse_tags(tags)

    if mode == "upload":
        for var, msg in [
            (mod_url, "MOD_URL"),
            (addon_path, "ADDON_PATH"),
            (thumbnail_path, "THUMBNAIL_PATH"),
            (name, "NAME"),
            (summary, "SUMMARY"),
            (description, "DESCRIPTION"),
            (category_enum, "CATEGORY"),
        ]:
            assert_required(var, f"Missing required input for upload: {msg}")

        for var, msg in [
            (addon_url, "ADDON_URL"),
            (file_url, "FILE_URL"),
        ]:
            if var:
                print(f"::warning title=Optional input::{msg} is not required for upload mode. Ignoring.")

        mod = moddb.Mod(moddb.get_page(mod_url))
        client.upload_addon(
            mod=mod,
            addon_path=addon_path,
            thumbnail_path=thumbnail_path,
            category=category_enum,
            name=name,
            summary=summary,
            description=description,
            platforms=platform_list,
            licence=license_enum,
            credits=credits or "",
            tags=tag_list
        )

        print("✅ Addon uploaded successfully")
        set_output("result", "uploaded")

    elif mode == "update":
        assert_required(addon_url, "Missing required input: ADDON_URL")

        for var, msg in [
            (mod_url, "MOD_URL")
        ]:
            if var:
                print(f"::warning title=Optional input::{msg} is not required for update mode. Ignoring.")

        addon = moddb.Addon(moddb.get_page(addon_url))
        client.update_addon(
            addon=addon,
            addon_path=addon_path,
            thumbnail_path=thumbnail_path,
            category=category_enum,
            name=name,
            summary=summary,
            description=description,
            platforms=platform_list,
            licence=license_enum,
            credits=credits,
            tags=tag_list,
            url=file_url
        )

        print("✅ Addon updated successfully")
        set_output("result", "updated")

    else:
        print(f"::error title=Invalid mode::{mode} is not supported. Use 'upload' or 'update'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
