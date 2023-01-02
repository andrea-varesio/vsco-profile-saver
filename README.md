# ⚠️ WARNING ⚠️
This project is no longer being maintained. Use at your own risk.

# VSCO Profile Saver

## What is it
It's a tool to automate the download of original media files from **your own** VSCO profile.

This tool is able to handle interruptions during download and, at any point, you can resume the last session with `vps.py -r`, or a different session with `vps.py -R RESUME_FILE`.

Session files are generated when the script is started and are located in the script's directory in the `vsco_sessions` subdirectory.

## What it does NOT do
This tool cannot download media files from _any_ VSCO profile, as it requires a `media.json` file exported from your account settings.

## Requirements
- Install Python requirements with `pip install -r requirements.txt`
- `images.json` and/or `videos.json` file [*].

[*] You first need to log into your VSCO account from a desktop browser, then head to account settings and export a `Snapshot` of your data. Once you download the `.zip` file, extract it and feed the required `.json` files to this script (`vps.py -i /path/to/media.json`).

## Usage
```
vps.py [-h] [-l] [-i INPUT | -r | -R RESUME_FILE] [-o OUTPUT_DIR] [-v | -q]
```

Short | Argument | Info
---|---|---
`-h` | `--help` | show this help message and exit
`-l` | `--license` | show license and exit
`-i INPUT` | `--input INPUT` | path to input media.json
`-r` | `--resume` | resume last session
`-R RESUME_FILE` | `--resume-file RESUME_FILE` | resume specified session
`-o OUTPUT_DIR` | `--output-dir OUTPUT_DIR` | path to output dir (Default: $HOME)
`-v` | `--verbose` | increase verbosity
`-q` | `--quiet` | disable all verbosity


## Contributions
Contributions are welcome, feel free to submit issues and/or pull requests.

The script works without any issues with `images.json`, however it has not been tested with `videos.json`.

## Disclaimer
This tool is neither affiliated with, nor endorsed by VSCO in any way.

## LICENSE
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

"vsco-profile-saver" - Download all media files from your VSCO account.<br />
Copyright (C) 2023 Andrea Varesio <https://www.andreavaresio.com/>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a [copy of the GNU General Public License](https://github.com/andrea-varesio/vsco-profile-saver/blob/main/LICENSE)
along with this program.  If not, see <https://www.gnu.org/licenses/>.

<div align="center">
<a href="https://github.com/andrea-varesio/vsco-profile-saver/">
  <img src="http://hits.dwyl.com/andrea-varesio/vsco-profile-saver.svg?style=flat-square" alt="Hit count" />
</a>
</div>
