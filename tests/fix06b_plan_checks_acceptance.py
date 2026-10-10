"""The acceptance test of the plan-level fixes after the H3 handover (Project notes 42; the build plan is note 43,
work package B): stop asking for stillness, cut at contact, and check that the plan makes physical sense.

What it proves, on small fixtures only: copies of the WP12a gold (references/examples/01 and 02, scene 10) and a generic test
scene written here in neutral words (a climber in a 2.4 metre shaft, a patient, a guard). No group reads a whole
story; no group reads the clip file or its code.

Groups:
- B1 the constants: hold_action_every_s replaces hold_needs_still_s; the physical sense numbers are there, each with
  a meaning and a source and marked as a judgement;
- B1 CRAFT-26 turned round: a 7-second moment with one action is flagged, with four actions it is not; a pause held
  on picture needs its last moments filled;
- B1 the old still sub-part: a breakdown that still writes it, with enough actions, raises nothing about stillness,
  and no check asks for it;
- B1 CRAFT-27: stillness words in a moment, a does or an end are flagged; energy: still and quoted story words are
  not;
- B2 CRAFT-28: a contact and its result in one shot are flagged; the same pair split across a cut is not;
- B3 PHYS-01 to PHYS-11: each flags its generic slip (a 2.4 metre shaft round a 2 metre car; a heavy 30 centimetre
  flashlight held in the teeth; a line spoken round it; a strap cut with nothing; cover under an open grid roof; a
  rung that rolls; a weak man holding up a heavy man; a weak man running; a chair wedged under a door handle; a
  door kicked open; more than two things in one person's hands; a tiny thing given emphasis in a wide shot; a thing
  out of reach); each line is a warning that asks a question;
- after the round 1 cross-examination of Project notes 43, on realistic writer wordings in neutral words: F11
  CRAFT-26 counts held moments only and reads commas and "and"; F15 CRAFT-27 counts a stillness word only where
  it describes a person; F12 CRAFT-28 reads "swings the bottle into", effect-as-cause and a thing as the effect's
  subject; F16 the physical sense checks read more wordings and drop a false alarm; F13 the kit texts no longer
  teach stillness; F4 and F6 the gold's kitchen and bottle say what is there, so the route raises no ROUTE-15;
- after the round 2 cross-examination: N7 and N8, the reviewer's own wordings for CRAFT-26, CRAFT-27, CRAFT-28 and
  the physical sense checks are all judged right; a contact split across two shots is read by the same rule; a
  held-out set written before the round 2 rules changed is judged no worse than it was after them; N11, library B1
  and its digest no longer teach "while she stays still", and errata 23 lists B1;
- the gold scene 10 (and its chat-saved copy) raises none of the new warnings, and none of the old checks either;
- the new checks are warnings, registered with a plain sentence, listed for steps 4, 7 and 8 in _config/schema/steps.json,
  and their titles say they are judgements (J);
- no new or changed file holds an email address.

Usage: python tests/fix06b_plan_checks_acceptance.py
Standard library only.
"""

import json
import re
import sys
import tempfile
from pathlib import Path

REPOSITORY = Path(__file__).resolve().parents[1]
SKILL = REPOSITORY / ".claude" / "skills" / "breaking-down-stories"
TOOLS = SKILL / "tools"
sys.path.insert(0, str(TOOLS))

from stage_tools import check_records  # noqa: E402
from stage_tools.record_format import DIVIDER_LINE, load_skill_data, parse_file  # noqa: E402

SCHEMA, WORDS, CONSTANTS = load_skill_data()
GOLD_FILES = {"context": SKILL / "references" / "examples" / "02 The Catch - scene 10 - context.md",
              "scene": SKILL / "references" / "examples" / "01 The Catch - scene 10.md"}
CHAT_FOLDER = REPOSITORY / "tests" / "fixtures" / "chat saved scene 10"
EXCERPT = REPOSITORY / "tests" / "fixtures" / "The Catch - lines 397-489.txt"
NEW_CHECKS = ["CRAFT-26", "CRAFT-27", "CRAFT-28"] + [f"PHYS-{number:02d}" for number in range(1, 12)]
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
RESULTS = []


def report(passed, group, detail=""):
    RESULTS.append(bool(passed))
    print(f"{'PASS' if passed else 'FAIL'}  {group}" + (f": {detail}" if detail else ""), flush=True)


def group(title):
    def decorator(function):
        try:
            detail = function()
        except AssertionError as error:
            report(False, title, str(error)[:900])
            return function
        except Exception as error:  # a fault fails this group only
            report(False, title, f"{type(error).__name__}: {error}"[:900])
            return function
        report(True, title, detail or "")
        return function
    return decorator


# ---------------------------------------------------------------- fixtures

def gold_texts():
    return {name: path.read_text(encoding="utf-8") for name, path in GOLD_FILES.items()}


def edit(texts, name, heading, find, replace):
    """Replace a text found exactly once inside one record of a copy of the gold."""
    text = texts[name]
    start = text.index(f"### {heading}")
    end = text.find("\n### ", start + 4)
    end = len(text) if end < 0 else end
    block = text[start:end]
    assert block.count(find) == 1, f"{heading} holds {find!r} {block.count(find)} times"
    texts[name] = text[:start] + block.replace(find, replace) + text[end:]
    return texts


def record_file(text, title):
    count = len(re.findall(r"^### ", text, re.MULTILINE))
    return f"# {title}\n\n{DIVIDER_LINE}\n\n{text.strip()}\n\nEND OF FILE | {title} | {count} records\n"


