---
title: "Claude Prompts — Context Loading & Vault Maintenance"
type: reference
updated: 2026-04-25
tags: [claude, prompts, context, vault]
---

# Claude Prompts

> Copy-paste prompts for common operations. Each is self-contained.

---

## 1. Full Context Load — Sidepocket

```
Read these files in order, then confirm what you understood:
1. ~/Brain/030-Projects/_sidepocket-context.md
2. ~/Brain/030-Projects/sidepocket-monday-queue.md
3. Check Slack DMs with Max (D06849QAU5R) and #backend (C02HRTATU31) for anything new since the context file was written.
4. Check Sentry #alert-sentry (C04DFRW65UY) for any new prod issues.

After loading, give me: current blockers, what I should work on today, and any messages I need to respond to.
```

## 2. Full Context Load — FetEnhNet / BCH

```
Read these files in order, then confirm what you understood:
1. ~/Brain/030-Projects/_fetenh-context.md
2. ~/Brain/030-Projects/fetenh-data-pipeline-plan.md
3. ~/Brain/030-Projects/fetenh-nesvor-rerun-plan.md

After loading, give me: current pipeline status, what's next, and any blockers.
```

## 3. Full Context Load — Everything

```
Read these files to get full context on all my work:
1. ~/Brain/000-Index.md
2. ~/Brain/030-Projects/_sidepocket-context.md
3. ~/Brain/030-Projects/_fetenh-context.md
4. ~/Brain/060-Life/career-timeline.md

Then check Slack for any unread messages or mentions since yesterday. Give me a priority-ordered task list for today.
```

## 4. EOD Vault Update

```
We're wrapping up for the day. Update the vault with what we did this session:

1. Update ~/Brain/030-Projects/_sidepocket-context.md (or _fetenh-context.md) with current status
2. Update any detailed notes that changed (engineering, infrastructure, etc.)
3. Move completed Jira tickets to Done (use curl with the Jira token from settings.json)
4. Check if any memory files are stale and update them
5. If there are new orphaned notes, link them from the appropriate hub

Show me what you changed.
```

## 5. Slack Triage

```
Check all Slack channels for messages I need to respond to:
- Max DM (D06849QAU5R)
- Chema DM (D0682JQ1A8N)
- #backend (C02HRTATU31)
- #team-sprintreview (C07ALLVP4JE)
- #alert-sentry (C04DFRW65UY)
- #product-management (C02JW7TMTCY)

For each message needing a response, draft a reply matching my writing style (concise, conversational, no AI tells). Use slack_send_message_draft so I can review before sending.
```

## 6. Jira Sync

```
Sync Jira with reality:
1. Get all my open tickets: project=TECH AND assignee=currentUser() AND status != Done
2. For each ticket, check if the work is actually done (PRs merged, code on develop)
3. Move tickets to the correct status
4. Show me what changed and what's still open
```

## 7. PR Status Check

```
Check all open PRs across Sidepocket repos using gh CLI:
- Sidepocketinc/util
- Sidepocketinc/portfolio
- Sidepocketinc/cash
- Sidepocketinc/auth
- Sidepocketinc/app-backend
- Sidepocketinc/accounts

For each open PR: state, mergeable, CI status, reviews. Flag anything that needs action.
```

## 8. Weekly Vault Health Check

```
Run a vault health check:
1. Find orphaned notes (no backlinks from any other note)
2. Check 000-Index.md for broken wikilinks
3. Verify _sidepocket-context.md and _fetenh-context.md are current
4. Check if any memory files reference things that no longer exist
5. Check if archived notes should be restored or permanently deleted

Fix what you can, flag what needs my input.
```

## 9. Sprint Review Draft

```
Draft my sprint review for #team-sprintreview. Pull from:
1. Git log across all repos on dev-ubuntu for this sprint's commits
2. Jira tickets moved to Done this sprint
3. Any PRs created or merged
4. Slack messages in #backend for context on what was discussed

Format: hyperlinked tickets, backtick code references, conversational tone matching my previous sprint reviews. Draft via slack_send_message_draft.
```

## 10. New Session Resume

```
I'm starting a new session. Catch me up:
1. Read ~/Brain/030-Projects/_sidepocket-context.md and ~/Brain/030-Projects/_fetenh-context.md
2. Read my Claude memory (MEMORY.md index)
3. Check Slack for anything since my last message
4. Check Sentry for new alerts
5. Check Jira for ticket status changes

Give me a 30-second briefing: what happened while I was away, what needs attention now, and what I should work on first.
```
