# Step 16. Resume and recovery

This file is "carrying on": it is not one of the 12 steps the user counts. Use it whenever the user types "Continue my breakdown." or "continue", and whenever something goes wrong. Read it each time, never from memory.

**One-line task:** Pick up where the work stopped, say in one line where things stand, and carry on with the next unit, or recover from a cut-off reply, skipped records, a full chat, a lost file, an unreadable attachment or a refusal, using the files and never memory.

Quote the one-line task back, word for word, before you do anything else.

## Purpose

Files are the only memory. Example: in Claude Code the user types "Continue my breakdown." the next day; you run `stage.py status` and answer "Yesterday we finished scenes 1 to 12. Next: scene 13. Nothing is waiting for you.", then read step 7's file and design scene 13. App memory features are turned off or ignored, because remembered facts from older versions can contradict the files (D1 R10). A reply that fails is never repaired by hand: it is sent again, in whole records (D1 §6.2).

## When it runs

- The user resumes, in any app, in a new chat or the same one.
- A reply was cut off or skipped records, the chat is full, a file is lost, an attachment cannot be read to its end, a step is refused, or you cannot quote a choice you need.
- The app compacted the conversation: run `status` again and re-read the current step file.

## Inputs

PROJECT and `00 Start here.md` (where things stand, the next step, the big choices, the log); the manifest in `For machines - do not edit/` (units done, each batch's expected and received counts, locks; code surfaces); the newest save ZIP on the Claude website and ChatGPT; in chat, the files the resume line named.

## Outputs

None, or the missing records sent again; on the Claude website and ChatGPT a save ZIP when a chat ends; in chat without code, `00 Start here` and `02 Whole-film summary` rewritten at a stop point.

## Card parts to open

At every depth: `reference/07 Report and message formats.md`, whole.

## Procedure

1. **Where are we?** On a code surface run `stage.py status`; without code read `00 Start here`. Say one line: what is done, what is next, what waits for the user. Never answer from memory: if you cannot quote a choice from `01 Choices` or `00 Start here`, ask for that file.
2. **By surface.**
   - Claude desktop with a folder, and Claude Code: `status`, then `stage.py next`, then the next unit's step file, read fresh, its one-line task quoted.
   - The Claude website and ChatGPT: the user attaches the newest save ZIP; run `stage.py unpack <zip>`, read `00 Start here`, then as above. One group of scenes per chat (`units_per_chat`), and earlier if the app says it is summarising or usage passes `chat_usage_handover_share` (D1 R5, R6): finish the unit, run `stage.py pack` (`023 Save - The Catch - after scene 10.zip`), and give the message below. On ChatGPT the download link expires: say so (D1 R7).
3. **A reply cut off** (no END line, or a count short of the approved list; D1 R4). The user types **continue**: send again from the start of the record that was cut (shot 170, when the reply stopped inside it), then the END line. A record is never split across replies.
4. **Records skipped** (IDs missing from the approved list, or a shortening marker such as "same as above"). The user types **continue**: send only the missing records, complete, then an END line counting them (D1 §6.2).
5. **A format slip** ("medium closeup", an unknown field): the checker makes tidy fixes itself and logs them (FORM-13); real problems come back as "Fix only these". Fix only those lines, at most `repair_rounds_max` rounds (C5 R13), then one plain question with a default, or a trace to the earliest wrong record.
6. **An early choice changed** ("make it 16:9"): run `stage.py impact` on what it changes, say in plain words what it touches and how long it takes, ask once if it is costly, then redo only those units. Locked records change only through an answered choice.
7. **A file lost.** `00 Start here` lists what should exist. On Claude surfaces restore it from git or the last save ZIP; `apply` keeps earlier versions in `For machines - do not edit/history/`. In chat apps redo that scene from the story.
8. **An attachment not read to the end**: if you cannot quote its first and last lines, ask the user to paste the missing part.
9. **A fact not in the story** (the CITE checks): mark it "not found in the story"; fix it, or keep it labelled `invented` and listed.
10. **A refusal** of the story's content (scene 6's gunshot and blood): say once that this is planning for the user's own film and you need only camera, staging and continuity fields; use production words ("gunshot sound effect", "wound make-up"). If refused again, log it and suggest another model or app for that scene. Never disguise the content (D1 §6.5, R12).
11. **Then carry on** with the next unit of its own step, as that step's file says.