# A generic test scene in neutral words: a climber in a narrow shaft, a weak patient, a heavy guard. Each shot holds
# one slip a physical sense check must catch.
GENERIC_WORLD = """
### CHARACTER CH-TEST-CLIMBER The climber
- names: CLIMBER, THE CLIMBER
- fixed_description: the climber, a lean woman in her thirties in grey overalls and a dark knitted cap
- height_m: 1.7
- build: lean and strong

### CHARACTER CH-TEST-PATIENT The patient
- names: PATIENT, THE PATIENT
- fixed_description: the patient, a thin man in his forties in a pale hospital gown
- height_m: 1.75
- build: thin, weak from the drug, his knees unsteady

### CHARACTER CH-TEST-GUARD The guard
- names: GUARD, THE GUARD
- fixed_description: the guard, a tall, heavy, broad man in a dark uniform
- height_m: 1.92
- build: tall, heavy and broad

### LOCATION LOC-TEST-SHAFT The shaft
- headings: INT. SHAFT - NIGHT
- dressing: a bare steel car whose roof is a grid of flat bars
- size: [2.4, 2.4, 20.0]
- object: CAR | at: [1.2, 1.2] | size: [2.0, 2.0, 2.4] | base: 0 | material: a bare steel car | meaning: the car | furniture: none
- object: LADDER | at: [0.05, 1.2] | size: [0.1, 0.6, 20.0] | base: 0 | material: steel rungs on the wall | meaning: the way up | furniture: none
- object: HATCH | at: [1.2, 2.35] | size: [0.4, 0.1, 0.8] | base: 0 | material: a small steel hatch | meaning: the way out | furniture: none
- object: ROPES | at: [2.3, 2.3] | size: [0.05, 0.05, 20.0] | base: 0 | material: steel cables | meaning: what the car hangs from | furniture: none
- mark: CLIMB | at: [0.15, 1.6]

### PROP PR-TEST-FLASHLIGHT The flashlight
- names: flashlight, the flashlight
- fixed_description: a heavy black metal flashlight about 30 centimetres long
- real_size: [0.05, 0.05, 0.3]

### PROP PR-TEST-STRAP The strap
- names: the strap
- fixed_description: a grey webbing strap with a steel buckle
- real_size: [0.04, 0.6, 0.01]

### PROP PR-TEST-BOLT The bolt
- names: the bolt
- fixed_description: a small steel bolt
- real_size: [0.02, 0.02, 0.05]

### PROP PR-TEST-ROPE The rope
- names: the rope
- fixed_description: a coil of blue rope
- real_size: [0.3, 0.3, 0.1]

### PROP PR-TEST-HOOK The hook
- names: the hook
- fixed_description: a steel hook on a short handle
- real_size: [0.05, 0.25, 0.02]

### PROP PR-TEST-BAG The bag
- names: the bag
- fixed_description: a canvas tool bag
- real_size: [0.4, 0.2, 0.25]

### SCENE SC90 The shaft
- location: LOC-TEST-SHAFT
- characters: CH-TEST-CLIMBER, CH-TEST-PATIENT, CH-TEST-GUARD
- start: CH-TEST-CLIMBER | at: CLIMB | faces: [1.0, 0.0] | posture: standing
- start: CH-TEST-PATIENT | at: [1.2, 1.2] | faces: [0.0, 1.0] | posture: standing
- start: CH-TEST-GUARD | at: [1.6, 1.2] | faces: [0.0, 1.0] | posture: standing

### SPEECH SC90-D01 Keep going
- speaker: CH-TEST-CLIMBER
- text: Keep going.
- parenthetical: round the flashlight

### SHOT SC90-SH010 Teeth
- size: medium
- subject: CH-TEST-CLIMBER | does: climbs the rungs with the flashlight in her teeth
- thing: PR-TEST-FLASHLIGHT | emphasis: 1
- hear: SC90-D01 | speaker: on_screen | at: 1
- screen_time: 3
- moment: 0-3 | shows: she climbs two rungs, breathing hard through her nose; her right hand closes on the next rung

### SHOT SC90-SH020 Strap
- size: medium_close_up
- subject: CH-TEST-CLIMBER | does: cuts the strap and pulls it free
- thing: PR-TEST-STRAP | emphasis: 1
- screen_time: 3
- moment: 0-3 | shows: she cuts the strap; it falls away

### SHOT SC90-SH030 Cover
- size: wide
- subject: CH-TEST-PATIENT | does: crouches in the corner of the car
- subject: CH-TEST-GUARD | does: crouches beside him
- screen_time: 3
- moment: 0-3 | shows: the two men take cover in the corner of the car from the shots coming down

### SHOT SC90-SH040 Rung
- size: close_up
- subject: CH-TEST-CLIMBER | does: grips the broken rung
- screen_time: 3
- moment: 0-3 | shows: the rung rolls under her hand like a rolling pin

### SHOT SC90-SH050 Holding up
- size: medium
- subject: CH-TEST-PATIENT | does: holds up the guard against the grid
- subject: CH-TEST-GUARD | does: hangs off his shoulder
- screen_time: 3
- moment: 0-3 | shows: the patient takes the guard's weight

### SHOT SC90-SH060 Running
- size: wide
- subject: CH-TEST-PATIENT | does: runs to the hatch
- screen_time: 3
- moment: 0-3 | shows: the patient runs the length of the car

### SHOT SC90-SH070 Brace
- size: medium
- subject: CH-TEST-GUARD | does: wedges a chair under the door handle
- screen_time: 3
- moment: 0-3 | shows: the guard wedges a chair under the door handle

### SHOT SC90-SH080 Kick
- size: medium
- subject: CH-TEST-GUARD | does: kicks the gate open
- screen_time: 3
- moment: 0-3 | shows: the guard kicks the gate open

### SHOT SC90-SH090 Hands
- size: medium
- subject: CH-TEST-CLIMBER | does: holds the rope, the hook and the bag
- thing: PR-TEST-ROPE | emphasis: 1
- thing: PR-TEST-HOOK | emphasis: 1
- thing: PR-TEST-BAG | emphasis: 1
- screen_time: 3
- moment: 0-3 | shows: she shifts her grip on all three

### SHOT SC90-SH100 Bolt
- size: wide
- subject: CH-TEST-CLIMBER | does: looks down the shaft
- thing: PR-TEST-BOLT | emphasis: 2 | at: on the car's roof
- screen_time: 3
- moment: 0-3 | shows: she looks down at the car below, breathing hard

### SHOT SC90-SH110 Reach
- size: medium
- subject: CH-TEST-CLIMBER | does: holds on with one hand
- screen_time: 3
- moment: 0-3 | shows: the climber takes hold of the ropes; she breathes out
"""

# Realistic writer wordings for the round 1 findings of Project notes 43 (F11, F12, F15, F16), in neutral words: a
# woman (Anna) and a man (Ben) in a small kitchen. Each case becomes one shot of scene 91.
WORDING_WORLD = """
### CHARACTER CH-TEST-WOMAN The woman
- names: WOMAN, THE WOMAN, ANNA
- fixed_description: the woman, a tall woman in her forties in a grey coat
- height_m: 1.72

### CHARACTER CH-TEST-MAN The man
- names: MAN, THE MAN, BEN
- fixed_description: the man, a young man in a blue jacket
- height_m: 1.8

### LOCATION LOC-TEST-ROOM The room
- headings: INT. ROOM - NIGHT
- dressing: a small kitchen with a table and a window

### PROP PR-TEST-LAMP The lamp
- names: lamp, the lamp
- fixed_description: a small brass oil lamp
- real_size: [0.12, 0.12, 0.3]

### PROP PR-TEST-PHONE The phone
- names: phone, the phone
- fixed_description: a small black phone
- real_size: [0.07, 0.15, 0.01]

### PROP PR-TEST-ROPE The rope
- names: rope, the rope
- fixed_description: a coil of blue rope
- real_size: [0.3, 0.3, 0.1]

### SCENE SC91 The room
- location: LOC-TEST-ROOM
- characters: CH-TEST-WOMAN, CH-TEST-MAN
"""

# F11, CRAFT-26: (should be flagged, held, span, shows).
HELD_WORDINGS = [
    (False, "no", "0-4", "Anna walks slowly round the end of the table and stops square between the two men, facing Ben"),
    (False, "yes", "8-15", "she swallows once, breathes out slowly through her nose, blinks, her lips press together, "
                           "a slow breath in, her eyes on Ben, she blinks again"),
    (False, "yes", "8-15", "she swallows once and breathes out slowly through her nose and blinks and presses her lips "
                           "together and blinks again"),
    (False, "no", "0-6", "Ben climbs the ladder rung by rung toward the hatch"),
    (False, "yes", "0-9", "she reads the letter, her lips moving, turns the page, frowns, reads on to the end"),
    (False, "yes", "0-6", "a breath; a blink; a small frown"),
    (True, "yes", "0-7", "her face; her eyes on Ben; Ben's words land; the fridge hums"),
    (True, "yes", "0-7", "Anna does nothing at all; she takes it in; it sinks in; she is a statue"),
    (True, "no", "0-6", "her eyes on the door, her hands in her lap"),
    (True, "no", "0-8", "Anna listens; she nods"),
    (True, "yes", "0-10", "Ben looks at her"),
]

# F15, CRAFT-27: (should be flagged, shows).
STILLNESS_WORDINGS = [
    (False, "her hair still wet from the rain, she looks up"),
    (False, "she presses a bag of frozen peas to Ben's shoulder"),
    (False, "she tugs at the rigid collar of her shirt"),
    (False, "her eyes go to the still water in the glass"),
    (False, "Ben, still in his coat, sits down"),
    (True, "she doesn't stir; not a muscle moves"),
    (True, "she sits like a statue"),
    (True, "she holds her position, unblinking"),
    (True, "Ben stands frozen in the doorway"),
    (True, "she sits still beside him"),
]

# F12, CRAFT-28: (should be flagged, first moment, a second moment or None).
CONTACT_WORDINGS = [
    (True, "she swings the bottle into the window; the glass cracks", None),
    (True, "the glass shatters as the bottle smashes into it", None),
    (True, "Ben bumps the table and the water glass tips over", None),
    (True, "she slams the flask down on the counter and the cap pops off", None),
    (True, "Ben trips over the cable and goes down", None),
    (True, "she throws the cup at the wall", "the cup shatters against it"),
    (False, "rain hits the window and drops run down the glass", None),
    (False, "she hits the light switch; the room drops into shadow", None),
    (False, "Ben's word hits her; her face falls", None),
    (False, "someone knocks at the back door; the room falls silent", None),
    (False, "she pushes the door open and the light falls across the floor", None),
]

# F16, PHYS: (the check that should fire or None, the field, the words).
PHYSICAL_WORDINGS = [
    ("PHYS-09", "moment", "Anna wedges a chair under the back door's handle"),
    ("PHYS-02", "moment", "Ben climbs with the lamp gripped by his teeth"),
    ("PHYS-10", "subject", "climbs out, the lit phone in one hand, the lamp and the rope in the other"),
    ("PHYS-10", "moment", "Ben holds the lit phone, the lamp and the rope"),
    (None, "moment", "Anna grips the chair's top rail and rolls her shoulders"),
    (None, "moment", "Ben steadies himself on the rail as the boat rolls"),
    (None, "moment", "Anna braces herself against the door frame"),
]


