# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### Git: Surveillance Drone Repo

- **Remote:** `https://github.com/david12daniel/SurveillanceDrone`
- **Local (Linux):** `/home/david12daniel/.openclaw/agents/thermal-surveillance-drone`
- **Local (Windows):** `c:\Users\Josiah Laperriere\Documents\Coding\SurveillanceDrone\SurveillanceDrone`
- **Credential helper:** `store --file .git/git-creds` (GitHub PAT stored in `.git/git-creds`, chmod 600)
  - To re-issue: create a classic token with `repo` scope, then:
    `echo "https://david12daniel:TOKEN@github.com" > .git/git-creds && chmod 600 .git/git-creds`
- **Pointer only on Linux:** Windows checkout has its own credentials
- **Push:** `cd /path/to/SurveillanceDrone && git push origin master`

---

Add whatever helps you do your job. This is your cheat sheet.

## Related

- [Agent workspace](/concepts/agent-workspace)