"""clip_book.py: the clip book of a route, a model plus the place it runs. The first route is MiniMax H3 in ComfyUI,
Reference to Video (_config/adapters/video_models.json, minimax-h3-comfyui-r2v; Project notes 42 and 43).

In plain words:
- a clip is one run of the video model, and it holds one to three shots of one scene (or part of one long shot);
  code groups each scene's video shots into clips: the same place, at most four people's pictures, clearly
  different framings cut together, two singles of two people facing each other only after a shot showing both, a
  contact pair kept together so the cut lands on the contact, a held take always a clip of its own, a moving camera
  always a clip of its own, and a long shot that is not held split at its planned cutaways;
- each clip's length is on the route's own grid (17 x k + 5 frames at 24 frames a second, 124 to 362 frames), with
  a tail of at least 1.3 seconds after the part to keep, because H3 breaks up near the end; the seconds to type in
  the template's Duration box land on the intended frames whichever way the template rounds;
- the prompt is written by code from the records in MiniMax's reference format: six sections in MiniMax's order, a
  <Subject N> for the place and for each person (their fixed description and state line word for word, tied to
  their <Picture N>), timed shots, spoken lines word for word inside <d>[Language] ...</d>, the room's sound, and
  non_diegetic_music: N/A. Words H3 would show or say (no, not, still, words about speaking, comparisons) are kept
  out: a clause that needs one is left out and listed on the clip page;
- every clip gets a start picture brief built from its first moment, from a master picture of the empty place
  (one per place, numbered M1, M2 ... by the place's first scene in the whole project);
- it writes the clip book in "20 Prompts for AI video/MiniMax H3 in ComfyUI/" (settings, pictures to make first,
  one page per scene with one part per clip, the shot map, what to change when a clip goes wrong, and the take log
  with the route's rules and their marks) and one machine file per scene in "For machines - do not edit/prompts/"
  ("SC10 - minimax-h3-comfyui-r2v.json"), which the route checks (checks_clip_book.py, ROUTE-01 ...) read.

compile_prompts.py calls compile_route() for compile --route <name> or when PROJECT video_route is h3_comfyui_r2v.
Prompts are compiled, never typed: change a record and compile again. Standard library only.
"""

import json
import math
import re
from dataclasses import dataclass, field as dataclass_field, replace as dataclass_replace
from pathlib import Path

from .derive_fields import (constant, cut_points, element_name, element_of, is_yes, number_of, scene_label,
                            scene_of, shot_number)
from .record_format import normalise_word, split_item, split_list

ROUTE_FOLDER = "MiniMax H3 in ComfyUI"
ROUTE_VALUE = "h3_comfyui_r2v"          # PROJECT video_route
ROUTE_MODEL = "minimax-h3-comfyui-r2v"  # the adapter entry
ROUTE_FILE_KIND = "clip_book"           # the marker the GEN lint reads: a route pack is checked by the route checks
KEPT_OUT_LISTS = ("absence", "stillness", "talk", "comparison")
HELD_WORDS = ("stays", "stay", "remains", "remain")
# a voice clause longer than this, or tied to a time ('until', 'once he'), tells the character's story, not a sound
# H3 can make ("with warmth held back until she spends it on one person near the end"; review F17, J)
VOICE_CLAUSE_WORDS_MAX = 7
VOICE_STORY_WORDS = re.compile(r"\b(?:until|unless|when|whenever|once|while|after|before|near the end|by the end|"
                               r"someone|used to)\b", re.IGNORECASE)
BODY_PARTS = ("hands", "hand", "fist", "fists", "fingers", "knuckles", "palm", "palms", "wrist", "wrists", "arm", "arms",
              "sleeve", "sleeves", "cuff", "chest", "belly", "shoulder", "shoulders", "feet", "foot", "legs",
              "knees", "boots")
SPEAKING_MOMENT = re.compile(r"\b(?:says?|asks?|answers?|speaks?|calls?|words?|lines?|replies|reply)\b", re.IGNORECASE)
LINE_GAP_S = 0.2           # between two lines, the second never starts before the first ends plus this
LINE_END_MARGIN_S = 1.0    # a line should end this long before the keep point: lines start late in H3 (review F18, J)
SIZE_SCALE = ["extreme_wide", "wide", "medium_wide", "medium", "medium_close_up", "close_up", "extreme_close_up"]
SIZE_WORDS = {"extreme_wide": "extreme wide shot", "wide": "wide shot", "medium_wide": "medium wide shot",
              "medium": "medium shot", "medium_close_up": "medium close-up", "close_up": "close-up",
              "extreme_close_up": "extreme close-up", "insert": "close insert shot"}