# The round 2 cross-examination (Project notes 43, findings N7 and N8): the reviewer's own wordings, which the round 2
# rules were made to judge right. Same shapes as the lists above.
ROUND_2_HELD_WORDINGS = [
    (False, "yes", "0-6", "she turns the ring on her finger, looks at the clock and sighs"),
    (False, "no", "0-8", "Ben hauls the sack up the stairs to the landing"),
    (False, "no", "0-6", "Anna kneads the dough, folds it over and presses it flat"),
    (False, "yes", "0-4", "her fingers tighten on the cup; she glances at the window"),
    (False, "yes", "0-6", "he scratches his jaw, shifts his weight, rubs his eyes"),
    (False, "yes", "0-8", "Anna bites her lip, glances down, picks at the label on the bottle and looks back up"),
    (False, "no", "0-5", "the kettle boils and Ben pours the water"),
    (False, "yes", "0-6", "a slow breath out; her shoulders drop; she nods"),
    (False, "no", "0-4", "Ben steps back from the door and lowers the gun"),
    (False, "yes", "0-4", "his lips part, close again"),
    (False, "no", "0-6", "Anna sweeps the broken glass into a pile"),
    (False, "yes", "0-6", "Ben taps the pen on the desk, clicks it, taps it again"),
    (False, "yes", "0-4", "she tucks a strand of hair behind her ear and swallows"),
    (False, "no", "0-10", "they drag the sack across the yard to the car"),
    (False, "yes", "0-6", "he exhales, looks away, then back at her"),
    (False, "yes", "0-6", "Anna sniffs, wipes her nose with her sleeve, straightens up"),
    (True, "yes", "0-8", "she watches him"),
    (True, "no", "0-6", "her gaze fixed on the door"),
    (True, "yes", "0-6", "Ben waits"),
    (True, "yes", "0-8", "they look at each other across the table"),
    (True, "no", "0-6", "Anna, motionless, on the edge of the bed"),
    (True, "yes", "0-6", "a long silence between them"),
    (True, "no", "0-8", "she stares at the letter"),
    (True, "no", "0-6", "Ben sits at the table, looking at his hands"),
    (True, "yes", "0-6", "she holds his gaze; the clock ticks"),
    (True, "no", "0-8", "Anna stands by the window, her back to us"),
    (True, "yes", "0-10", "he listens to her, his head bowed"),
]
ROUND_2_STILLNESS_WORDINGS = [
    (False, "she wipes the still-warm pan"),
    (False, "the frozen chicken thaws in the sink"),
    (False, "Ben, stiff from the cold, rubs his hands"),
    (False, "she pours still water into two glasses"),
    (False, "Ben is still on the phone when she comes in"),
    (False, "still shaking, she sets the cup down"),
    (False, "the rigid plastic case snaps open"),
    (False, "she hangs the frozen laundry on the line"),
    (False, "she still has the key in her hand"),
    (False, "Ben stills the swinging lamp with one hand"),
    (True, "she stands there, utterly still"),
    (True, "Ben remains seated, not moving"),
    (True, "her hands freeze over the keyboard"),
    (True, "she sits perfectly motionless"),
    (True, "he doesn't move a muscle"),
    (True, "Anna holds stock still"),
    (True, "Ben stays exactly where he is"),
    (True, "she is frozen to the spot"),
    (True, "they don't move"),
    (True, "her face goes still"),
    (True, "he keeps very still"),
    (True, "she stays put"),
]
ROUND_2_CONTACT_WORDINGS = [
    (True, "he slams his fist onto the table; the plates jump", None),
    (True, "the car ploughs into the fence and the fence collapses", None),
    (True, "Ben hurls the brick through the window; glass sprays across the floor", None),
    (True, "the ball strikes the vase and it topples", None),
    (True, "she shoves the bookcase against the door; books spill out", None),
    (True, "he swings the axe into the door and the panel splinters", None),
    (True, "the truck rams the barrier; the barrier buckles", None),
    (True, "she kicks the bucket over and water floods the floor", None),
    (True, "the mug hits the floor and breaks", None),
    (True, "Ben punches the mirror; it cracks", None),
    (True, "the wave smashes against the boat and the mast snaps", None),
    (True, "she bangs the jar on the counter", "the lid pops off"),
    (False, "Ben drops into a chair and sighs", None),
    (False, "she knocks back her drink; her eyes water", None),
    (False, "the light hits the wall and the shadows grow", None),
    (False, "he throws a glance at the door; her face drops", None),
    (False, "she drives into town; the rain breaks", None),
    (False, "the thought hits him; his hands fall to his sides", None),
    (False, "she bumps into an old friend; her smile breaks", None),
    (False, "he runs into the room and the music stops", None),
    (False, "she kicks the ball and the crowd falls silent", None),
    (False, "Ben slams on the brakes and the dog runs off", None),
]
ROUND_2_PHYSICAL_WORDINGS = [
    ("PHYS-02", "moment", "Ben bites down on the flashlight and climbs"),
    ("PHYS-02", "moment", "the flashlight between her teeth, Anna climbs the ladder"),
    ("PHYS-02", "moment", "Ben carries the flashlight in his mouth"),
    (None, "moment", "she clenches her teeth"),
    (None, "moment", "Ben grits his teeth and hauls the rope"),
    ("PHYS-05", "moment", "Anna slices through the tape"),
    ("PHYS-05", "moment", "Ben cuts the rope free"),
    (None, "moment", "she cuts him off mid-sentence"),
    (None, "moment", "Ben cuts across the yard"),
    (None, "moment", "the light cuts out"),
    ("PHYS-07", "moment", "the bar spins under his hands"),
    (None, "moment", "she rolls the pipe across the floor"),
    (None, "moment", "the barrel rolls down the ramp"),
    ("PHYS-09", "moment", "Ben kicks the gate open"),
    ("PHYS-09", "moment", "Anna shoulders the door open"),
    ("PHYS-09", "moment", "she props a chair against the door"),
    (None, "moment", "Ben braces his feet against the wall and pulls"),
    ("PHYS-10", "moment", "Anna carries the phone, the flashlight and the rope up the stairs"),
    ("PHYS-10", "moment", "Ben juggles the phone, the rope and the flashlight"),
    ("PHYS-10", "moment", "with the phone and the flashlight in her hands, she grabs the rope"),
    (None, "moment", "she puts the phone down, picks up the flashlight and the rope"),
    (None, "moment", "Ben pockets the phone and takes the flashlight and the rope"),
]
ROUND_2_PROPS = """
### PROP PR-TEST-FLASHLIGHT The flashlight
- names: flashlight, the flashlight
- fixed_description: a heavy black metal flashlight about 30 centimetres long
- real_size: [0.05, 0.05, 0.3]
"""

