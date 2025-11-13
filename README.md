# deleteNodeModules.py

A small utility to find and remove common build/artifact folders such as `node_modules`, `.next`, and `dist` recursively.

## What it does
- Recursively walks from a specified root directory and finds directories named `node_modules`, `.next`, or `dist`.
- By default the script runs in a safe "dry run" mode where it only prints what would be deleted.

## Tested
I tested this on macOS (zsh) and it works fine in dry-run mode. Use with care before disabling dry-run.

## Safety / Dry-run
The script has a safety flag at the top of the file:

```python
# Safety: set to True to do a dry run (only log what would be deleted).
# Set to False to actually remove files/directories.
DRY_RUN = True
```

- Default: `DRY_RUN = True` (dry-run).
- To perform actual deletion, open `deleteNodeModules.py` and change `DRY_RUN = True` to `DRY_RUN = False`.

Important: disabling dry-run will delete files and directories permanently (via `shutil.rmtree`). Make sure you have backups or use version control and run the script from the correct directory.

## Usage
1. Open a terminal in the repository folder (or specify your target directory by editing the script):

```bash
cd /path/to/your/project
python3 deleteNodeModules.py
```

2. By default the script starts at `./` (the current directory) and `min_depth = 0` (so it will consider matches at any depth). If you want to change those defaults, edit the bottom section of the script:

```python
if __name__ == '__main__':
    target_directory = './'  # Replace with your root folder path
    min_depth = 0  # Minimum depth to start deleting (0 = all levels)
    
    find_and_delete_targets(target_directory, min_depth)
```

- Set `target_directory` to the path you want to scan.
- Increase `min_depth` to avoid deleting shallow matches (for example, `min_depth = 1` will skip immediate children of the root).

## Examples
- Dry run from current directory (default):

```bash
python3 deleteNodeModules.py
```

- Dry run from a custom folder (edit `target_directory` in the file), or run it from that folder:

```bash
cd /Users/alice/projects
python3 /path/to/deleteNodeModules.py
```

- To actually delete, edit `deleteNodeModules.py` and set `DRY_RUN = False`, then run the script. Double-check the path and `min_depth` first.

## Notes & Recommendations
- Always run the script in dry-run mode first to verify which directories it will remove.
- Consider adding a CLI wrapper (argparse) if you'd like to toggle dry-run, set target path, and set min depth without editing the file.
- The script removes directories using `shutil.rmtree` when `DRY_RUN` is `False` — this is irreversible.

## Troubleshooting
- If you hit permission errors, run as a user with the appropriate permissions or adjust ownership/permissions for target folders. Use caution with `sudo`.

## Install & run from terminal (pip)

After publishing to PyPI, developers can install and use the tool directly from the terminal. Recommended steps:

1. Install via pip (from PyPI):

```bash
python3 -m pip install --user cleanup-nodemodule
```

2. Make sure your user-level bin directory is on your PATH. On macOS that is commonly `$HOME/Library/Python/<pyversion>/bin`. Example for zsh/Python 3.9:

```bash
export PATH="$HOME/Library/Python/3.9/bin:$PATH"
# add the above line to ~/.zshrc to make it permanent
```

3. Run the installed CLI (dry-run is the default):

```bash
cleanup-nodemodule --help
cleanup-nodemodule -p /path/to/project      # dry-run: shows what would be deleted
cleanup-nodemodule -p /path/to/project --no-dry-run  # actually deletes targets
```

4. To uninstall or upgrade:

```bash
python3 -m pip uninstall cleanup-nodemodule
python3 -m pip install --user --upgrade cleanup-nodemodule
```

5. If the command `cleanup-nodemodule` isn't found after installation, either add the user scripts directory to PATH (see step 2) or run the script with the full path, for example:

```bash
$HOME/Library/Python/3.9/bin/cleanup-nodemodule --help
```

Security & behavior reminders
- The CLI defaults to dry-run (safe). To make the run destructive you must pass `--no-dry-run` explicitly.
- Always run a dry-run first and check the output before using `--no-dry-run`.

If you'd like, I can add a short `Examples` section showing real sample output from a dry-run and a recommended GitHub Actions workflow to publish on tag.

## macOS: Add Python install location to your PATH (optional)

If you installed Python via the official macOS installer or a framework build, the Python scripts directory may be at:

```
/Library/Frameworks/Python.framework/Versions/3.14/bin
```

If that directory is not already on your `PATH` you can add it so the `cleanup-nodemodule` command is available in every new terminal.

- Quick check (prints nothing if present):

```bash
echo "$PATH" | grep -q "/Library/Frameworks/Python.framework/Versions/3.14/bin" || echo "not present"
```

- To temporarily add it in the current shell session:

```bash
export PATH="/Library/Frameworks/Python.framework/Versions/3.14/bin:$PATH"
```

- To add it permanently for zsh (recommended on macOS), append the export to `~/.zshrc` only if it isn't already present:

```bash
grep -qxF 'export PATH="/Library/Frameworks/Python.framework/Versions/3.14/bin:$PATH"' ~/.zshrc 2>/dev/null || \
    echo 'export PATH="/Library/Frameworks/Python.framework/Versions/3.14/bin:$PATH"' >> ~/.zshrc

# Reload your shell configuration (or open a new terminal)
source ~/.zshrc
```

Notes:
- Replace `3.14` with your installed Python minor version if different (for example `3.11` or `3.9`).
- If you use a different shell (bash, fish, etc.) add the same export to your shell's startup file (e.g., `~/.bash_profile`, `~/.profile`, or `~/.config/fish/config.fish`).
- Appending to `~/.zshrc` is safe because the `grep` check avoids duplicate lines.


## License / Contribution
This is a small utility — feel free to adapt it. If you'd like, I can add CLI flags (safe defaults) or a confirmation prompt before destructive runs.
