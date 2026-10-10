# Using Gemini or another chat app

## What it looks like

Gemini cannot run Stage's tools, so every file arrives in a copy box that you save yourself. The end of a reply looks like this:

```
END OF FILE | Scene 10 - Saye's kitchen | 58 records
```

```
Checked in words: 14 of 14 passed.
Save as: 11 Scenes/Scene 10 - Saye's kitchen.md   (save only if the box ends with the END line)
To continue later: new chat in this project; attach 00 Start here, 02 Whole-film summary,
10 Film rules, 10 Steps 07-08 - scenes and shots, your story and Scene 10 - Saye's
kitchen; type: Continue my breakdown. Next is scene 11.
```

The END line closes the copy box and counts the records (the entries below the divider line), so a reply that was cut off shows at once. Then come the AI's own count check, the name to save the box under and the message for the next chat.

## What you need

- **Gemini AI Pro or higher.** The kit's knowledge is about 75,000 words, about 100,000 tokens (the pieces AI apps count text in). The free plan gives 32,000 tokens; with your story and the day's files added, a working chat needs AI Pro.
- **A free Claude account**, for the check at the end of each group of scenes.
- The folder `Chat kit`, in `03 Kits to upload` in Stage.

## First, privacy

Do this once, before you upload a story that is not published: open **Gemini Apps Activity** and turn **Keep Activity** off. Chats are then kept only 72 hours; your saved files are Stage's memory anyway. Never use Google AI Studio's free tier for an unpublished story: its reviewers may read what you send.

## Make a Gem, once

1. Make a new Gem and name it Stage.
2. Paste the whole of `00 Paste into instructions.txt` into its instructions.
3. Add the six knowledge files `01` to `06` of `Chat kit`. Leave out `07 Tools.zip`, which Gemini cannot run, and the step files `08` to `12`.
4. Make a folder on your computer named after your story, such as **The Catch - breakdown**, with a folder **11 Scenes** inside it.

If your app shows different names for these menus, follow the app.

## The first chat

In a new chat with the Gem, attach your story and `08 Steps 00-02 - start, reading, plan.md`, and type:

```
Break down my story.
```

## Saving each reply

- Copy each box and save it in your folder under the name after "Save as", as a plain text file ending in `.md` (in TextEdit, choose Make Plain Text first).
- **Save only a box whose last line is the END line.** If a reply stops without it, it was cut off: type **continue**, and the AI sends that part again.
- When a reply adds to a file you already saved, it names a new file such as `09 Continuity - scenes 06-10.md` or `Scene 10 - Saye's kitchen - shots 130-200.md`. Save it beside the first; the check on the Claude website joins them. When a reply changes something you saved, it gives the whole file again and names any older files to delete.
- For a 40-page script you save about 80 files in all.

## Which files each chat needs

The "To continue later" line always names them: the step file for this part of the work, your story, `00 Start here`, `02 Whole-film summary`, `10 Film rules`, the previous scene file, and `08 Places and things` when the scene's place has a floor plan. Gemini takes at most 10 files in one message; when a line names more, it says "attach, in two messages", and you type the message with the second.

| Step file | Attach it to the chats for |
|---|---|
| `08 Steps 00-02 - start, reading, plan` | starting, reading the story and planning it (steps 1 to 3 of 12) |
| `09 Steps 03-06 - world, people, continuity, film rules` | steps 4 to 7 |
| `10 Steps 07-08 - scenes and shots` | every chat that designs scenes or writes shots (steps 8 and 9) |
| `11 Steps 09-11 and 16 - film pass, check, book, resume` | steps 10 to 12, and any chat that carries on after a problem |
| `12 Steps for add-ons - storyboards, prompts, finishing` | storyboards, prompts for AI video and the edit plan |

## A check chat after each group of scenes

An AI does not judge its own work well in the reply that wrote it, so after the last shots of a group of scenes the reply says "Next: a check." Start a new chat with the Gem, attach what it names (that group's scene files, your story, `02 Whole-film summary`, `10 Film rules`, `05 Checks in words` and your last health check file), and type:

```
Check my group of scenes.
```

It gives back a health check file for that group. Save it; the next working chat reads it and fixes what it found first.

## The real check, on the Claude website

Checks in words are weaker than the checker program. At the end of each group, or at least before the finished check, take your folder to the Claude website (free): set up the skill there (02 Using Claude, way 3, steps 1 to 3), make one ZIP of your folder, attach it with your story, and type **Check my breakdown.** Claude turns every quotation you saved into a line number, runs every check, and gives back the health check, the book, the spreadsheets and the captions. Until you do this, `00 Start here` says "Checked by the checker: never".

## Optional: line numbers instead of quotations

Without code there are no line numbers, so the AI points to your story with short exact quotations instead. If you prefer line numbers, open the Claude website once at the start, attach your story and type **Make 03 Story - numbered for my story.** Save it in your folder and attach it to every chat instead of your story.

## Carrying on another day

Start a new chat with the Gem, attach the files the last "To continue later" line names, and type **Continue my breakdown.** When a chat gets long, the AI saves `00 Start here` and `02 Whole-film summary` again and gives you the message for the next chat.

When you get a newer Stage, replace the Gem's instructions and all six knowledge files. Your breakdowns keep working.

## Another chat app

Any chat app that cannot run code works the same way: put `00 Paste into instructions.txt` into its instruction box (or paste it as your first message), add the six knowledge files where it keeps files for every chat, and follow this guide.