# A held-out set for the round 2 changes: written and scored before any rule changed, and never used to choose the
# rules, so it shows how the rules do on wordings nobody tuned them to. Before the changes it gave 5 false alarms
# and 16 misses; after them 2 false alarms and 12 misses (CRAFT-26: 0 and 2, CRAFT-27: 1 and 2, CRAFT-28: 1 and 5,
# physical sense: 0 and 3). The group below holds those figures as a ceiling, so a later change can only lower them.
HELD_OUT_CEILING = {"CRAFT-26": (0, 2), "CRAFT-27": (1, 2), "CRAFT-28": (1, 5), "PHYS": (0, 3)}
HELD_OUT_HELD = [
    (False, "yes", "0-6", "she rubs her thumb along the edge of the table, looks up, then down again"),
    (False, "no", "0-8", "Ben carries the crate across the yard and sets it on the cart"),
    (False, "yes", "0-4", "he wets his lips and swallows"),
    (False, "yes", "0-6", "Anna twists the cap off, sniffs the bottle, wrinkles her nose"),
    (False, "no", "0-6", "she scrubs the pot under the tap"),
    (False, "yes", "0-8", "Ben drums his fingers on the table, checks his watch, drums again, sighs"),
    (False, "yes", "0-6", "her chin trembles; she presses her lips together; she blinks hard"),
    (False, "no", "0-10", "Anna climbs the stairs two at a time and bursts through the door at the top"),
    (False, "yes", "0-4", "he scratches the back of his neck, then shrugs"),
    (False, "yes", "0-6", "she lifts the cup, blows on it, sets it down untouched"),
    (True, "yes", "0-8", "Anna gazes out of the window"),
    (True, "no", "0-6", "Ben leans against the doorframe, arms folded"),
    (True, "yes", "0-6", "the two of them face each other in silence"),
    (True, "no", "0-8", "she kneels by the grave, her head bowed"),
    (True, "yes", "0-6", "Ben's eyes on the floor"),
    (True, "no", "0-8", "Anna lies on the bed, staring at the ceiling"),
    (True, "yes", "0-10", "he watches the door; she watches him"),
    (True, "no", "0-6", "Ben waits by the car"),
    (True, "yes", "0-8", "she studies his face"),
]
HELD_OUT_STILLNESS = [
    (False, "she stirs the still-steaming soup"),
    (False, "Ben pulls a frozen pizza from the box"),
    (False, "she is still angry when he walks in"),
    (False, "the stiff hinge creaks as she opens the gate"),
    (False, "Ben still holds the letter"),
    (False, "a still life hangs above the table"),
    (False, "she freezes the leftovers"),
    (False, "the motionless fan above them starts to turn"),
    (True, "she stands motionless at the sink"),
    (True, "Ben goes rigid"),
    (True, "Anna doesn't budge"),
    (True, "he stays where he is"),
    (True, "she remains perfectly still"),
    (True, "Ben sits without moving a muscle"),
    (True, "they both freeze"),
    (True, "she keeps her hands still on the table"),
    (True, "Anna stays right where she is"),
    (True, "he holds himself still"),
]
HELD_OUT_CONTACT = [
    (True, "Ben throws the plate against the wall; it shatters", None),
    (True, "the door slams into his shoulder and he staggers back", None),
    (True, "she smashes the lamp over his head and he crumples", None),
    (True, "the cart crashes into the shelf and tins tumble to the floor", None),
    (True, "Ben knocks the glass off the table; it breaks on the tiles", None),
    (True, "Anna stamps on the phone; the screen cracks", None),
    (True, "he shoulders the door and it bursts open", None),
    (True, "the stone hits the windscreen", "the windscreen cracks"),
    (True, "she pushes him and he falls against the sink", None),
    (True, "Ben kicks the chair; it skids across the floor", None),
    (False, "the news hits her hard; she drops onto the sofa", None),
    (False, "Ben pushes his plate away and the dog jumps up", None),
    (False, "she strikes a match and the candle flickers", None),
    (False, "the car pulls into the drive and the engine stops", None),
    (False, "he hits play; the music bursts from the speakers", None),
    (False, "Anna slams the drawer shut", None),
    (False, "sunlight strikes the glass and the room glows", None),
    (False, "his words cut through the noise; the room goes quiet", None),
    (False, "Ben breaks into a run", None),
    (False, "she pushes through the crowd and the doors open ahead of her", None),
]
HELD_OUT_PHYSICAL = [
    ("PHYS-02", "moment", "Ben clamps the flashlight in his teeth and reaches up"),
    ("PHYS-02", "moment", "with the flashlight in her mouth, Anna climbs"),
    (None, "moment", "Ben bites his lip and climbs"),
    ("PHYS-05", "moment", "Anna saws through the rope"),
    ("PHYS-05", "moment", "Ben cuts the cord"),
    (None, "moment", "the engine cuts out"),
    (None, "moment", "she cuts in before he can answer"),
    ("PHYS-07", "moment", "the pipe turns under her foot"),
    ("PHYS-07", "moment", "the log rolls under his boots"),
    (None, "moment", "she rolls her eyes"),
    ("PHYS-09", "moment", "Ben barges the door open"),
    ("PHYS-09", "moment", "Anna jams a chair under the handle"),
    (None, "moment", "Ben leans against the door and catches his breath"),
    ("PHYS-10", "moment", "Anna grabs the phone, the rope and the flashlight and runs"),
    ("PHYS-10", "moment", "Ben carries the flashlight, the rope and the phone in his arms"),
    (None, "moment", "Anna hands him the phone and picks up the rope"),
    (None, "moment", "Ben sets down the flashlight and the rope, then takes the phone"),
]


def wording_shot(number, shows, held="no", span="0-3", does="looks on", extra="", second=None):
    """One shot of scene 91 for a wording case."""
    end = float(span.split("-")[1]) + (3 if second else 0)
    lines = [f"### SHOT SC91-SH{number:03d} Case {number}", "- size: medium",
             f"- subject: CH-TEST-WOMAN | does: {does}"] + ([extra] if extra else []) + [
             f"- screen_time: {end:g}", f"- moment: {span} | shows: {shows}"]
    if second:
        lines.append(f"- moment: {span.split('-')[1]}-{end:g} | shows: {second}")
    lines.append(f"- held: {held}")
    return "\n" + "\n".join(lines) + "\n"


def flagged_cases(result, check_ids):
    """{case number: set of check IDs} of the scene 91 lines of a run."""
    found = {}
    for line in result.all_problems:
        if line.record.startswith("SC91-SH") and line.check_id in check_ids:
            found.setdefault(int(line.record[7:]), set()).add(line.check_id)
    return found


# Each physical sense check, the generic record it must flag, and the field.
PHYSICAL_SLIPS = [
    ("PHYS-01", "LOC-TEST-SHAFT", "mark", "a mark in the gap between a 2 metre car and a 2.4 metre shaft"),
    ("PHYS-01", "LOC-TEST-SHAFT", "object", "a ladder with 0.1 metres clear in front of it, a 0.4 metre hatch"),
    ("PHYS-02", "SC90-SH010", "subject", "a heavy 30 centimetre flashlight held in the teeth"),
    ("PHYS-03", "SC90-D01", "parenthetical", "a line spoken round the flashlight"),
    ("PHYS-03", "SC90-SH010", "subject", "the climber speaks on screen with the flashlight in her teeth"),
    ("PHYS-04", "SC90-SH110", "moment", "the ropes out of reach across the shaft"),
    ("PHYS-05", "SC90-SH020", "moment", "a strap cut with nothing to cut it"),
    ("PHYS-06", "SC90-SH030", "moment", "cover under an open grid roof"),
    ("PHYS-07", "SC90-SH040", "moment", "a rung that rolls"),
    ("PHYS-08", "SC90-SH050", "subject", "a weak man holding up a heavy man"),
    ("PHYS-08", "SC90-SH060", "moment", "a weak man running"),
    ("PHYS-09", "SC90-SH070", "moment", "a chair wedged under a door handle"),
    ("PHYS-09", "SC90-SH080", "moment", "a gate kicked open"),
    ("PHYS-10", "SC90-SH090", "subject", "three things in one person's hands"),
    ("PHYS-11", "SC90-SH100", "thing", "a 5 centimetre bolt given emphasis 2 in a wide shot"),
]


def write_files(folder, texts, extra=None):
    folder.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in ("context", "scene"):
        path = folder / GOLD_FILES[name].name
        path.write_text(texts[name], encoding="utf-8")
        paths.append(path)
    if extra:
        path = folder / "Scene 90 - the shaft.md"
        path.write_text(record_file(extra, "Scene 90 - the shaft"), encoding="utf-8")
        paths.append(path)
    return paths


def run(paths, check_ids, story=True, step=None):
    check_records.load_check_families()
    source = check_records.StorySource.from_file(str(EXCERPT), CONSTANTS) if story and EXCERPT.is_file() else None
    files = [parse_file(path, path.name, SCHEMA) for path in paths]
    result = check_records.run_checks(files, SCHEMA, WORDS, CONSTANTS, story=source, check_ids=check_ids, step=step)
    assert not result.crashed and not result.families_broken, (result.crashed, result.families_broken)
    return result


def lines_of(result, check_id=None):
    """The problem lines of a run, the scene outside the gold project's scope (the generic scene 90) included."""
    return [problem for problem in result.all_problems if check_id is None or problem.check_id == check_id]


# ---------------------------------------------------------------- the groups

