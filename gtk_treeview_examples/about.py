# about.py

import platform

from importlib.metadata import distribution, files
from pathlib import Path
import tomlkit

NAME = ''
# Single-source the project version from pyproject.toml
VERSION = 'Unknown'
COPYRIGHT = 'Copyright © 2021 Chris Brown and Marcris Software'
DESCRIPTION = ''
AUTHORS = [
    'Chris Brown <chris@marcrisoft.co.uk>'
]

def whence(distributionname, modulename):
    # obtain and print the project's version,
    # either from pyproject.toml during development ...
    global VERSION, DESCRIPTION
    pyproject_toml_path = Path('../pyproject.toml')
    if pyproject_toml_path.exists():
        with open(file=str(pyproject_toml_path)) as f:
            pyproject_toml = tomlkit.parse(string=f.read())
            if 'tool' in pyproject_toml and 'poetry' in pyproject_toml['tool']:
                VERSION = pyproject_toml['tool']['poetry']['version']
                DESCRIPTION = pyproject_toml['tool']['poetry']['description']

        print(f"Using {modulename} development version (to be version {VERSION})")
    else:
        # ... or using importlib.metadata.version once installed.
        dist = distribution(distributionname)
        metadata = dist.metadata
        print(f"Using {modulename} from package {metadata['name']} version {metadata['version']}")
        print(f"Imported from {files(metadata['name'])[0].locate()}")

        return metadata