NUMBER_WORDS = {0: "no", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
SHOTS_OPENING = {1: "The shot is", 2: "Both shots are", 3: "All three shots are"}
CLOTHING_NOUNS = ("shirt", "blouse", "coat", "jacket", "cardigan", "jumper", "sweater", "dress", "skirt", "trousers",
                  "jeans", "suit", "uniform", "overalls", "robe", "gown", "pyjamas", "vest", "hoodie", "boots",
                  "shoes", "apron", "scrubs", "t-shirt")
QUOTED_IN_LINE = re.compile(r'\s*[:,]?\s*"[^"]*"')
PICTURE_ONE = ("<Picture 1> is the shot-planning reference for [Shot 1]: it sets where the camera stands, the shot "
               "size, the set, the props, the light and where each person is at the first moment; the poses, eyes and "
               "faces come from the shots below, and the people move on from their places at once.")
PICTURE_ONE_EMPTY = ("<Picture 1> is the shot-planning reference for [Shot 1]: it sets where the camera stands, the "
                     "shot size, the set, the props and the light.")
LEFT_OUT_WHY = "Left out, because H3 would show it"


# ---------------------------------------------------------------- the route's facts

@dataclass
class RouteFacts:
    """One route entry of _config/adapters/video_models.json (kind: route), with the numbers the clip book needs."""
    name: str
    facts: dict
    display: str
    fps: int = 24
    block: int = 17
    offset: int = 5
    min_frames: int = 124
    max_frames: int = 362
    tail_s_min: float = 1.3
    people_pictures_max: int = 4
    references_max: int = 9
    shots_per_clip_max: int = 3

    @classmethod
    def from_adapters(cls, adapters, name=ROUTE_MODEL):
        facts = adapters.video.get(name) or {}
        frames = facts.get("frames") or {}
        inputs = facts.get("inputs") or {}
        return cls(name=name, facts=facts, display=facts.get("name") or name, fps=int(facts.get("fps") or 24),
                   block=int(frames.get("block") or 17), offset=int(frames.get("offset") or 5),
                   min_frames=int(frames.get("min") or 124), max_frames=int(frames.get("max") or 362),
                   tail_s_min=float(facts.get("tail_s_min") or 1.3),
                   people_pictures_max=int(inputs.get("people_pictures_max") or 4),
                   references_max=int(inputs.get("references_max") or 9),
                   shots_per_clip_max=int(facts.get("shots_per_clip_max") or 3))

    @property
    def longest_s(self):
        return self.max_frames / self.fps

    @property
    def longest_kept_s(self):
        """The most a clip can keep: its longest length less the smallest tail."""
        return self.longest_s - self.tail_s_min

    def on_grid(self, frames):
        return (frames - self.offset) % self.block == 0

    def grid(self):
        """Every length on the grid from the shortest to the longest, in frames."""
        first = self.min_frames + (-(self.min_frames - self.offset)) % self.block
        return list(range(first, self.max_frames + 1, self.block))

    def rules(self):
        return [dict(entry) for entry in self.facts.get("rules") or [] if isinstance(entry, dict)]

    def size_for(self, frame_shape):
        """(full size, test size, crop note) for the film's frame shape."""
        sizes = self.facts.get("sizes") or {}
        shape = str(frame_shape or "16_9").replace(":", "_")
        chosen = sizes.get(shape)
        note = ""
        if not isinstance(chosen, dict):
            chosen = sizes.get("16_9") or {"full": [1344, 768], "test": [1024, 576]}
            note = sizes.get("other_shapes") or "make it at the 16_9 sizes and crop in the edit"
        return chosen.get("full") or [1344, 768], chosen.get("test") or [1024, 576], note


def frames_from_duration_box(seconds, javascript_remainder, fps=24, block=17, offset=5):
    """Repeat the ComfyUI template's sum: seconds typed in Float (Duration) -> frames, snapped to the 17 x k + 5 grid.
    The template's own code takes a remainder that can be negative (as JavaScript does) or always positive (as
    Python does); both forms are kept, so a value that lands the same both ways is safe (the reference code of
    Project notes 42)."""
    raw_frames = max(offset, round(seconds * fps))
    step = offset - (raw_frames % block)
    step = math.fmod(step, block) if javascript_remainder else step % block
    return int(raw_frames + step)


def duration_to_type(frames, fps=24, block=17, offset=5):
    """The one-decimal number of seconds to type that lands exactly on these frames both ways, or None."""
    best = None
    for tenths in range(1, 400):
        seconds = tenths / 10
        if seconds > frames / fps + 1e-9:
            break
        if (frames_from_duration_box(seconds, False, fps, block, offset) == frames
                and frames_from_duration_box(seconds, True, fps, block, offset) == frames):
            best = seconds
    return best


def frames_for(kept_s, route):
    """(frames, fits): the shortest length on the route's grid that holds the kept part plus the smallest tail, never
    under the route's shortest length; fits is False when even the longest length cannot hold it (then the longest)."""
    needed = max(route.min_frames, math.ceil((kept_s + route.tail_s_min) * route.fps - 1e-9))
    for frames in route.grid():
        if frames >= needed:
            return frames, True
    return route.max_frames, False


def mm_ss_ms(seconds):
    whole = max(0.0, float(seconds))
    return f"{int(whole // 60):02d}:{whole % 60:06.3f}"


def plain_number(value):
    value = round(float(value), 2)
    return str(int(value)) if abs(value - round(value)) < 1e-9 else (f"{value:.2f}".rstrip("0").rstrip("."))


def three_digits(identifier):
    number = shot_number(identifier)
    return f"{number:03d}" if number is not None else str(identifier)


def and_list(words):
    words = [word for word in words if word]
    if len(words) <= 1:
        return "".join(words)
    return ", ".join(words[:-1]) + " and " + words[-1]


def sentence(text):
    text = re.sub(r"\s+", " ", str(text or "")).strip().strip(";,")
    if not text:
        return ""
    text = text[0].upper() + text[1:]
    return text if text[-1] in ".!?\"" or text.endswith("</d>") else text + "."


def with_article(name):
    """'the flask' for a thing's name, kept as it is when it already has 'the' or an owner ("Saye's scissors")."""
    name = str(name or "").strip()
    if re.match(r"^(?:the|a|an)\s", name, re.IGNORECASE) or re.search(r"\w's\b", name):
        return name
    return f"the {name}"


def plural_noun(words):
    """True when a list of parts reads as plural ('hands', 'fist and sleeve'), False for one singular part."""
    return len(words) > 1 or (bool(words) and words[0].endswith("s"))


def lower_first(text):
    from .compile_prompts import lower_first as compile_lower_first
    return compile_lower_first(text)


def deserted(place_name):
    """'The kitchen is deserted.' or 'Saye's kitchen is deserted.' for a place's plain name."""
    if place_name.lower().startswith("the "):
        return f"The {place_name[4:]} is deserted."
    return f"{place_name[:1].upper() + place_name[1:]} is deserted."


def record_words(breakdown, identifier):
    """A record named in plain words for a page the user reads: 'Saye's kitchen (as Bare before dawn)'."""
    record = breakdown.record(identifier) if identifier else None
    if record is not None and record.type_name == "STATE":
        return f"{element_name(breakdown, element_of(identifier))} (as {record.title or 'in this state'})"
    if identifier == "STYLE":
        return "the film's style"
    return element_name(breakdown, identifier) if identifier else "a record"


def scene_number_words(scene_identifier):
    return re.sub(r"^SC0*", "", scene_identifier or "") or "0"


def trim_kept_out(fixer, text, lists):
    """(the words kept, True when the first clause was kept, [the pieces cut]) of a description with only the words
    of the named lists cut out: each comma clause holding one is cut at its first 'with', 'and', 'or', 'where' or
    'but' before the word, or goes whole when what stands before is under two words (ClipWriter.trimmed)."""
    text = straight_text(str(text or "")).strip()
    if not text or not fixer.kept_out_word(text, lists):
        return text, True, []
    sentences = [piece for piece in re.split(r"(?<=[.!?])\s+", text) if piece.strip()]
    if len(sentences) > 1:
        kept_sentences, first_kept, cut = [], True, []
        for index, piece in enumerate(sentences):
            words, first, pieces = trim_kept_out(fixer, piece, lists)
            cut += pieces
            first_kept = first_kept and (first or index > 0)
            if words:
                kept_sentences.append(words.rstrip(".") + ".")
        return " ".join(kept_sentences), first_kept, cut
    ending = text[-1] if text[-1] in ".!?" else ""
    text = text.rstrip(".!?")
    kept_clauses, first_kept, cut = [], True, []
    for clause_index, clause in enumerate(clause for clause in re.split(r"\s*;\s*", text) if clause.strip()):
        kept_pieces = []
        for piece_index, piece in enumerate(piece for piece in re.split(r",\s*", clause) if piece.strip()):
            if not fixer.kept_out_word(piece, lists):
                kept_pieces.append(piece)
                continue
            lead = []
            for part in re.split(r"\s+(?=(?:with|and|or|where|but)\s)", piece):
                if fixer.kept_out_word(part, lists):
                    break
                lead.append(part)
            standing = " ".join(lead).strip()
            if standing and len(standing.split()) >= 2:
                kept_pieces.append(standing)
                cut.append(piece[len(standing):].strip())
            else:
                cut.append(piece.strip())
                if clause_index == 0 and piece_index == 0:
                    first_kept = False
        if kept_pieces:
            kept_clauses.append(", ".join(kept_pieces))
        elif clause_index == 0:
            first_kept = False
    kept = "; ".join(kept_clauses)
    return (kept + ending if kept else ""), first_kept, cut


# ---------------------------------------------------------------- clips and their shots

@dataclass
class ClipShot:
    """One shot (or one part of a long shot) inside a clip, with where it sits in the plan shot and in the clip."""
    plan: object
    shot_start: float
    shot_end: float
    clip_start: float = 0.0
    part: int = 1
    parts: int = 1

    @property
    def length(self):
        return round(self.shot_end - self.shot_start, 3)

    @property
    def identifier(self):
        return self.plan.identifier

    @property
    def shot(self):
        return self.plan.shot


@dataclass
class RouteClip:
    """One clip of the clip book: its shots, its length on the grid, its prompt, pictures, questions and notes."""
    identifier: str
    scene: str
    number: int
    shots: list
    frames: int = 0
    keep_s: float = 0.0
    seconds_to_type: float = None
    overflow_s: float = 0.0
    contact_cuts: list = dataclass_field(default_factory=list)   # indexes of shots a contact cut leads into
    held: bool = False
    split_note: str = ""
    notes: list = dataclass_field(default_factory=list)
    problems: list = dataclass_field(default_factory=list)
    left_out: list = dataclass_field(default_factory=list)
    people: list = dataclass_field(default_factory=list)
    sections: list = dataclass_field(default_factory=list)
    prompt: str = ""
    speeches: list = dataclass_field(default_factory=list)
    connections: list = dataclass_field(default_factory=list)
    start_picture: dict = dataclass_field(default_factory=dict)
    master_picture: dict = dataclass_field(default_factory=dict)
    character_pictures: list = dataclass_field(default_factory=list)
    questions: list = dataclass_field(default_factory=list)
    check_notes: list = dataclass_field(default_factory=list)
    keys: list = dataclass_field(default_factory=list)
    key_problems: list = dataclass_field(default_factory=list)
    style_sentence: str = ""
    filler_s: float = None
    words_unknown: list = dataclass_field(default_factory=list)
    timed: list = dataclass_field(default_factory=list)
    starts_because: str = ""
    joins: list = dataclass_field(default_factory=list)
    over_cap: dict = dataclass_field(default_factory=dict)
    mirror: dict = dataclass_field(default_factory=dict)
    part_moments: list = dataclass_field(default_factory=list)
    record_left_out: list = dataclass_field(default_factory=list)
    lengthened: bool = False

    @property
    def length_s(self):
        return self.frames / 24 if self.frames else 0.0

    @property
    def tail_s(self):
        return round(self.length_s - self.keep_s, 3)

    @property
    def title(self):
        return (self.shots[0].shot.title or "").strip() or f"Shot {three_digits(self.shots[0].identifier)}"


def size_of(shot):
    return normalise_word(shot.get("size") or "")


def is_insert(shot):
    return normalise_word(shot.get("kind") or "") == "insert" or size_of(shot) == "insert"


def is_static(plan):
    return normalise_word(plan.shot.get("move") or "static") == "static" and not plan.guide_video


def people_of(plan):
    """The people seen in a shot (its CH subjects), by reference, in order."""
    return [person for person in plan.people if person.is_person]


def elements_seen(plan):
    return {person.element for person in people_of(plan)}


def setup_side(breakdown, plan):
    setup = breakdown.record(plan.shot.get("setup") or "")
    side = normalise_word(setup.get("side") or "") if setup is not None else ""
    return side if side and side not in ("none", "open") else ""


def size_steps(first, second):
    if first in SIZE_SCALE and second in SIZE_SCALE:
        return abs(SIZE_SCALE.index(first) - SIZE_SCALE.index(second))
    return None


def difference_words(first, second):
    """How shot second differs clearly from shot first, in plain words ('it is an insert', 'another angle' ...), or ''
    when it does not: two steps or more on the size scale, another angle, another setup, or second is an insert
    (Project notes 43, A3)."""
    if is_insert(second.shot):
        return "it is an insert"
    steps = size_steps(size_of(first.shot), size_of(second.shot))
    if steps is not None and steps >= 2:
        return f"{NUMBER_WORDS.get(steps, str(steps))} sizes apart"
    if normalise_word(first.shot.get("angle") or "eye_level") != normalise_word(second.shot.get("angle") or "eye_level"):
        return "another angle"
    if (first.shot.get("setup") or "") != (second.shot.get("setup") or "") or not first.shot.get("setup"):
        return "another camera place"
    return ""


def differs_clearly(first, second):
    """True when shot second differs clearly from shot first (difference_words)."""
    return bool(difference_words(first, second))


def flipped_in_edit(plan):
    """True when the shot's take is made unflipped and flipped left to right in the edit (the mirror world's routes a
    and b, 8.5): every shot of one clip must agree, because one take is flipped whole or not at all."""
    return bool(getattr(plan, "prompt_flipped_all", False))


def mirror_route_of(plan):
    mirror = getattr(plan, "mirror", None)
    return getattr(mirror, "route", "none") if mirror is not None else "none"


def is_single(plan):
    """A single: a shot that is not an insert and shows exactly one person."""
    return not is_insert(plan.shot) and len(elements_seen(plan)) == 1


def looks_at(plan):
    """The people (CH IDs) a shot's people face or look at."""
    found = set()
    for person in people_of(plan):
        for value in (str(person.faces or ""), str(person.item.get("eyeline") or "").strip()):
            target = element_of(value.upper()) if value.lower().startswith("ch-") else ""
            if target and target != person.element:
                found.add(target)
    return sorted(found)


def facing_each_other(first, second):
    """True when two singles show two people who face each other: either one faces or looks at the other."""
    one, other = next(iter(elements_seen(first))), next(iter(elements_seen(second)))
    return one != other and (other in looks_at(first) or one in looks_at(second))


def words_of_moments(shot):
    return [straight_text(split_item(written).get("shows") or "") for written in shot.get_all("moment")]


def straight_text(text):
    for curly, straight in {"“": '"', "”": '"', "‘": "'", "’": "'"}.items():
        text = text.replace(curly, straight)
    return text


def phrase_found(text, phrases):
    lowered = f" {text.casefold()} "
    found = None
    for phrase in phrases:
        index = None
        match = re.search(r"(?<![\w-])" + re.escape(phrase.casefold()) + r"(?![\w-])", lowered)
        if match:
            index = match.start()
        if index is not None and (found is None or index < found[0]):
            found = (index, phrase)
    return found


def contact_words(words):
    lists = words.get("contact_words") or {}
    return list(lists.get("cause") or []), list(lists.get("effect") or [])


def contact_in_shot(shot, words):
    """(cause, effect) when a shot's moments, in order, hold a cause word and then an effect word: a contact shown on
    screen inside one shot; else None."""
    causes, effects = contact_words(words)
    text = " ; ".join(words_of_moments(shot))
    cause = phrase_found(text, causes)
    if cause is None:
        return None
    effect = phrase_found(text[cause[0] + len(cause[1]):], effects)
    return (cause[1], effect[1]) if effect else None


def contact_pair(first, second, words):
    """True when shot first ends on a cause word and shot second opens on the result (an effect word)."""
    causes, effects = contact_words(words)
    first_moments = words_of_moments(first.shot)
    second_moments = words_of_moments(second.shot)
    if not first_moments or not second_moments:
        return False
    if contact_in_shot(first.shot, words):
        return False
    ending = first_moments[-1] + " ; " + str(first.shot.get("end") or "")
    return phrase_found(ending, causes) is not None and phrase_found(second_moments[0], effects) is not None


class Grouper:
    """Groups one scene's video shots into clips (Project notes 43, A3)."""

    def __init__(self, compiler, route):
        self.compiler = compiler
        self.breakdown = compiler.breakdown
        self.route = route
        self.words = compiler.words

    def fits(self, kept):
        return kept + self.route.tail_s_min <= self.route.longest_s + 1e-9

    def references(self, shots):
        found = []
        for clip_shot in shots:
            for person in people_of(clip_shot.plan):
                if person.reference not in found:
                    found.append(person.reference)
        return found

    def can_join(self, shots, candidate, contact=False):
        """(True, why it joins) when candidate may join the clip of these shots; else (False, why it starts a new
        clip). Both reasons are plain words for the clip page (Project notes 43, round 1 review F5)."""
        last = shots[-1]
        number, before = three_digits(candidate.identifier), three_digits(last.identifier)
        most = self.route.shots_per_clip_max
        if len(shots) >= most:
            return False, f"the clip before already holds {NUMBER_WORDS.get(most, str(most))} shots, the most a clip may hold"
        kept = sum(clip_shot.length for clip_shot in shots) + candidate.length
        if not self.fits(kept):
            return False, (f"with the clip before it would keep {plain_number(kept)} seconds, too long for one clip "
                           f"with its tail (H3 makes at most {plain_number(self.route.longest_s)} seconds)")
        if any(clip_shot.plan.held for clip_shot in shots):
            return False, f"shot {before} before it is a held take, which is always a clip of its own"
        if candidate.plan.held:
            return False, f"shot {number} is a held take, which is always a clip of its own"
        if not is_static(last.plan):
            return False, f"shot {before} before it has a moving camera, which is always a clip of its own"
        if not is_static(candidate.plan):
            return False, f"shot {number} has a moving camera, which is always a clip of its own"
        if candidate.parts > 1 or last.parts > 1:
            return False, "a part of a long shot is always a clip of its own"
        place = self.place_of(candidate.plan)
        if place != self.place_of(last.plan):
            return False, f"shot {number} is in another place"
        if flipped_in_edit(last.plan) != flipped_in_edit(candidate.plan):
            flipped = number if flipped_in_edit(candidate.plan) else before
            return False, (f"shot {flipped} is made unflipped and flipped left to right in the edit (the mirror world) "
                           "and the other is not, and one take is flipped whole or not at all")
        references = self.references(shots)
        elements = {}
        for reference in references:
            elements.setdefault(element_of(reference), reference)
        for person in people_of(candidate.plan):
            if person.element in elements and elements[person.element] != person.reference:
                return False, f"{person.name} is in another state in shot {number} (other clothes or marks)"
        # the cap counts pictures: a shot whose people are all wired already adds none, so it may always join
        new = [person.reference for person in people_of(candidate.plan) if person.reference not in references]
        total = len(set(references) | set(new))
        cap = self.route.people_pictures_max
        if new and total > cap:
            return False, (f"shot {number} would make {NUMBER_WORDS.get(total, str(total))} people's pictures in one "
                           f"clip, over the route's {NUMBER_WORDS.get(cap, str(cap))}")
        pictures = (f"{NUMBER_WORDS.get(total, str(total))} people's picture{'s' if total != 1 else ''} in all"
                    + ("" if new else ", none of them new"))
        if contact:
            return True, (f"shot {number} opens on the result of the hit that ends shot {before}, so the cut lands on "
                          f"the contact; {pictures}")
        side_last, side_next = setup_side(self.breakdown, last.plan), setup_side(self.breakdown, candidate.plan)
        if side_last and side_next and side_last != side_next:
            return False, f"the cut from shot {before} to shot {number} crosses the line"
        difference = difference_words(last, candidate)
        if not difference:
            return False, (f"shot {number} is framed too like shot {before} (the same camera place and angle, within "
                           "one size), and H3 can smooth such a cut into one move")
        if is_single(candidate.plan):
            for clip_shot in shots:
                if is_single(clip_shot.plan) and facing_each_other(clip_shot.plan, candidate.plan):
                    both = elements_seen(clip_shot.plan) | elements_seen(candidate.plan)
                    if not both <= elements_seen(shots[0].plan):
                        return False, (f"shots {three_digits(clip_shot.identifier)} and {number} are singles of two "
                                       "people facing each other, and the clip has no shot showing both first")
        return True, f"shot {number} is in the same place, clearly different from shot {before} ({difference}); {pictures}"

    def place_of(self, plan):
        scene = self.breakdown.record(scene_of(plan.identifier), "SCENE")
        return scene.get("location") if scene is not None else None

    def pieces_of(self, plan):
        """[ClipShot] for one plan shot: whole, or split at its planned cutaways (else in equal parts) when it is
        longer than the route's longest clip and not held."""
        length = plan.screen_time or 0.0
        longest = self.route.longest_kept_s
        if plan.held or length <= longest + 1e-9:
            return [ClipShot(plan, 0.0, length)], ""
        points = [point for point in cut_points(self.breakdown, plan.shot) if 0 < point < length]
        pieces, start = [], 0.0
        for point in points + [length]:
            if point - start <= longest + 1e-9:
                if pieces and pieces[-1][1] == start and point - pieces[-1][0] <= longest + 1e-9:
                    pieces[-1] = (pieces[-1][0], point)
                else:
                    pieces.append((start, point))
                start = point
        if pieces and start >= length - 1e-9:
            note = "split at its planned cutaway" + ("s" if len(pieces) > 2 else "")
        else:
            count = math.ceil(length / longest)
            share = length / count
            pieces = [(round(share * index, 3), round(share * (index + 1), 3)) for index in range(count)]
            note = ("split into equal parts because no planned cutaway fits: plan a cutaway, or join the parts in the "
                    "edit")
        count = len(pieces)
        return [ClipShot(plan, start, end, part=index + 1, parts=count) for index, (start, end) in
                enumerate(pieces)], note

    def group(self, scene_identifier, plans):
        clips, current, current_notes, joins = [], [], [], []
        contact_into = set()
        why = {"start": ""}

        def close():
            if current:
                clips.append((list(current), list(current_notes), sorted(contact_into), why["start"], list(joins)))
            current.clear()
            current_notes.clear()
            contact_into.clear()
            joins.clear()

        for plan in plans:
            if not plan.video:
                continue
            number = three_digits(plan.identifier)
            pieces, split_note = self.pieces_of(plan)
            if plan.held or len(pieces) > 1 or not is_static(plan):
                close()
                for piece in pieces:
                    current.append(piece)
                    if split_note:
                        current_notes.append(f"shot {number} is {split_note}")
                    if len(pieces) > 1:
                        why["start"] = (f"shot {number} is {plain_number(plan.screen_time)} seconds long, too long "
                                        f"for one clip with its tail, so it is made in {NUMBER_WORDS.get(len(pieces), str(len(pieces)))} "
                                        f"parts; this is part {piece.part}, a clip of its own")
                        why["after"] = f"shot {number} before it is made in parts, each a clip of its own"
                    elif plan.held:
                        why["start"] = f"shot {number} is a held take, which is always a clip of its own"
                        why["after"] = f"shot {number} before it is a held take, which is always a clip of its own"
                    else:
                        why["start"] = f"shot {number} has a moving camera, which is always a clip of its own"
                        why["after"] = f"shot {number} before it has a moving camera, which is always a clip of its own"
                    close()
                continue
            piece = pieces[0]
            if current:
                contact = contact_pair(current[-1].plan, plan, self.words)
                ok, reason = self.can_join(current, piece, contact=contact)
                if ok:
                    if contact:
                        contact_into.add(len(current))
                    current.append(piece)
                    joins.append(reason)
                    continue
                close()
                why["start"] = reason
            elif not clips:
                why["start"] = f"shot {number} is the first shot of the scene made as video"
            else:
                why["start"] = why.get("after") or "the shot before is a clip of its own"
            current.append(piece)
        close()
        result = []
        for number, (shots, notes, contacts, starts_because, joined) in enumerate(clips, start=1):
            clock = 0.0
            for clip_shot in shots:
                clip_shot.clip_start = round(clock, 3)
                clock += clip_shot.length
            clip = RouteClip(f"{scene_identifier}-CL{number:02d}", scene_identifier, number, shots,
                             contact_cuts=list(contacts), notes=list(notes),
                             held=any(clip_shot.plan.held for clip_shot in shots),
                             starts_because=starts_because, joins=list(joined))
            over = len(self.references(shots))
            if over > self.route.people_pictures_max and not (shots[0].parts > 1 and shots[0].part > 1):
                # one shot that shows more people than the cap: reported once, on its first clip (review F3)
                crowded = max(shots, key=lambda clip_shot: len(people_of(clip_shot.plan)))
                clip.over_cap = {"shot": crowded.identifier, "pictures": over, "cap": self.route.people_pictures_max}
            kept = round(clock, 3)
            frames, fits = frames_for(kept, self.route)
            if not fits:
                kept_fit = math.floor(self.route.longest_kept_s * 100 + 1e-6) / 100
                clip.overflow_s = round(kept - kept_fit, 2)
                kept = kept_fit
            clip.frames = frames
            clip.keep_s = math.floor(kept * 100 + 1e-6) / 100  # never rounded up into the tail
            clip.seconds_to_type = duration_to_type(frames, self.route.fps, self.route.block, self.route.offset)
            result.append(clip)
        return result


# ---------------------------------------------------------------- the words of one clip

@dataclass
class Event:
    at: float
    order: int
    text: str


class ClipWriter:
    """Writes one clip's six sections from the records, its start picture brief, connections and questions."""

    def __init__(self, compiler, route, master_pictures):
        self.compiler = compiler
        self.breakdown = compiler.breakdown
        self.adapters = compiler.adapters
        self.fixer = compiler.fixer
        self.writer = compiler.writer
        self.route = route
        self.masters = master_pictures
        project = compiler.project
        self.language = ((project.get("language") if project is not None else None) or "english").capitalize()
        # 'stays', 'remains': a held hand or a held look written as staying freezes like 'still' does (review F10, J);
        # the route's gate leaves such clauses out, from the not_an_action words of stillness_words
        held = (compiler.words.get("stillness_words") or {}).get("not_an_action") or []
        self.fixer.word_lists.setdefault("held", [word for word in held if word in HELD_WORDS])

    # -- words
    def gate(self, text, clip, where, record_level=False):
        """A record's words with the word swaps made, negations rewritten, and every clause H3 would show or say left
        out (listed on the clip page with where it came from). A record-level piece (the place's state line, its set
        objects, the room sound) is the same in every clip of the scene, so it is listed once, at the top of the
        scene's page (review F4)."""
        notes = clip.record_left_out if record_level else clip.left_out
        text = self.fixer.rewrite_negations(self.fixer.swap_words(straight_text(str(text or ""))))
        text = text.replace("words added later", "lettering added later")
        # only the words H3 would show or say are cut: 'looks up and speaks' keeps 'looks up' (review F10)
        text, _, dropped = trim_kept_out(self.fixer, text, KEPT_OUT_LISTS + ("held",))
        for piece in dropped:
            note = f"{LEFT_OUT_WHY}: '{piece}' ({where}). Write what happens instead."
            if note not in notes:
                notes.append(note)
        sink = []
        text = self.fixer.fix(text, sink, where)
        for entry in sink:
            note = f"{LEFT_OUT_WHY}: {entry}"
            if note not in notes:
                notes.append(note)
        return text.strip()

    def key(self, text):
        """A pasted key (fixed description, state line): the word swaps only, never reworded or cut."""
        return self.fixer.key_words(str(text or "").strip())

    def renamed(self, text, cast, plan):
        from .compile_prompts import RECORD_ID, swap_image_sides
        text = straight_text(str(text or ""))
        text = cast.rename(text)
        if plan.prompt_flipped_all:
            text = swap_image_sides(text)
        return RECORD_ID.sub(lambda match: cast.label(match.group(0)) if match.group(0).startswith("CH-")
                             else lower_first(element_name(self.breakdown, match.group(0))), text)

    def person_tag(self, person):
        """A short tag made from the person's noun and the first clothing phrase of their state line ("the woman in
        the faded mid-blue work shirt"), the same in every clip for one state."""
        noun = person.noun if person.noun not in ("thing", "") else "person"
        state = str(person.state_line or "")
        phrase = re.split(r"[;,]", state)[0].strip() if state else ""
        phrase = re.split(r"\s+(?:with|over|under|and a|hanging|soaked|buttoned)\s+", phrase)[0].strip()
        tag = f"the {noun}"
        if phrase:
            rest = re.sub(r"^(?:a|an|the|his|her|their)\s+", "", phrase, flags=re.IGNORECASE)
            clothing = any(re.search(rf"\b{re.escape(word)}\b", rest.casefold()) for word in CLOTHING_NOUNS)
            if clothing:
                tag = f"the {noun} in the {rest}" if rest != phrase else f"the {noun} in {rest}"
            elif re.match(r"^(?:a|an)\s", phrase, flags=re.IGNORECASE):
                tag = f"the {noun} with {phrase}"
            # anything else ('bare chest') reads badly after 'with': the noun alone (review F17)
        if self.fixer.kept_out_word(tag, KEPT_OUT_LISTS) or len(tag.split()) > 12:
            tag = f"the {noun}"
        return self.fixer.swap_words(tag)

    def voice_words(self, speaker):
        """The speaker's voice description as its clauses that hold no word H3 would show or say and describe a sound
        (pitch, accent, pace), joined the same way every time, so a voice reads the same in every clip. A long clause
        or one tied to a time tells the character's story and is left out (review F17)."""
        text = self.fixer.swap_words(self.writer.voice_description(speaker))
        clauses = [piece.strip().rstrip(".") for part in re.split(r"[;.]", text) for piece in part.split(",")]
        kept = [clause for clause in clauses if clause and not self.fixer.kept_out_word(clause, KEPT_OUT_LISTS)
                and not self.fixer.negation_left(clause) and len(clause.split()) <= VOICE_CLAUSE_WORDS_MAX
                and not VOICE_STORY_WORDS.search(clause)]
        kept = [re.sub(r"^(?:and|but|or)\s+", "", clause) for clause in kept]
        return lower_first(", ".join(clause for clause in kept if clause))

    # -- the mirror world (8.5), through compile_prompts' own rules
    def picture_turned(self, plan, reference):
        """True when the picture of this element wired to H3 is a copy flipped left to right. H3 makes the take as the
        finished film shows it on every route but a and b (which flip the take in the edit), so on the plate route a
        mirrored person's wired picture is flipped as on the direct route (J: H3 draws the later shots of a clip from
        the wired pictures, with no plate picture); compile_prompts.reference_turned decides the rest."""
        from .compile_prompts import reference_turned
        from .derive_fields import MirrorRoute
        if mirror_route_of(plan) == "plate":
            plan = dataclass_replace(plan, mirror=MirrorRoute("direct", "e", plan.mirror.text_graphic, []))
        try:
            return bool(reference_turned(self.compiler, plan, reference))
        except Exception:  # the mirror states need the eras and set plans; a gap there must not stop the clip book
            return False

    def master_turned(self, plan, place_identifier):
        """True when the clip's start picture is made from the master picture flipped left to right: on routes a and b
        the take is made before the flip, and on the plate route the plate is (compile_prompts.reference_turned)."""
        from .compile_prompts import reference_turned
        from .derive_fields import MirrorRoute
        if not place_identifier:
            return False
        if mirror_route_of(plan) == "plate":
            plan = dataclass_replace(plan, mirror=MirrorRoute("flip_all", "a", plan.mirror.text_graphic, []))
        try:
            return bool(reference_turned(self.compiler, plan, place_identifier))
        except Exception:
            return False

    def sides_turned(self, plan, person, for_picture=False):
        """True when the picture described shows this person reversed from their own words, so their left and right
        are turned in the words (compile_prompts.shows_pre_reversed; B1 method 1)."""
        from .compile_prompts import shows_pre_reversed
        turned = flipped_in_edit(plan) or (for_picture and mirror_route_of(plan) == "plate" and person.flipped)
        return bool(shows_pre_reversed(self.breakdown, plan.shot, person.element, turned))

    def person_keys(self, person, clip, plan=None, for_picture=False):
        """(fixed description, state line, {kind: the stored words}) of a person as the picture described shows them:
        the word swaps only, and left and right turned when the picture shows them reversed (never reworded)."""
        fixed, state = self.key(person.fixed_description), self.key(person.state_line)
        sources = {"fixed description": fixed, "state line": state}
        if plan is None:
            turned = person.element in (clip.mirror or {}).get("sides_turned", [])
        else:
            turned = self.sides_turned(plan, person, for_picture)
        if turned:
            from .compile_prompts import swap_own_sides
            fixed, state = swap_own_sides(fixed), swap_own_sides(state)
        return fixed, state, sources

    def mirror_of(self, clip, people, place_record):
        """The clip's mirror world: the shots' routes, whether the take is flipped in the edit, whose wired pictures
        are flipped and whose own sides are turned in the words, the master picture's flip, and the parts the route
        cannot make safely, in plain words (review F2)."""
        routes = [mirror_route_of(clip_shot.plan) for clip_shot in clip.shots]
        first = clip.shots[0].plan
        found = {"routes": routes, "flip_in_edit": flipped_in_edit(first), "plate": routes[0] == "plate",
                 "open": "open" in routes, "pictures_turned": [], "sides_turned": [], "problems": [],
                 "master_turned": self.master_turned(first, place_record.identifier if place_record is not None else "")}
        for person in people:
            plans = [clip_shot.plan for clip_shot in clip.shots if person.element in elements_seen(clip_shot.plan)]
            pictures = {self.picture_turned(plan, person.reference) for plan in plans}
            sides = {self.sides_turned(plan, person) for plan in plans}
            if True in pictures:
                found["pictures_turned"].append(person.element)
            if True in sides:
                found["sides_turned"].append(person.element)
            if len(pictures) > 1 or len(sides) > 1:
                found["problems"].append(
                    f"{person.name} is mirrored in some shots of this clip and shown as normal in others, and one wired "
                    "picture and one description cannot be both. Give those shots clips of their own.")
        for clip_shot, route in zip(clip.shots[1:], routes[1:]):
            if route == "plate":
                found["problems"].append(
                    f"shot {three_digits(clip_shot.identifier)} is in the mirror world on the plate route (its mirrored "
                    "people are made in one picture, flipped), but it is a later shot of this clip, so it has no picture "
                    "of its own: H3 draws its mirrored people from their flipped pictures and the words alone, which is "
                    "untested. Check the sides with the questions below, or give the shot a clip of its own.")
        return found

    def lengthen_for_late_lines(self, clip):
        """A line that ends less than a second before the keep point may fall into the tail: H3 starts lines up to
        about two seconds late (testers' notes). The clip is made one step longer on the grid when that still fits,
        so the late line is finished before H3 breaks up; the keep point stays where the plan cuts (review F18, J)."""
        late = [speech for speech in clip.speeches if clip.keep_s - speech.get("ends_s", 0.0) < LINE_END_MARGIN_S - 1e-6]
        if not late:
            return
        longer = clip.frames + self.route.block
        if clip.overflow_s <= 0 and longer <= self.route.max_frames:
            clip.frames = longer
            clip.seconds_to_type = duration_to_type(longer, self.route.fps, self.route.block, self.route.offset)
            clip.lengthened = True
        words = and_list([f'"{speech["line"]}"' for speech in late])
        clip.notes.append(
            f"the line{'s' if len(late) > 1 else ''} {words} end{'s' if len(late) == 1 else ''} less than a second "
            f"before the keep point ({plain_number(clip.keep_s)} seconds), and H3 often starts lines late"
            + (": the clip is made one step longer so the line still finishes before H3 breaks up; keep by what you "
               "see" if clip.lengthened else ": keep by what you see, or move the line earlier in the shot"))

    # -- one clip
    def write(self, clip):
        breakdown = self.breakdown
        first_plan = clip.shots[0].plan
        people = []
        for clip_shot in clip.shots:
            for person in people_of(clip_shot.plan):
                if person.element not in [known.element for known in people]:
                    people.append(person)
        clip.people = people
        from .compile_prompts import Cast
        cast = Cast(breakdown, self.adapters, dataclass_replace(first_plan, people=list(people)), motion_only=False)
        for person in people:
            person.label = person.name
        subject_of = {person.element: f"<Subject {index + 2}>" for index, person in enumerate(people)}
        picture_of = {person.element: f"<Picture {index + 2}>" for index, person in enumerate(people)}
        tags = {person.element: self.person_tag(person) for person in people}
        in_start = {person.element for person in people_of(first_plan)}
        place_record, place_state = self.place(first_plan)
        place_name = lower_first(place_record.title) if place_record is not None and place_record.title else "the place"
        master = self.masters.get(place_record.identifier if place_record is not None else "", {})
        clip.master_picture = dict(master)
        # the mirror world: which pictures are wired flipped, whose own sides are turned in the words, whether the take
        # is flipped in the edit, and what the route cannot make safely (8.5; review F2)
        clip.mirror = self.mirror_of(clip, people, place_record)
        if clip.mirror.get("master_turned") and master.get("file"):
            from .compile_prompts import turned_file
            clip.master_picture["flipped_file"] = turned_file(master["file"])
        # subject_definitions
        clip.keys, clip.key_problems = [], []
        definitions = [self.place_definition(clip, place_record, place_state, place_name)]
        for person in people:
            fixed, state, sources = self.person_keys(person, clip)
            # a key that is 'none' or empty is left out, never joined as '; ...' (review F17)
            if fixed:
                description = fixed.rstrip(".") + (f"; {state.rstrip('.')}" if state else "")
            else:
                description = person.name + (f": {state.rstrip('.')}" if state else "")
            for kind, text, record in (("fixed description", fixed, person.element), ("state line", state, person.reference)):
                if text:
                    key = {"record": record, "what": kind, "text": text}
                    if sources[kind] != text:
                        # the picture H3 makes shows this person reversed from their own words: left and right are
                        # turned, the one change the old compiler makes too (B1 method 1; GEN-04)
                        key.update({"source": sources[kind], "sides_turned": True})
                    clip.keys.append(key)
                    found = self.fixer.kept_out_word(text, KEPT_OUT_LISTS)
                    if found:
                        clip.key_problems.append({"record": record, "what": kind, "word": found,
                                                  "record_words": record_words(breakdown, record)})
            subject_word, _, possessive = person.pronoun
            verb = "are" if subject_word.lower() == "they" else "is"
            line = f"{subject_of[person.element]} is {description}. {possessive} face, hair and build come from " \
                   f"{picture_of[person.element]}"
            if person.element in in_start:
                line += f", and {subject_word} {verb} {tags[person.element]} in <Picture 1>"
            definitions.append(line + ".")
        definitions.append(PICTURE_ONE if people else PICTURE_ONE_EMPTY)
        # summary
        shot_count = len(clip.shots)
        entries = []
        for clip_shot in clip.shots:
            from .compile_prompts import list_item_line
            line = list_item_line(breakdown, clip_shot.identifier) or clip_shot.shot.title or ""
            # a quoted line belongs inside <d> ... </d> in the shot, never in the summary
            line = re.sub(r"\s*;\s*;", ";", QUOTED_IN_LINE.sub("", straight_text(line))).strip(" ;,:")
            words = self.gate(self.renamed(line, cast, clip_shot.plan), clip,
                              f"shot {three_digits(clip_shot.identifier)}, its line in the shot list")
            if words:
                entries.append(lower_first(words).rstrip("."))
        who = ""
        if people:
            who = ", with " + and_list([f"{subject_of[person.element]} ({person.name})" for person in people])
        summary = f"[reference generation] In <Subject 1>, {place_name}{who}: " + "; then ".join(entries or ["the shot plays"]) + "."
        sizes = [SIZE_WORDS.get(size_of(clip_shot.shot), size_of(clip_shot.shot).replace("_", " ") or "shot")
                 for clip_shot in clip.shots]
        if shot_count == 1:
            summary += f" One continuous {sizes[0]}."
        else:
            summary += f" {NUMBER_WORDS[shot_count].capitalize()} shots: a {', then a '.join(sizes)}."
        summary += " <Picture 1> plans the first shot"
        for person in people:
            summary += f"; {picture_of[person.element]} gives {person.name}'s face and build"
        summary += "."
        # retention_analysis
        all_shots = ", ".join(f"[Shot {index}]" for index in range(1, shot_count + 1))
        keeps = self.place_keeps(place_record, place_name)
        retention = [f"<Subject 1> (appears in {all_shots}): fully_preserved - {keeps} are kept as defined."]
        for person in people:
            seen = [index for index, clip_shot in enumerate(clip.shots, start=1)
                    if person.element in elements_seen(clip_shot.plan)]
            line = (f"{subject_of[person.element]} (appears in {', '.join(f'[Shot {index}]' for index in seen)}): "
                    f"partially_preserved - {person.name}'s face, hair and build from {picture_of[person.element]} are "
                    f"kept exactly; {person.pronoun[1]} clothes are as described above")
            if person.element in in_start:
                line += " and as worn in <Picture 1>"
            retention.append(line + ".")
        picture_line = ("<Picture 1> ([Shot 1] shot-planning reference): fully_preserved - [Shot 1] opens on the camera "
                        "position, shot size, set, props, light")
        picture_line += (" and placement of <Picture 1>, and the people move on from their places in it from the first "
                         "frame." if people else " of <Picture 1>.")
        retention.append(picture_line)
        # detailed_description
        description = self.detailed_description(clip, cast, people, subject_of, tags, place_name)
        # overall_soundscape
        soundscape = self.soundscape(clip, cast)
        clip.sections = [
            ("subject_definitions", definitions),
            ("summary", [summary]),
            ("retention_analysis", retention),
            ("detailed_description", description),
            ("overall_soundscape", [soundscape]),
            ("non_diegetic_music", [self.route.facts.get("music") or "N/A"]),
        ]
        clip.prompt = "\n\n".join(name + ":\n" + "\n".join(lines) for name, lines in clip.sections)
        # pictures, connections, questions
        clip.character_pictures = []
        clip.connections = [{"input": "ref_image_0", "picture": "the start picture you made for this clip",
                             "file": self.start_picture_file(clip), "label": "<Picture 1>"}]
        for index, person in enumerate(people, start=1):
            from .compile_prompts import state_words_of, turned_file
            file_name = f"Reference pictures/{person.name}{state_words_of(person.reference)}.png"
            flipped = person.element in clip.mirror.get("pictures_turned", [])
            wired = turned_file(file_name) if flipped else file_name
            entry = {"person": person.element, "state": person.reference, "name": person.name, "file": wired}
            if flipped:
                entry.update({"flipped": True, "unflipped_file": file_name})
            clip.character_pictures.append(entry)
            clip.connections.append({"input": f"ref_image_{index}",
                                     "picture": f"your {person.name} picture" + (", flipped left to right" if flipped else ""),
                                     "file": wired, "label": f"<Picture {index + 1}>"})
        clip.start_picture = self.start_picture(clip, cast, place_record, place_name, tags)
        clip.questions, clip.check_notes = self.questions(clip, people)
        self.lengthen_for_late_lines(clip)
        for clip_shot in clip.shots:
            found = contact_in_shot(clip_shot.shot, self.compiler.words)
            if found:
                clip.problems.append(
                    f"shot {three_digits(clip_shot.identifier)} shows a contact inside one shot ('{found[0]}', then "
                    f"'{found[1]}'): H3 cannot reliably make one thing break or push another at the moment of "
                    "contact. End the shot at the contact and start the next shot with the result already there.")
        for index in clip.contact_cuts:
            clip.notes.append(f"contact cut into shot {three_digits(clip.shots[index].identifier)}: the sound of the hit "
                              "goes on the cut")
        if clip.overflow_s > 0:
            total = sum(clip_shot.length for clip_shot in clip.shots)
            clip.problems.append(
                f"shot {three_digits(clip.shots[0].identifier)} is a held take of {plain_number(total)} seconds; with "
                f"its tail that is longer than H3's longest clip ({plain_number(self.route.longest_s)} seconds), so "
                f"{plain_number(clip.keep_s)} seconds of the plan's hold fit. Make the other "
                f"{plain_number(clip.overflow_s)} seconds in the edit, or redesign the shot with a motivated cut.")
        return clip

    def place(self, plan):
        scene = self.breakdown.record(scene_of(plan.identifier), "SCENE")
        location = self.breakdown.record(scene.get("location"), "LOCATION") if scene is not None and scene.get("location") else None
        from .compile_prompts import location_state
        return location, location_state(self.breakdown, plan.shot)

    def objects_of(self, place_record):
        return objects_of(place_record)

    def place_definition(self, clip, place_record, place_state, place_name):
        """<Subject 1>: the place shown in <Picture 1>, its state line and its set objects. The place's state line
        goes through the gate as its set objects and the room sound do: a clause naming something absent is left out
        and listed once on the scene's page. Only people's keys are kept whole, because rewording those re-rolls a
        face; the place's look comes from the start picture (review F4)."""
        source = straight_text(self.key(place_state.get("state_line"))) if place_state is not None else ""
        if source.lower() == "none":
            source = ""
        state_line = ""
        if source:
            record = place_state.identifier
            where = f"the state line of {record_words(self.breakdown, record)}"
            state_line = self.gate(self.trimmed(source, clip, where)[0], clip, where, record_level=True)
            if state_line:
                key = {"record": record, "what": "state line", "text": state_line}
                if state_line != source:
                    key.update({"source": source, "gated": True})
                clip.keys.append(key)
        objects = []
        for name, material in self.objects_of(place_record):
            words = self.gate(f"the {name}, {material}", clip, f"the set object {name}", record_level=True)
            if words and len(words.split()) > 1:
                objects.append(words.rstrip("."))
        text = f"<Subject 1> is {place_name} shown in <Picture 1>"
        if state_line:
            text += f": {state_line.rstrip('.')}"
        if objects:
            text += "; in it " + "; ".join(objects)
        return text + "."

    def place_keeps(self, place_record, place_name):
        names = [f"the {name}" for name, _ in self.objects_of(place_record)][:6]
        return and_list([f"{place_name}'s walls, floor and light"] + names) if names else f"{place_name} and its set"

    def camera(self, clip_shot, cast, clip):
        """(the camera's first sentence, the move sentence) of one shot, through compile's own camera words."""
        from .compile_prompts import Clip, ClipPiece, Routing
        for person in clip_shot.plan.people:
            # every shot's own people carry their names, so the camera never reads "at 's eye height" (review F17)
            if person.is_person and not person.label:
                person.label = person.name
        fake = Clip(clip_shot.identifier + ".1", clip_shot.identifier, clip.scene, self.route.name,
                    ClipPiece(clip_shot.identifier + ".1", 1, 1, clip_shot.shot_start, clip_shot.shot_end,
                              clip_shot.length, "", "", "", True), clip_shot.plan, Routing(""))
        first, move = self.writer.camera_words(fake, cast, False)
        first = self.gate(first, clip, f"shot {three_digits(clip_shot.identifier)}, its camera")
        if is_static(clip_shot.plan):
            move = ""  # a static clip has one camera sentence, written once for the whole clip
        elif move:
            move = self.gate(move, clip, f"shot {three_digits(clip_shot.identifier)}, its camera move")
        return first, move

    def placement(self, person, cast, plan, facing_too=True):
        """'on the left third of the frame, facing Saye' for a person in a shot, or ''. Sides are swapped only when
        the whole take is flipped in the edit (routes a and b), as the old compiler does for a video prompt: on the
        plate route the clip starts from the finished picture, so nobody is turned in it (8.5; review F2)."""
        phrase = self.adapters.phrase
        place = person.at
        turned = flipped_in_edit(plan)
        if turned and place:
            place = {"left_third": "right_third", "right_third": "left_third", "left_edge": "right_edge",
                     "right_edge": "left_edge"}.get(place, place)
        where = phrase("placement", place, default="") if place else ""
        if not facing_too:
            return where
        faces = str(person.faces or "")
        if turned:
            faces = {"frame_left": "frame_right", "frame_right": "frame_left"}.get(faces, faces)
        if re.match(r"^(CH|PR|LOC)-", faces):
            target = cast.label(faces) if faces.startswith("CH-") else lower_first(element_name(self.breakdown, element_of(faces)))
            facing = phrase("facing", "person", default="facing {name}").replace("{name}", target)
        else:
            facing = phrase("facing", faces, default="") if faces else ""
        return ", ".join(part for part in (where, facing) if part)

    def moments(self, clip_shot, cast, clip, until):
        """[(clip seconds, end seconds, words)] of a shot's moments inside its part of the shot and before until."""
        from .compile_prompts import CUTAWAY_WORDS, without_quoted_speech, parse_span
        plan = clip_shot.plan
        spoken = []
        for _, _, entry in plan.on_screen + plan.off_screen:
            line = re.sub(r"\s*\([^)]*\)\s*", " ", straight_text(str(entry.get("text") or ""))).strip()
            if line:
                spoken.append(line)
        found = []
        for written in plan.shot.get_all("moment"):
            item = split_item(written)
            span = parse_span(item.first)
            if span is None:
                continue
            start, end = max(span[0], clip_shot.shot_start), min(span[1], clip_shot.shot_end)
            if end <= start + 1e-9:
                continue
            at = round(clip_shot.clip_start + start - clip_shot.shot_start, 3)
            stop = round(clip_shot.clip_start + end - clip_shot.shot_start, 3)
            if at >= until - 1e-9:
                continue
            shows = straight_text(item.get("shows") or "")
            for line in spoken:
                shows = re.sub(r'(?<!\w)"?' + re.escape(line) + r'"?(?!\w)', "", shows)
            shows = without_quoted_speech(shows, spoken)
            shows = re.sub(r"\s*\b(?:and|then)\s*$", "", CUTAWAY_WORDS.sub(" ", shows).strip())
            shows = re.sub(r"\s*;\s*;", ";", re.sub(r"\s+([;,.])", r"\1", shows)).strip(" ;,")
            if clip_shot.parts > 1 and (span[0] < clip_shot.shot_start - 1e-6 or span[1] > clip_shot.shot_end + 1e-6):
                shows = self.share_of_moment(shows, span, clip_shot, clip)
            where = (f"shot {three_digits(plan.identifier)}, the moment from {plain_number(span[0])} to "
                     f"{plain_number(span[1])} seconds")
            words = self.gate(self.renamed(shows, cast, plan), clip, where)
            if not words:
                continue
            first_word = re.sub(r"[^a-z]", "", words.split()[0].lower()) if words.split() else ""
            focus = next(iter(people_of(plan)), None)
            if (focus is not None and first_word.endswith("s") and not first_word.endswith("ss")
                    and first_word not in ("his", "hers", "its", "this", "thus", "as", "is", "was", "whose")
                    and not words[:1].isupper()):
                words = f"{focus.name} {words}"
            found.append((at, min(stop, until), words))
        return found

    def share_of_moment(self, shows, span, clip_shot, clip):
        """The part of a moment that falls inside this part of a long shot: its actions (split at semicolons, commas
        and 'then') spread evenly over the moment's seconds, and each part keeps the actions that start inside it, so
        no part performs the whole moment again. A moment of one action goes on in every part. The moment is listed,
        so the page and the route check can ask for it to be split at the part's boundary (review F7)."""
        clauses = [piece.strip() for part in re.split(r"\s*;\s*", shows)
                   for piece in re.split(r",\s*(?:then\s+)?|\s+then\s+", part) if piece.strip()]
        boundary = clip_shot.shot_start if span[0] < clip_shot.shot_start - 1e-6 else clip_shot.shot_end
        entry = {"shot": clip_shot.identifier, "moment": f"{plain_number(span[0])}-{plain_number(span[1])}",
                 "boundary_s": round(boundary, 3), "part": clip_shot.part}
        if entry not in clip.part_moments:
            clip.part_moments.append(entry)
        if len(clauses) < 2:
            return shows
        share = (span[1] - span[0]) / len(clauses)
        kept = [clause for index, clause in enumerate(clauses)
                if clip_shot.shot_start - 1e-6 <= span[0] + index * share < clip_shot.shot_end - 1e-6]
        return "; ".join(kept)

    def line_times(self, plan):
        """{speech ID: seconds into the shot} for every line the shot hears. A line's own `at` first; an on-screen
        line without one takes a speaking moment of its own (the moment that holds its words, else the next moment
        that speaks, in the order the shot lists its lines: never the moment an earlier line took); the others follow
        the order the shot lists them in, each after the line before it (its words at its speaker's pace, and a short
        gap) or just before the next line whose time is known. No line without a time of its own starts before the
        line before it has ended (review F1)."""
        from .compile_prompts import heard_line, parse_span
        heard = []
        for written in plan.shot.get_all("hear"):
            item = split_item(written)
            identifier = (item.first or "").strip()
            entry = next((entry for speech, _, entry in plan.on_screen + plan.off_screen if speech == identifier), None)
            if identifier and entry is not None:
                heard.append((identifier, item, entry))
        moments = []
        for written in plan.shot.get_all("moment"):
            moment = split_item(written)
            span = parse_span(moment.first)
            if span:
                moments.append((span, straight_text(moment.get("shows") or "").lower()))
        times, fixed, used = {}, set(), set()
        for identifier, item, entry in heard:
            at = number_of(item.get("at"))
            if at is not None:
                fixed.add(identifier)
            elif normalise_word(item.get("speaker") or "") == "on_screen":
                line = straight_text(heard_line(item, entry)).lower()
                chosen = next((index for index, (span, words) in enumerate(moments)
                               if index not in used and line and line[:12] in words), None)
                if chosen is None:
                    after = max([moments[index][0][0] for index in used], default=-1.0)
                    chosen = next((index for index, (span, words) in enumerate(moments)
                                   if index not in used and span[0] > after and SPEAKING_MOMENT.search(words)), None)
                if chosen is not None:
                    used.add(chosen)
                    at = moments[chosen][0][0]
            if at is not None:
                times[identifier] = at

        def length_of(identifier, item, entry):
            return self.line_length(item, entry)

        clock = 0.3
        for index, (identifier, item, entry) in enumerate(heard):
            if identifier in times:
                if identifier not in fixed and index and times[identifier] < clock - 1e-6:
                    # its speaking moment starts before the line before has ended: the line waits for it
                    times[identifier] = round(clock, 2)
                clock = times[identifier] + length_of(identifier, item, entry)
                continue
            later = next((times[other] for other, _, _ in heard[index + 1:] if other in times), None)
            moment = clock
            if later is not None:
                moment = max(clock, later - length_of(identifier, item, entry) - LINE_GAP_S)
            times[identifier] = round(moment, 2)
            clock = moment + length_of(identifier, item, entry)
        return times

    def line_length(self, item, entry):
        """Seconds a line takes: its words at its speaker's pace, and a short breath."""
        from .compile_prompts import heard_line
        words = len(heard_line(item, entry).split())
        pace = self.breakdown.pace_of(entry.get("speaker") or "") or 2.5
        return words / pace + 0.3

    def speeches_of(self, clip_shot, clip, until):
        """[(clip seconds, identifier, item, entry, on screen)] of the lines heard in this part of the shot."""
        plan = clip_shot.plan
        found = []
        times = self.line_times(plan)
        for identifier, item, entry in list(plan.on_screen) + list(plan.off_screen):
            at = times.get(identifier)
            if at is None or not (clip_shot.shot_start - 1e-9 <= at < clip_shot.shot_end - 1e-9):
                continue
            moment = round(clip_shot.clip_start + at - clip_shot.shot_start, 3)
            if moment >= until - 1e-9:
                from .compile_prompts import heard_line
                words = heard_line(item, entry) or "a line"
                note = f'the line "{words}" falls after the part kept, so it is laid in during the edit'
                if note not in clip.notes:
                    clip.notes.append(note)
                continue
            on_screen = normalise_word(item.get("speaker") or "") == "on_screen"
            found.append((moment, identifier, item, entry, on_screen))
        return sorted(found, key=lambda entry: entry[0])

    def detailed_description(self, clip, cast, people, subject_of, tags, place_name):
        breakdown = self.breakdown
        shot_count = len(clip.shots)
        until = clip.keep_s
        # the style sentence
        style = breakdown.singleton("STYLE")
        style_words = str(style.get("style_words") or "").strip() if style is not None else ""
        clip.style_sentence = (f"The target video is photographic live action in this look: {style_words.rstrip('.')}."
                               if style_words else "The target video is photographic live action.")
        found = self.fixer.kept_out_word(style_words, KEPT_OUT_LISTS)
        if found:
            clip.key_problems.append({"record": "STYLE", "what": "style words", "word": found,
                                      "record_words": "the film's style"})
        # how many shots, and when they cut
        if shot_count == 1:
            contract = "This clip is one single continuous shot from start to finish."
        else:
            cuts = [mm_ss_ms(clip_shot.clip_start) for clip_shot in clip.shots[1:]]
            cut_words = f"one cut at {cuts[0]}" if len(cuts) == 1 else "cuts at " + and_list(cuts)
            contract = (f"This clip has exactly {NUMBER_WORDS[shot_count]} shots, with {cut_words}; the shots play once "
                        f"each, in this order, and the clip ends on [Shot {shot_count}].")
        # the camera, in one sentence
        cameras = [self.camera(clip_shot, cast, clip) for clip_shot in clip.shots]
        moving = [move for (first, move), clip_shot in zip(cameras, clip.shots) if not is_static(clip_shot.plan) and move]
        if moving:
            camera_sentence = sentence(moving[0])
        else:
            camera_sentence = f"{SHOTS_OPENING.get(shot_count, 'Every shot is')} " \
                              f"{self.route.facts.get('camera_static') or 'static, on a tripod, with no camera movement whatsoever'}."
        # who is in it
        names = [person.name for person in people]
        off_screen = any(not on for clip_shot in clip.shots for _, _, _, _, on in self.speeches_of(clip_shot, clip, until))
        if not names:
            who = f"The clip shows {place_name}; the people are out of the picture."
        elif len(names) == 1:
            who = f"{names[0]} is the only person in the picture in this clip."
        else:
            who = f"Exactly {NUMBER_WORDS.get(len(names), str(len(names)))} people appear in this clip: {and_list(names)}."
        if off_screen:
            who = who.rstrip(".") + "; a voice also comes from off screen."
        # each person is alive, with blinks never in the tail
        alive = [self.alive_sentence(clip, people, until)] if people else []
        opening = " ".join([clip.style_sentence, contract, camera_sentence, who] + alive)
        lines = [opening]
        speaker_numbers = {}
        mentioned_things = set()
        for index, clip_shot in enumerate(clip.shots):
            plan = clip_shot.plan
            first, _ = cameras[index]
            first = first.rstrip(".")
            if index == 0:
                parts = [f"[Shot 1] {first}; the camera position, shot size, set, props and light are exactly as in "
                         "<Picture 1>."]
                look = self.look_block(plan)
                if look:
                    parts.append(look if look.endswith(".") else look + ".")
                    from .compile_prompts import look_of
                    record = look_of(breakdown, plan.shot)
                    clip.keys.append({"record": record.identifier, "what": "look block", "text": look})
                    found = self.fixer.kept_out_word(look, KEPT_OUT_LISTS)
                    if found:
                        clip.key_problems.append({"record": record.identifier, "what": "look block", "word": found,
                                                  "record_words": f"the look {record.title or ''}".strip()})
            else:
                article = "an" if first[:1].lower() in "aeiou" else "a"
                parts = [f"[Shot {index + 1}] At {mm_ss_ms(clip_shot.clip_start)}, the camera cuts to {article} "
                         f"{first[:1].lower() + first[1:]}."]
                if index in clip.contact_cuts:
                    parts.append("The result of the hit is already there from the first frame of this shot.")
            for person in people_of(plan):
                lead = f"{subject_of[person.element]}, {person.name}, {tags[person.element]},"
                if is_insert(plan.shot):
                    # an insert shows only part of a person: say which part, and that the face is out of the frame
                    where = self.placement(person, cast, plan, facing_too=False)
                    seen = and_list(self.visible_parts(person, plan))
                    parts.append(sentence(f"{lead} is in the shot only as {person.pronoun[1]} {seen}"
                                          + (f", {where}" if where else "")
                                          + f"; {person.pronoun[1]} face is outside the frame"))
                    continue
                where = self.placement(person, cast, plan)
                parts.append(sentence(f"{lead} is {where}" if where else f"{lead} is in the shot"))
            for written in plan.shot.get_all("thing"):
                text = self.thing_words(written, plan, cast, clip, mentioned_things)
                if text:
                    parts.append(text)
            if any(not str(split_item(value).first or "").strip() in ("", "none") for value in split_list(plan.shot.get("text") or "")):
                parts.append("Every surface with printed words is plain, with lettering added later.")
            events = []
            for at, stop, words in self.moments(clip_shot, cast, clip, until):
                if abs(at - clip_shot.clip_start) < 1e-6:
                    if index == 0:
                        text = f"For the first {plain_number(stop - at)} seconds, {lower_first(words).rstrip('.')}."
                    else:
                        text = sentence(words)
                else:
                    text = f"At about {mm_ss_ms(at)}, {lower_first(words).rstrip('.')}."
                    clip.timed.append(at)
                events.append(Event(at, 0, text))
            for at, identifier, item, entry, on_screen in self.speeches_of(clip_shot, clip, until):
                text = self.speech_words(clip, cast, plan, identifier, item, entry, on_screen, speaker_numbers,
                                         subject_of, at)
                if text:
                    if abs(at - clip_shot.clip_start) > 1e-6:
                        clip.timed.append(at)
                    events.append(Event(at, 1, text))
            events.sort(key=lambda event: (event.at, event.order))
            parts += [event.text for event in events]
            end = plan.shot.get("end")
            last = index == len(clip.shots) - 1
            if end and str(end).strip().lower() != "none" and clip.overflow_s <= 0 and clip_shot.part == clip_shot.parts:
                words = self.gate(self.renamed(end, cast, plan), clip, f"shot {three_digits(plan.identifier)}, its end")
                if words:
                    parts.append(f"The shot ends on this: {lower_first(words).rstrip('.')}.")
            if last:
                parts.append(self.filler(clip, clip_shot, people_of(plan)))
            lines.append(" ".join(part for part in parts if part))
        return lines

    def look_block(self, plan):
        from .compile_prompts import look_of
        look = look_of(self.breakdown, plan.shot)
        text = str(look.get("look_block") or "").strip() if look is not None else ""
        return self.key(text) if text and text.lower() != "none" else ""

    def visible_parts(self, person, plan):
        """The parts of a person an insert shows ('fist', 'knuckles', 'sleeve'), in the order the person's own action
        names them, at most three; a part another person owns ('her hands' in his action) is skipped; 'hands' when
        none is named (review F9)."""
        text = straight_text(str(person.item.get("does") or "")).lower()
        own = person.pronoun[1].lower()
        found = []
        for match in re.finditer(r"\b(" + "|".join(BODY_PARTS) + r")\b", text):
            before = re.findall(r"[\w']+", text[:match.start()])[-3:]
            owners = [word for word in before if word in ("his", "her", "their", "its") or word.endswith("'s")]
            if owners and owners[-1] not in (own, f"{person.name.lower()}'s"):
                continue
            word = match.group(1)
            if word not in found and word.rstrip("s") not in found and word + "s" not in found:
                found.append(word)
        return found[:3] or ["hands"]

    def trimmed(self, text, clip, where):
        """A record's description with only the words that name something absent (or ask for stillness, talk about
        speaking, compare) cut out: each clause holding one is cut at its first 'with', 'and', 'or' or 'where' before
        the word ('a bare, clean kitchen with nothing on the walls' -> 'a bare, clean kitchen'; 'a bottle with a white
        cap and no label' -> 'a bottle with a white cap'), or left out whole when no part of it stands alone. Returns
        (the words kept, True when the first clause, the one that names the thing, was kept); what is cut is listed
        once on the scene's page, with the record to reword (review F4 and F6)."""
        words, first_kept, cut = trim_kept_out(self.fixer, text, KEPT_OUT_LISTS + ("held",))
        for piece in cut:
            note = f"{LEFT_OUT_WHY}: '{piece}' ({where}). Reword it to say what is there."
            if note not in clip.record_left_out:
                clip.record_left_out.append(note)
        return words, first_kept

    def described_thing(self, fixed, name, clip, where):
        """A thing's fixed description with only the words that name something absent cut out ('... with a white
        screw cap and no label' -> '... with a white screw cap'), or its plain name when the clause that names the
        thing goes, so a sentence always keeps its subject (review F6)."""
        if not fixed:
            return name
        words, first_kept = self.trimmed(fixed, clip, where)
        return words if words and first_kept else name

    def thing_words(self, written, plan, cast, clip, mentioned):
        """A thing in the shot, once a clip: its fixed description and state when it has emphasis, else its name and
        state, and where it is."""
        from .compile_prompts import composited_texts, leave_words_for_later, state_record
        item = split_item(written)
        reference = (item.first or "").strip()
        if not reference or reference.lower() == "none" or reference.startswith(("MO-", "TX-")):
            return ""
        element = element_of(reference)
        if element in mentioned:
            return ""
        mentioned.add(element)
        record = self.breakdown.record(element)
        state = state_record(self.breakdown, reference)
        emphasis = number_of(item.get("emphasis"), 0) or 0
        name = lower_first(element_name(self.breakdown, element))
        state_line = str(state.get("state_line") or "") if state is not None else ""
        fixed = str(record.get("fixed_description") or "") if record is not None else ""
        if state_line.lower() == "none":
            state_line = ""
        if fixed.lower() == "none":
            fixed = ""
        where = self.renamed(item.get("at") or "", cast, plan)
        called = with_article(name)  # never "the the flask" (review F17)
        if emphasis >= 1 and fixed:
            subject = self.described_thing(fixed.rstrip("."), name, clip, f"the description of {called}")
        else:
            subject = name
        text = subject.rstrip(".") + (f", {state_line}" if state_line else "")
        text = leave_words_for_later(sentence(text + (f", {where}" if where else "")), composited_texts(self.breakdown, plan.shot))
        return self.gate(text, clip, f"shot {three_digits(plan.identifier)}, {called}")

    def speech_words(self, clip, cast, plan, identifier, item, entry, on_screen, numbers, subject_of, at):
        from .compile_prompts import heard_line, person_noun
        line = heard_line(item, entry)
        speaker = element_of(entry.get("speaker") or "")
        if not line:
            clip.words_unknown.append(identifier)
            return ""
        if speaker not in numbers:
            numbers[speaker] = f"S{len(numbers) + 1}"
        number = numbers[speaker]
        voice = self.voice_words(speaker)
        delivery = self.fixer.delivery_words(entry.get("parenthetical"))
        if delivery and self.fixer.kept_out_word(delivery, KEPT_OUT_LISTS):
            delivery = ""
        says = f"says, {delivery}:" if delivery else "says:"
        line_text = f"<d>[{self.language}] {line}</d>"
        when = f"At about {mm_ss_ms(at)}, " if at > 1e-6 else ""
        clip.speeches.append({"speech": identifier, "speaker": speaker, "line": line, "speaker_number": number,
                              "on_screen": bool(on_screen and speaker in subject_of), "at": round(at, 3),
                              "ends_s": round(at + self.line_length(item, entry) - 0.3, 3)})
        if on_screen and speaker in subject_of:
            text = f"{subject_of[speaker]} ({number})" + (f", {voice}," if voice else "") + f" {says} {line_text}"
            return (when + text) if when else text[:1].upper() + text[1:]
        character = self.breakdown.record(speaker, "CHARACTER")
        noun = person_noun(self.adapters, character.get("fixed_description") if character is not None else "", character)
        article = "an" if noun[:1] in "aeiou" else "a"
        text = f"from off screen, {article} {noun}'s voice ({number})" + (f", {voice}," if voice else "") + f" {says} {line_text}"
        listeners = [person.name for person in people_of(plan) if person.faces != "away" and person.element != speaker]
        closed = f" {and_list(listeners)}'s lips are closed meanwhile." if len(listeners) == 1 else (
            f" {and_list(listeners)} keep their lips closed meanwhile." if listeners else "")
        text = (when + text) if when else text[:1].upper() + text[1:]
        return text + closed

    def alive_sentence(self, clip, people, until):
        """The 'alive' sentence: everyone seen breathes, moves their eyes and shifts their weight throughout, with
        blinks every 2.5 to 3.5 seconds of the shots they are in, never in the tail (Project notes 42). A person seen
        only in inserts of this clip shows no face: only their hands (or the parts the insert shows) move with their
        breathing (review F9)."""
        partial = [person for person in people if self.only_in_inserts(clip, person)]
        people = [person for person in people if person not in partial]
        extra = []
        for person in partial:
            plan = next(clip_shot.plan for clip_shot in clip.shots if person.element in elements_seen(clip_shot.plan))
            parts = self.visible_parts(person, plan)
            extra.append(f"{person.name}'s {and_list(parts)} {'are' if plural_noun(parts) else 'is'} alive in every "
                         f"second of this clip, shifting a little with {person.pronoun[1]} breathing.")
        if not people:
            return " ".join(extra)
        return " ".join([self.face_alive_sentence(clip, people, until)] + extra)

    def only_in_inserts(self, clip, person):
        return all(is_insert(clip_shot.shot) for clip_shot in clip.shots if person.element in elements_seen(clip_shot.plan))

    def face_alive_sentence(self, clip, people, until):
        blink_lines = []
        for index, person in enumerate(people):
            blinks = []
            for clip_shot in clip.shots:
                if person.element not in elements_seen(clip_shot.plan) or is_insert(clip_shot.shot):
                    continue  # no blink where the face is out of the frame (review F9)
                start, end = clip_shot.clip_start, min(clip_shot.clip_start + clip_shot.length, until)
                moment = start + 1.0 + 0.4 * (index % 3)
                while moment < end - 0.3:
                    blinks.append(round(moment, 1))
                    moment += 3.0
            if blinks:
                clip.timed += blinks
                blink_lines.append((person.name, "at about " + and_list([mm_ss_ms(moment) for moment in blinks])))
        if len(people) == 1:
            person = people[0]
            subject, possessive, _ = person.pronoun
            text = (f"{person.name} is alive in every second of this clip, during and between the actions below: "
                    f"{possessive} chest rises and falls with breathing, {possessive} eyes make small movements, and "
                    f"{possessive} weight shifts")
            if blink_lines:
                text += f"; {subject} blinks {blink_lines[0][1]}"
            return text + "."
        text = (f"{and_list([person.name for person in people])} are alive in every second of this clip, during and "
                "between the actions below: their chests rise and fall with breathing, their eyes make small movements, "
                "and their weight shifts")
        if blink_lines:
            text += "; they blink, " + "; ".join(f"{name} {times}" for name, times in blink_lines)
        return text + "."

    def filler(self, clip, clip_shot, people):
        """The one 'From ... to the end' line of small actions, inside the last shot and before the keep point."""
        start = clip_shot.clip_start
        keep = clip.keep_s
        moment = max(start + 0.4, keep - 1.2)
        if moment >= keep - 0.05:
            moment = start + (keep - start) / 2
        moment = round(moment, 1)
        if not (start < moment < keep):
            moment = round(start + (keep - start) / 2, 2)
        clip.filler_s = moment
        if people and is_insert(clip_shot.shot):
            parts = [self.visible_parts(person, clip_shot.plan) for person in people]
            seen = and_list([f"{person.name}'s {and_list(part)}" for person, part in zip(people, parts)])
            plural = len(people) > 1 or plural_noun(parts[0])
            text = f"{seen} {'shift' if plural else 'shifts'} a little with the breathing"
        elif len(people) == 1:
            person = people[0]
            text = (f"{person.name} breathes evenly, {person.pronoun[1]} eyes make small movements and "
                    f"{person.pronoun[1]} weight settles")
        elif people:
            text = (f"{and_list([person.name for person in people])} breathe evenly, their eyes make small movements "
                    "and their weight settles")
        else:
            text = "the light and the room carry on as they are, with the room's sound"
        return f"From {mm_ss_ms(moment)} to the end, {text}."

    def soundscape(self, clip, cast):
        from .compile_prompts import room_sound_of
        silent = all(normalise_word(clip_shot.shot.get("silence") or "none") == "true_silence" for clip_shot in clip.shots)
        if silent:
            return "N/A"
        first = clip.shots[0]
        room = self.gate(room_sound_of(self.breakdown, first.shot), clip, "the room sound", record_level=True)
        parts = [sentence(room)] if room else []
        most = int(number_of(constant(self.breakdown.constants, "named_sounds_per_prompt_max", 3), 3))
        effects = []
        for clip_shot in clip.shots:
            for written in clip_shot.shot.get_all("effect"):
                item = split_item(written)
                what = (item.first or "").strip()
                if not what or what.lower() == "none":
                    continue
                at = number_of(item.get("at"))
                if at is not None and not (clip_shot.shot_start - 1e-9 <= at <= clip_shot.shot_end + 1e-9):
                    continue
                words = self.gate(self.renamed(what, cast, clip_shot.plan), clip, f"shot {three_digits(clip_shot.identifier)}, a sound")
                if words:
                    effects.append(words)
        for words in effects[:most]:
            parts.append(sentence(f"The sound of {lower_first(words)}"))
        for words in effects[most:]:
            clip.notes.append(f"the sound of {words} is laid in during the sound edit (a prompt names at most {most} sounds)")
        for index in clip.contact_cuts:
            parts.append(f"The hit sounds right on the cut at {mm_ss_ms(clip.shots[index].clip_start)}.")
        return " ".join(part for part in parts if part) or "The room's own quiet sound."

    def start_picture_file(self, clip):
        return f"Start pictures/Scene {scene_number_words(clip.scene)} - clip {clip.number:02d} - start picture.png"

    def start_picture(self, clip, cast, place_record, place_name, tags):
        """The brief for the clip's start picture: its first shot's first frame, from the master picture. In the mirror
        world it follows compile_prompts' own rules: on routes a and b the picture is made unflipped (the master
        picture flipped, the people's sides turned) because the take is flipped in the edit; on the plate route it is
        made in two steps, the plate (the place with its mirrored people, flipped) and then the others added
        (compile_prompts.plate_route_prompts; 8.5, review F2). An insert shows only part of a person (review F9); a
        later part of a long shot starts where the part before ends (review F7)."""
        clip_shot = clip.shots[0]
        plan = clip_shot.plan
        mirror = clip.mirror or {}
        master = clip.master_picture or {}
        people = people_of(plan)
        code = master.get("code", "the master picture")
        master_file = master.get("flipped_file") or master.get("file", "")
        master_words = f"{code} flipped left to right" if master.get("flipped_file") else code
        seen = {person.element for person in people}
        insert = is_insert(plan.shot)
        moments = self.moments(clip_shot, cast, clip, clip.keep_s)
        first_moment = moments[0][2] if moments else ""
        opening = self.first_frame(first_moment)
        names = [person.name for person in people]
        if not names:
            closing = deserted(place_name)
        elif insert:
            closing = (f"{and_list(names)} {'is the only person' if len(names) == 1 else 'are the only people'} in the "
                       "picture, seen only as " + and_list([f"{person.name}'s {and_list(self.visible_parts(person, plan))}"
                                                            for person in people]) + ".")
        elif len(names) == 1:
            closing = f"{names[0]} is the only person in the picture."
        else:
            closing = f"{and_list(names)} are the only people in the picture."
        continuity = ""
        if clip_shot.parts > 1 and clip_shot.part > 1:
            continuity = (f"This picture goes on from the part before (shot {three_digits(clip_shot.identifier)}, part "
                          f"{clip_shot.part - 1}): match its last kept frame, with the people, their hands and the "
                          "props where that frame leaves them.")
        if mirror.get("plate"):
            return self.plate_start_picture(clip, cast, plan, people, place_name, master_words, master_file,
                                            opening, continuity, closing, first_moment)
        attach = [f"{master_words} ({master_file})".replace(" ()", "")]
        for entry in clip.character_pictures:
            if entry["person"] not in seen:
                continue
            flipped = " flipped left to right" if entry.get("flipped") else ""
            attach.append(f"your {entry['name']} picture{flipped} ({entry['file']})")
        first, _ = self.camera(clip_shot, cast, clip)
        parts = [f"Use {master_words} as the set and keep it exactly: {place_name}, with its walls, furniture and "
                 "fittings where they are."]
        if mirror.get("flip_in_edit"):
            parts.append("This picture is made as the take is made, before it is flipped left to right in the edit.")
        setup = self.breakdown.record(plan.shot.get("setup") or "")
        position = ""
        if setup is not None and setup.get("use"):
            position = self.gate(str(setup.get("use")).split(":")[0], clip, "the start picture's camera place")
        lens = number_of(plan.shot.get("lens_mm"))
        lens_words = ""
        if lens:
            for band in self.adapters.phrase("lens", "ranges", default=[]) or []:
                if lens <= band.get("up_to_mm", 0):
                    lens_words = band.get("words") or "a normal lens"
                    break
        camera = f"Camera: {first.rstrip('.')}" + (f", from the setup for {lower_first(position)}" if position else "") + \
                 (f", {lens_words}" if lens_words else "") + "."
        parts.append(camera)
        for person in people:
            fixed, state, _ = self.person_keys(person, clip, plan, for_picture=True)
            if insert:
                where = self.placement(person, cast, plan, facing_too=False)
                seen_parts = self.visible_parts(person, plan)
                verb = "is" if len(seen_parts) == 1 and not seen_parts[0].endswith("s") else "are"
                text = (f"{person.name} (use my {person.name} picture for the skin and clothes): only "
                        f"{person.pronoun[1]} {and_list(seen_parts)} {verb} in the picture"
                        + (f", {where}" if where else "") + ".")
                if state:
                    text += f" {person.pronoun[2]} clothes: {state.rstrip('.')}."
                parts.append(text)
                continue
            where = self.placement(person, cast, plan)
            text = f"{person.name} (use my {person.name} picture for the face, hair and build): "
            text += (fixed.rstrip(".") + (f"; {state.rstrip('.')}" if state else "")) if fixed else state.rstrip(".")
            text = text.rstrip(": ") + "."
            if where:
                text += f" {person.name} is {where}."
            eyeline = str(person.item.get("eyeline") or "").strip()
            if eyeline.lower() in ("down", "up"):
                text += (f" {person.pronoun[2]} eyes look {eyeline.lower()}, away from the camera; "
                         f"{person.pronoun[1]} mouth is closed.")
            elif eyeline and eyeline.lower() not in ("none", "open", "camera"):
                target = cast.label(eyeline) if eyeline.startswith("CH-") else (
                    lower_first(element_name(self.breakdown, element_of(eyeline))) if re.match(r"^(PR|LOC|CH)-", eyeline)
                    else self.gate(eyeline, clip, "an eyeline"))
                if target:
                    text += f" {person.pronoun[2]} eyes are on {target}, away from the camera; {person.pronoun[1]} mouth is closed."
            else:
                text += f" {person.pronoun[2]} eyes are on what {person.pronoun[0]} is doing, away from the camera; {person.pronoun[1]} mouth is closed."
            parts.append(text)
        if opening:
            parts.append(sentence(f"The picture is the instant this begins: {lower_first(opening).rstrip('.')}"))
        holds = self.things_in_hand(plan, cast)
        if holds:
            parts.append(sentence("At that instant " + and_list(holds)))
        mentioned = set()
        for written in plan.shot.get_all("thing"):
            words = self.thing_words(written, plan, cast, clip, mentioned)
            if words:
                parts.append(words)
        light = self.light_words(plan)
        if light:
            parts.append(f"Light: {lower_first(light).rstrip('.')}.")
        if continuity:
            parts.append(continuity)
        parts.append(closing)
        prompt = " ".join(part for part in parts if part)
        found = self.fixer.kept_out_word(prompt, ("absence",))
        return {"file": self.start_picture_file(clip), "master": master.get("code"), "attach": attach,
                "prompt": prompt, "who": closing, "first_moment": first_moment, "kept_out_word": found or ""}

    def plate_start_picture(self, clip, cast, plan, people, place_name, master_words, master_file, opening, continuity,
                            closing, first_moment):
        """The start picture on the plate route, in compile_prompts' two steps: the plate (the place and its mirrored
        people as the model makes them, before the flip), flipped left to right, then the people shown as normal
        added with an edit model (plate_route_prompts; 8.5, C2 R5)."""
        from .compile_prompts import plate_route_prompts
        plate, edit = plate_route_prompts(self.compiler, plan, self.fixer.fix(cast.rename(opening or "")))
        mirrored = [person for person in people if person.flipped]
        added = [person for person in people if not person.flipped]
        first_attach = [f"{master_words} ({master_file})".replace(" ()", "")]
        first_attach += [f"your {person.name} picture (as it is, unflipped)" for person in mirrored]
        parts = [f"Step 1, the plate: use {master_words} as the set and keep it exactly: {place_name}, with its walls, "
                 f"furniture and fittings where they are. Attach {and_list(first_attach)}.", plate,
                 "Then flip this picture left to right."]
        if edit:
            parts.append("Step 2: give the flipped plate and " + and_list(
                [f"your {person.name} picture" for person in added] or ["the plate alone"])
                + " to an edit model, with these words: " + edit)
        if continuity:
            parts.append(continuity)
        parts.append(closing)
        prompt = " ".join(part for part in parts if part)
        return {"file": self.start_picture_file(clip), "master": (clip.master_picture or {}).get("code"),
                "attach": first_attach + [f"your {person.name} picture" for person in added], "prompt": prompt,
                "who": closing, "first_moment": first_moment, "plate": True,
                "kept_out_word": self.fixer.kept_out_word(prompt, ("absence",)) or ""}

    @staticmethod
    def first_frame(moment_words):
        """The first action of a moment, which a still picture can catch the instant of: up to its first semicolon or
        'then' (review F9: a picture cannot hold a sequence of actions)."""
        first = re.split(r"\s*;\s*|,?\s+then\s+", str(moment_words or "").strip())[0]
        return first.strip(" ,.")

    def things_in_hand(self, plan, cast):
        """'the flask is already in Eli's fist' for each thing the shot places in someone's hands (its `at`), in place
        of a fixed phrase (review F9)."""
        found = []
        for written in plan.shot.get_all("thing"):
            item = split_item(written)
            reference = (item.first or "").strip()
            if not reference or reference.lower() == "none" or reference.startswith(("MO-", "TX-")):
                continue
            where = self.renamed(item.get("at") or "", cast, plan)
            match = re.search(r"\b(?:in|on|between|under)\b[^,;]*?\b(?:hand|hands|fist|fists|fingers|palm|palms|grip|"
                              r"arms)\b", where, re.IGNORECASE)
            if not match:
                continue
            name = lower_first(element_name(self.breakdown, element_of(reference)))
            name = with_article(name)
            verb = "are" if name.endswith("s") and not name.endswith("ss") else "is"
            found.append(f"{name} {verb} already {match.group(0)}")
        return found

    def light_words(self, plan):
        from .compile_prompts import light_sentence, look_of
        look = look_of(self.breakdown, plan.shot)
        if look is None:
            return ""
        return light_sentence(self.key(look.get("look_block") or ""))

    def questions(self, clip, people):
        """(questions, what failure looks like and what to change first) for one clip (Project notes 42, W10)."""
        from .compile_prompts import side_questions
        phrase = self.adapters.phrase
        questions = []
        partial = [person for person in people if self.only_in_inserts(clip, person)]
        faces = [person for person in people if person not in partial]
        for person in faces:
            questions.append(f"Is it the same face as your {person.name} picture?")
        for person in partial:
            # an insert shows no face: ask about what it does show (review F9)
            plan = next(clip_shot.plan for clip_shot in clip.shots if person.element in elements_seen(clip_shot.plan))
            questions.append(f"Do {person.name}'s {and_list(self.visible_parts(person, plan))} and clothes match your "
                             f"{person.name} picture?")
        if clip.speeches:
            questions.append(phrase("check_questions", "said_once", default="Is each line said once, by the right mouth?"))
        for clip_shot in clip.shots:
            # which side a ring or a scar is on, in the take as made (8.5; compile_prompts' own side questions), said
            # per shot when the clip has several, since the sides change with the camera
            for question in side_questions(self.compiler, clip_shot.plan):
                if len(clip.shots) > 1:
                    question = f"Shot {three_digits(clip_shot.identifier)}: {question[:1].lower()}{question[1:]}"
                questions.append(question)
        for person in faces:
            questions.append(phrase("check_questions", "moves_between",
                                    default="Does {name} move between the written actions: breathing, eyes, small shifts?")
                             .replace("{name}", person.name))
        if len(clip.shots) > 1:
            questions.append(phrase("check_questions", "cut_lands",
                                    default="Does each cut land within about a second of its written time?"))
        questions.append(phrase("check_questions", "tail_left_out",
                                default="Is the tail, after second {seconds}, left out of the kept part?")
                         .replace("{seconds}", plain_number(clip.keep_s)))
        if clip.contact_cuts:
            questions.append(phrase("check_questions", "contact_across_cut",
                                    default="Does the hit happen across the cut, never on screen?"))
        if all(is_static(clip_shot.plan) for clip_shot in clip.shots):
            questions.append(phrase("check_questions", "camera_holds",
                                    default="Does the camera hold its framing, with no drift or zoom?"))
        notes = []
        if people:
            notes.append("If a face goes stiff after a line, or a person stops between the written actions, run another "
                         "seed before changing any words.")
        if clip.speeches:
            notes.append("If a line comes from the wrong mouth or is said twice, change the seed first.")
        if len(clip.shots) > 1:
            notes.append("Cuts can land about a second late: trim by what you see, not by the numbers.")
        if clip.contact_cuts:
            notes.append("If the hit shows before the cut, trim that shot to end earlier; the next shot already shows "
                         "the result.")
        notes.append(f"Step through the last two seconds frame by frame: H3 often breaks up there. Keep only seconds 0 "
                     f"to {plain_number(clip.keep_s)}.")
        if (clip.mirror or {}).get("flip_in_edit"):
            notes.append("Answer the side questions on the take as it comes out of H3, before you flip it in the edit.")
        return list(dict.fromkeys(questions)), notes


# ---------------------------------------------------------------- master pictures and the picture style block

def objects_of(place_record):
    """[(name, material)] of the place's set objects (its set plan), in the order written; an opening is left out."""
    found = []
    if place_record is None:
        return found
    for written in place_record.get_all("object"):
        item = split_item(written)
        name = (item.first or "").strip().replace("_", " ").lower()
        material = (item.get("material") or "").strip()
        if name and material and not material.lower().startswith(("none", "an open doorway")):
            found.append((name, material))
    return found


def places_in_order(breakdown):
    """[(LOCATION record, first scene)] of every place the scenes use, by the place's first scene in the project."""
    found = {}
    for scene_identifier in breakdown.scene_identifiers():
        scene = breakdown.record(scene_identifier, "SCENE")
        location = scene.get("location") if scene is not None else None
        if location and location not in found:
            record = breakdown.record(location, "LOCATION")
            if record is not None:
                found[location] = (record, scene_identifier)
    return list(found.values())


def master_pictures(compiler, route):
    """{LOCATION ID: master picture} for every place, numbered M1, M2 ... by the place's first scene (stable across
    compiles), each an empty set picture's prompt."""
    breakdown = compiler.breakdown
    fixer = compiler.fixer
    masters = {}
    for number, (record, first_scene) in enumerate(places_in_order(breakdown), start=1):
        code = f"M{number}"
        name = lower_first(record.title or element_name(breakdown, record.identifier))
        states = [state for state in breakdown.records_of("STATE") if state.get("element") == record.identifier]
        state_line = fixer.key_words(str(states[0].get("state_line") or "")) if states else ""
        # the place's state line loses the clauses that name something absent, as in every clip (review F4)
        state_line = trim_kept_out(fixer, state_line, KEPT_OUT_LISTS)[0] if state_line.lower() != "none" else ""
        parts = [f"Photograph of {name}, empty" + (f": {state_line.rstrip('.')}." if state_line else ".")]
        objects = [f"the {object_name}, {material}" for object_name, material in objects_of(record)]
        objects_text = fixer.drop_kept_out(fixer.swap_words("; ".join(objects)), KEPT_OUT_LISTS) if objects else ""
        if objects_text:
            parts.append(sentence(f"In it: {objects_text}"))
        setup, lens = main_setup(breakdown, record.identifier)
        if setup is not None and setup.get("use"):
            position = fixer.drop_kept_out(fixer.swap_words(str(setup.get("use")).split(":")[0].strip()), KEPT_OUT_LISTS)
            if position:
                parts.append(sentence(f"Camera: {position}" + (f", {lens}" if lens else ", a normal lens")))
        look = next((look for look in breakdown.records_of("LOOK") if look.get("for") == record.identifier), None)
        if look is not None and look.get("look_block"):
            from .compile_prompts import light_sentence
            light = light_sentence(fixer.key_words(look.get("look_block")))
            if light:
                parts.append(f"Light: {lower_first(light).rstrip('.')}.")
        parts.append(deserted(name))
        masters[record.identifier] = {
            "code": code, "place": record.identifier, "name": name, "first_scene": first_scene,
            "file": f"Master pictures/{code} - {record.title or name}.png", "prompt": " ".join(parts),
        }
    return masters


def main_setup(breakdown, location):
    """(SETUP record, lens words) of the widest shot in the place's scenes, or (None, '')."""
    best = None
    for scene_identifier in breakdown.scene_identifiers():
        scene = breakdown.record(scene_identifier, "SCENE")
        if scene is None or scene.get("location") != location:
            continue
        for shot in breakdown.shots_of(scene_identifier):
            size = size_of(shot)
            rank = SIZE_SCALE.index(size) if size in SIZE_SCALE else 99
            setup = breakdown.record(shot.get("setup") or "")
            if setup is not None and (best is None or rank < best[0]):
                best = (rank, setup, number_of(shot.get("lens_mm")))
    if best is None:
        return None, ""
    lens = best[2]
    words = ""
    if lens:
        words = "a wide-angle lens" if lens <= 28 else "a normal lens" if lens <= 60 else "a long lens"
    return best[1], words


def look_block_paragraph(compiler):
    """The one paragraph pasted first in every picture prompt (Project notes 43, A6)."""
    breakdown = compiler.breakdown
    shape = compiler.frame_shape
    shape_words = {"2.39": "Wide 2.4:1 frame", "1.85": "Wide 1.85:1 frame", "16_9": "16:9 frame",
                   "4_3": "4:3 frame", "9_16": "Tall 9:16 frame"}.get(shape, "16:9 frame")
    style = breakdown.singleton("STYLE")
    style_words = str(style.get("style_words") or "").strip().rstrip(".") if style is not None else ""
    parts = ["A real photograph from a film set.", f"{shape_words}.",
             "Natural skin with pores and fine lines; real materials with wear and scratches."]
    if style_words:
        parts.append(sentence(compiler.fixer.key_words(style_words)))
    parts += ["Light comes only from the sources named here.",
              "People are caught in the middle of what they are doing, mouths closed, their eyes on their task and "
              "away from the camera."]
    return " ".join(parts)


# ---------------------------------------------------------------- one compile of the route

def route_rule_marks(compiler, route):
    from .checks_clip_book import rule_marks
    return rule_marks(compiler.breakdown, route.rules(), route.facts)


def clip_entry(clip, route, words):
    """The machine file's entry for one clip (what the route checks and the pages read)."""
    shots = []
    for index, clip_shot in enumerate(clip.shots):
        shot = clip_shot.shot
        shots.append({
            "shot": clip_shot.identifier, "title": shot.title, "part": clip_shot.part, "parts": clip_shot.parts,
            "shot_from_s": round(clip_shot.shot_start, 3), "shot_to_s": round(clip_shot.shot_end, 3),
            "clip_from_s": round(clip_shot.clip_start, 3),
            "clip_to_s": round(min(clip_shot.clip_start + clip_shot.length, clip.keep_s), 3),
            "size": size_of(shot), "angle": normalise_word(shot.get("angle") or "eye_level"),
            "setup": shot.get("setup") or "", "insert": is_insert(shot), "static": is_static(clip_shot.plan),
            "held": bool(clip_shot.plan.held), "people": sorted(elements_seen(clip_shot.plan)),
            "single": is_single(clip_shot.plan), "looks_at": looks_at(clip_shot.plan),
            "contact_cut_into": index in clip.contact_cuts,
            "contact_on_screen": list(contact_in_shot(shot, words) or []) or None,
        })
    return {
        "clip": clip.identifier, "scene": clip.scene, "number": clip.number, "title": clip.title,
        "frames": clip.frames, "length_s": round(clip.frames / route.fps, 3), "seconds_to_type": clip.seconds_to_type,
        "keep_s": clip.keep_s, "tail_s": round(clip.frames / route.fps - clip.keep_s, 3),
        "overflow_s": clip.overflow_s, "held": clip.held, "shots": shots,
        "sections": [{"name": name, "lines": lines} for name, lines in clip.sections],
        "prompt": clip.prompt, "connections": clip.connections,
        "people": [{"person": person.element, "state": person.reference, "name": person.name} for person in clip.people],
        "speeches": clip.speeches, "keys": clip.keys, "key_problems": clip.key_problems,
        "style_sentence": clip.style_sentence, "filler_s": clip.filler_s, "timed_s": sorted(set(clip.timed)),
        "start_picture": clip.start_picture, "master_picture": clip.master_picture,
        "character_pictures": clip.character_pictures, "questions": clip.questions, "check_notes": clip.check_notes,
        "problems": clip.problems, "left_out": clip.left_out, "notes": clip.notes, "words_unknown": clip.words_unknown,
        "starts_because": clip.starts_because, "joins": clip.joins, "over_cap": clip.over_cap or None,
        "mirror": clip.mirror, "part_moments": clip.part_moments, "record_left_out": clip.record_left_out,
        "lengthened": clip.lengthened,
    }


def compile_scene(compiler, route, scene_identifier, masters):
    """The clips of one scene, grouped and written."""
    from .compile_prompts import analyse_shot
    breakdown = compiler.breakdown
    plans = [analyse_shot(breakdown, compiler.adapters, shot, compiler.raw) for shot in breakdown.shots_of(scene_identifier)]
    clips = Grouper(compiler, route).group(scene_identifier, plans)
    writer = ClipWriter(compiler, route, masters)
    for clip in clips:
        writer.write(clip)
    # a mirror world not known yet is said once a scene, on its first clip that meets it (review F2)
    unknown = next((clip for clip in clips if (clip.mirror or {}).get("open")), None)
    if unknown is not None:
        unknown.mirror["open_note"] = (
            f"which people and things are mirrored in scene {scene_number_words(scene_identifier)} is not known yet: the "
            "mirror rule's era lines were not found in the story given, so no picture is flipped and nobody's sides "
            "are turned. Compile with the whole story (--story) before making these clips")
    return plans, clips


def route_pack(compiler, route, scene_identifier, plans, clips, masters, marks):
    """The machine file of one scene's clip book."""
    full, test, crop = route.size_for(compiler.frame_shape)
    shot_map = []
    for clip in clips:
        for clip_shot in clip.shots:
            entry = {"shot": clip_shot.identifier, "clip": clip.identifier, "part": clip_shot.part,
                     "parts": clip_shot.parts, "clip_from_s": round(clip_shot.clip_start, 3),
                     "clip_to_s": round(min(clip_shot.clip_start + clip_shot.length, clip.keep_s), 3),
                     "title": clip_shot.shot.title}
            if clip.overflow_s > 0:
                # the plan holds the shot longer than H3 makes: the rest is made in the edit (review F18)
                entry.update({"plan_s": round(clip_shot.length, 3), "made_in_edit_s": clip.overflow_s})
            shot_map.append(entry)
    not_video = [plan.identifier for plan in plans if not plan.video]
    not_video_kinds = {plan.identifier: ("a still, moved in the edit" if plan.still_only else
                                         "a card" if plan.kind == "card" else
                                         "black" if plan.kind == "black" else "made from its parts in the edit")
                       for plan in plans if not plan.video}
    titles = {plan.identifier: plan.shot.title for plan in plans if not plan.video}
    return {
        "about": ("The clip book of one scene for a route (a model plus the place it runs), compiled by stage.py "
                  "compile from the records; never edit it. Change a record and compile again."),
        "kind": ROUTE_FILE_KIND, "route": ROUTE_VALUE, "model": route.name, "model_name": route.display,
        "scene": scene_identifier, "scene_label": scene_label(compiler.breakdown, scene_identifier),
        "compiled_on": compiler.today.isoformat(),
        "model_facts_date": compiler.adapters.checked_on.isoformat() if compiler.adapters.checked_on else None,
        "frame_shape": compiler.frame_shape, "size_full": full, "size_test": test, "crop_note": crop,
        "fps": route.fps, "tail_s_min": route.tail_s_min,
        "rule_marks": marks, "look_block": look_block_paragraph(compiler),
        "master_pictures": [master for master in masters.values() if master.get("first_scene")],
        "clips": [clip_entry(clip, route, compiler.words) for clip in clips], "shot_map": shot_map, "not_video": not_video,
        "not_video_kinds": not_video_kinds, "not_video_titles": titles,
    }


def route_pack_name(scene_identifier, route_name=ROUTE_MODEL):
    return f"{scene_identifier} - {route_name}.json"


def compile_route(context, compiler, project, scenes, route_name=ROUTE_MODEL, lint_only=False):
    """compile --route: group, write, check and save the clip book of these scenes. Returns the exit code."""
    from .compile_prompts import MACHINE_FOLDER, PACK_FOLDER, PROMPTS_FOLDER, write_text
    from .checks_clip_book import lint_route_packs
    from .project_files import StageStop
    route = RouteFacts.from_adapters(compiler.adapters, route_name)
    if not route.facts:
        raise StageStop(f"The route {route_name} is not in the model facts (_config/adapters/video_models.json).")
    breakdown = compiler.breakdown
    masters = master_pictures(compiler, route)
    marks = route_rule_marks(compiler, route)
    packs = {}
    for scene_identifier in scenes:
        plans, clips = compile_scene(compiler, route, scene_identifier, masters)
        packs[scene_identifier] = route_pack(compiler, route, scene_identifier, plans, clips, masters, marks)
    problems = lint_route_packs(compiler, project, list(packs.values()), route)
    context.say(f"Model facts are {compiler.age if compiler.age is not None else 'of unknown age:'} days old"
                + (f" (checked on {compiler.adapters.checked_on.isoformat()})." if compiler.adapters.checked_on else "."))
    for scene_identifier, pack in packs.items():
        groups = []
        for entry in pack["clips"]:
            shots = ", ".join(three_digits(shot["shot"]) for shot in entry["shots"])
            groups.append(f"clip {entry['number']:02d}: shot{'s' if len(entry['shots']) > 1 else ''} {shots}")
        context.say(f"{pack['scene_label']}: {len(pack['clips'])} clip{'s' if len(pack['clips']) != 1 else ''} for "
                    f"{route.display} ({'; '.join(groups)}).")
        for entry in pack["clips"]:
            for problem in entry["problems"]:
                context.say(f"  Clip {entry['number']:02d}: {problem}")
    errors = [problem for problem in problems if getattr(problem, "level", "") == "E"]
    warnings = [problem for problem in problems if getattr(problem, "level", "") == "W"]
    for problem in problems:
        context.say(str(problem))
    context.say(f"Route checks: {len(errors)} error{'s' if len(errors) != 1 else ''}, {len(warnings)} "
                f"suggestion{'s' if len(warnings) != 1 else ''} (rules still unclear until the take log decides them).")
    if lint_only:
        context.summary = f"compile --route --lint-only: {len(errors)} route check errors"
        return 1 if errors else 0
    folder = Path(project.folder)
    machine = folder / MACHINE_FOLDER / PROMPTS_FOLDER
    pages = folder / PACK_FOLDER / ROUTE_FOLDER
    written = []
    with project.lock():
        machine.mkdir(parents=True, exist_ok=True)
        for scene_identifier, pack in packs.items():
            write_text(machine / route_pack_name(scene_identifier, route.name),
                       json.dumps(pack, indent=1, ensure_ascii=False) + "\n")
        all_packs = read_route_packs(machine, route.name)
        for scene_identifier, pack in packs.items():
            page = pages / f"{pack['scene_label']}.md"
            write_text(page, scene_page(compiler, route, pack))
            written.append(str(page.relative_to(folder)))
        for name, text in (("00 Settings and how to run a clip.md", settings_page(compiler, route, all_packs)),
                           ("01 Pictures to make first.md", pictures_page(compiler, route, all_packs, masters)),
                           ("Shot map.md", shot_map_page(route, all_packs)),
                           ("If a clip goes wrong.md", troubleshooting_page(route)),
                           ("Take log.md", take_log_page(compiler, route, marks))):
            write_text(pages / name, text)
            written.append(str((pages / name).relative_to(folder)))
        try:
            project.add_log_entry("Compiled the clip book for MiniMax H3 in ComfyUI for "
                                  + ", ".join("scene " + scene_number_words(scene) for scene in packs) + ".")
        except (OSError, ValueError):
            pass
    for name in written:
        context.say(f"Written: {name}")
    total = sum(len(pack["clips"]) for pack in packs.values())
    context.summary = f"compile --route {route.name}: {total} clips, {len(errors)} route check errors"
    return 1 if errors else 0


def read_route_packs(machine_folder, route_name=ROUTE_MODEL):
    """Every scene's clip book machine file for the route, in scene order."""
    from .record_format import sort_key_for_identifier
    packs = []
    for path in Path(machine_folder).glob(f"* - {route_name}.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict) and data.get("kind") == ROUTE_FILE_KIND:
            packs.append(data)
    return sorted(packs, key=lambda pack: sort_key_for_identifier(pack.get("scene") or ""))


# ---------------------------------------------------------------- the pages

def plain(lines):
    from .compile_prompts import plain_page
    return plain_page("\n".join(lines).rstrip() + "\n")


def size_words(size):
    return f"{size[0]} x {size[1]}"


def settings_page(compiler, route, packs):
    facts = route.facts
    shape = compiler.frame_shape
    full, test, crop = route.size_for(shape)
    lines = [f"# {route.display}: settings and how to run a clip", "",
             "## How to use this page", "",
             f"- Where: {facts.get('place') or 'ComfyUI'}.",
             "- Set the boxes below once, then run each clip from its page in this folder.",
             "- Never change a prompt by hand. Change the shot in the breakdown and compile again.",
             f"- Size for this film: {size_words(full)} for the real clips, {size_words(test)} for quick layout tests"
             + (f" ({crop})." if crop else "."),
             "", "## The settings, by the names in the template", ""]
    for setting in facts.get("settings") or []:
        lines.append(f"- {setting.get('box')}: {setting.get('set')}. Why: {setting.get('why')}")
    lines += ["", "## How to run a clip", "",
              "1. Make the clip's start picture from its master picture and character pictures (see 01 Pictures to "
              "make first), and go through the checklist there.",
              "2. In ComfyUI, load the start picture into the first image box, wired to ref_image_0 on the H3 box. It "
              "becomes <Picture 1>.",
              "3. Wire the character pictures listed for the clip, in that order, to ref_image_1, ref_image_2 and so "
              "on. They become <Picture 2>, <Picture 3>. Wire nothing else, and remove the template's sample pictures.",
              "4. Copy the prompt from the line after COPY FROM HERE to the line before COPY TO HERE, and paste it into "
              "Input Text (Prompt).",
              "5. Type the clip's seconds into Float (Duration).",
              f"6. Run it small first ({size_words(test)}) to check the layout: the right people and place, the cuts "
              f"roughly where they should be, speech from the right mouths. Then run it full size ({size_words(full)}).",
              "7. Answer the clip's questions. Step through the last two seconds frame by frame: that is where H3 "
              "breaks up.",
              "8. Keep the part given under KEEP and throw away the tail.",
              "9. If something is wrong, read If a clip goes wrong before changing anything.",
              "10. Tell Claude what you saw in each take, with its seed and settings: Claude logs the take and what it "
              "showed about the route's rules (see Take log).",
              "", "## Traps", "",
              "- The pictures' order must match the numbers in the prompt: the first picture wired is <Picture 1>.",
              "- Wiring a person's picture makes that person appear. People who are only heard are never wired.",
              "- Lightning on makes clips stiff.",
              "- The template has no negative prompt, and naming a thing to avoid adds it. Write what should be there.",
              "- Typing a clip's exact seconds can tip it into a longer length with no prompt behind the extra part. "
              "Type the seconds given.",
              "- Always trim the tail. In dark clips, step through the end frame by frame.",
              "- Before changing one thing in a prompt, search the whole prompt for every mention of it.",
              "- Rewording a person's description re-rolls their face: the prompts paste each description exactly.",
              "- If speech is wrong, change the seed before changing words.",
              "- The start picture beats the words: the camera, the number of people, their eyes and the props come "
              "from the picture.",
              "- Small test runs are for layout only. Judge faces and acting at full size.",
              "- Cuts can land up to about a second late, and lines can start late. Trim by what you see."]
    return plain(lines)


def pictures_page(compiler, route, packs, masters):
    lines = [f"# {route.display}: pictures to make first", "",
             "## How to use this page", "",
             "- Make the master pictures first, once each: the places, empty.",
             "- Then make each clip's start picture from its master picture and character pictures, with the prompt on "
             "the clip's page.",
             "- Paste the picture style block first in every picture prompt, then the picture's own prompt.",
             "- Show every start picture to yourself against the checklist before it is used.",
             "", "## The picture style block (paste this first in every picture prompt)", "",
             "```text", packs[0]["look_block"] if packs else look_block_paragraph(compiler), "```", "",
             "## Master pictures (make these first, once)", ""]
    used = []
    for pack in packs:
        for entry in pack.get("clips") or []:
            code = (entry.get("master_picture") or {}).get("code")
            if code and code not in used:
                used.append(code)
    for master in masters.values():
        if master["code"] not in used:
            continue
        lines += [f"### {master['code']} - {master['name']} (empty)", "",
                  "Attach: nothing.", "Prompt (picture style block first, then this):", "",
                  "```text", master["prompt"], "```", "", f"Save it as: {master['file']}", ""]
    flipped = {}
    for pack in packs:
        for entry in pack.get("clips") or []:
            clip_words = f"scene {scene_number_words(pack.get('scene'))}, clip {entry['number']:02d}"
            master = entry.get("master_picture") or {}
            if master.get("flipped_file"):
                flipped.setdefault((master.get("file"), master["flipped_file"]), []).append(clip_words)
            for picture in entry.get("character_pictures") or []:
                if picture.get("flipped"):
                    flipped.setdefault((picture.get("unflipped_file"), picture["file"]), []).append(clip_words)
    if flipped:
        # the mirror world: copies flipped left to right, made once each (8.5; review F2)
        lines += ["## Copies flipped left to right (the mirror world)", "",
                  "Make each picture as usual, then save a copy flipped left to right. The clips listed use the copy.", ""]
        for (original, copy), clips in flipped.items():
            lines.append(f"- {original} -> {copy}: {'; '.join(dict.fromkeys(clips))}.")
        lines.append("")
    lines += ["## Start pictures", "",
              "- Make each clip's start picture from the master picture and character pictures listed on its page, "
              "never from the last frame of an earlier clip: every copy of a copy loses quality.",
              "- Keep the camera where the prompt puts it. H3 takes the camera position from this picture.",
              "- Exactly the people listed. Count them, and look in windows, doorways and reflections.",
              "- Each person in the right state: clothes, marks, what they carry.",
              "- Mouths closed, eyes on their task, nobody looking into the lens.",
              "- Hands already on the things they will move.",
              "- Make the moment the clip starts, not its most dramatic moment.",
              "", "## Checklist before you use a picture", "",
              "- [ ] The right place, with the camera where the prompt says",
              "- [ ] The right number of people, nobody extra",
              "- [ ] Faces match your character pictures",
              "- [ ] Clothes in the right state",
              "- [ ] Props in the right state",
              "- [ ] Light only from the named sources",
              "- [ ] Mouths closed; nobody looking into the lens",
              "- [ ] Any printed words plain or readable as planned (words are laid in during the edit)",
              "- [ ] Straight lines straight; hands with five fingers",
              f"- [ ] The film's frame shape, at least as large as the full size on the settings page"]
    return plain(lines)


def scene_page(compiler, route, pack):
    full, test, crop = pack["size_full"], pack["size_test"], pack.get("crop_note")
    lines = [f"# {pack['scene_label']} - {route.display}", "",
             "## How to use this page", "",
             "- One part per clip. For each clip: make its start picture, connect the pictures in the order given, "
             "paste the prompt, type the seconds, run it, answer the questions, and keep only the part given.",
             f"- Sizes: {size_words(full)} for the real clip, {size_words(test)} for a quick layout test"
             + (f" ({crop})." if crop else "."),
             "- Settings, the picture style block and the master pictures are in this folder's other pages.",
             "- Never change a prompt here. Change the shot in the breakdown and compile again.", ""]
    # notes that hold for the whole scene, written once (review F2 and F4)
    scene_notes = []
    for entry in pack["clips"]:
        open_note = (entry.get("mirror") or {}).get("open_note")
        if open_note and sentence(open_note) not in scene_notes:
            scene_notes.append(sentence(open_note))
        for problem in entry.get("key_problems") or []:
            # a description is the same in every clip, so its problem is said once a scene (review F4)
            note = sentence(f"the {problem['what']} of {problem.get('record_words') or problem['record']} holds "
                            f"'{problem['word']}', which H3 would show or say; it is pasted word for word in every clip "
                            "that shows them, so reword it to say what is there")
            if note not in scene_notes:
                scene_notes.append(note)
    record_notes = []
    for entry in pack["clips"]:
        for note in entry.get("record_left_out") or []:
            if note not in record_notes:
                record_notes.append(note)
    if scene_notes or record_notes:
        lines += ["## For every clip of this scene", ""]
        lines += [f"- {note}" for note in scene_notes]
        if record_notes:
            lines.append("- These words of the place and its things are left out of every clip's prompt and pictures, "
                         "because H3 would show what they name:")
            lines += [f"  - {note}" for note in record_notes]
        lines.append("")
    for entry in pack["clips"]:
        shots = entry["shots"]
        numbers = ", ".join(three_digits(shot["shot"]) + (f" (part {shot['part']} of {shot['parts']})" if shot["parts"] > 1 else "")
                            for shot in shots)
        count = NUMBER_WORDS.get(len(shots), str(len(shots)))
        lines += [f"## Clip {entry['number']:02d} - {entry['title']}", "",
                  f"Scene {scene_number_words(pack['scene'])} - plan shot{'s' if len(shots) > 1 else ''} {numbers} - "
                  f"{count} shot{'s' if len(shots) > 1 else ''}"]
        # why the clip starts here, and why its shots share it (review F5)
        if entry.get("starts_because"):
            lines.append(sentence(f"Starts a new clip because {entry['starts_because']}"))
        for reason in entry.get("joins") or []:
            lines.append(sentence(f"Shares this clip: {reason}"))
        lines += [f"Length: {entry['frames']} frames ({entry['length_s']:.2f} seconds). Type {entry['seconds_to_type']} "
                  "in Float (Duration).", "", "### Start picture", ""]
        picture = entry["start_picture"]
        master = entry.get("master_picture") or {}
        lines.append(f"Master picture: {master.get('code', 'none')}" + (f" - {master.get('name')}" if master.get("name") else "")
                     + (f" ({master.get('file')})" if master.get("file") else "") + ".")
        characters = [f"{character['name']} ({character['file']})" for character in entry.get("character_pictures") or []]
        lines.append("Character pictures: " + (", ".join(characters) if characters else "none") + ".")
        lines.append("Give the picture tool: " + ", ".join(picture.get("attach") or []) + ".")
        lines += ["Prompt (paste the picture style block first, then this):", "", "```text", picture.get("prompt", ""), "```", "",
                  f"Save it as: {picture.get('file')}", "", "### Connect in this order", ""]
        for index, connection in enumerate(entry["connections"], start=1):
            lines.append(f"{index}. {connection['input']}: {connection['picture']} ({connection['file']}) -> "
                         f"{connection['label']}")
        lines += ["Connect nothing else.", "", "### H3 prompt", "", "```text", "----- COPY FROM HERE -----",
                  entry["prompt"], "----- COPY TO HERE -----", "```", "", "### Check", ""]
        lines += [f"- {question}" for question in entry["questions"]]
        lines += [f"- {note}" for note in entry.get("check_notes") or []]
        lines += ["", "### Keep", "", f"Seconds 0 to {plain_number(entry['keep_s'])}. Throw away the rest (the tail, "
                  f"{plain_number(entry['tail_s'])} seconds)."]
        for shot in shots:
            part = f", part {shot['part']} of {shot['parts']} (its seconds {plain_number(shot['shot_from_s'])} to " \
                   f"{plain_number(shot['shot_to_s'])})" if shot["parts"] > 1 else ""
            lines.append(f"- Plan shot {three_digits(shot['shot'])}{part} = seconds {plain_number(shot['clip_from_s'])} "
                         f"to {plain_number(shot['clip_to_s'])}.")
        if entry.get("overflow_s"):
            lines.append(f"- The plan holds this shot {plain_number(entry['overflow_s'])} seconds longer than H3 can "
                         "make: make the rest in the edit, or redesign the shot.")
        mirror = entry.get("mirror") or {}
        if mirror.get("flip_in_edit"):
            lines.append("- Flip the kept part left to right in the edit before you cut it in: this clip is in the "
                         "mirror world, and H3 makes it unflipped.")
        for moment in entry.get("part_moments") or []:
            lines.append(f"- The part before or after this one shares the moment from {moment['moment'].replace('-', ' to ')} "
                         f"seconds of shot {three_digits(moment['shot'])}: match the people, hands and props at the join "
                         f"(second {plain_number(moment['boundary_s'])} of the shot).")
        extras = entry.get("problems", []) + mirror.get("problems", []) + entry.get("notes", [])
        if entry.get("over_cap"):
            over = entry["over_cap"]
            extras.append(f"shot {three_digits(over['shot'])} shows {over['pictures']} people, so this clip connects "
                          f"{over['pictures']} people's pictures, more than the {over['cap']} the route allows: H3 may mix "
                          "up faces. Frame fewer people, or split the shot into shots of fewer people each")
        if entry.get("words_unknown"):
            count = len(entry["words_unknown"])
            extras.append(f"{count} spoken line{'s are' if count != 1 else ' is'} left out of this prompt, because the "
                          "story's speeches are missing, so this clip is not ready: read the story (stage.py read) or "
                          "compile with --story, then compile again")
        if extras or entry.get("left_out"):
            lines += ["", "### Notes", ""]
            lines += [f"- {sentence(note)}" for note in extras]
            lines += [f"- {note}" for note in entry.get("left_out") or []]
        lines.append("")
    if pack.get("not_video"):
        lines += ["## Made in the edit, not as clips", "",
                  "These shots are cards, black or stills, made in the edit: "
                  + ", ".join(three_digits(identifier) for identifier in pack["not_video"]) + ".", ""]
    return plain(lines)


def shot_map_page(route, packs):
    lines = [f"# {route.display}: shot map", "",
             "## How to use this page", "",
             "- Every plan shot of the scenes compiled, in film order: which clip holds it and which seconds of the clip "
             "are that shot, or how the edit makes it. The edit is put together from this list.", "",
             "| Plan shot | Clip | Seconds in the clip | Title |", "|---|---|---|---|"]
    for pack in packs:
        from .record_format import sort_key_for_identifier
        rows = []
        for entry in pack.get("shot_map") or []:
            part = f" (part {entry['part']} of {entry['parts']})" if entry.get("parts", 1) > 1 else ""
            clip_number = entry["clip"].split("-CL")[-1]
            seconds = f"{plain_number(entry['clip_from_s'])} to {plain_number(entry['clip_to_s'])}"
            if entry.get("made_in_edit_s"):
                seconds += (f" (the plan holds {plain_number(entry['plan_s'])} seconds: the last "
                            f"{plain_number(entry['made_in_edit_s'])} made in the edit)")
            rows.append((entry["shot"], entry.get("part", 1),
                         f"| Scene {scene_number_words(pack['scene'])}, shot {three_digits(entry['shot'])}{part} | "
                         f"clip {clip_number} | {seconds} | {entry.get('title') or ''} |"))
        kinds = pack.get("not_video_kinds") or {}
        titles = pack.get("not_video_titles") or {}
        for identifier in pack.get("not_video") or []:
            rows.append((identifier, 1, f"| Scene {scene_number_words(pack['scene'])}, shot {three_digits(identifier)} | "
                                        f"made in the edit ({kinds.get(identifier, 'no clip')}) | none | "
                                        f"{titles.get(identifier) or ''} |"))
        rows.sort(key=lambda row: (sort_key_for_identifier(row[0]), row[1]))
        lines += [row[2] for row in rows]
    return plain(lines)


def troubleshooting_page(route):
    lines = [f"# {route.display}: if a clip goes wrong", "",
             "## How to use this page", "",
             "- Change one thing at a time, with the seed fixed, so you can tell what helped.",
             "- Find what you see, then make the first change given. Tell Claude about the take either way.", ""]
    for entry in route.facts.get("troubleshooting") or []:
        lines += [f"## {entry.get('symptom')}", "", sentence(f"First change: {entry.get('first_change')}"), ""]
    return plain(lines)


def take_log_page(compiler, route, marks):
    breakdown = compiler.breakdown
    counts = route.facts.get("rule_marks_from_takes", {})
    lines = [f"# {route.display}: take log", "",
             "## How to use this page", "",
             "- The route's rules start unclear: each is a suggestion until real takes decide it.",
             "- After each take, tell Claude what you saw. Claude logs the take and, for each rule the take tested, "
             "whether it held (confirmed), failed (wrong) or could not tell (unclear).",
             f"- A rule is confirmed when at least {counts.get('takes_to_confirm', 2)} takes say confirmed and none says "
             f"wrong; it is dropped as wrong when at least {counts.get('takes_to_drop', 2)} takes say wrong and more say "
             "wrong than confirmed. A confirmed rule, or one the makers' own documents state, stops a clip until it is "
             "fixed; an unclear one is a suggestion; a wrong one is no longer checked.",
             "- Times in the rules are written as minutes and seconds, 00:04.500 being 4.5 seconds.", "",
             "## The route's rules", "",
             "| Rule | What it says | Where it comes from | Mark | Takes that decided it |", "|---|---|---|---|---|"]
    for rule in route.rules():
        mark = marks.get(rule["id"], {})
        decided = [take_words(identifier) for identifier in mark.get("confirmed", []) + mark.get("wrong", [])]
        shown = mark.get("mark", rule.get("mark"))
        if shown == "wrong":
            shown = "wrong (dropped: no longer checked)"
        kind = "the makers' documents" if rule.get("kind") == "format" else "testers' notes and judgement"
        lines.append(f"| {rule_words(rule['id'])} | {rule['says']} | {kind} | {shown} | "
                     f"{', '.join(decided) if decided else 'none yet'} |")
    lines += ["", "## Takes on this route", ""]
    takes = [take for take in breakdown.records_of("TAKE")
             if re.search(r"-CL\d{2}$", (take.get("clip") or "").strip()) or route.name in (take.get("model") or "")]
    if not takes:
        lines.append("None yet.")
    for take in sorted(takes, key=lambda record: record.identifier or ""):
        verdicts = []
        for written in take.get_all("rule"):
            item = split_item(written)
            verdicts.append(f"{rule_words((item.first or '').strip())} {item.get('verdict') or 'unclear'}")
        kept = take.get("kept") or "not decided"
        lines.append(f"- {take_words(take.identifier)}: seed {take.get('seed') or 'not written'}, "
                     f"settings {take.get('settings') or 'not written'}; kept: {kept}"
                     + (f"; {', '.join(verdicts)}" if verdicts else "") + ".")
    return plain(lines)


def rule_words(identifier):
    """'rule 15' for the route rule H3R-15: the user reads no codes (review F14)."""
    match = re.search(r"(\d+)$", identifier or "")
    return f"Rule {int(match.group(1))}" if match else "a rule"


def take_words(identifier):
    """'scene 10, clip 07, take 1' for the take TK-SC10-CL07-T01."""
    match = re.match(r"^TK-SC0*(\d+)-CL(\d+)-T0*(\d+)$", identifier or "")
    if not match:
        return "a take"
    return f"scene {match.group(1)}, clip {match.group(2)}, take {match.group(3)}"