def main():
    temporary_folder = tempfile.TemporaryDirectory(prefix="fix06b-")
    temporary = Path(temporary_folder.name)
    counter = {"n": 0}

    def fresh(texts, extra=None):
        counter["n"] += 1
        return write_files(temporary / f"case {counter['n']:02d}", texts, extra)

    @group("B1: hold_action_every_s (2.0 s) replaces hold_needs_still_s; the physical sense numbers are in "
           "_config/rules/constants.json with a meaning, a source and the judgement mark")
    def constants():
        table = CONSTANTS["constants"]
        assert "hold_needs_still_s" not in table, "the old constant is still there"
        entry = table["hold_action_every_s"]
        assert entry["value"] == 2.0 and entry.get("judgement") is True, entry
        wanted = {"body_pass_clearance_m": 0.5, "body_climb_clearance_m": 0.75, "teeth_hold_length_max_m": 0.2,
                  "reach_share_of_height": 0.6, "visible_thing_emphasis_min": 2, "tall_person_height_m": 1.85}
        wrong = [f"{name} {table.get(name, {}).get('value')!r}" for name, value in wanted.items()
                 if table.get(name, {}).get("value") != value]
        assert not wrong, wrong
        sizes = table["visible_thing_min_size_m_by_size"]["value"]
        assert sizes.get("wide") == 0.1, sizes
        for name in list(wanted) + ["visible_thing_min_size_m_by_size", "hold_action_every_s"]:
            for key in ("value", "unit", "meaning", "source"):
                assert table[name].get(key) not in (None, ""), f"{name}.{key}"
            assert table[name].get("judgement") is True, f"{name} is not marked a judgement"
        readers = [path.name for path in (TOOLS / "stage_tools").glob("*.py")
                   if "hold_needs_still_s" in path.read_text(encoding="utf-8")
                   and path.name not in ("compile_prompts.py",)]
        assert not readers, f"still reading the old constant: {readers}"
        return f"hold_action_every_s 2.0 s; {len(wanted) + 1} physical sense numbers, each a judgement with a source"

    @group("B1: CRAFT-26 turned round: a 7-second moment with one action is flagged, with four actions it is not")
    def held_moment():
        one = edit(gold_texts(), "scene", "SHOT SC10-SH150",
                   "- moment: 8-15 | shows: swallows once; breathes out slowly through her nose; blinks; her lips press "
                   "together; a slow breath in, her eyes on Saye; she blinks again",
                   "- moment: 8-15 | shows: listens; swallows once")
        lines = lines_of(run(fresh(one), ["CRAFT-26"]), "CRAFT-26")
        hits = [line for line in lines if line.record == "SC10-SH150" and line.field_name == "moment"
                and "8-15" in line.what]
        assert hits, [str(line) for line in lines]
        assert "1 small action" in hits[0].what and "at least 3" in hits[0].what, hits[0]
        assert hits[0].level == "W", hits[0]
        assert "stay still" in hits[0].fix and "never a list" in hits[0].fix, hits[0].fix
        four = edit(gold_texts(), "scene", "SHOT SC10-SH150",
                    "- moment: 8-15 | shows: swallows once; breathes out slowly through her nose; blinks; her lips "
                    "press together; a slow breath in, her eyes on Saye; she blinks again",
                    "- moment: 8-15 | shows: swallows once; breathes out through her nose; blinks; then her lips "
                    "press together")
        lines = lines_of(run(fresh(four), ["CRAFT-26"]), "CRAFT-26")
        assert not lines, [str(line) for line in lines]
        stillness = edit(gold_texts(), "scene", "SHOT SC10-SH150",
                         "- moment: 8-15 | shows: swallows once; breathes out slowly through her nose; blinks; her lips "
                         "press together; a slow breath in, her eyes on Saye; she blinks again",
                         "- moment: 8-15 | shows: swallows once; her head stays still; her hands do not move; she "
                         "waits")
        lines = lines_of(run(fresh(stillness), ["CRAFT-26"]), "CRAFT-26")
        assert lines and "1 small action" in lines[0].what, [str(line) for line in lines]
        return f"one action: {hits[0]}; four actions: silent; a list of still parts counts as no action"

    @group("B1: a pause held on picture needs the shot's last moments to carry small actions")
    def held_pause():
        texts = edit(gold_texts(), "scene", "SHOT SC10-SH190",
                     "- moment: 7.5-9 | shows: Iona's eyes go to Jude and she steps aside, toward him; Eli is in plain "
                     "sight again",
                     "- moment: 7.5-9 | shows: nobody moves")
        texts = edit(texts, "scene", "SHOT SC10-SH190",
                     "- moment: 4-7.5 | shows: Saye waits, her eyes on Iona; Iona swallows, her hands open at her "
                     "sides; Jude's chest rises and falls on the table",
                     "- moment: 4-7.5 | shows: Saye waits")
        lines = [line for line in lines_of(run(fresh(texts), ["CRAFT-26"]), "CRAFT-26")
                 if "pause of 3 s" in line.what]
        assert lines and lines[0].record == "SC10-SH190", [str(line) for line in lines]
        return str(lines[0])

    @group("B1: a breakdown that still writes the old still sub-part, with enough actions, raises nothing about "
           "stillness; FORM accepts it and no check asks for it")
    def old_still_sub_part():
        texts = edit(gold_texts(), "scene", "SHOT SC10-SH150", "| energy: held | display: 1 |",
                     "| energy: held | display: 1 | still: head, hands, torso |")
        texts = edit(texts, "scene", "SHOT SC10-SH010", "| tactic: hiding | energy: still | display: 1 |",
                     "| tactic: hiding | energy: still | display: 1 | still: whole_body |")
        form = [f"FORM-{number:02d}" for number in range(1, 14)]
        result = run(fresh(texts), ["CRAFT-15", "CRAFT-26", "CRAFT-27"] + form)
        lines = [str(line) for line in result.problems]
        assert not lines, lines
        definition = next(part for field in SCHEMA.record_types["SHOT"]["fields"] if field["name"] == "subject"
                          for part in field["sub_parts"] if part["key"] == "still")
        assert "depth" not in definition and "old field" in definition["meaning"].lower(), definition
        gold = run(fresh(gold_texts()), form)
        assert not [str(line) for line in gold.problems if "still" in line.what], [str(line) for line in gold.problems]
        return "silent with still written; the gold without it passes FORM-05 at standard depth"

    @group("B1: CRAFT-27 flags stillness words in a moment, a does and an end; energy: still and quoted story words "
           "are left alone")
    def stillness_words():
        texts = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                     "- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stops",
                     "- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stays still")
        texts = edit(texts, "scene", "SHOT SC10-SH110", "does: lies on the table between them, his chest rising and "
                     "falling", "does: lies motionless on the table between them")
        texts = edit(texts, "scene", "SHOT SC10-SH110", "- end: Eli by the fridge, the open bottle in one hand, eyes "
                     "on Saye", "- end: Eli frozen by the fridge, nobody moves")
        lines = lines_of(run(fresh(texts), ["CRAFT-27"]), "CRAFT-27")
        fields = sorted({line.field_name for line in lines if line.record == "SC10-SH110"})
        assert fields == ["end", "moment", "subject"], [str(line) for line in lines]
        assert all(line.level == "W" for line in lines), lines
        quoted = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                      "- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stops",
                      '- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stops; "Stay still."')
        quoted = edit(quoted, "scene", "SHOT SC10-SH110", "- end: Eli by the fridge, the open bottle in one hand",
                      "- end: Eli by the fridge, still holding the open bottle in one hand")
        lines = lines_of(run(fresh(quoted), ["CRAFT-27"]), "CRAFT-27")
        assert not lines, [str(line) for line in lines]
        return f"{len(lines_of(run(fresh(texts), ['CRAFT-27']), 'CRAFT-27'))} lines on moment, does and end; " \
               "energy: still, a quoted line and 'still holding' pass"

    @group("B2: CRAFT-28 flags a contact and its result in one shot; the pair split across a cut is the fix and "
           "passes")
    def contact_cut():
        together = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                        "- moment: 3.5-6 | shows: he twists it the other way and it comes off; his eyes come up to "
                        "Saye",
                        "- moment: 3.5-6 | shows: he kicks the chair by the fridge; the chair topples")
        lines = lines_of(run(fresh(together), ["CRAFT-28"]), "CRAFT-28")
        assert lines and lines[0].record == "SC10-SH110" and lines[0].level == "W", [str(line) for line in lines]
        assert "different size or angle" in lines[0].fix and "sound" in lines[0].fix, lines[0].fix
        next_moment = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                           "- moment: 0-3.5 | shows: he twists the cap; it will not turn; he stops",
                           "- moment: 0-3.5 | shows: he twists the cap; he kicks the chair by the fridge")
        next_moment = edit(next_moment, "scene", "SHOT SC10-SH110",
                           "- moment: 3.5-6 | shows: he twists it the other way and it comes off; his eyes come up "
                           "to Saye", "- moment: 3.5-6 | shows: the chair topples onto the floor")
        assert lines_of(run(fresh(next_moment), ["CRAFT-28"]), "CRAFT-28"), "cause and effect in two moments of one shot"
        split = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                     "- moment: 3.5-6 | shows: he twists it the other way and it comes off; his eyes come up to Saye",
                     "- moment: 3.5-6 | shows: he twists it the other way; he kicks the chair by the fridge")
        split = edit(split, "scene", "SHOT SC10-SH120",
                     "- moment: 0-2.5 | shows: Saye holds Eli's look, then her head turns to the flask on the counter",
                     "- moment: 0-2.5 | shows: the chair topples onto the floor; Saye's head turns to the flask on "
                     "the counter")
        lines = lines_of(run(fresh(split), ["CRAFT-28"]), "CRAFT-28")
        assert not lines, [str(line) for line in lines]
        negated = edit(gold_texts(), "scene", "SHOT SC10-SH110",
                       "- moment: 3.5-6 | shows: he twists it the other way and it comes off; his eyes come up to Saye",
                       "- moment: 3.5-6 | shows: he kicks the chair; it does not fall")
        assert not lines_of(run(fresh(negated), ["CRAFT-28"]), "CRAFT-28"), "a negated effect was flagged"
        return f"together: {lines_of(run(fresh(together), ['CRAFT-28']), 'CRAFT-28')[0]}; split across the cut and " \
               "negated: silent"

    @group("B3: each physical sense check flags its generic slip, as a warning that asks a question")
    def physical_slips():
        result = run(fresh(gold_texts(), GENERIC_WORLD), [f"PHYS-{number:02d}" for number in range(1, 12)])
        found = lines_of(result)
        missing, wrong = [], []
        for check_id, record, field_name, about in PHYSICAL_SLIPS:
            hits = [line for line in found if line.check_id == check_id and line.record == record
                    and line.field_name == field_name]
            if not hits:
                missing.append(f"{check_id} {record} {field_name} ({about})")
                continue
            if hits[0].level != "W" or "?" not in hits[0].what or not hits[0].fix.startswith("Fix:"):
                wrong.append(str(hits[0]))
        assert not missing, f"not caught: {missing}; got {[str(line) for line in found]}"
        assert not wrong, wrong
        hatch = [line for line in found if line.check_id == "PHYS-01" and "hatch" in line.what]
        ladder = [line for line in found if line.check_id == "PHYS-01" and "climb" in line.what]
        assert hatch and ladder, [str(line) for line in found if line.check_id == "PHYS-01"]
        teeth = next(line for line in found if line.check_id == "PHYS-02")
        assert "0.3 metres" in teeth.what and "heavy" in teeth.what, teeth
        return f"{len(PHYSICAL_SLIPS)} slips caught by {len({entry[0] for entry in PHYSICAL_SLIPS})} checks; " \
               f"for example: {teeth}"

    @group("B3: other ways of writing the same slips are caught too, and near misses are not")
    def physical_phrasings():
        variants = [
            ("- subject: CH-TEST-PATIENT | does: holds up the guard against the grid",
             "- subject: CH-TEST-PATIENT | does: holds the guard up against the grid", "PHYS-08", "SC90-SH050"),
            ("does: climbs the rungs with the flashlight in her teeth",
             "does: climbs the rungs with the flashlight clamped in her jaws", "PHYS-02", "SC90-SH010"),
            ("- moment: 0-3 | shows: the two men take cover in the corner of the car from the shots coming down",
             "- moment: 0-3 | shows: the guard drags the patient into the corner for cover from the shots fired down "
             "through the roof grid", "PHYS-06", "SC90-SH030"),
            ("- moment: 0-3 | shows: the guard kicks the gate open", "- moment: 0-3 | shows: the gate is kicked open",
             "PHYS-09", "SC90-SH080"),
            ("- moment: 0-3 | shows: the patient runs the length of the car",
             "- moment: 0-3 | shows: the patient sprints for the hatch", "PHYS-08", "SC90-SH060"),
        ]
        world = GENERIC_WORLD.replace("- dressing: a bare steel car whose roof is a grid of flat bars",
                                      "- dressing: a bare steel car")
        missed = []
        for old, new, check_id, record in variants:
            assert world.count(old) == 1, old
            changed = world.replace(old, new)
            found = [line for line in lines_of(run(fresh(gold_texts(), changed), [check_id]), check_id)
                     if line.record == record]
            if not found:
                missed.append(f"{check_id} {record}: {new}")
        assert not missed, missed
        near = world.replace("- subject: CH-TEST-PATIENT | does: holds up the guard against the grid",
                             "- subject: CH-TEST-PATIENT | does: holds her hand up against the grid")
        near = near.replace("- moment: 0-3 | shows: the patient takes the guard's weight",
                            "- moment: 0-3 | shows: the patient raises one hand")
        near = near.replace("- subject: CH-TEST-PATIENT | does: runs to the hatch",
                            "- subject: CH-TEST-PATIENT | does: runs his hand along the grid")
        near = near.replace("- moment: 0-3 | shows: the patient runs the length of the car",
                            "- moment: 0-3 | shows: his fingers find the hatch")
        found = [str(line) for line in lines_of(run(fresh(gold_texts(), near), ["PHYS-08"]), "PHYS-08")]
        assert not found, found
        return f"{len(variants)} other phrasings caught; 'holds her hand up' and 'runs his hand along' pass"

    @group("B3: the same generic scene with the slips mended raises no physical sense line")
    def physical_mended():
        mended = GENERIC_WORLD
        replacements = [
            ("- size: [2.4, 2.4, 20.0]", "- size: [4.0, 4.0, 20.0]"),
            ("- object: CAR | at: [1.2, 1.2]", "- object: CAR | at: [2.6, 2.0]"),
            ("- mark: CLIMB | at: [0.15, 1.6]", "- mark: CLIMB | at: [0.6, 1.6]"),
            ("size: [0.4, 0.1, 0.8]", "size: [0.8, 0.1, 1.8]"),
            ("- object: ROPES | at: [2.3, 2.3]", "- object: ROPES | at: [0.3, 2.3]"),
            ("a heavy black metal flashlight about 30 centimetres long", "a pen light the length of a finger"),
            ("- real_size: [0.05, 0.05, 0.3]", "- real_size: [0.02, 0.02, 0.09]"),
            ("- parenthetical: round the flashlight", "- parenthetical: none"),
            ("- hear: SC90-D01 | speaker: on_screen | at: 1", "- hear: none"),
            ("does: cuts the strap and pulls it free", "does: cuts the strap with a utility knife and pulls it free"),
            ("a dark knitted cap", "a dark knitted cap, a utility knife clipped to her belt"),
            ("a grid of flat bars", "a grid of flat bars, with a wooden deck over one end"),
            ("the rung rolls under her hand like a rolling pin", "the rung bends a little under her hand"),
            ("does: holds up the guard against the grid", "does: leans on the grid beside the guard"),
            ("does: runs to the hatch", "does: limps to the hatch"),
            ("the patient runs the length of the car", "the patient limps the length of the car"),
            ("- dressing: a bare steel car", "- exit: GATE | leads_to: the corridor; the gate opens away from the car\n"
                                             "- dressing: a bare steel car"),
            ("does: holds the rope, the hook and the bag", "does: holds the rope and the hook; the bag hangs on her back"),
            ("- thing: PR-TEST-BOLT | emphasis: 2", "- thing: PR-TEST-BOLT | emphasis: 1"),
        ]
        for old, new in replacements:
            assert mended.count(old) == 1, old
            mended = mended.replace(old, new)
        result = run(fresh(gold_texts(), mended), [f"PHYS-{number:02d}" for number in range(1, 12)])
        lines = [str(line) for line in lines_of(result)]
        assert not lines, lines
        return f"{len(replacements)} mends; no line"

    @group("F11: CRAFT-26 counts held moments only and reads commas and 'and': a long walk, a comma list and an "
           "'and' list of small actions pass; poses, non-actions and one small action in a long moment are flagged")
    def held_wordings():
        text = WORDING_WORLD + "".join(wording_shot(number, shows, held=held, span=span)
                                       for number, (_, held, span, shows) in enumerate(HELD_WORDINGS, 1))
        found = flagged_cases(run(fresh(gold_texts(), text), ["CRAFT-26"]), {"CRAFT-26"})
        wrong = [f"{'missed' if expected else 'false alarm'}: [held {held}, {span}] {shows}"
                 for number, (expected, held, span, shows) in enumerate(HELD_WORDINGS, 1)
                 if bool(found.get(number)) != expected]
        assert not wrong, wrong
        return (f"{sum(1 for case in HELD_WORDINGS if not case[0])} wordings pass, "
                f"{sum(1 for case in HELD_WORDINGS if case[0])} are flagged, as they should be")

    @group("F15: CRAFT-27 leaves 'still wet', 'frozen peas', 'the rigid collar', 'the still water' and 'Ben, still in "
           "his coat' alone, and flags 'doesn't stir', 'like a statue', 'holds her position, unblinking'")
    def stillness_wordings():
        text = WORDING_WORLD + "".join(wording_shot(number, shows)
                                       for number, (_, shows) in enumerate(STILLNESS_WORDINGS, 1))
        found = flagged_cases(run(fresh(gold_texts(), text), ["CRAFT-27"]), {"CRAFT-27"})
        wrong = [f"{'missed' if expected else 'false alarm'}: {shows}"
                 for number, (expected, shows) in enumerate(STILLNESS_WORDINGS, 1)
                 if bool(found.get(number)) != expected]
        assert not wrong, wrong
        return f"{len(STILLNESS_WORDINGS)} wordings judged as they should be"

    @group("F12: CRAFT-28 reads 'swings the bottle into', an effect before its cause with 'as', 'bumps' and 'slams "
           "... down', and leaves rain, light, a room and a face alone")
    def contact_wordings():
        text = WORDING_WORLD + "".join(wording_shot(number, first, second=second)
                                       for number, (_, first, second) in enumerate(CONTACT_WORDINGS, 1))
        result = run(fresh(gold_texts(), text), ["CRAFT-28"])
        found = flagged_cases(result, {"CRAFT-28"})
        wrong = [f"{'missed' if expected else 'false alarm'}: {first}" + (f" / {second}" if second else "")
                 for number, (expected, first, second) in enumerate(CONTACT_WORDINGS, 1)
                 if bool(found.get(number)) != expected]
        assert not wrong, wrong
        effect_first = [line for line in result.all_problems if line.record == "SC91-SH002"]
        assert effect_first and '"shatters" as "smashes into"' in effect_first[0].what, effect_first
        return f"{len(CONTACT_WORDINGS)} wordings judged as they should be; for example: {effect_first[0].what}"

    @group("F16: the physical sense checks read 'the back door's handle', 'gripped by his teeth', 'in one hand ... "
           "in the other' and a moment's hands, and leave 'rolls her shoulders' and 'the door frame' alone")
    def physical_wordings():
        things = "\n".join(f"- thing: {name} | emphasis: 1" for name in ("PR-TEST-LAMP", "PR-TEST-PHONE",
                                                                          "PR-TEST-ROPE"))
        text = WORDING_WORLD
        for number, (_, field_name, words) in enumerate(PHYSICAL_WORDINGS, 1):
            if field_name == "subject":
                text += wording_shot(number, "she moves on", does=words, extra=things)
            else:
                text += wording_shot(number, words, extra=things)
        checks = [f"PHYS-{number:02d}" for number in range(1, 12)]
        found = flagged_cases(run(fresh(gold_texts(), text), checks), set(checks))
        wrong = [f"{expected or 'no line'} wanted, got {sorted(found.get(number, []))}: {words}"
                 for number, (expected, _, words) in enumerate(PHYSICAL_WORDINGS, 1)
                 if sorted(found.get(number, [])) != ([expected] if expected else [])]
        assert not wrong, wrong
        return f"{len(PHYSICAL_WORDINGS)} wordings judged as they should be"

    def judged(held_cases, stillness_cases, contact_cases, physical_cases):
        """{check: (false alarms, misses)} of four lists of wordings, each run as one shot of scene 91."""
        found = {}
        text = WORDING_WORLD + "".join(wording_shot(number, shows, held=held, span=span)
                                       for number, (_, held, span, shows) in enumerate(held_cases, 1))
        flagged = flagged_cases(run(fresh(gold_texts(), text), ["CRAFT-26"]), {"CRAFT-26"})
        found["CRAFT-26"] = [(expected, f"[held {held}, {span}] {shows}", bool(flagged.get(number)))
                             for number, (expected, held, span, shows) in enumerate(held_cases, 1)]
        text = WORDING_WORLD + "".join(wording_shot(number, shows) for number, (_, shows) in enumerate(stillness_cases, 1))
        flagged = flagged_cases(run(fresh(gold_texts(), text), ["CRAFT-27"]), {"CRAFT-27"})
        found["CRAFT-27"] = [(expected, shows, bool(flagged.get(number)))
                             for number, (expected, shows) in enumerate(stillness_cases, 1)]
        text = WORDING_WORLD + "".join(wording_shot(number, first, second=second)
                                       for number, (_, first, second) in enumerate(contact_cases, 1))
        flagged = flagged_cases(run(fresh(gold_texts(), text), ["CRAFT-28"]), {"CRAFT-28"})
        found["CRAFT-28"] = [(expected, first + (f" / {second}" if second else ""), bool(flagged.get(number)))
                             for number, (expected, first, second) in enumerate(contact_cases, 1)]
        things = "\n".join(f"- thing: {name} | emphasis: 1" for name in ("PR-TEST-FLASHLIGHT", "PR-TEST-PHONE",
                                                                          "PR-TEST-ROPE"))
        text = WORDING_WORLD + ROUND_2_PROPS + "".join(wording_shot(number, words, extra=things)
                                                       for number, (_, _, words) in enumerate(physical_cases, 1))
        checks = [f"PHYS-{number:02d}" for number in range(1, 12)]
        flagged = flagged_cases(run(fresh(gold_texts(), text), checks), set(checks))
        found["PHYS"] = [(expected, f"[{expected}] {words}", sorted(flagged.get(number, [])) == ([expected] if expected
                                                                                                else []))
                         for number, (expected, _, words) in enumerate(physical_cases, 1)]
        wrong = {}
        for check, cases in found.items():
            if check == "PHYS":
                wrong[check] = ([words for expected, words, right in cases if not right and not expected],
                                [words for expected, words, right in cases if not right and expected])
            else:
                wrong[check] = ([words for expected, words, got in cases if got and not expected],
                                [words for expected, words, got in cases if expected and not got])
        return wrong

    @group("N7 and N8: the reviewer's round 2 wordings are all judged right: CRAFT-26 reads stares, sits and stands "
           "held in a long moment and 'close again' as an action; CRAFT-27 reads 'stays put' and 'stays exactly "
           "where'; CRAFT-28 reads 'the plates jump', 'ploughs into', 'bangs the jar' and leaves 'the thought hits "
           "him' alone; the physical sense checks read 'spins', 'shoulders the door open' and 'juggles' and leave "
           "'cuts him off', 'cuts across' and 'cuts out' alone")
    def round_2_wordings():
        wrong = judged(ROUND_2_HELD_WORDINGS, ROUND_2_STILLNESS_WORDINGS, ROUND_2_CONTACT_WORDINGS,
                       ROUND_2_PHYSICAL_WORDINGS)
        faults = {check: pair for check, pair in wrong.items() if pair[0] or pair[1]}
        assert not faults, faults
        count = sum(len(cases) for cases in (ROUND_2_HELD_WORDINGS, ROUND_2_STILLNESS_WORDINGS,
                                             ROUND_2_CONTACT_WORDINGS, ROUND_2_PHYSICAL_WORDINGS))
        return f"{count} wordings, no false alarm and no miss"

    @group("N7: a contact split across two shots is read by the same rule as CRAFT-28 and the clip grouping: 'slams "
           "her fist onto the counter' ends one shot and 'the plates jump' opens the next; an abstract cause is none")
    def round_2_contact_across_shots():
        from stage_tools.checks_craft_reasons_words import cause_positions, contact_found, effect_positions
        ending, opening = "she looks at Ben once, then slams her fist onto the counter", "the plates jump"
        assert cause_positions(WORDS, ending), "no cause read at the end of the first shot"
        assert effect_positions(WORDS, opening), "no effect read at the start of the next shot"
        assert contact_found(WORDS, [ending, opening]) is not None, "the two moments in one shot are not a contact"
        assert not cause_positions(WORDS, "the thought hits him"), "an abstract cause is read as a contact"
        assert not cause_positions(WORDS, "the news hits her hard"), "an abstract cause is read as a contact"
        return "the cause, the effect and the pair are read; 'the thought hits him' and 'the news hits her' are not"

    @group("N7 and N8: the held-out wordings, written before the round 2 rules changed and never used to choose them, "
           "are judged no worse than the figures measured after the change (5 false alarms and 16 misses before, 2 "
           "and 12 after)")
    def held_out_wordings():
        wrong = judged(HELD_OUT_HELD, HELD_OUT_STILLNESS, HELD_OUT_CONTACT, HELD_OUT_PHYSICAL)
        over = {check: (len(alarms), len(misses), HELD_OUT_CEILING[check])
                for check, (alarms, misses) in wrong.items()
                if len(alarms) > HELD_OUT_CEILING[check][0] or len(misses) > HELD_OUT_CEILING[check][1]}
        assert not over, (over, wrong)
        alarms = sum(len(pair[0]) for pair in wrong.values())
        misses = sum(len(pair[1]) for pair in wrong.values())
        return f"{alarms} false alarms and {misses} misses on {sum(map(len, (HELD_OUT_HELD, HELD_OUT_STILLNESS, HELD_OUT_CONTACT, HELD_OUT_PHYSICAL)))} held-out wordings"

    @group("N11: library B1 and its digest no longer teach 'while she stays still', and errata 23 lists B1")
    def b1_without_stillness():
        library = SKILL / "references" / "library"
        b1 = (library / "B1 Camera, lens and movement.md").read_text(encoding="utf-8")
        digest = (library / "digests" / "B1 Camera, lens and movement - digest.md").read_text(encoding="utf-8")
        for name, text in (("B1", b1), ("the B1 digest", digest)):
            assert "while she stays still" not in text, f"{name} still teaches 'while she stays still'"
            assert "while she breathes and blinks" in text, f"{name} lacks the new push-in phrasing"
        errata = (library / "02 Errata.md").read_text(encoding="utf-8")
        entry_23 = errata[errata.index("### 23."):errata.index("### 24.")]
        applies = next(line for line in entry_23.splitlines() if line.startswith("- **Applies to**"))
        assert "B1" in applies and "digest" in applies, applies
        return "B1 and its digest say 'while she breathes and blinks'; errata 23 applies to both"

    @group("F13: the kit texts no longer teach stillness: step 14, the schema's TAKE example, D15 rule 3, the "
           "record-format example, card 10 and the A4 digest; errata 23 lists D15 R3 and D15 marks its old prompts "
           "withdrawn")
    def texts_without_stillness():
        read = lambda *parts: SKILL.joinpath(*parts).read_text(encoding="utf-8")  # noqa: E731
        stage_14 = read("stages", "14 Add-on - generation packs", "CONTEXT.md")
        assert "Only her mouth moves" not in stage_14 and "said once, by the right mouth" in stage_14
        take = next(field for field in SCHEMA.record_types["TAKE"]["fields"] if field["name"] == "review")
        assert "only" not in take["example"].lower() and "move between the written actions" in take["example"]
        d15 = read("references", "library", "D15 Directing performance.md")
        rule_3 = next(line for line in d15.splitlines() if line.startswith("3. If the line, eyeline or cut"))
        assert 'with "still" or one movement' not in rule_3 and "breath and blinks going on" in rule_3, rule_3
        for number, following in ((1, 2), (2, 3), (6, None)):
            start = d15.index(f"### Example {number}.")
            section = d15[start:d15.index(f"### Example {following}.") if following else d15.index("## 11.")]
            assert "withdrawn" in section and "10 October 2026" in section, f"Example {number} is not marked withdrawn"
        assert "| still:" not in read("references", "formats", "01 Record format.md")
        assert "while she stays still" not in read("references", "cards", "10 Camera.md")
        digest = read("references", "library", "digests", "A4 Editing, transitions, rhythm and sound - digest.md")
        rule_55 = next(line for line in digest.splitlines() if line.startswith("55. "))
        assert 'prompt "listening, does not speak"' not in rule_55 and "lips closed" in rule_55, rule_55
        errata = read("references", "library", "02 Errata.md")
        entry_23 = errata[errata.index("### 23."):errata.index("### 24.")]
        assert "D15 R3" in entry_23 and "### 27." in errata, entry_23[:300]
        return "six texts rewritten; errata 23 lists D15 R3; entry 27 covers the listener rule"

    @group("F4 and F6, the gold part: the kitchen's state line and the bottle say what is there, and the route "
           "raises no ROUTE-15 line for the chat-saved scene 10")
    def gold_says_what_is_there():
        absence = [word for word in WORDS["absence_words"]["words"]]
        pattern = re.compile(r"(?<![A-Za-z'])(" + "|".join(re.escape(word) for word in absence) + r")(?![A-Za-z'])",
                             re.I)
        values = []
        for path in [GOLD_FILES["context"], CHAT_FOLDER / "08 Places and things.md",
                     CHAT_FOLDER / "09 Continuity.md"]:
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.startswith(("- state_line: a bare, clean kitchen", "- fixed_description: a clear, unlabelled")):
                    values.append(line)
        assert len(values) == 4, values
        holding = [value for value in values if pattern.search(value)]
        assert not holding, holding
        import os
        import shutil
        import subprocess
        project = temporary / "route project"
        shutil.copytree(CHAT_FOLDER, project)
        environment = dict(os.environ)
        environment["STAGE_LOCK_WAIT_SECONDS"] = "2"
        completed = subprocess.run([sys.executable, str(TOOLS / "stage.py"), "compile", "--project", str(project),
                                    "--scene", "SC10", "--route", "h3-comfyui", "--story", str(EXCERPT)],
                                   capture_output=True, text=True, encoding="utf-8", cwd=str(REPOSITORY),
                                   env=environment, timeout=900)
        output = completed.stdout + completed.stderr
        assert "clips for MiniMax H3 in ComfyUI" in output, output[-800:]
        assert "ROUTE-15" not in output, [line for line in output.splitlines() if "ROUTE-15" in line][:3]
        page = next((project / "20 Prompts for AI video").rglob("Scene 10*.md")).read_text(encoding="utf-8")
        assert "A clear, unlabelled plastic water bottle" in page and "no label" not in page
        return "4 values with no absence word; compile --route: no ROUTE-15 line, the bottle described in its clip"

    @group("the gold scene 10 and its chat-saved copy raise none of the new warnings, and the new rules break no "
           "other check there")
    def gold_clean():
        result = run(fresh(gold_texts()), None)
        new = [str(line) for line in result.problems if line.check_id in NEW_CHECKS]
        assert not new, new
        craft = [str(line) for line in result.problems if line.check_id.split("-")[0] in ("CRAFT", "PHYS")]
        assert not craft, craft
        detail = f"gold: {len(result.checks_run)} checks, none of the new ones fires"
        if CHAT_FOLDER.is_dir():
            chat = run(sorted(CHAT_FOLDER.rglob("*.md")), NEW_CHECKS + ["CRAFT-15"])
            lines = [str(line) for line in chat.problems]
            assert not lines, lines
            detail += f"; chat copy: silent on {len(NEW_CHECKS) + 1} checks"
        stills = [line for line in GOLD_FILES["scene"].read_text(encoding="utf-8").splitlines()
                  if line.startswith("- subject:") and "| still:" in line]
        assert not stills, stills[:2]
        return detail

    @group("the new checks are warnings with a plain sentence and a J title, listed for steps 4, 7 and 8")
    def registration():
        check_records.load_check_families()
        problems = []
        for check_id in NEW_CHECKS:
            definition = check_records.REGISTRY.get(check_id)
            if definition is None:
                problems.append(f"{check_id} not registered")
                continue
            if definition.level != "W" or definition.build != 1:
                problems.append(f"{check_id} is {definition.level} build {definition.build}")
            if "J" not in re.findall(r"\bJ\b", definition.title):
                problems.append(f"{check_id}'s title does not say J")
            plain = definition.plain
            if not plain or plain[0].isupper() or re.search(r"[A-Z]{2,}-\d\d|\bJ\b", plain):
                problems.append(f"{check_id}'s plain sentence {plain!r}")
        steps = json.loads((SKILL / "_config" / "schema" / "steps.json").read_text(encoding="utf-8"))["steps"]
        listed = {entry["step"]: entry["checks"] for entry in steps}
        if "PHYS-01" not in listed[4]:
            problems.append("step 4 does not list PHYS-01")
        if "PHYS-03" not in listed[7]:
            problems.append("step 7 does not list PHYS-03")
        for check_id in NEW_CHECKS:
            if check_id not in listed[8]:
                problems.append(f"step 8 does not list {check_id}")
        assert not problems, problems
        return f"{len(NEW_CHECKS)} warnings; step 4 lists PHYS-01, step 7 PHYS-03, step 8 all of them"

    @group("no new or changed file of this work holds an email address")
    def no_email():
        files = [Path(__file__), TOOLS / "stage_tools" / "checks_physical_sense.py",
                 TOOLS / "stage_tools" / "checks_craft_reasons_words.py", SKILL / "_config" / "rules" / "constants.json",
                 SKILL / "_config" / "rules" / "words.json", GOLD_FILES["scene"]]
        found = [f"{path.name}: {match}" for path in files
                 for match in EMAIL.findall(path.read_text(encoding="utf-8"))]
        assert not found, found
        return f"{len(files)} files read"

    temporary_folder.cleanup()
    failing = RESULTS.count(False)
    print(f"RESULT: {'PASS' if not failing else 'FAIL'} ({RESULTS.count(True)} passed, {failing} failing groups)")
    return 1 if failing else 0


if __name__ == "__main__":
    sys.exit(main())
