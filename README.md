# PRE//BOARD — Class XII Progress Tracker

A balanced dark-mode study dashboard with a calm green accent.

## Subject combinations
- **PCM:** English Core, Physics, Chemistry, Mathematics, Computer Science
- **PCB:** English Core, Physics, Chemistry, Biology, Hindi Core
- **PCMB:** English Core, Physics, Chemistry, Mathematics, Biology, and either Computer Science or Hindi Core

The PCMB option selector chooses Computer Science or Hindi. Mathematics and Biology remain separate checklists.

## Website features
- Modern Academic dashboard with overall and subject-wise progress
- Chapter search and status filters
- Collapsible subject sections
- Focus mode for distraction-reduced chapter work
- Select All / Clear All for the active stream and for each subject
- Existing auto-save toggle, manual save, reset, JSON export and import
- Existing progress, stream, PCMB choice and autosave localStorage keys retained
- Countdown to 16 November 2026

Progress remains stored in the current browser's local storage. It is not automatically synced between devices. Use Export/Import Backup to transfer progress.

## Publish with GitHub Pages
1. Put `index.html` in the root of your GitHub repository.
2. Open **Settings → Pages**.
3. Choose **Deploy from a branch**, branch `main`, folder `/(root)`, then Save.
4. Expected URL: `https://sajid097141.github.io/progress-tracker/`.

## Desktop Python version
The included `preboard_tracker_dark_fixed.py` remains the existing Tkinter desktop version. Run it with `python preboard_tracker_dark_fixed.py`; it saves to `preboard_progress.json` in the same folder.
