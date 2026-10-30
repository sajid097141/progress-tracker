# PRE//BOARD — Class XII Progress Tracker

A minimal black-and-green CBSE Class XII pre-board tracker.

## Stream combinations
- **PCM:** English, Physics, Chemistry, Mathematics, Computer Science
- **PCB:** English, Physics, Chemistry, Biology, Computer Science
- **PCMB:** English, Physics, Chemistry, Mathematics, Biology, Computer Science

Mathematics and Biology are separate checklists. Select PCM, PCB or PCMB to control which subjects count toward overall progress.

## Website (GitHub Pages)
1. Put `index.html` in the root of your GitHub repository.
2. Open **Settings → Pages**.
3. Choose **Deploy from a branch**, branch `main`, folder `/(root)`, then Save.
4. Expected URL: `https://sajid097141.github.io/progress-tracker/`.

The supplied `preboard_progress.json` is embedded as first-run starting data. Existing browser-saved progress takes priority.

## Features
- PCM / PCB / PCMB stream selector
- Separate Mathematics and Biology checklists
- Subject-wise and overall progress
- Auto-save toggle and manual save
- JSON backup export/import
- Countdown to 16 November 2026

Website progress is stored in that browser's local storage, not synced between devices. Use Export/Import Backup to transfer it.

## Desktop Python version
Run `python preboard_tracker_dark_fixed.py` with Python 3. The Tkinter version saves progress to `preboard_progress.json` in the same folder and includes the stream selector and Biology checklist.
