# PRE//BOARD — Class XII Progress Tracker

A minimal black-and-green CBSE Class XII pre-board tracker. The original layout, progress controls, autosave, filters and backup features are retained.

## Subject combinations
- **PCM:** English Core, Physics, Chemistry, Mathematics, Computer Science
- **PCB:** English Core, Physics, Chemistry, Biology, Hindi Core
- **PCMB:** English Core, Physics, Chemistry, Mathematics, Biology, and **either Computer Science or Hindi Core**

In PCMB, use the optional-subject selector to choose Computer Science or Hindi.

## Website (GitHub Pages)
1. Put `index.html` in the root of your GitHub repository.
2. Open **Settings → Pages**.
3. Choose **Deploy from a branch**, branch `main`, folder `/(root)`, then Save.
4. Expected URL: `https://sajid097141.github.io/progress-tracker/`.

`preboard_progress.json` contains the starting checkmarks and is embedded as first-run data in the website. Existing browser-saved progress takes priority.

## Features
- PCM / PCB / PCMB stream selector
- PCMB optional subject: Computer Science or Hindi Core
- Separate Mathematics and Biology checklists
- Subject-wise and overall progress
- Auto-save toggle, manual save, JSON backup export/import
- Countdown to 16 November 2026

Website progress is stored in the current browser's local storage, not synced between devices. Use Export/Import Backup to transfer it.

## Desktop Python version
Run `python preboard_tracker_dark_fixed.py` with Python 3. The Tkinter version saves progress to `preboard_progress.json` in the same folder.
