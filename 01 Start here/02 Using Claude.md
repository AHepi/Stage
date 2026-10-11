# Using Claude

## What it looks like

```
You:     Break down my story.        (with The Catch attached, or in My stories)
Claude:  Hello. I'll turn The Catch into a scene-by-scene plan for making it as a film,
         including with AI picture and video tools.
         Here is one finished moment from your story ... Scene 10, shot 150 ...
         One question first:
         1. Is this story yours, or do you have permission to adapt it?   [It's mine]
You:     defaults
```

From then on Claude works through the story, saves every file, checks each piece with the checker program and stops only when a choice needs you. There are three ways to run it on Claude; pick one below.

## First, privacy

Do this once, before you upload a story that is not published: open **Settings**, then **Privacy**, and turn off **"Help improve our AI models"**. The AI asks you once whether it is off and writes your answer into your project.

## Way 1: Claude desktop with a connected folder (best)

You need Claude desktop and a paid plan (Pro or Max).

1. Download the Stage folder and unzip it where you keep your work. On GitHub: the green **Code** button, then **Download ZIP**.
2. In Claude desktop, open **Customize**, then **Skills**, and upload `Skill for Claude apps.zip` from the folder `03 Kits to upload` in Stage (the same clicks as in way 3, step 2).
3. Choose **Cowork** in the message box and connect the Stage folder, so that Claude can read and write its files.
4. Put your story in the folder `My stories`.
5. Type: **Break down my story.**

Your project appears in `My breakdowns/<your story's title>/`, and every file is saved there the moment it is made. There is nothing to download.

## Way 2: Claude Code (best, and needed for grey previews)

You need Claude Code and a paid plan (Pro or Max).

1. Open the Stage folder in Claude Code. The skill loads by itself from the folder, and the file `CLAUDE.md` tells Claude what the folder is for.
2. Put your story in `My stories` and type: **Break down my story.**
3. For grey previews, install Blender (free, from blender.org) so that Claude Code can start it. When the breakdown is finished, type: **Make grey previews.**

## Way 3: the Claude website (good, and free)

This works on every plan, the free one too.

1. **Settings**, then **Capabilities**: turn on **"Code execution and file creation"**. The skill needs it, because it lets Claude run the checker.
2. **Customize**, then **Skills**, then **+**, **Create skill**, **Upload a skill**, and choose `Skill for Claude apps.zip` from `03 Kits to upload`.
3. Test it: in a new chat, type **Which skills do you have?** The answer should name breaking-down-stories.
4. Make a project for your film (**Projects**, then **New project**), named after your story. The free plan allows five projects.
5. In a new chat in that project, attach your story and type: **Break down my story.**

If your app shows different names for these menus, follow the app: the makers move them from time to time.

## Saving

- **Claude desktop with a folder, and Claude Code:** every file is written to `My breakdowns/<title>/` as soon as it is made. The file `00 Start here` in that folder always says where things stand and what to type next.
- **The Claude website:** the work lives in the chat's own workspace. At every stop Claude makes one **save file**, a ZIP named like `023 Save - The Catch - after scene 10.zip`, and offers it for download. Download each one and keep them together in one folder. The newest save file holds the whole project so far; the number at the front grows with every save, so the newest has the highest number.

## Carrying on another day

- **Claude desktop with a folder, and Claude Code:** type **Continue my breakdown.** Claude looks at your files and answers in one line, for example: "Yesterday we finished scenes 1 to 12. Next: scene 13. Nothing is waiting for you."
- **The Claude website:** start a new chat in the same project, attach the newest save file, and type **Continue my breakdown.**

When you get a newer Stage, replace the whole kit, never single files: on the Claude website or Claude desktop, remove the old skill and upload the new `Skill for Claude apps.zip`. Your breakdowns keep working.

## When the chat gets long

On the Claude website, one chat does one group of scenes. When a chat gets long, or Claude says it is summarising earlier messages, it finishes the piece it is on, makes a save file and says:

```
This chat is getting long. Start a new chat in this project, attach the save file,
and type: Continue my breakdown.
```

Do just that; nothing is lost. In Claude desktop and Claude Code nothing lives only in the chat, so a long chat does no harm: Claude reads the files again.

When you reach your plan's usage limit, Claude stops until it resets (**Settings**, then **Usage**, shows when). Carry on then with the same message.

## Checking a folder saved from another app

If you did the work in Gemini or another chat app that cannot run code, the Claude website does the real check, even on the free plan.

1. Set up the skill on the Claude website (way 3, steps 1 to 3).
2. Make one ZIP of your breakdown folder: right-click it and choose **Compress** (on Windows: **Send to**, then **Compressed folder**).
3. In a new chat, attach the ZIP and your story, and type: **Check my breakdown.**

Claude makes the folder checkable (it turns every quotation you saved into a line number of your story), runs every check, and hands back `13 Health check`, the book, the spreadsheets and the captions to download. If a file you saved was cut off, it names the file, so you can save that part again from its chat.

If the website refuses the ZIP, attach files 00 to 10 and the scene files of one group of scenes instead, and check one group in each chat: the website takes at most 20 files in one chat.

## If something looks wrong

- Claude's reply stops in the middle: type **continue**. It sends the cut part again.
- You want to know where things stand: type **Where are we?**
- You want to change something: say it in your own words, such as "Make the frame 16 to 9". Claude says what it touches and how long it takes, asks once if it is costly, and redoes only that.

The full list of what you can type is in **05 How to read your breakdown**.
