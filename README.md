# About
This script maps Windows cursor names to Xcursor counterparts and creates a ready-to-use Xcursor file structure.
Requires already converted Windows cursor files (by for example `win2xcur`).

Link to [win2xcur] GitHub page.

[win2xcur]: https://github.com/quantum5/win2xcur/tree/master

## Definitions
    <input_folder>    - folder with Windows cursor files (.ani and .cur)
    <convert_folder>  - folder with files converted by win2xcur
    <output_folder>   - folder with properly named Xcursor files

## Step by step instruction

1.     pip install win2xcur
    - used to do the initial conversion between Windows and Xcursor file formats
    - can (and probably should) be used with a venv

2.     win2xcur <input_folder>/*.{ani,cur} -o <convert_folder>
    - the output folder must exist
    - if the original cursor does not have .ani files (or .cur, but that's very rare) you'll get an error, in which case use:
      
      `<input_folder>/*.cur -o <convert_folder>`

3.     python ./cursor_map.py -i <convert_folder> -o <output_folder> -n "YourCursorName"
    - depending on your PATH entry use 'python' or 'python3'
    - the cursor name should match the output folder name for consistency
    - optionally specify a custom mappings file with `-m <mappings_file>`

4. open `<output_folder>/cursors/default` in an image editor and export to thumbnail.png, save in `<output_folder>`

## Destination folder
Once you have a folder with proper Xcursor files, move it to either:
- /usr/share/icons - makes cursor available for all users, requires root
- /home/<your_username>/.icons - makes it available only for you


# Notes
- Right now the script creates copies instead of making symbolic links for icons that share the icon data but differ in name. Minor performance overhead for the system.
- Entries in `mappings.txt` were filled by hand through an eyeball search, mistakes may have been made. Feel free to tweak `mappings.txt` to your liking.