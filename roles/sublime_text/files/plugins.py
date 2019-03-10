
import argparse
import json
import os


class Packages(object):
    def __init__(self, installed=[]):
        self.installed = installed
        self.ensured = []


def xdg_user_config():
    try:
        return os.environ["XDG_CONFIG_HOME"]
    except KeyError:
        # Ensure that HOME is only requested as backup
        return os.path.join(os.environ["HOME"], ".config")


def main():

    parser = argparse.ArgumentParser("Plugin installer")
    parser.add_argument("--ensure", action="append")

    args = parser.parse_args()

    packages = Packages()
    ensure_packages = args.ensure

    json_path = os.path.join(
        xdg_user_config(),
        "sublime-text-3/Packages/User/Package Control.sublime-settings"
    )
    with open(json_path) as f:
        data = json.load(f)

    packages.installed = set(sorted(data.get(
        "installed_packages",
        packages.installed
    )))
    packages.ensured = packages.installed.union(set(ensure_packages))

    if packages.installed == packages.ensured:
        return  # Already all installed

    data["installed_packages"] =\
        sorted(packages.ensured)

    with open(json_path, "w") as f:
        json.dump(data, f, indent="\t", sort_keys=True)


if __name__ == "__main__":
    main()
