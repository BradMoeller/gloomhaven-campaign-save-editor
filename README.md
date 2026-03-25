# Gloomhaven Save Editor

<img width="711" height="420" alt="image" src="https://github.com/user-attachments/assets/cbc35d8a-702e-412c-a393-211225f81fbe" />


Pick the wrong card when leveling up in a Gloomhaven campaign? Use this cross-platform editor to fix your save file.

`gloomhaven_editor.py` is a small desktop app for editing Gloomhaven digital campaign save files. It reads the game's `.dat` save format directly, detects the characters in the save, and lets you update each character's owned ability cards without hand-editing binary data.

## Quick Download

[Download `gloomhaven_editor.py`](https://raw.githubusercontent.com/BradMoeller/gloomhaven-campaign-save-editor/main/gloomhaven_editor.py)

## Features

- Opens Gloomhaven digital campaign `.dat` save files
- Detects imported characters automatically
- Creates one tab per imported character using `Name (Class)` labels
- Shows owned and not-owned ability cards for all supported classes
- Marks cards currently in the hand loadout with `*`
- Removes cards from the hand automatically if they are removed from owned cards
- Creates a `.bak` backup before saving
- Works on Windows, macOS, and Linux

## Requirements

- Python 3
- Tkinter

If Python is not installed yet, use one of the options below.

### Install Python

#### Windows

Download and install Python 3 from:

```text
https://www.python.org/downloads/windows/
```

During install, enable:

- `Add python.exe to PATH`

Then verify:

```powershell
py --version
```

If `py` is unavailable, try:

```powershell
python --version
```

#### macOS

Option 1: install Python 3 from python.org:

```text
https://www.python.org/downloads/macos/
```

Option 2: install with Homebrew:

```bash
brew install python
```

Then verify:

```bash
python3 --version
```

#### Linux

Most Linux distributions already include Python 3. If not, install it with your package manager.

Examples:

```bash
# Ubuntu / Debian
sudo apt install python3

# Fedora
sudo dnf install python3

# Arch
sudo pacman -S python
```

Then verify:

```bash
python3 --version
```

Tkinter is bundled with most Python installers on Windows and macOS. On Linux, you may need to install it separately.

Examples:

```bash
# Ubuntu / Debian
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

## Run It

Clone the repo or download the files, then run:

### Windows

```powershell
py gloomhaven_editor.py
```

If `py` is not available:

```powershell
python gloomhaven_editor.py
```

### macOS

```bash
python3 gloomhaven_editor.py
```

### Linux

```bash
python3 gloomhaven_editor.py
```

You can also make it executable and run it directly:

```bash
chmod +x gloomhaven_editor.py
./gloomhaven_editor.py
```

## How To Use

1. Close Gloomhaven.
2. Launch the editor.
3. Click `Open .dat…`.
4. Pick your campaign save file.
5. Use `Own >>` and `<< Unown` to adjust owned cards.
6. Click `Save`.

The editor creates a backup next to the save file before writing changes:

```text
Campaign_MyParty_123456.dat.bak
```

## Where Save Files Usually Live

The app shows a reference window when you click `Open .dat…`, but the common locations are below.

### Windows

Campaign saves are usually under:

```text
C:\Users\<YourUser>\AppData\LocalLow\FlamingFowlStudios\Gloomhaven\GloomSaves\Campaign
```

Look for folders named like:

```text
Campaign_<PartyName>_<ID>
```

Then open the `.dat` file inside that folder.

### macOS

Gloomhaven typically runs through a compatibility layer, so saves are often inside the Steam app data tree rather than a native macOS game folder:

```text
~/Library/Application Support/Steam/steamapps/compatdata/780290/pfx/drive_c/users/steamuser/AppData/LocalLow/FlamingFowlStudios/Gloomhaven/GloomSaves/Campaign
```

### Linux

On Linux, the important anchor is your Steam library's `steamapps` folder. That Steam library may be in your home directory or on another mounted drive.

Examples:

```text
~/.steam/steam/steamapps
~/.local/share/Steam/steamapps
/mnt/<drive>/SteamLibrary/steamapps
/media/<user>/<drive>/SteamLibrary/steamapps
```

From `steamapps`, go to:

```text
compatdata/780290/pfx/drive_c/users/steamuser/AppData/LocalLow/FlamingFowlStudios/Gloomhaven/GloomSaves/Campaign
```

Then open the `.dat` file inside your campaign folder.

## Editing Rules

- The editor manages `OwnedAbilityCardIDs`.
- Removing a card from owned cards also removes it from the saved hand loadout if needed.
- Hand editing is not exposed directly in the UI.
- The editor writes within the existing save-array capacity. If the owned-card array is full, remove a card first.

## Supported Classes

The editor includes ability card data for all 17 Gloomhaven digital classes:

- Brute
- Tinkerer
- Spellweaver
- Scoundrel
- Cragheart
- Mindthief
- Sunkeeper
- Quartermaster
- Summoner
- Nightshroud
- Plagueherald
- Berserker
- Soothsinger
- Doomstalker
- Sawbones
- Elementalist
- Beast Tyrant

## Notes

- Always close the game before editing saves.
- Keep the `.bak` file until you confirm the save loads correctly.
- This tool is intended for Gloomhaven digital campaign saves, not tabletop helper apps or board game save formats.

## License

MIT