## Record template

None of its own. Records sent again follow the template of the step that was interrupted (for shots, the SHOT part of `templates/11 Scene.md`).

## IDs you will be given

None new. Copy every ID from the approved list, the manifest or the saved file; a record sent again keeps its ID. Never renumber to close a gap; an omitted record keeps its number.

## Batch and chunk rules

The resume is one line, then the next unit under its own step's batch rule. A re-sent part is the missing records only, in ID order, within the step's batch size.

## Self-check

Answer each question yes or no; each "no" is a fix before you report.

1. Did the one line of where things stand come from the files, not from memory?
2. Did you read the next unit's step file afresh and quote its one-line task?
3. After a cut-off, does the re-sent part start at the record that was cut and end with the END line?
4. After skipped records, did you send only the missing IDs?
5. Did a change redo only what `impact` named, leaving locked records alone?
6. After a refusal, did you use production words once and never disguise the content?

## The report

The resume line, then the next unit's own report (`reference/07 Report and message formats.md`):

```
Yesterday we finished scenes 1 to 12. Next: scene 13. Nothing is waiting for you.
```

When the chat is long (the Claude website, ChatGPT):

```
This chat is getting long. Start a new chat in this project, attach the save file,
and type: Continue my breakdown.
```

When something went wrong (the user types only the word in bold, **continue**):

```
My reply was cut off inside shot 170. Type continue and I'll send it again from shot 170.
```

## Checkpoint

None. A recovery that needs the user asks one plain question with a default; "continue" answers every cut-off.

## How to redo

"continue" sends again. A record is never split across replies, and a saved file that failed its checks is sent whole again before the user saves it.

## If you cannot run code

Every line reference is a quote anchor, here as in every step; a re-sent record keeps its quote anchors word for word.

1. The user starts a new chat in the Gem or Project, attaches the files the resume line named (the step-group file, the story, `00 Start here`, `02 Whole-film summary`, `10 Film rules`, `08 Places and things` when needed, the previous scene file) and types "Continue my breakdown." Quote the step file's one-line task, then carry on from "Next step".
2. One group of scenes (3 to 5 scenes) per chat. At the budget, rewrite `00 Start here` and `02 Whole-film summary` in copy boxes and give the exact message for the new chat. At a group's end the resume line names the check chat.
3. File names: a reply that only adds records to a saved file saves them as `<numbered file> - <what they hold>.md` (`09 Continuity - scenes 06-10.md`, `Scene 10 - Saye's kitchen - shots 130-200.md`), each with its own END line; `adopt` merges them by ID. A reply that changes a saved record saves the whole file again and names the extra files to delete.
4. A box with no END line is never saved. After **continue**, send the file again in parts that each end with an END line: first the records that were complete, as `Scene 10 - Saye's kitchen - shots 130-160.md`, then, in the next reply, the rest from the start of the cut record, as `Scene 10 - Saye's kitchen - shots 170-200.md`.
5. `00 Start here` shows "Checked by the checker: never" until the real check. Report, then:

```
Save as: nothing new in this reply.
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 10 Steps 07-08 - scenes and shots, your story and Scene 12 - Demonstration
room; type: Continue my breakdown. Next is scene 13.
```

**One-line task, again:** Pick up where the work stopped, say in one line where things stand, and carry on with the next unit, or recover from a cut-off reply, skipped records, a full chat, a lost file, an unreadable attachment or a refusal, using the files and never memory.
