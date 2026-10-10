"""compile_prompts.py: turn the breakdown into prompts for AI video and picture models (blueprint section 8), and run
the command compile.

In plain words:
- reads the dated model facts in _config/adapters/ (video_models, image_models, audio_models, routing, phrasebook);
- works out, for every shot, what making it needs (a start picture, a guide video, a line seen spoken, a held take
  longer than 15 seconds ...), picks one model for each scene (the scene model: the one the routing names most
  often for the needs of its shots with recurring characters), and sends a shot elsewhere only when the scene
  model cannot make it, with the reason logged (8.4, K29);
- works out each clip: screen time plus handles, rounded up to a length the model allows; a held take is never
  split; other shots split only at a planned cutaway (derive_fields.clip_plan);
- fills the model-neutral generation spec of 8.1 from the records and writes it in each model's own order and
  syntax: fixed descriptions, state lines and the look block pasted word for word; motion only when a start picture
  is attached; reasons, record IDs and music never; negations turned into allowed forms; the speaker form of the
  model (Veo: a colon and no quotation marks; Kling: a name, the delivery and the line in quotation marks);
- prices each clip (planned draft and final takes from D13's table) and says how old the model facts are;
- lints the packs with the GEN checks (checks_plan_generation_film.lint_packs) and prints their lines;
- writes each scene's packs as JSON in "For machines - do not edit/prompts/" (the shape the GEN checks read), one
  page per scene and model in "20 Prompts for AI video/", and the pictures to make first;
- with --storyboard, writes the storyboard frame prompts to "18 Storyboard/Scene NN - frame prompts.md" instead;
- routed_model(breakdown, shot) tells other tools (the shot list's Model column, the estimate) the model a shot goes to.

Command: compile [--scene <one ID, a comma list or SC07..SC10>] [--model <list>] [--force-model <name>]
[--route <name>] [--storyboard] [--lint-only] [--story <path>]. Exit 0: no GEN error; 1: GEN errors printed; 2: could
not run. With --route (or PROJECT video_route h3_comfyui_r2v) it makes a route's clip book instead (clip_book.py).

Numbers come from _config/rules/constants.json by name (handles_s, on_screen_speakers_per_clip_max,
named_sounds_per_prompt_max, model_facts_max_age_days) and from the adapter files.
Standard library only.

After the full run on The Catch (Project notes 31 and 32):
- the project's word swaps are made in pasted place, look and subject text too, once.

After the second full run (Project notes 39 and 40):
- a split speech sends only its own words; a speaking shot stays whole on a model long enough to hold it; a motion-
  only prompt leaves the picture's description out; words composited later are never asked of the model.
- after its cross-examination: words that stand for their thing become the thing the TEXT's title names, a single
  mark a letter or a number with the right article, a quoted cue "that line"; a speaking shot is kept whole only
  when chaining it would cut through its line.

After the H3 handover (Project notes 42 and 43):
- no sentence from a subject's old `still` sub-part is written for any model, display level 1 says "small
  movements", and no take question asks whether something stays still;
- for MiniMax H3 (hosted, both entries) the clauses that name something absent or ask for stillness are left out and
  listed, a must-not and the display sentence are left out, the camera has one sentence and music is N/A;
- a route (kind: route, such as MiniMax H3 in ComfyUI) is never chosen by routing; compile --route makes its clip
  book (clip_book.py), and PROJECT video_route h3_comfyui_r2v makes it the default.
"""

import datetime
import json
import math
import re
from dataclasses import dataclass, field as dataclass_field, replace as dataclass_replace
from pathlib import Path

from .derive_fields import (Breakdown, allowed_lengths, clip_plan, constant, cut_points, element_name, element_of,
                            feature_hidden, flipped_after, held_take, image_sides, is_yes, mirror_route, number_of,
                            person_name,
                            project_prompt_swaps, round_up_to, scene_label, scene_of, seconds_text, set_plan,
                            shot_mirror_states, shot_number, speech_part, speech_words_part, subject_items,
                            swap_prompt_words, swap_sources_banned)
from .record_format import (LIMITS_FILE, adapter_file, load_json, normalise_word, sort_key_for_identifier, split_item,
                            split_list)

MACHINE_FOLDER = "For machines - do not edit"
PROMPTS_FOLDER = "prompts"
SYNTAX_TEST_FOLDER = "prompts - syntax tests"
PACK_FOLDER = "20 Prompts for AI video"
SYNTAX_TEST_PAGES = "Syntax tests"
STORYBOARD_FOLDER = "18 Storyboard"
ADAPTER_FILES = ("video_models.json", "image_models.json", "audio_models.json", "routing.json", "phrasebook.json")
SPEECHES_FILE = "speeches.json"
SIZES_CLOSE = ("medium_close_up", "close_up", "extreme_close_up")
SIZES_WIDE = ("wide", "extreme_wide")
RECORD_ID = re.compile(r"\b(?:SC\d{2,3}[A-Z]?(?:-[A-Z]+\d+)?|(?:CH|VO|LOC|PR|TX|MO|CAM|WR|LK|CR|VS|RC|LX|PL|FT|ST|CF|SQ|"
                       r"CP|FIND|CHOICE|RT|PIC|PV|TK|VT|FX|MU)-[A-Z0-9][A-Z0-9-]*(?:\.S\d{2})?)\b")
NEGATION = re.compile(r"\b(?:no|not|without)\b|\b\w+n't\b", re.IGNORECASE)
ALLOWED_NEGATION = re.compile(r"\b(?:does|do|did)\s+not\s+\w+|\b(?:is|are)\s+not\s+visible\b", re.IGNORECASE)
IMAGE_SIDE_PHRASES = re.compile(
    r"\b(left|right)(?=(?:\s+|-)(?:of|edge|third|side of the (?:frame|image|picture)|half))|"
    r"(?<=\bframe[- ])(left|right)\b|(?<=\bimage[- ])(left|right)\b|(?<=\bscreen[- ])(left|right)\b|"
    r"(?<=\bto the )(left|right)\b|(?<=\btoward the )(left|right)\b|(?<=\btowards the )(left|right)\b|"
    r"(?<=\bon the )(left|right)(?! (?:hand|arm|foot|leg|shoulder|side of (?:his|her|their)))\b", re.IGNORECASE)
QUOTES = {"“": '"', "”": '"', "‘": "'", "’": "'"}
# What a cut leaves must start with its own subject (WordFixer.stands_alone; review N2): these words never start one
NOT_A_SUBJECT_START = {"on", "in", "at", "by", "from", "to", "toward", "towards", "into", "onto", "under", "over", "beside",
                       "behind", "across", "along", "around", "round", "through", "near", "against", "between", "above",
                       "below", "off", "out", "up", "down", "away", "back", "either", "with", "without", "for", "of",
                       "as", "like", "until", "while", "before", "after", "during", "inside", "outside", "past", "and",
                       "but", "or", "nor", "yet", "so", "then", "also", "again", "once", "meanwhile", "still", "even"}
SUBJECT_STARTS = {"the", "a", "an", "her", "his", "their", "its", "my", "our", "your", "she", "he", "they", "it", "we",
                  "i", "you", "both", "neither", "each", "every", "one", "two", "three", "four", "this", "that", "these",
                  "those", "someone", "somebody", "everyone", "nobody", "something", "everything", "all"}
BE_AND_HAVE = {"is", "are", "was", "were", "has", "have", "had", "does", "do", "did", "be", "am"}


# ---------------------------------------------------------------- the adapter files

def normalised_name(name):
    """A model name for comparing: lower case, runs of other characters as one space ('Kling O3' = 'kling o3')."""
    return re.sub(r"[^a-z0-9.]+", " ", str(name or "").casefold()).strip()


def read_date(text):
    try:
        return datetime.date.fromisoformat(str(text).strip()[:10])
    except (TypeError, ValueError):
        return None


class Adapters:
    """The dated model facts of _config/adapters/*.json, with the names and aliases of every model."""

    def __init__(self, documents=None, skill_folder=None):
        if documents is None:
            documents = {}
            for name in ADAPTER_FILES:
                try:
                    documents[name] = load_json(adapter_file(name), skill_folder)
                except (OSError, ValueError):
                    documents[name] = {}
        self.documents = documents
        video = documents.get("video_models.json") or {}
        self.video = video.get("models") or {}
        self.generic = video.get("generic_adapter") or {}
        self.retired = dict(video.get("retired") or {})
        self.image = (documents.get("image_models.json") or {}).get("models") or {}
        self.image_document = documents.get("image_models.json") or {}
        self.audio = documents.get("audio_models.json") or {}
        self.routing = documents.get("routing.json") or {}
        self.phrases = documents.get("phrasebook.json") or {}
        self.aliases = {}
        for name, facts in self.video.items():
            self.aliases[normalised_name(name)] = name
            for alias in facts.get("aliases") or []:
                self.aliases.setdefault(normalised_name(alias), name)
        self.retired_names = {normalised_name(name): name for name in self.retired}
        dates = [read_date(document.get("checked_on")) for document in documents.values() if isinstance(document, dict)]
        dates = [date for date in dates if date]
        self.checked_on = min(dates) if dates else None

    @property
    def present(self):
        return bool(self.video)

    def find(self, name):
        """(exact name, facts, retired name or None) for a model name or alias; a retired name gives its first
        replacement; (None, None, None) when unknown."""
        key = normalised_name(name)
        if key in self.aliases:
            canonical = self.aliases[key]
            return canonical, self.video[canonical], None
        if key in self.retired_names:
            old = self.retired_names[key]
            for replacement in self.retired.get(old) or []:
                if replacement in self.video:
                    return replacement, self.video[replacement], old
        return None, None, None

    def display(self, name):
        facts = self.video.get(name) or {}
        return facts.get("name") or name

    def age_days(self, today):
        return (today - self.checked_on).days if self.checked_on else None

    def phrase(self, *path, default=""):
        node = self.phrases
        for key in path:
            if not isinstance(node, dict) or key not in node:
                return default
            node = node[key]
        return node if node is not None else default

    def need(self, name):
        return (self.routing.get("needs") or {}).get(name) or {}


# ---------------------------------------------------------------- small helpers for words and numbers

def number_text(value):
    """17 for 17.0, 16.5 for 16.5."""
    if value is None:
        return "?"
    value = float(value)
    return str(int(value)) if abs(value - round(value)) < 1e-9 else seconds_text(value)


def money(value):
    return f"${value:,.2f}"


def ordinal(number):
    number = int(number)
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"


def mm_ss(seconds):
    seconds = max(0, int(round(seconds)))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def mm_ss_ms(seconds):
    whole = max(0.0, float(seconds))
    return f"{int(whole // 60):02d}:{whole % 60:06.3f}"


def sentence(text):
    """One sentence: first letter capital, ending with a full stop (unless it ends with other punctuation)."""
    text = re.sub(r"\s+", " ", str(text or "")).strip().strip(";,")
    if not text:
        return ""
    text = text[0].upper() + text[1:]
    return text if text[-1] in ".!?\"" else text + "."


STARTING_WORDS = {"the", "a", "an", "she", "he", "they", "her", "his", "their", "it", "its", "both", "nobody", "everyone",
                  "one", "two", "three", "then", "and", "as", "at", "in", "on", "from", "with", "when", "while", "after",
                  "before", "still", "only", "all", "each", "this", "that", "these", "those", "there", "here", "no",
                  "some", "someone", "something", "late", "early", "slowly", "quickly", "later", "first", "now"}


def lower_first(text):
    """The first letter in lower case when the first word is an ordinary word, never a name ('Iona' stays)."""
    text = str(text or "").strip()
    first = re.sub(r"[^A-Za-z]", "", text.split()[0]) if text.split() else ""
    if first.lower() in STARTING_WORDS or (first and first[0].islower()):
        return text[:1].lower() + text[1:]
    return text


RESEARCH_CODE = (r"(?:blueprint\s)?(?:[A-D]\d{1,2}|K\d{1,2}|[A-Z]{2,6}-\d{2}[a-z]?|\d{1,2}(?:\.\d{1,2})+|§\s?\d+(?:\.\d+)*"
                 r"|R\d+|[Rr]ule\s\d+|Recipe\s\d+|Ex\d+|L\d+)")
RESEARCH_GROUP = RESEARCH_CODE + r"(?:[\s:]+" + RESEARCH_CODE + r")*"
RESEARCH_BRACKET = re.compile(r"\s*\((?:" + RESEARCH_GROUP + r")(?:\s*[;,]\s*(?:" + RESEARCH_GROUP + r"))*\)")
RESEARCH_TAIL = re.compile(r"(?:\s*[;,]\s*(?:" + RESEARCH_GROUP + r"))+(?=\))")


def plain_words(text):
    """The words a person reads: research codes like '(C2 Rule 15)' or '; K24' taken out (they stay in the code and
    in the machine files)."""
    text = RESEARCH_BRACKET.sub("", str(text or ""))
    text = RESEARCH_TAIL.sub("", text)
    text = re.sub(r",\s*" + RESEARCH_GROUP + r"\)", ")", text)
    return re.sub(r"\s+([.,;:])", r"\1", text)


def plain_page(lines_text):
    """plain_words on every line of a page except inside the prompt boxes."""
    out, inside = [], False
    for line in lines_text.split("\n"):
        if line.startswith("```"):
            inside = not inside
            out.append(line)
            continue
        out.append(line if inside else plain_words(line))
    return "\n".join(out)


def and_list(words):
    words = [word for word in words if word]
    if len(words) <= 1:
        return "".join(words)
    return ", ".join(words[:-1]) + " and " + words[-1]


def straight_quotes(text):
    for curly, straight in QUOTES.items():
        text = text.replace(curly, straight)
    return text


def words_in(text):
    return len([piece for piece in str(text or "").split() if re.search(r"\w", piece)])


def is_none(value):
    return value is None or normalise_word(str(value)) in ("", "none", "open", "auto")


def parse_span(text):
    match = re.match(r"^\s*(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)\s*$", str(text or ""))
    return (float(match.group(1)), float(match.group(2))) if match else None


def swap_image_sides(text):
    """Swap image-side words (frame left, right of the lens, the left edge ...) for a prompt whose picture is flipped
    in the edit; own sides ('her left hand') stay (C3 L27)."""
    def swap(match):
        word = match.group(0)
        other = "right" if word.lower() == "left" else "left"
        return other.capitalize() if word[0].isupper() else other
    return IMAGE_SIDE_PHRASES.sub(swap, text)


def swap_own_sides(text):
    """Every left and right in a record's words turned to the other side: 'a plain gold ring on her left hand' ->
    '... on her right hand'. Used where the picture the model makes shows an element pre-reversed (B1 method 1:
    "ring on the other hand, bandage on the other palm"): a mirrored element made as it finally appears (the direct
    route), or an element shown normally made before the clip's flip (routes a and b)."""
    def turn(match):
        word = match.group(0)
        other = "right" if word.lower() == "left" else "left"
        return other.capitalize() if word[0].isupper() else other
    return re.sub(r"\b(?:left|right)\b", turn, text or "", flags=re.IGNORECASE)


def shows_pre_reversed(breakdown, shot, element, turned):
    """True when the picture described shows the element reversed from its own words: a mirrored element in a
    picture that is not flipped after, or an element shown normally in a picture that is (8.5; B1 method 1)."""
    try:
        state = (shot_mirror_states(breakdown, shot).get(element_of(element)) or {}).get("mirror_state")
    except Exception:  # the mirror states need the eras; a gap there must not stop the prompts
        return False
    if state not in ("mirrored", "normal"):
        return False
    return (state == "mirrored") != bool(turned)


# ---------------------------------------------------------------- the words of the records, made fit for a prompt

CUTAWAY_WORDS = re.compile(r"(?:^|(?<=[;,.]))\s*(?:(?:after|at|on|from) the |a )?cut ?aways?(?: (?:to|on) [^,;.]+)?"
                           r"(?: ?(?:,|;|:|and|then)\s*)?|(?:the film |the edit )?cuts? away(?: (?:to|on) [^,;.]+)?",
                           re.IGNORECASE)


def heard_line(item, entry):
    """The words a shot hears of a speech: the hear item's words when they split the speech at a phrase (time floors
    count them so), else the whole speech (the second full run, Project notes 39: the whole speech was sent)."""
    whole = re.sub(r"\s*\([^)]*\)\s*", " ", straight_quotes(str((entry or {}).get("text") or ""))).strip()
    part = straight_quotes(str(item.get("words") or "")).strip().strip('"').strip()
    return part if part and whole and speech_words_part(part, whole) else whole


def without_quoted_speech(shows, spoken):
    """A moment's words without a quotation of part of a heard speech: the line is sent once, as the line (the second
    full run, Project notes 39: a speech quoted across two moments was pasted twice)."""
    def without_quotation(match):
        if not any(speech_words_part(match.group(2), line) for line in spoken):
            return match.group(0)
        # a quoted cue ('at "Jude's blood" her eyes go down') keeps its place as "at that line" (the cross-examination)
        return f"{match.group(1)}that line" if match.group(1) else ""
    shows = re.sub(r'(\b(?:at|on|after)\s+)?"([^"]+)"', without_quotation, shows)
    return re.sub(r"\s*[:,]\s*(?=;|$)", "", shows)


# A start picture carries the look and the people's descriptions: with one, a moment's or the end's piece that
# repeats them (a clause of at least this many words, as GEN-05 reads it) is left out, so the prompt is the action.
PICTURE_CLAUSE_WORDS_MIN = 4


def picture_clauses(texts):
    """The clauses of the look block and descriptions a start picture carries, as GEN-05 splits them."""
    found = []
    for text in texts:
        for piece in re.split(r"[.;,:!?]\s*|\s+[-–—]\s+|\(|\)", straight_quotes(str(text or ""))):
            words = piece.split()
            if len(words) >= PICTURE_CLAUSE_WORDS_MIN:
                found.append(" ".join(words).casefold())
    return found


def action_only(words, clauses):
    """A moment's words without the pieces (between semicolons and commas) that hold a clause the start picture
    carries: "The ship's dark side, stars on every side; the woman comes out" keeps "The ship's dark side; the woman
    comes out" when the look block says "stars on every side"."""
    if not clauses or not words:
        return words
    kept_parts = []
    for part in words.split(";"):
        pieces = [piece for piece in part.split(",")
                  if not any(clause in " ".join(piece.split()).casefold() for clause in clauses)]
        if pieces:
            kept_parts.append(",".join(pieces).strip())
    return "; ".join(part for part in kept_parts if part).strip(" ;,")


# Composited text (8.5, K17): the model draws a plain surface and the words are laid on after. The second full run
# (Project notes 39) found the compiler writing "Plain, unmarked surfaces." and then the shot's own "a toy carriage
# marked F". In a moment, the end or a thing's description, words after a marking or reading word are said as words
# added later; words that stand for their thing ("her elbow hits the red STOP", "level with PASSAGE FLOOR") become
# the thing the TEXT's title names ("the red button"), and a single mark becomes a letter or a number (its
# cross-examination: "the red label with words added later" lost the button, and "an mark" its article).
WORDS_ADDED_LATER = "with words added later"
MARKING_WORDS = ("marked", "labelled", "labeled", "printed", "stitched", "stamped", "stencilled", "stenciled",
                 "written", "lettered")
LETTER_WORDS = ("letter", "letters", "word", "words", "number", "numbers")
TEXT_KIND_NOUNS = {"sign": "sign", "label": "label", "stencil": "stencil", "screen": "screen", "monitor": "screen",
                   "document": "page", "visor": "readout", "tag": "tag"}
DETERMINERS = ("the", "a", "an", "its", "her", "his", "their", "this", "that", "one")
READING_WORDS = ("reading", "reads", "saying", "says", "spelling", "spells")
LEVEL_WITH_WORDS = ("level", "even", "flush", "line")  # "level with PASSAGE FLOOR": a place, not words it bears
REPLACED = "\x00"  # marks a replacement until its article is fitted ("an F" becomes "a letter")
BACKWARDS_WORDS = re.compile(r"\b(?:backwards?|reversed|mirror(?:ed)?)\s+(?:text|writing|letters|lettering|words)\b"
                             r"|\b(?:text|writing|letters|lettering|words)\s+(?:backwards?|reversed|in reverse)\b",
                             re.IGNORECASE)


def thing_named_by_title(title, words):
    """The thing a TEXT's words are on, from its title without the words ("The STOP button" gives "button", "The
    diagram's line label" gives "diagram's line label"), or "" when the title says no more than the words, ends
    on a possessive, or holds a name in capitals."""
    rest = re.sub(r"(?<!\w)" + re.escape(words) + r"(?!\w)", " ", str(title or ""), flags=re.IGNORECASE)
    rest = re.sub(r"^(?:the|a|an)\s+", "", " ".join(rest.split()).strip(" ,;:."), flags=re.IGNORECASE)
    rest = rest[:1].lower() + rest[1:]
    if not re.search(r"[a-z]{3}", rest) or re.search(r"['\u2019]s?$|^['\u2019]", rest) or re.search(r"[A-Z]", rest) \
            or len(rest.split()) > 6:
        return ""
    return rest


def leave_words_for_later(text, texts_composited):
    """text with the words of each composited TEXT [(words, kind) or (words, kind, thing)] said as words added
    later, as the thing they stand for, or, for a single mark, as a letter or a number."""
    if not text or not texts_composited:
        return text
    for composited in texts_composited:
        words, kind = composited[0], composited[1]
        thing = composited[2] if len(composited) > 2 else ""
        flags = re.IGNORECASE if words != words.upper() or not re.search(r"[A-Z]", words) else 0
        pattern = re.compile(r"(?:\b(?:" + "|".join(READING_WORDS) + r")\s+)?(?<!\w)" + re.escape(words) + r"(?!\w)",
                             flags)
        single_mark = len(words.split()) == 1 and len(words) <= 3
        source = text

        def replacement(match):
            before = [word.lower() for word in re.findall(r"[A-Za-z']+", source[:match.start()])[-3:]]
            if match.group(0).split()[0].lower() in READING_WORDS:
                return WORDS_ADDED_LATER
            if before[-1:] == ["with"] and before[-2:-1] and before[-2] in LEVEL_WITH_WORDS:
                before = before + ["of"]  # "level with PASSAGE FLOOR" names the thing, below
            elif before[-1:] == ["with"]:
                return WORDS_ADDED_LATER[len("with "):]
            if before[-1:] in (["and"], ["or"]) and re.search(r"added later,? (?:and|or)\s*$", source[:match.start()]):
                return WORDS_ADDED_LATER  # "labelled CONTROL and VALE": one phrase, joined below
            if before[-1:] and before[-1] in LETTER_WORDS:
                return ""  # "a large black letter F painted on its side": the letter, without its words
            if before[-1:] and (before[-1] in MARKING_WORDS or before[-1] in TEXT_KIND_NOUNS
                                or before[-1] in TEXT_KIND_NOUNS.values()):
                return WORDS_ADDED_LATER
            determined = any(word in DETERMINERS for word in before[-2:])
            if single_mark:
                noun = "number" if re.search(r"[0-9]", words) else "letter" if words.isalpha() else "mark"
                return REPLACED + (noun if determined else f"a {noun}")
            if thing:
                return REPLACED + (thing if determined else f"the {thing}")
            noun = f"{TEXT_KIND_NOUNS.get(normalise_word(kind or ''), 'surface')} {WORDS_ADDED_LATER}"
            return REPLACED + (noun if determined else f"a {noun}")
        text = pattern.sub(replacement, source)
    text = re.sub(r"\b([Aa])n(\s+)" + REPLACED + r"(?=[^aeiouAEIOU])", r"\1\2", text)
    text = re.sub(r"\b([Aa])(\s+)" + REPLACED + r"(?=[aeiouAEIOU])", r"\1n\2", text)
    text = text.replace(REPLACED, "")
    text = BACKWARDS_WORDS.sub("words added later", text)
    text = re.sub(r"(with words added later)(?:,? (?:and|or) \1)+", r"\1", text)
    return re.sub(r"[ \t]{2,}", " ", text)


class WordFixer:
    """Word swaps (torch becomes flashlight), negation rewrites and banned-word guards for the prompt's own words.
    Pasted keys (fixed descriptions, state lines, the look block) get the word swaps only (key_words): the project's
    swaps apply to every word the model reads, and GEN-04 accepts exactly the swapped form."""

    def __init__(self, adapters, words, project_record):
        self.swaps = project_prompt_swaps(words, project_record)
        rewrites = adapters.phrase("negation_rewrites", default={}) or {}
        self.patterns = [(re.compile(entry["find"], re.IGNORECASE), entry["replace"]) for entry in rewrites.get("patterns") or []]
        self.gerunds = rewrites.get("gerunds") or {}
        groups = (words.get("banned_prompt_words") or {}).get("groups") or {}
        banned = [word for group in groups.values() for word in group]
        banned += swap_sources_banned(self.swaps)
        self.banned = sorted(set(banned), key=lambda word: (-len(word), word))
        self.allowed_lines = {re.sub(r"\s+", " ", line).strip().casefold()
                              for line in (words.get("allowed_negations") or {}).get("lines") or []}
        self.delivery = {key: value for key, value in (adapters.phrase("delivery_rewrites", default={}) or {}).items()
                         if key not in ("note", "marks")}
        # The words a model with no negative side would show (absence) or freeze on (stillness), and the words the
        # H3 route also keeps out (talk about speaking, comparisons): _config/rules/words.json (Project notes 42 and 43).
        self.word_lists = {
            "absence": list((words.get("absence_words") or {}).get("words") or []),
            "stillness": list((words.get("stillness_words") or {}).get("words") or [])
            + list((words.get("stillness_words") or {}).get("phrases") or []),
            "talk": list((words.get("talk_about_speaking") or {}).get("words") or []),
            "comparison": list((words.get("comparison_markers") or {}).get("markers") or []),
        }
        self.allowed_phrases = [phrase.casefold() for phrase in
                                (words.get("absence_words") or {}).get("allowed_phrases") or []]
        stillness = words.get("stillness_words") or {}
        self.verb_lists = (set(stillness.get("small_actions") or []), set(stillness.get("body_parts") or []),
                           set(stillness.get("pose_words") or []))

    def verb_of(self, gerund):
        gerund = gerund.lower()
        if gerund in self.gerunds:
            return self.gerunds[gerund]
        stem = gerund[:-3]
        if len(stem) > 2 and stem[-1] == stem[-2] and stem[-1] not in "lsz":
            return stem[:-1]
        if stem.endswith("v") or (len(stem) <= 4 and re.search(r"[^aeiou][aeiou][kstzcg]$", stem)):
            return stem + "e"
        return stem

    def swap_words(self, text):
        return swap_prompt_words(text, self.swaps)

    def key_words(self, text):
        """A pasted key (fixed description, state line, look block) with the word swaps made and nothing else."""
        return swap_prompt_words(text, self.swaps) if text else text

    def rewrite_negations(self, text):
        for pattern, replacement in self.patterns:
            if "{verb}" in replacement:
                text = pattern.sub(lambda match, template=replacement: template.replace("{verb}", self.verb_of(match.group(1))), text)
            else:
                text = pattern.sub(replacement, text)
        return re.sub(r"\s+,", ",", re.sub(r"\s{2,}", " ", text)).strip()

    def negation_left(self, text):
        """The part of a sentence still negating something visible, or None."""
        if re.sub(r"\s+", " ", text).strip().casefold() in self.allowed_lines:
            return None
        rest = ALLOWED_NEGATION.sub(" ", text)
        match = NEGATION.search(rest)
        return match.group(0) if match else None

    def banned_in(self, text):
        return [word for word in self.banned if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", text, re.IGNORECASE)]

    def kept_out_word(self, text, lists):
        """The first word of the named lists (absence, stillness, talk, comparison) in text, or None. Spoken lines
        (<d>...</d>), printed words in quotation marks and the allowed phrases ('with no camera movement
        whatsoever', 'N/A') are never counted."""
        plain = re.sub(r"<d>.*?</d>", " ", straight_quotes(str(text or "")), flags=re.DOTALL)
        plain = re.sub(r'"[^"]*"', " ", plain).casefold()
        for phrase in self.allowed_phrases:
            plain = plain.replace(phrase, " ")
        for name in lists:
            for word in sorted(self.word_lists.get(name) or [], key=len, reverse=True):
                lowered = word.casefold()
                if lowered == "n't":
                    match = re.search(r"\b\w+n't\b", plain)
                else:
                    match = re.search(r"(?<![\w-])" + re.escape(lowered) + r"(?![\w-])", plain)
                if match:
                    return match.group(0)
        return None

    def has_verb(self, text):
        """True when the words hold a verb ('breathes', 'is', 'will turn'), by the plan check's own reading
        (checks_craft_reasons_words.looks_like_a_verb)."""
        from .checks_craft_reasons_words import looks_like_a_verb
        words = [word.strip(".,;:'\"").lower() for word in str(text or "").split()]
        words = [word for word in words if word]
        small_actions, body_parts, pose_words = self.verb_lists
        return any(word in BE_AND_HAVE or looks_like_a_verb(words, index, small_actions, body_parts, pose_words)
                   for index, word in enumerate(words))

    def stands_alone(self, text, action=False):
        """True when what a cut leaves can stand as a clause of its own: two words or more, starting with its own
        subject (never a lone adverb such as 'unsteady', a lone place such as 'either side of the scar', or a verb
        with its subject cut away such as 'then looks away'), and, for an action, holding a verb (review N2)."""
        words = re.findall(r"[A-Za-z][\w'-]*", str(text or ""))
        if len(words) < 2 or len(re.findall(r"[A-Za-z][\w'-]*", re.split(r",", str(text))[0])) < 2:
            return False  # 'unsteady', or 'level, from the counter': a lone word where the subject stood
        first, lowered = words[0], words[0].lower()
        if lowered in NOT_A_SUBJECT_START or (lowered.endswith("ly") and not first[:1].isupper()):
            return False
        if (lowered not in SUBJECT_STARTS and not first[:1].isupper() and not lowered.endswith("'s")
                and re.search(r"(?:[^s]s|ing|ed)$", lowered)):
            return False  # 'looks away', 'turning back': the verb's subject was in the part cut
        return self.has_verb(text) if action else True

    def cut_kept_out(self, text, lists, action=False):
        """(the words kept, True when the first clause's first piece was kept, [the pieces cut]) of text with only the
        words of the named lists cut out: each comma piece holding one is cut at its first 'with', 'and', 'or', 'where'
        or 'but' before the word ('a bare, clean kitchen with nothing on the walls' -> 'a bare, clean kitchen'), or
        goes whole when what stands before is under two words. A clause whose first piece goes whole must leave words
        that stand alone (stands_alone), and an action must keep a verb; otherwise the whole clause goes and is listed,
        never a fragment such as 'unsteady' or 'either side of the scar' (review N2)."""
        text = straight_quotes(str(text or "")).strip()
        if not text or not lists or not self.kept_out_word(text, lists):
            return text, True, []
        sentences = [piece for piece in re.split(r"(?<=[.!?])\s+", text) if piece.strip()]
        if len(sentences) > 1:
            kept_sentences, first_kept, cut = [], True, []
            for index, piece in enumerate(sentences):
                words, first, pieces = self.cut_kept_out(piece, lists, action)
                cut += pieces
                first_kept = first_kept and (first or index > 0)
                if words:
                    kept_sentences.append(words.rstrip(".!?") + (piece.strip()[-1] if piece.strip()[-1] in "!?" else "."))
            return " ".join(kept_sentences), first_kept, cut
        ending = text[-1] if text[-1] in ".!?" else ""
        text = text.rstrip(".!?")
        kept_clauses, first_kept, cut = [], True, []
        for clause_index, clause in enumerate(clause for clause in re.split(r"\s*;\s*", text) if clause.strip()):
            if not self.kept_out_word(clause, lists):
                kept_clauses.append(clause.strip())
                continue
            kept_pieces, clause_cut, subject_lost = [], [], False
            for piece_index, piece in enumerate(piece for piece in re.split(r",\s*", clause) if piece.strip()):
                if not self.kept_out_word(piece, lists):
                    kept_pieces.append(piece)
                    continue
                lead = []
                for part in re.split(r"\s+(?=(?:with|and|or|where|but)\s)", piece):
                    if self.kept_out_word(part, lists):
                        break
                    lead.append(part)
                standing = " ".join(lead).strip()
                if standing and len(standing.split()) >= 2:
                    kept_pieces.append(standing)
                    clause_cut.append(piece[len(standing):].strip())
                else:
                    clause_cut.append(piece.strip())
                    subject_lost = subject_lost or piece_index == 0
            remainder = ", ".join(piece.strip() for piece in kept_pieces if piece.strip())
            if remainder and ((subject_lost and not self.stands_alone(remainder, action))
                              or (action and self.has_verb(clause) and not self.has_verb(remainder))):
                clause_cut, remainder = [clause.strip()], ""  # a fragment would be left: the whole clause goes
            cut += [piece for piece in clause_cut if piece]
            if remainder:
                kept_clauses.append(remainder)
            if clause_index == 0 and (subject_lost or not remainder):
                first_kept = False
        kept = "; ".join(kept_clauses).strip(" ;,:")
        return (kept + ending if kept else ""), first_kept, cut

    def drop_kept_out(self, text, lists, dropped=None):
        """text with only the words of the named lists cut out (cut_kept_out), never leaving a fragment; each piece
        left out is added to dropped."""
        if not lists or not text or not self.kept_out_word(text, lists):
            return text
        kept, _, cut = self.cut_kept_out(text, lists)
        if dropped is not None:
            dropped.extend(piece for piece in cut if piece)
        return kept.strip()

    def fix(self, text, left_out=None, what="", keep_out=(), why_out=""):
        """Swap words and rewrite negations; a sentence that still negates or holds a banned word is left out (and
        listed in left_out). keep_out names word lists (absence, stillness, talk, comparison) whose clauses are left
        out first, for a model with no negative side (H3), each listed with why_out."""
        text = self.rewrite_negations(self.swap_words(str(text or "")))
        if keep_out:
            dropped = []
            text = self.drop_kept_out(text, keep_out, dropped)
            if left_out is not None:
                for piece in dropped:
                    left_out.append(f"{what}: \"{piece}\": {why_out or 'left out, because the model would show it'}")
        kept = []
        for piece in re.split(r"(?<=[.!?;])\s+", text):
            if not piece.strip():
                continue
            problem = self.negation_left(piece)
            banned = self.banned_in(piece)
            if problem or banned:
                if left_out is not None:
                    reason = (f"it negates something visible ('{problem}'), which makes models show it (C3 L14)" if problem
                              else f"it holds {', '.join(repr(word) for word in banned)}, banned from prompts (GEN-12)")
                    left_out.append(f"{what}: \"{piece.strip()}\": {reason}")
                continue
            kept.append(piece.strip())
        return " ".join(kept).strip()

    def delivery_words(self, text):
        text = (text or "").strip().strip("()").strip()
        if not text or is_none(text):
            return ""
        lowered = text.casefold()
        if lowered in self.delivery:
            return self.delivery[lowered]
        if NEGATION.search(text) or self.banned_in(text):
            return ""
        return text


# ---------------------------------------------------------------- what a shot needs

@dataclass
class Person:
    """One subject in a shot, with the words the prompt uses for them."""
    reference: str
    element: str
    item: object
    name: str
    noun: str
    pronoun: tuple
    fixed_description: str = ""
    state_line: str = ""
    label: str = ""
    at: str = ""
    faces: str = ""
    flipped: bool = False
    is_person: bool = True


@dataclass
class ShotPlan:
    """What making one shot needs, worked out from its records before any model is chosen."""
    shot: object
    identifier: str
    scene: str
    kind: str
    video: bool
    route: str
    route_note: str
    held: bool
    held_why: str
    screen_time: float
    needed_s: float
    mirror: object
    prompt_flipped_all: bool
    start_picture: bool = False
    end_picture: bool = False
    guide_video: bool = False
    still_only: bool = False
    performance: bool = False
    people: list = dataclass_field(default_factory=list)
    on_screen: list = dataclass_field(default_factory=list)
    off_screen: list = dataclass_field(default_factory=list)
    silent_picture: bool = False
    silent_why: str = ""
    needs: list = dataclass_field(default_factory=list)
    recurring: bool = False
    cost_class: str = "easy"
    faces_to_reference: int = 0
    author_model: str = None
    author_model_why: str = ""
    whole_for_speech: bool = False
    speech_spans: list = None  # [(from, to)] seconds of the shot's speeches; None when a time is not known
    handles_s: float = 0.75

    @property
    def sends_speech(self):
        return bool(self.on_screen) and not self.silent_picture


def character_is_recurring(breakdown, element):
    record = breakdown.record(element, "CHARACTER")
    if record is None:
        return False
    if normalise_word(record.get("tier") or "") in ("principal", "minor"):
        return True
    return any(voice.get("character") == element for voice in breakdown.records_of("VOICE"))


def person_noun(adapters, fixed_description, record):
    nouns = adapters.phrase("people", "nouns", default=["woman", "man", "person"])
    text = f" {str(fixed_description or '').lower()} "
    found = [(text.find(f" {noun} "), noun) for noun in nouns if f" {noun} " in text or f" {noun}," in text]
    found = [(index if index >= 0 else text.find(f" {noun},"), noun) for index, noun in found]
    if found:
        return sorted(found)[0][1]
    if record is not None and normalise_word(record.get("tier") or "") == "non_human":
        return "figure"
    return adapters.phrase("people", "fallback", default="person")


def name_of(breakdown, element, fixed_description):
    """The name the prompt gives an element: the fixed description's first words when they are a name ('Dr Saye'),
    else the plain name."""
    first = str(fixed_description or "").split(",")[0].strip()
    if first and len(first.split()) <= 3 and first[:1].isupper() and not first.lower().startswith(("a ", "an ", "the ")):
        return first
    if element and element.startswith("CH-"):
        return person_name(element)
    return element_name(breakdown, element)


def state_record(breakdown, reference):
    record = breakdown.record(reference)
    return record if record is not None and record.type_name == "STATE" else None


def feature_shown(shot, feature):
    """True for a plot-sided feature the shot can show: in a close shot or an insert only when the shot's own words
    name it (a ring in a ring insert), elsewhere always (C1 R22)."""
    if not feature.get("plot"):
        return False
    size = normalise_word(shot.get("size") or "")
    if size not in ("insert", "close_up", "extreme_close_up") and normalise_word(shot.get("kind") or "") != "insert":
        return True
    words = " ".join([split_item(written).get("does") or "" for written in shot.get_all("subject")] +
                     [split_item(written).get("shows") or "" for written in shot.get_all("moment")] +
                     [split_item(written).first or "" for written in shot.get_all("thing")] +
                     [shot.get("focus_on") or "", shot.get("must_show") or "", shot.get("end") or ""]).lower()
    nouns = re.findall(r"[a-z]+", str(feature.get("feature") or "").lower())
    return bool(nouns) and nouns[-1].rstrip("s") in words


HAND_NOUNS = ("ring", "palm", "hand", "finger", "wrist", "glove", "nail", "knuckle", "thumb")


def side_words(adapters, feature, where):
    """Where a sided feature falls, in words: hand words for rings and palms, side words for the rest."""
    nouns = re.findall(r"[a-z]+", str(feature.get("feature") or "").lower())
    on_hand = any(noun.rstrip("s") in HAND_NOUNS for noun in nouns)
    if where in ("nearest the camera", "far from the camera") and not on_hand:
        return "on the side nearest the camera" if where == "nearest the camera" else "on the far side"
    return adapters.phrase("side", where, default="")


def build_people(breakdown, adapters, shot, mirror):
    """The subjects of a shot as Person, with the prompt side of each (flipped routes swap sides, 8.5)."""
    people = []
    flipped_route = mirror.route in ("flip_all", "flip_with_mirrored_references")
    try:
        sides = {entry["element"]: entry for entry in image_sides(breakdown, shot)}
    except Exception:  # sides need the set plan and eras; a gap there must not stop the prompts
        sides = {}
    for item in subject_items(breakdown, shot):
        reference = item.first.strip()
        if is_none(reference):
            continue
        element = element_of(reference)
        record = breakdown.record(element)
        state = state_record(breakdown, reference)
        fixed = record.get("fixed_description") if record is not None else ""
        noun = person_noun(adapters, fixed, record) if element.startswith("CH-") else "thing"
        pronouns = tuple(adapters.phrase("people", "pronouns", noun, default=["they", "their", "Their"]))
        entry = sides.get(element) or {}
        flipped = flipped_route or (mirror.route == "plate" and entry.get("mirror_state") == "mirrored")
        people.append(Person(
            reference=reference, element=element, item=item, name=name_of(breakdown, element, fixed), noun=noun,
            pronoun=pronouns if len(pronouns) == 3 else ("they", "their", "Their"),
            fixed_description=str(fixed or "").strip() if not is_none(fixed) else "",
            state_line=str(state.get("state_line") or "").strip() if state is not None and not is_none(state.get("state_line")) else "",
            at=normalise_word(item.get("at") or ""),
            faces=(item.get("faces") or "").strip() if re.match(r"^(CH|PR|LOC)-", (item.get("faces") or "").strip())
            else normalise_word(item.get("faces") or ""),
            flipped=flipped, is_person=element.startswith("CH-")))
    return people


def speech_entry(breakdown, raw, identifier):
    entry = dict(breakdown.speech(identifier) or {})
    entry.update({key: value for key, value in (raw.get(identifier) or {}).items() if value is not None})
    return entry


def analyse_shot(breakdown, adapters, shot, raw_speeches):
    """A ShotPlan: the shot's route, its held-take status, its speeches, the pictures it needs and its needs (8.4)."""
    constants = breakdown.constants
    identifier = shot.identifier
    kind = normalise_word(shot.get("kind") or "live")
    route = normalise_word(shot.get("route") or "auto") or "auto"
    screen_time = number_of(shot.get("screen_time"), 0.0) or 0.0
    handles = constant(constants, "handles_s", 0.75)
    held, held_why = held_take(breakdown, shot)
    try:
        mirror = mirror_route(breakdown, shot)
    except Exception:
        from .derive_fields import MirrorRoute
        mirror = MirrorRoute("open", "open", False, ["the mirror route could not be worked out"])
    plan = ShotPlan(shot=shot, identifier=identifier, scene=scene_of(identifier), kind=kind, video=True, route=route,
                    route_note="", held=held, held_why=held_why, screen_time=screen_time,
                    needed_s=round(screen_time + 2 * handles, 3), mirror=mirror,
                    prompt_flipped_all=mirror.route in ("flip_all", "flip_with_mirrored_references"))
    plan.people = build_people(breakdown, adapters, shot, mirror)
    if kind in ("card", "black") or route == "composite_only":
        plan.video = False
        plan.route = "composite_only"
        plan.route_note = ("a card: drawn as a text graphic and composited (K17)" if kind == "card"
                           else "black or a composite: made in the edit, no clip" if kind == "black"
                           else "composited from its elements in finishing, no clip")
    elif route == "still_with_move":
        plan.video = False
        plan.still_only = True
        plan.start_picture = True
        plan.route_note = "a checked still, moved slowly in the editor (C1 Ex8; C1 rule 24)"
    else:
        motion = bool(shot.get_all("motion")) and not all(is_none(value) for value in shot.get_all("motion"))
        physics = not is_none(shot.get("physics_note"))
        previs = number_of(shot.get("previs_level"), 0) or 0
        if route == "performance_transfer":
            plan.performance = True
            plan.start_picture = True
            plan.route_note = "acted on a phone and copied onto the character (C1 R12)"
        if route == "guide_video" or motion or physics or previs >= 3:
            plan.guide_video = True
            plan.route_note = plan.route_note or "camera and blocking copied from a grey preview video (C1 R4, R8)"
        if route == "start_end_pictures":
            plan.start_picture = plan.end_picture = True
            plan.route_note = "an exact first and last picture, the last edited from the first (C2 Rule 15)"
        elif route == "start_picture":
            plan.start_picture = True
            plan.route_note = "a checked start picture; the prompt is motion only (C3 R1)"
        elif route == "auto" and is_yes(shot.get("framing_critical")) and not plan.guide_video:
            plan.start_picture = True
            plan.route_note = "the framing is critical, so a checked start picture fixes it (C2 Rule 2; C1 R3)"
        elif route == "text":
            plan.route_note = "words only, no pictures attached"
        elif route in ("references", "auto") and not plan.route_note:
            plan.route_note = "reference pictures of every element state in frame (C2 Rule 1)"
        if mirror.route == "plate" and not plan.guide_video:
            plan.start_picture = True
            plan.route_note = ("the plate route of the mirror world: the place and its mirrored people made as one picture, "
                               "flipped, the others added unflipped, then animated from that start picture (8.5)")
    # speeches
    heard = [split_item(written) for written in shot.get_all("hear")]
    speakers_on = []
    for item in heard:
        if not item.first or is_none(item.first):
            continue
        identifier_speech = item.first.strip()
        entry = speech_entry(breakdown, raw_speeches, identifier_speech)
        if not entry.get("speaker"):
            # the story's speeches are missing: the speaker is taken to be the person the shot is on
            focus = element_of(shot.get("focus_on") or "")
            first_person = next((person.element for person in plan.people if person.is_person), "")
            entry["speaker"] = focus if focus.startswith("CH-") else first_person
            entry["speaker_guessed"] = True
        if normalise_word(item.get("speaker") or "") == "on_screen":
            plan.on_screen.append((identifier_speech, item, entry))
            speaker = element_of(entry.get("speaker") or "")
            if speaker and speaker not in speakers_on:
                speakers_on.append(speaker)
        else:
            plan.off_screen.append((identifier_speech, item, entry))
    most = int(number_of(constant(breakdown.constants, "on_screen_speakers_per_clip_max", 1), 1))
    if len(speakers_on) > most:
        plan.silent_picture = True
        plan.silent_why = (f"{len(speakers_on)} people are seen speaking in one clip, so the picture is made silent, each "
                           "line is laid in from its voice take and the mouths are fitted after (C1 R2; D3 §12)")
    if plan.video and plan.sends_speech and not plan.held and not cut_points(breakdown, shot):
        # The second full run (Project notes 39): a shot with no planned cutaway, longer than its model's clip, was
        # chained through its speech. Like a held take, it goes whole to a model whose clip is long enough, when one
        # exists; a shot with a planned cutaway is still split there.
        plan.whole_for_speech = any(is_candidate(facts) and round_up_to(plan.needed_s, allowed_lengths(facts) or [])
                                    is not None for facts in adapters.video.values())
        plan.handles_s = constant(constants, "handles_s", 0.75)
        plan.speech_spans = []
        for identifier_speech, item, _ in plan.on_screen + plan.off_screen:
            at = number_of(item.get("at"))
            words = item.get("words")
            part = speech_part(breakdown, identifier_speech, words.strip('"\u201c\u201d') if words else None)
            if at is None or part is None:
                plan.speech_spans = None  # when a line is spoken is not known: the shot is kept whole
                break
            plan.speech_spans.append((at, at + part[4]))
    plan.recurring = any(character_is_recurring(breakdown, person.element) for person in plan.people if person.is_person)
    plan.faces_to_reference = len([person for person in plan.people if person.is_person])
    written_model = shot.get("model")
    if written_model and not is_none(written_model):
        item = split_item(written_model)
        if item.first and not is_none(item.first):
            plan.author_model = item.first.strip()
            plan.author_model_why = (item.get("why") or "").strip()
    # needs (8.4)
    if plan.video:
        needs = []
        if plan.held and plan.needed_s > 15 + 1e-9:
            needs.append("long_take")
        if plan.performance:
            needs.append("performance_transfer")
        if plan.guide_video:
            needs.append("physics" if (not is_none(shot.get("physics_note")) or shot.get_all("motion")) else "guide_video")
        if plan.end_picture:
            needs.append("exact_start_end")
        if any(normalise_word((breakdown.record(person.element, "CHARACTER") or {}).get("tier") if breakdown.record(person.element, "CHARACTER") else "") == "non_human"
               for person in plan.people):
            needs.append("recurring_creature")
        if plan.sends_speech and any(character_is_recurring(breakdown, element_of(entry.get("speaker") or ""))
                                     for _, _, entry in plan.on_screen):
            needs.append("dialogue_recurring")
        size = normalise_word(shot.get("size") or "")
        if size in SIZES_WIDE and not heard:
            needs.append("wide_establishing")
        if not plan.sends_speech and size in SIZES_CLOSE and plan.people and any(person.is_person for person in plan.people):
            needs.append("silent_performance")
        plan.needs = needs
    written_cost = normalise_word(shot.get("cost_class") or "")
    if written_cost and written_cost != "none":
        plan.cost_class = written_cost
    elif not plan.video:
        plan.cost_class = "still_move" if plan.still_only else "graphic"
    elif plan.guide_video or plan.performance:
        plan.cost_class = "hard"
    elif plan.sends_speech:
        plan.cost_class = "dialogue"
    return plan


# ---------------------------------------------------------------- can a model make it, and which model

def model_price(facts, resolution, audio_on=True):
    """Dollars a generated second at a resolution, with or without sound; a range is priced at its high end; None when
    the model facts give no price."""
    prices = (facts or {}).get("price_usd_per_s")
    if not isinstance(prices, dict):
        return None
    keys = []
    if resolution:
        keys += [f"{resolution}_{'audio' if audio_on else 'silent'}", resolution]
    keys += ["audio" if audio_on else "silent", "default", "standard", "own_gpu"]
    if not audio_on:
        keys.append("audio")
    for key in keys:
        value = prices.get(key)
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, list) and value and all(isinstance(part, (int, float)) for part in value):
            return float(max(value))
    for key, value in prices.items():
        if isinstance(value, (int, float)) and re.match(r"^\d+p$|^\dk$", key):
            return float(value)
    return None


def is_silent_model(facts):
    audio = (facts or {}).get("audio")
    return audio is False or (isinstance(audio, str) and audio.split(",")[0].strip().lower() in ("none", "silent", "no"))


def is_route(facts):
    """True for a route entry (kind: route): a model plus the place it runs, such as MiniMax H3 in ComfyUI. A route
    is made only when asked (compile --route, or PROJECT video_route), never chosen by routing (Project notes 43)."""
    return normalise_word((facts or {}).get("kind") or "") == "route"


def is_candidate(facts):
    return (facts.get("status") == "current" and "generation" in (facts.get("use") or [])
            and bool(allowed_lengths(facts)) and not is_route(facts))


def chain_cuts_speech(plan, lengths):
    """True when chaining the shot on a model with these clip lengths (as clip_plan chains it) would cut through one
    of its speeches, or when that cannot be told: only then is a speaking shot kept whole (its cross-examination: a
    20-second shot whose line ends long before the first cut is chained on the scene's model as before)."""
    spans = getattr(plan, "speech_spans", None)
    handles = getattr(plan, "handles_s", 0.75)
    screen_time = getattr(plan, "screen_time", None)
    if spans is None or not screen_time or not lengths or max(lengths) - 2 * handles <= 0:
        return True
    count = math.ceil(screen_time / (max(lengths) - 2 * handles))
    splits = [screen_time / count * index for index in range(1, count)]
    return any(start + 1e-9 < split < end - 1e-9 for split in splits for start, end in spans)


def able(adapters, name, facts, plan, licensed_only=False):
    """(True, '') when the model can make the shot; else (False, why in plain words)."""
    display = adapters.display(name)
    if facts is None:
        return False, f"{name} is not in the model facts"
    if facts.get("status") == "retired":
        return False, f"{display} is retired"
    if "generation" not in (facts.get("use") or []):
        return False, f"{display} does not make new clips"
    lengths = allowed_lengths(facts)
    if not lengths:
        return False, f"{display}'s clip lengths are not known"
    if licensed_only and not facts.get("licensed_data"):
        return False, f"{display} is not trained on licensed footage only, and the project asks for that"
    if plan.held and round_up_to(plan.needed_s, lengths) is None:
        return False, (f"a held take ({plan.held_why}) of {number_text(plan.needed_s)} seconds with its handles is longer "
                       f"than {display} allows ({number_text(max(lengths))} seconds), and a held take is never split")
    if plan.whole_for_speech and round_up_to(plan.needed_s, lengths) is None and chain_cuts_speech(plan, lengths):
        return False, (f"a line is seen spoken in this shot of {number_text(plan.needed_s)} seconds with its handles, "
                       f"longer than {display} allows ({number_text(max(lengths))} seconds), and a shot is never split "
                       "through its speech")
    inputs = facts.get("inputs") or {}
    if plan.start_picture and not inputs.get("start_picture"):
        return False, f"{display} takes no start picture"
    if plan.end_picture and not inputs.get("end_picture"):
        return False, f"{display} takes no end picture"
    if (plan.guide_video or plan.performance) and not inputs.get("guide_video"):
        return False, f"{display} takes no guide video"
    if plan.sends_speech and is_silent_model(facts):
        return False, f"{display} makes no sound, and a line is seen spoken"
    if not plan.start_picture and plan.recurring:
        most = inputs.get("references_max")
        if isinstance(most, int) and plan.faces_to_reference > most:
            return False, f"{display} takes {most} reference pictures and this shot has {plan.faces_to_reference} faces"
    return True, ""


def default_resolution(adapters, facts, prefer=None):
    sizes = [str(size) for size in (facts.get("resolution") or [])]
    if prefer and prefer in sizes:
        return prefer
    for size in (adapters.routing.get("resolution") or {}).get("preference") or ["1080p", "2k", "768p", "720p", "480p", "360p"]:
        if size in sizes:
            return size
    return sizes[0] if sizes else None


def choose_scene_model(adapters, plans, licensed_only=False):
    """The scene model (8.4, K29): over the shots with recurring characters (all video shots when there are none),
    each candidate scores 2 where the routing names it first for a need, 1 where it names it as backup, 0.5 where it
    can make the shot but is named for none of its needs. The highest score wins; a tie goes to the cheaper price."""
    points = (adapters.routing.get("scene_model") or {}).get("points") or {"first": 2, "backup": 1, "able": 0.5}
    shots = [plan for plan in plans if plan.video and plan.recurring] or [plan for plan in plans if plan.video]
    if not shots:
        return None, {}
    scores = {}
    for name, facts in adapters.video.items():
        if not is_candidate(facts) or (licensed_only and not facts.get("licensed_data")):
            continue
        total = 0.0
        for plan in shots:
            ok, _ = able(adapters, name, facts, plan, licensed_only)
            if not ok:
                continue
            earned = 0.0
            for need in plan.needs:
                row = adapters.need(need)
                if name in (row.get("first") or []):
                    earned += points.get("first", 2)
                elif name in (row.get("backup") or []):
                    earned += points.get("backup", 1)
            total += earned if earned else points.get("able", 0.5)
        scores[name] = total
    if not scores:
        return None, {}

    def order(name):
        price = model_price(adapters.video[name], default_resolution(adapters, adapters.video[name]))
        return (-scores[name], price if price is not None else 99.0, name)
    best = sorted(scores, key=order)[0]
    return best, scores


@dataclass
class Routing:
    model: str
    note: str = ""
    override: bool = False
    warning: str = ""
    error: str = ""
    need: str = ""


def route_shot(adapters, plan, scene_model, forced=None, licensed_only=False):
    """The model for one shot: the forced model; else the shot's own choice; else the scene model when it can make
    it; else the first model named for the need the scene model cannot meet, else its backup, else the cheapest
    model that can."""
    if forced:
        return Routing(forced, note=f"every shot is compiled for {adapters.display(forced)} to test its words (--force-model)")
    if plan.author_model:
        name, facts, retired = adapters.find(plan.author_model)
        if name and is_route(facts):
            warning = (f"the shot names {adapters.display(name)}, a route made only as a clip book (compile --route), "
                       "so routing chooses a model for this pack")
        elif name:
            warning = (f"{plan.author_model} is retired; it is compiled for {adapters.display(name)}, its replacement "
                       "(blueprint 8.2)") if retired else ""
            why = plan.author_model_why or "the shot names it"
            return Routing(name, note=f"the shot's own choice: {why}", override=name != scene_model, warning=warning)
        else:
            warning = f"the shot names {plan.author_model}, which is not in the model facts, so routing chooses"
    else:
        warning = ""
    if scene_model:
        ok, why_not = able(adapters, scene_model, adapters.video.get(scene_model), plan, licensed_only)
        if ok:
            return Routing(scene_model, warning=warning)
    else:
        why_not = "no scene model could be chosen"
    order = (adapters.routing.get("need_order") or [])
    for need in [need for need in order if need in plan.needs] + [need for need in plan.needs if need not in order]:
        row = adapters.need(need)
        for rank, names in (("first", row.get("first") or []), ("backup", row.get("backup") or [])):
            for name in names:
                if name == scene_model:
                    continue
                ok, _ = able(adapters, name, adapters.video.get(name), plan, licensed_only)
                if ok:
                    return Routing(name, override=True, need=need, warning=warning,
                                   note=(f"{why_not}; it goes to {adapters.display(name)}, the {rank} choice for "
                                         f"{row.get('meaning', need)} (blueprint 8.4)"))
    able_models = []
    for name, facts in adapters.video.items():
        if is_candidate(facts) and name != scene_model and able(adapters, name, facts, plan, licensed_only)[0]:
            price = model_price(facts, default_resolution(adapters, facts))
            able_models.append((price if price is not None else 99.0, name))
    if able_models:
        name = sorted(able_models)[0][1]
        return Routing(name, override=True, warning=warning,
                       note=f"{why_not}; it goes to {adapters.display(name)}, the cheapest model that can make it")
    return Routing(scene_model, warning=warning,
                   error=f"{why_not}, and no model in the model facts can make it: redesign the shot (8.4)")


# ---------------------------------------------------------------- clips

@dataclass
class ClipPiece:
    identifier: str
    number: int
    count: int
    start: float
    end: float
    length_s: float
    resolution: str
    shape: str
    crop_to: str
    audio_on: bool
    chained: bool = False
    note: str = ""


def generation_shape(adapters, facts, frame_shape):
    table = ((adapters.routing.get("frame_shape") or {}).get("generation_shape") or {})
    wanted = table.get(frame_shape) or table.get("16_9") or ["16:9"]
    shapes = facts.get("shapes") if isinstance(facts.get("shapes"), list) else None
    if shapes is None:
        return "16:9" if "16:9" in wanted else wanted[0]
    for shape in wanted:
        if shape in shapes:
            return shape
    return "16:9" if "16:9" in shapes else shapes[0]


def forced_length(facts, resolution, references):
    spec = facts.get("length_s") or {}
    for key, conditions in spec.items():
        match = re.fullmatch(r"forced_(\d+(?:\.\d+)?)_when", key)
        if match and isinstance(conditions, list):
            wanted = {str(condition).lower() for condition in conditions}
            if (resolution or "").lower() in wanted or ("references" in wanted and references):
                return float(match.group(1))
    return None


def plan_pieces(breakdown, adapters, plan, model, facts, frame_shape, references, audio_on, need=""):
    """The clips of a shot on one model: lengths with handles, where it splits, the resolution and shape."""
    handles = constant(breakdown.constants, "handles_s", 0.75)
    derived = clip_plan(breakdown, plan.shot, model)
    lengths = allowed_lengths(facts) or []
    prefer = None
    row = adapters.need(need) if need else {}
    if row.get("first_resolution") and model in (row.get("first") or []):
        prefer = row["first_resolution"]
    resolution = default_resolution(adapters, facts, prefer)
    spec = facts.get("length_s") or {}
    if any(key.startswith("forced_") for key in spec):
        # Veo: 1080p and 4K force 8 s, so short clips stay at 720p unless reference pictures force 8 s anyway
        forced_by_references = forced_length(facts, "720p", references)
        if forced_by_references is None and max(derived.clip_lengths or [0]) < 8 and "720p" in (facts.get("resolution") or []):
            resolution = "720p"
    shape = generation_shape(adapters, facts, frame_shape)
    pieces = []
    if derived.fits or not derived.held:
        bounds = [0.0] + list(derived.split_at or []) + [plan.screen_time]
        count = max(1, len(bounds) - 1)
        for index in range(count):
            start, end = bounds[index], bounds[index + 1]
            length = derived.clip_lengths[index] if index < len(derived.clip_lengths) else float(math.ceil(end - start + 2 * handles))
            must = forced_length(facts, resolution, references)
            if must is not None and length is not None and length <= must + 1e-9:
                length = must
            pieces.append(ClipPiece(f"{plan.identifier}.{index + 1}", index + 1, count, start, end, length, resolution,
                                    shape, frame_shape, audio_on, derived.chained,
                                    derived.note if count > 1 else ""))
    else:
        length = float(math.ceil(plan.needed_s - 1e-9))
        pieces.append(ClipPiece(f"{plan.identifier}.1", 1, 1, 0.0, plan.screen_time, length, resolution, shape,
                                frame_shape, audio_on, False, derived.note))
    return pieces


# ---------------------------------------------------------------- reading the records for one clip

def room_sound_of(breakdown, shot):
    written = shot.get("room_sound")
    if written and not is_none(written) and normalise_word(written) != "as_place":
        return written
    scene = breakdown.record(scene_of(shot.identifier), "SCENE")
    scene_room = scene.get("room_sound") if scene is not None else None
    if scene_room and not is_none(scene_room) and normalise_word(scene_room) != "as_place":
        return scene_room
    location = breakdown.record(scene.get("location"), "LOCATION") if scene is not None and scene.get("location") else None
    value = location.get("room_sound") if location is not None else None
    return value if value and not is_none(value) else ""


def look_of(breakdown, shot):
    scene = breakdown.record(scene_of(shot.identifier), "SCENE")
    look = breakdown.record(scene.get("look"), "LOOK") if scene is not None and scene.get("look") else None
    return look


def location_state(breakdown, shot):
    """The STATE record of the scene's place for this shot, or None."""
    scene = breakdown.record(scene_of(shot.identifier), "SCENE")
    location = scene.get("location") if scene is not None else None
    if not location or is_none(location):
        return None
    states = [record for record in breakdown.records_of("STATE") if record.get("element") == location]
    for state in states:
        from_value = state.get("from") or ""
        if scene_of(from_value.split("|")[0].strip()) == scene_of(shot.identifier):
            return state
    return states[-1] if states else None


def location_state_line(breakdown, shot):
    state = location_state(breakdown, shot)
    return (state.get("state_line") or "") if state is not None else ""


def state_words_of(reference):
    """' - state 2' for a state reference like CH-JUDE.S02, so two states of one element never share a file name."""
    found = re.search(r"\.S(\d{2})$", str(reference or ""))
    return f" - state {int(found.group(1))}" if found else ""


def composited_texts(breakdown, shot):
    """[(words, kind, thing)] of the TEXT records in the shot's frame (its text field, text things, and text on a thing it
    shows) whose words are laid on after, as GEN-06 reads them: every one but a single mark the model draws."""
    found = []
    things = {element_of(split_item(written).first or "") for written in shot.get_all("thing")}
    identifiers = list(text_in_frame(breakdown, shot))
    for record in breakdown.records_of("TEXT"):
        on = element_of(record.get("on") or "")
        if on and not is_none(on) and on in things and record.identifier not in identifiers:
            identifiers.append(record.identifier)
    for identifier in identifiers:
        record = breakdown.record(identifier, "TEXT")
        words = (record.get("words") or "").strip().strip('"') if record is not None else ""
        if not words or is_none(words):
            continue
        drawn = normalise_word(record.get("method") or "") == "model_drawn"
        if drawn and len(words.split()) == 1 and len(words) <= 3:
            continue
        found.append((words, record.get("kind") or "", thing_named_by_title(record.title, words)))
    return found


def text_in_frame(breakdown, shot):
    found = [identifier for identifier in split_list(shot.get("text") or "") if not is_none(identifier)]
    for written in shot.get_all("thing"):
        first = split_item(written).first or ""
        if first.startswith("TX-"):
            found.append(first)
    return sorted(set(found))


@dataclass
class Segment:
    text: str
    kind: str = "words"   # words (the compiler's, fixed), key (pasted word for word), speech (a line, verbatim)


class Cast:
    """Who is who in one clip's words: the prompt's label for every character, in frame or not."""

    def __init__(self, breakdown, adapters, plan, motion_only):
        self.labels = {}
        self.people = plan.people
        in_frame = [person for person in plan.people if person.is_person]
        if motion_only:
            self.label_by_place(breakdown, plan, in_frame)
        else:
            for person in in_frame:
                person.label = person.name
        for person in in_frame:
            self.labels[person.element] = person.label
        nouns_in_frame = {person.noun for person in in_frame}
        for character in breakdown.records_of("CHARACTER"):
            if character.identifier in self.labels:
                continue
            noun = person_noun(adapters, character.get("fixed_description"), character)
            self.labels[character.identifier] = f"the other {noun}" if noun in nouns_in_frame else f"the {noun} off screen"
        self.names = []
        for character in breakdown.records_of("CHARACTER"):
            label = self.labels.get(character.identifier)
            names = [person_name(character.identifier)]
            names += [name.strip() for name in split_list(character.get("names") or "") if name.strip()]
            fixed = character.get("fixed_description") or ""
            names.append(name_of(breakdown, character.identifier, fixed))
            for name in sorted({name for name in names if name}, key=len, reverse=True):
                self.names.append((name, label))

    @staticmethod
    def label_by_place(breakdown, plan, in_frame):
        """With a start picture people are 'the woman', 'the man' (C3 R1); two of a kind are told apart by where the
        picture shows them (swapped only when the whole picture is flipped after), then by depth, then by order."""
        from .derive_fields import projected_placement
        try:
            depths = {element: (samples[0].depth if samples and samples[0].depth else None)
                      for element, samples in projected_placement(breakdown, plan.shot).items()}
        except Exception:
            depths = {}
        by_noun = {}
        for person in in_frame:
            by_noun.setdefault(person.noun, []).append(person)
        for noun, same in by_noun.items():
            if len(same) == 1:
                same[0].label = f"the {noun}"
                continue
            groups = {}
            for person in same:
                place = person.at
                if plan.prompt_flipped_all and place:
                    place = {"left_third": "right_third", "right_third": "left_third", "left_edge": "right_edge",
                             "right_edge": "left_edge"}.get(place, place)
                where = {"left_edge": "on the left", "left_third": "on the left", "centre": "in the middle",
                         "right_third": "on the right", "right_edge": "on the right"}.get(place, "")
                groups.setdefault(where, []).append(person)
            for where, members in groups.items():
                if len(members) == 1 and where:
                    members[0].label = f"the {noun} {where}"
                    continue
                known = [person for person in members if depths.get(person.element)]
                if len(members) == 2 and len(known) == 2:
                    near, far = sorted(members, key=lambda person: depths[person.element])
                    near.label = f"the {noun} nearer the camera"
                    far.label = f"the {noun} farther back"
                    continue
                for index, person in enumerate(members, start=1):
                    person.label = f"the {ordinal(index)} {noun}" + (f" {where}" if where else "")

    def rename(self, text):
        """Every character's name in a record's words, as this clip's label for them. One pass, longest name first, so
        a name already inside its label ('Saye' in 'Dr Saye') is never renamed twice."""
        if not text:
            return text
        lookup = {}
        for name, label in self.names:
            if label:
                lookup.setdefault(name.lower(), label)
        for label in set(self.labels.values()):
            if label:
                lookup.setdefault(label.lower(), label)
        if not lookup:
            return text
        names = sorted(lookup, key=len, reverse=True)
        pattern = re.compile(r"(?<![\w-])(" + "|".join(re.escape(name) for name in names) + r")('s)?(?![\w-])",
                             re.IGNORECASE)

        def replace(match):
            label = lookup[match.group(1).lower()]
            if label.lower() == match.group(1).lower():
                return match.group(0)
            return label + (match.group(2) or "")
        return pattern.sub(replace, text)

    def label(self, element):
        return self.labels.get(element_of(element) or "", element_name(None, element) if element else "")


# ---------------------------------------------------------------- the generation spec and the prompt

@dataclass
class Clip:
    """One compiled clip: its spec, its prompt in the model's words, its inputs, questions and cost."""
    identifier: str
    shot: str
    scene: str
    model: str
    piece: ClipPiece
    plan: ShotPlan
    routing: Routing
    prompt: str = ""
    negative: str = None
    inputs: dict = dataclass_field(default_factory=dict)
    speeches: list = dataclass_field(default_factory=list)
    laid_in: list = dataclass_field(default_factory=list)
    words_unknown: list = dataclass_field(default_factory=list)
    sounds: list = dataclass_field(default_factory=list)
    subjects: list = dataclass_field(default_factory=list)
    attach: list = dataclass_field(default_factory=list)
    questions: list = dataclass_field(default_factory=list)
    left_out: list = dataclass_field(default_factory=list)
    notes: list = dataclass_field(default_factory=list)
    spec: dict = dataclass_field(default_factory=dict)
    takes: tuple = (0, 0)
    draft: dict = dataclass_field(default_factory=dict)
    cost: float = None
    price: float = None
    draft_price: float = None
    seed: str = ""
    motion_only: bool = False
    post_ops: list = dataclass_field(default_factory=list)

    def as_pack_entry(self):
        return {
            "clip": self.identifier, "shot": self.shot, "model": self.model,
            "length_s": self.piece.length_s, "resolution": self.piece.resolution, "shape": self.piece.shape,
            "crop_to": self.piece.crop_to, "sound": "on" if self.piece.audio_on else "off",
            "prompt": self.prompt, "negative": self.negative,
            "inputs": self.inputs, "speeches": [identifier for identifier in self.speeches],
            "laid_in_from_voice_takes": list(self.laid_in), "words_unknown": list(self.words_unknown),
            "sounds": list(self.sounds), "subjects": list(self.subjects),
            "covers_s": [round(self.piece.start, 3), round(self.piece.end, 3)],
            "held": self.plan.held, "chained": self.piece.chained,
            "route": self.plan.route, "route_note": self.plan.route_note,
            "mirror_route": self.plan.mirror.route, "post_ops": list(self.post_ops),
            "override": self.routing.note if self.routing.override else None,
            "takes": {"draft": self.takes[0], "final": self.takes[1], "draft_model": self.draft.get("model"),
                      "draft_resolution": self.draft.get("resolution")},
            "price_usd_per_s": self.price, "draft_price_usd_per_s": self.draft_price,
            "cost_usd": None if self.cost is None else round(self.cost, 2),
            "seed": self.seed, "questions": list(self.questions), "left_out": list(self.left_out),
            "notes": list(self.notes), "spec": self.spec,
        }


class PromptWriter:
    """Builds one clip's generation spec (8.1) from the records and writes it in the model's own words (C3 §16)."""

    def __init__(self, breakdown, adapters, fixer, raw_speeches, project_record):
        self.breakdown = breakdown
        self.adapters = adapters
        self.fixer = fixer
        self.raw = raw_speeches
        self.project = project_record
        self.language = (project_record.get("language") if project_record is not None else None) or "english"

    # -- phrases
    def phrase(self, *path, default=""):
        return self.adapters.phrase(*path, default=default)

    def is_h3(self, clip):
        """True for MiniMax H3, hosted (both entries): a model with no negative side (Project notes 42, W3)."""
        return (self.adapters.video.get(clip.model) or {}).get("adapter") == "h3"

    def keep_out(self, clip):
        """The word lists whose clauses are left out of this clip's prompt: for H3, the words that name something
        absent and the words that ask for stillness (Project notes 42, W2 and W3); none for other models."""
        return ("absence", "stillness") if self.is_h3(clip) else ()

    H3_LEFT_OUT = "left out, because H3 has no negative side and would show it: write what happens instead"

    def fix_for(self, text, clip, what):
        """The fixer's words for this clip's model (word swaps, negations, and for H3 the clauses it would show)."""
        return self.fixer.fix(text, clip.left_out, what, keep_out=self.keep_out(clip), why_out=self.H3_LEFT_OUT)

    def clean(self, text, cast, flipped, clip, what):
        """A record's visible words, fit for the prompt: names as labels, image sides swapped for a flipped picture,
        word swaps, negations rewritten, IDs taken out."""
        text = straight_quotes(str(text or ""))
        text = cast.rename(text)
        if flipped:
            text = swap_image_sides(text)
        text = RECORD_ID.sub(lambda match: cast.label(match.group(0)) if match.group(0).startswith("CH-")
                             else lower_first(element_name(self.breakdown, match.group(0))), text)
        return self.fix_for(text, clip, what)

    def camera_words(self, clip, cast, motion_only):
        shot = clip.plan.shot
        size = normalise_word(shot.get("size") or "")
        parts = [self.phrase("size", size, default=size.replace("_", " ").capitalize())]
        frame = normalise_word(shot.get("frame") or "")
        frame_words = self.phrase("frame", frame, default="")
        if frame_words:
            nearest = next((person for person in clip.plan.people if person.faces == "away"), None)
            whose = next((person for person in clip.plan.people if person.is_person), None)
            frame_words = frame_words.replace("{nearest}", (nearest.label + "'s" if nearest else "the nearer person's")
                                              .replace("'s's", "'s"))
            frame_words = frame_words.replace("over the shoulder of the nearer person's", "over the shoulder")
            frame_words = frame_words.replace("over the shoulder of " + (nearest.label + "'s" if nearest else ""),
                                              "over " + (nearest.label + "'s shoulder" if nearest else "the shoulder"))
            frame_words = frame_words.replace("{whose}", (whose.label + "'s" if whose else "the character's"))
            frame_words = frame_words.replace("{anchor}", "hands")
            parts.append(frame_words)
        if normalise_word(shot.get("frame_detail") or "") == "symmetrical_profile":
            parts.append("a perfectly symmetrical profile framing")
        angle = normalise_word(shot.get("angle") or "eye_level")
        parts.append(self.phrase("angle", angle, default=""))
        height = str(shot.get("height") or "")
        match = re.match(r"^(eye|seated|kneeling):(CH-[A-Z0-9-]+)$", height.strip())
        if match and not motion_only:
            owner = next((person for person in clip.plan.people if person.element == match.group(2)), None)
            kind = "eye" if match.group(1) == "eye" else match.group(1) + " eye"
            parts.append(f"at {owner.label}'s {kind} height" if owner is not None else
                         f"at a {'standing' if match.group(1) == 'eye' else match.group(1)} person's eye height")
        elif normalise_word(height) == "floor":
            parts.append("from the floor")
        lens = number_of(shot.get("lens_mm"))
        if lens:
            for band in self.phrase("lens", "ranges", default=[]) or []:
                if lens <= band.get("up_to_mm", 0):
                    if band.get("words"):
                        parts.append(band["words"])
                    break
        focus = normalise_word(shot.get("focus") or "")
        if self.phrase("focus", focus, default=""):
            parts.append(self.phrase("focus", focus))
        first = sentence(", ".join(part for part in parts if part))
        move = normalise_word(shot.get("move") or "static")
        template = self.phrase("move", move, default=None)
        if template is None:
            clip.left_out.append(f"camera move {move.replace('_', ' ')}: never trusted to words; use a guide video or split "
                                 "the shot (C3 §4; B1 R14)")
            template = ""
        end_text = shot.get("end") or ""
        focus_person = next((person for person in clip.plan.people if person.is_person), None)
        move_text = template.replace("{end}", self.clean(end_text, cast, clip.plan.prompt_flipped_all, clip, "end") or "the subject")
        move_text = move_text.replace("{subject}", focus_person.label if focus_person else "the subject")
        move_text = move_text.replace("{direction}", "across")
        return first, move_text

    def subject_block(self, person, clip, cast, motion_only, for_picture=False):
        """The words for one subject: pasted keys (text mode), place and facing, what they do, stillness, must-not.
        For a still picture the words about motion (travel, stillness) are left out."""
        segments = []
        item = person.item
        pronoun_subject, pronoun_possessive, pronoun_capital = person.pronoun
        label = person.label or person.name
        capital_label = label[:1].upper() + label[1:]
        # The words describe the picture the model makes. Routes a and b flip the whole clip after, so every person is
        # described turned; on the plate route only the plate picture (the place and its mirrored people) is flipped
        # after, so a mirrored person is turned in that picture and never in the clip, which is animated from the
        # finished start picture (8.5).
        turned = clip.plan.prompt_flipped_all or (for_picture and person.flipped)
        if not motion_only and person.fixed_description:
            # an element the picture shows reversed from its own words has its left and right turned (B1 method 1;
            # GEN-04 accepts exactly this one change)
            reversed_here = shows_pre_reversed(self.breakdown, clip.plan.shot, person.element, turned)
            fixed = swap_own_sides(person.fixed_description) if reversed_here else person.fixed_description
            state_line = swap_own_sides(person.state_line) if reversed_here else person.state_line
            fixed, state_line = self.fixer.key_words(fixed), self.fixer.key_words(state_line)
            segments.append(Segment(fixed if fixed.endswith(".") else fixed + ".", "key"))
            if state_line:
                segments.append(Segment(f"{capital_label} now:", "words"))
                segments.append(Segment(state_line + ("" if state_line.endswith(".") else "."), "key"))
        if not motion_only:
            place = person.at
            if turned and place:
                place = {"left_third": "right_third", "right_third": "left_third", "left_edge": "right_edge",
                         "right_edge": "left_edge"}.get(place, place)
            faces = person.faces
            if turned:
                faces = {"frame_left": "frame_right", "frame_right": "frame_left"}.get(faces, faces)
            where = self.phrase("placement", place, default="") if place else ""
            if re.match(r"^(CH|PR|LOC)-", faces):
                target = cast.label(faces) if faces.startswith("CH-") else lower_first(element_name(self.breakdown, element_of(faces)))
                facing = self.phrase("facing", "person", default="facing {name}").replace("{name}", target)
            else:
                facing = self.phrase("facing", faces, default="") if faces else ""
            if where or facing:
                segments.append(Segment(sentence(f"{capital_label} is {', '.join(part for part in (where, facing) if part)}")))
            segments += [Segment(text) for text in self.side_sentences(person, clip, turned)]
        has_moments = any(parse_span(split_item(written).first) for written in clip.plan.shot.get_all("moment"))
        does = "" if has_moments else self.clean(item.get("does") or "", cast, clip.plan.prompt_flipped_all, clip,
                                                 f"{person.name}'s behaviour")
        if does:
            first_word = does.split()[0].lower() if does.split() else ""
            if first_word.endswith("s") and not first_word.endswith("ss") and first_word not in ("his", "hers", "its", "this", "thus", "as", "is", "was", "whose"):
                segments.append(Segment(sentence(f"{capital_label} {does}")))
            else:
                segments.append(Segment(sentence(f"{capital_label}: {does}")))
        travel = "" if for_picture else normalise_word(item.get("travel") or "")
        if travel and travel != "none":
            if turned:
                travel = {"frame_left": "frame_right", "frame_right": "frame_left"}.get(travel, travel)
            template = self.phrase("travel", travel, default="")
            if template:
                segments.append(Segment(template.replace("{who}", capital_label)))
        several = len([other for other in clip.plan.people if other.is_person]) > 1
        # The subject's old `still` sub-part is never written: a list of parts that stay still reads as an order to
        # freeze (Project notes 42, W2); held time is written as small timed actions in the moments instead.
        display = str(item.get("display") or "").strip()
        if self.is_h3(clip):
            display = ""  # H3: the display sentence is left out (Project notes 43, A9)
        if display in ("1", "2", "3") and person is clip.plan.people[0] and person.is_person:
            level = self.phrase("display", display, default="")
            if level:
                owner = pronoun_capital if motion_only and not several else f"{label}'s"
                segments.append(Segment(self.phrase("display", "sentence", default="{Whose} face and body show {level}.")
                                        .replace("{Whose}", owner[:1].upper() + owner[1:]).replace("{level}", level)))
        must_not = item.get("must_not")
        if must_not and not is_none(must_not) and self.is_h3(clip):
            # H3 has no negative side: "does not ..." would show the behaviour, so it is left out and listed
            clip.left_out.append(f"{person.name}'s must-not: \"{str(must_not).strip()}\": {self.H3_LEFT_OUT}")
        elif must_not and not is_none(must_not):
            behaviour = self.behaviour_from_must_not(must_not)
            if behaviour:
                text = self.phrase("must_not", "sentence", default="{Who} does not {behaviour}.").replace(
                    "{Who}", capital_label).replace("{behaviour}", self.clean(behaviour, cast, clip.plan.prompt_flipped_all, clip, "must-not"))
                segments.append(Segment(text))
        return segments

    def behaviour_from_must_not(self, text):
        """'a look toward the lens, saved for scene 13' -> 'look toward the lens'."""
        text = str(text).split(",")[0].strip()
        text = re.sub(r"^(?:a|an|the|any)\s+", "", text, flags=re.IGNORECASE)
        words = text.split()
        if not words:
            return ""
        first = words[0].lower()
        if first.endswith("ing"):
            words[0] = self.fixer.verb_of(first)
        elif first.endswith("s") and not first.endswith("ss"):
            words[0] = first[:-1]
        return " ".join(words)

    def side_sentences(self, person, clip, turned=None):
        """Where each visible sided feature falls in the prompt's picture (C1 R22; C2 Rule 35): its prompt side when the
        picture described is flipped after (turned), else the side the finished picture shows."""
        if turned is None:
            turned = clip.plan.prompt_flipped_all
        try:
            entries = [entry for entry in image_sides(self.breakdown, clip.plan.shot) if entry.get("element") == person.element]
        except Exception:
            return []
        found = []
        for entry in entries:
            for feature in entry.get("features") or []:
                where = feature.get("prompt") if turned else feature.get("image")
                if not feature.get("own") or where in (None, "open") or not feature_shown(clip.plan.shot, feature):
                    continue
                if feature_hidden(self.breakdown, clip.plan.shot, feature.get("feature")):
                    continue
                words = side_words(self.adapters, feature, where)
                if not words:
                    continue
                owner = f"{person.label}'s" if person.label else person.pronoun[1]
                found.append(self.phrase("side", "sentence", default="{whose} {feature} is {where}.")
                             .replace("{whose}", owner[:1].upper() + owner[1:]).replace("{feature}", feature["feature"])
                             .replace("{where}", words))
        return found

    def things_block(self, clip, cast, keep=None, turned=None, glass=True):
        """The things in frame (and the glass): keep chooses which things (a test on the thing's reference); turned says
        whether the picture described is flipped after, so its image sides are swapped (default: the whole clip is)."""
        segments = []
        shot = clip.plan.shot
        turned = clip.plan.prompt_flipped_all if turned is None else turned
        must_show = set(split_list(shot.get("must_show") or ""))
        for written in shot.get_all("thing"):
            item = split_item(written)
            reference = (item.first or "").strip()
            if not reference or is_none(reference) or reference.startswith(("MO-", "TX-")):
                continue
            if keep is not None and not keep(reference):
                continue
            element = element_of(reference)
            record = self.breakdown.record(element)
            state = state_record(self.breakdown, reference)
            emphasis = number_of(item.get("emphasis"), 0) or 0
            where = self.clean(item.get("at") or "", cast, turned, clip, "a thing's place")
            name = lower_first(element_name(self.breakdown, element))
            state_line = state.get("state_line") if state is not None and not is_none(state.get("state_line")) else ""
            fixed = record.get("fixed_description") if record is not None and not is_none(record.get("fixed_description")) else ""
            if shows_pre_reversed(self.breakdown, shot, reference, turned):
                state_line, fixed = swap_own_sides(state_line), swap_own_sides(fixed)
            if (emphasis >= 1 or reference in must_show or element in must_show) and fixed:
                text = fixed + (f", {state_line}" if state_line else "")
            else:
                text = name + (f", {state_line}" if state_line else "")
            text = sentence(text + (f", {where}" if where else ""))
            text = leave_words_for_later(text, composited_texts(self.breakdown, shot))
            segments.append(Segment(self.fix_for(text, clip, f"{name}")))
        for written in (shot.get_all("glass") if glass else []):
            item = split_item(written)
            surface = (item.first or "glass").strip()
            state = normalise_word(item.get("state") or "clear")
            camera = normalise_word(item.get("camera") or "")
            words = self.phrase("glass", state, default="")
            if not words:
                continue
            location = self.breakdown.record((self.breakdown.record(scene_of(shot.identifier), "SCENE") or {}).get("location")
                                             if self.breakdown.record(scene_of(shot.identifier), "SCENE") is not None else None)
            in_room = location is not None and any(split_item(value).first.strip().lower() == surface.lower()
                                                   for value in location.get_all("object"))
            if state == "clear" and (in_room or camera != "through"):
                words = "perfectly clear glass"
            segments.append(Segment(sentence(f"The {surface.lower()}: {words}")))
        return segments

    def moments(self, clip, cast):
        """[(clip start s, clip end s, words)] of the shot's moments inside this clip, in clip time (handles added)."""
        handles = constant(self.breakdown.constants, "handles_s", 0.75)
        piece = clip.piece
        found = []
        for written in clip.plan.shot.get_all("moment"):
            item = split_item(written)
            span = parse_span(item.first)
            if span is None:
                continue
            start, end = max(span[0], piece.start), min(span[1], piece.end)
            if end <= start + 1e-9:
                continue
            shows = straight_quotes(item.get("shows") or "")
            spoken = []
            for identifier, _, entry in clip.plan.on_screen + clip.plan.off_screen:
                line = re.sub(r"\s*\([^)]*\)\s*", " ", straight_quotes(str(entry.get("text") or ""))).strip()
                if line:
                    spoken.append(line)
                    # the spoken words are sent as the line itself, never inside the picture's words; matched as
                    # whole words, so a short line ("No") never cuts a word ("Nothing") apart
                    shows = re.sub(r'(?<!\w)"?' + re.escape(line) + r'"?(?!\w)', "", shows)
            shows = without_quoted_speech(shows, spoken)
            # a planned cutaway belongs to the edit, not to this picture (8.4): its words never reach the model
            shows = re.sub(r"\s*\b(?:and|then)\s*$", "", CUTAWAY_WORDS.sub(" ", shows).strip())
            shows = re.sub(r"\s*;\s*;", ";", re.sub(r"\s+([;,.])", r"\1", shows)).strip(" ;,")
            words = self.clean(shows, cast, clip.plan.prompt_flipped_all, clip, "a moment")
            if not words:
                continue
            first_word = re.sub(r"[^a-z]", "", words.split()[0].lower()) if words.split() else ""
            focus = next((person for person in clip.plan.people if person.is_person), None)
            if (focus is not None and first_word.endswith("s") and not first_word.endswith("ss")
                    and first_word not in ("his", "hers", "its", "this", "thus", "as", "is", "was", "whose")
                    and not words[:1].isupper()):
                words = f"{focus.label} {words}"
            clip_start = 0.0 if start <= piece.start + 1e-9 else start - piece.start + handles
            clip_end = min(piece.length_s, end - piece.start + handles)
            found.append((round(clip_start, 2), round(clip_end, 2), words))
        return found

    def speech_time(self, clip, item, entry, moments):
        at = number_of(item.get("at"))
        handles = constant(self.breakdown.constants, "handles_s", 0.75)
        if at is not None:
            return at - clip.piece.start + handles
        words = straight_quotes(str(entry.get("text") or "")).lower()
        for start, _, text in moments:
            lowered = text.lower()
            if words and words[:12] in lowered or re.search(r"\b(says?|asks?|answers?|speaks?|words?)\b", lowered):
                return start
        return None

    def delivery(self, item, entry, clip):
        parenthetical = entry.get("parenthetical")
        delivery = self.fixer.delivery_words(parenthetical)
        if not delivery:
            speaker = element_of(entry.get("speaker") or "")
            person = next((person for person in clip.plan.people if person.element == speaker), None)
            tactic = person.item.get("tactic") if person is not None else ""
            delivery = self.fixer.delivery_words(tactic) or self.phrase("delivery_default", default="level")
        return delivery

    def voice_description(self, speaker):
        character = self.breakdown.record(speaker, "CHARACTER")
        voice = self.breakdown.record(character.get("voice"), "VOICE") if character is not None and character.get("voice") else None
        if voice is None:
            voice = next((record for record in self.breakdown.records_of("VOICE") if record.get("character") == speaker), None)
        text = voice.get("voice_description") if voice is not None else ""
        return "" if is_none(text) else str(text)

    def speaker_line(self, facts, style, clip, cast, identifier, item, entry, index):
        """One sent line in the model's speaker form (GEN-09): Veo and Omni colon, no quotation marks; Kling, Wan
        and LTX a name, the delivery and the line in quotation marks; H3 its structured form."""
        line = heard_line(item, entry)
        speaker = element_of(entry.get("speaker") or "")
        who = cast.label(speaker) or "someone"
        who_capital = who[:1].upper() + who[1:]
        delivery = self.delivery(item, entry, clip)
        path = normalise_word(item.get("path") or entry.get("path") or "direct")
        path_words = self.phrase("audio", "paths", path, default="") if path not in ("direct", "off_screen") else ""
        template = facts.get("speaker")
        if not template:
            template = self.adapters.generic.get("speaker") or "{who} ({delivery}): \"{line}\""
        description = who_capital
        if "{description}" in template:
            voice = self.fix_for(self.voice_description(speaker), clip, "the voice description")
            voice = lower_first(voice).rstrip(".")
            description = f"{who_capital}, in the voice of {voice}," if voice else f"{who_capital}, {delivery},"
            if path_words:
                description = f"{description} {path_words},"
        delivery_text = delivery + (f"; {path_words}" if path_words and "{description}" not in template else "")
        voice_label = f"{who}'s voice" if not delivery else f"{delivery} voice"
        text = (template.replace("{description}", description).replace("{who}", who_capital)
                .replace("{delivery}", delivery_text).replace("{voice_label}", voice_label)
                .replace("{n}", str(index)).replace("{language}", self.language.capitalize()).replace("{line}", line))
        return text

    def audio_parts(self, clip, cast, facts):
        """(effect sentences, room sound words, sounds list) for a model with sound, capped at
        named_sounds_per_prompt_max; the rest is laid in during the sound edit (C3 §7E)."""
        shot = clip.plan.shot
        silence = normalise_word(shot.get("silence") or "none")
        if silence == "true_silence":
            return [], "", []
        most = int(number_of(constant(self.breakdown.constants, "named_sounds_per_prompt_max", 3), 3))
        room = "" if silence == "drop_out" else self.fix_for(room_sound_of(self.breakdown, shot), clip, "room sound")
        effects = []
        for written in shot.get_all("effect"):
            item = split_item(written)
            what = (item.first or "").strip()
            if not what or is_none(what):
                continue
            at = number_of(item.get("at"))
            if at is not None and not (clip.piece.start - 1e-9 <= at <= clip.piece.end + 1e-9):
                continue
            effects.append((-(number_of(item.get("sound_emphasis"), 0) or 0), len(effects), what))
        effects.sort()
        room_slots = 1 if room else 0
        kept = effects[:max(0, most - room_slots)]
        for _, _, what in effects[len(kept):]:
            clip.notes.append(f"the sound of {what} is laid in during the sound edit: a prompt names at most {most} sounds (C3 L13)")
        sentences = []
        sounds = []
        for _, _, what in sorted(kept, key=lambda entry: entry[1]):
            words = self.clean(what, cast, False, clip, "a sound")
            if words:
                sentences.append(words)
                sounds.append(words)
        if room:
            sounds.append("room sound: " + room)
        return sentences, room, sounds

    def build(self, clip, facts, today_label=""):
        """Fill clip.prompt, negative, inputs, speeches, sounds and the spec for one clip."""
        adapters = self.adapters
        plan = clip.plan
        shot = plan.shot
        style = facts.get("adapter") or "generic"
        motion_only = plan.start_picture or plan.still_only
        guide = plan.guide_video
        clip.motion_only = motion_only
        cast = Cast(self.breakdown, adapters, plan, motion_only)
        silent_model = is_silent_model(facts)
        # speeches: on screen and sent, the rest laid in from voice takes (8.6)
        sent, laid_in = [], []
        for identifier, item, entry in plan.on_screen:
            at = number_of(item.get("at"))
            inside = at is None or clip.piece.start - 1e-9 <= at <= clip.piece.end + 1e-9
            if at is None and clip.piece.number > 1:
                inside = False
            if not inside:
                continue
            if plan.silent_picture or silent_model:
                laid_in.append(identifier)
            elif not str(entry.get("text") or "").strip():
                clip.words_unknown.append(identifier)
            else:
                sent.append((identifier, item, entry))
        for identifier, item, entry in plan.off_screen:
            at = number_of(item.get("at"))
            if at is None and clip.piece.number > 1:
                continue
            if at is not None and not (clip.piece.start - 1e-9 <= at <= clip.piece.end + 1e-9):
                continue
            laid_in.append(identifier)
        clip.speeches = [identifier for identifier, _, _ in sent]
        clip.laid_in = laid_in
        if clip.words_unknown:
            clip.notes.append(f"the words of {', '.join(clip.words_unknown)} are not known here, because the story's "
                              "speeches are missing, so the line is left out of the prompt: read the story "
                              "(stage.py read) or compile with --story, then compile again")
        if silent_model and plan.on_screen:
            clip.notes.append(f"{adapters.display(clip.model)} makes no sound: every line is laid in from its voice take, "
                              "and a mouth seen speaking is fitted after (C3 R22; D3 §12)")
        if plan.silent_picture:
            clip.notes.append(plan.silent_why)
        # the parts of the spec
        people = [person for person in plan.people]
        camera_first, camera_move = self.camera_words(clip, cast, motion_only)
        subject_segments = []
        for person in people:
            subject_segments += self.subject_block(person, clip, cast, motion_only)
        clip.subjects = [person.reference for person in people]
        setting = []
        look_block = ""
        style_words = ""
        if not motion_only:
            location_line = location_state_line(self.breakdown, shot)
            if location_line and not is_none(location_line):
                setting.append(Segment(sentence(self.fix_for(location_line, clip, "the place"))))
            setting += self.things_block(clip, cast)
            look = look_of(self.breakdown, shot)
            if look is not None and not is_none(look.get("look_block")):
                look_block = self.fixer.key_words(look.get("look_block").strip())
                contrast = normalise_word(look.get("contrast") or "")
                if contrast in ("high", "extreme"):
                    for person in people:
                        character = self.breakdown.record(person.element, "CHARACTER")
                        skin = character.get("skin_light") if character is not None else None
                        if skin and not is_none(skin):
                            look_block += " " + sentence(skin)
            style_record = self.breakdown.singleton("STYLE")
            if style_record is not None and not is_none(style_record.get("style_words")):
                style_words = style_record.get("style_words").strip()
                style_words = style_words[:1].upper() + style_words[1:]
        if text_in_frame(self.breakdown, shot):
            setting.append(Segment(sentence(self.phrase("text", "surfaces", default="plain, unmarked surfaces"))))
        moments = self.moments(clip, cast)
        end_state = self.clean(shot.get("end") or "", cast, plan.prompt_flipped_all, clip, "the end") if clip.piece.number == clip.piece.count else ""
        if motion_only:
            # a start picture carries the look and the descriptions: the prompt is the action only (GEN-05)
            look = look_of(self.breakdown, shot)
            clauses = picture_clauses([look.get("look_block") if look is not None else ""]
                                      + [person.fixed_description for person in people]
                                      + [person.state_line for person in people])
            moments = [(start, end, action_only(words, clauses)) for start, end, words in moments]
            moments = [(start, end, words) for start, end, words in moments if words]
            end_state = action_only(end_state, clauses)
        composited = composited_texts(self.breakdown, shot)
        if composited:
            moments = [(start, end, leave_words_for_later(words, composited)) for start, end, words in moments]
            end_state = leave_words_for_later(end_state, composited)
        effect_sentences, room, sounds = ([], "", []) if silent_model else self.audio_parts(clip, cast, facts)
        clip.sounds = sounds
        # the negative field (K18)
        negative = None
        field_name = facts.get("negative_field")
        if field_name:
            nouns = []
            if facts.get("negative_default"):
                nouns.append(facts["negative_default"])
            nouns += ["subtitles", "captions", "text"]
            for reference in split_list(shot.get("must_not_show") or ""):
                if is_none(reference):
                    continue
                element = element_of(reference)
                if element.startswith("CH-"):
                    noun = "extra people"
                else:
                    noun = lower_first(element_name(self.breakdown, element))
                    noun = re.sub(r"^the\s+", "", noun, flags=re.IGNORECASE)
                if noun and noun not in nouns:
                    nouns.append(noun)
            nouns.append("music")
            negative = ", ".join(dict.fromkeys(nouns))
        clip.negative = negative
        # inputs and the lines that name them
        clip.inputs = self.inputs_for(clip, facts, people)
        references = clip.inputs.get("references") or []
        # assemble in the model's order
        order = facts.get("order") or self.adapters.generic.get("order") or []
        marker = facts.get("time_marker")
        pieces = {}
        pieces["sources"] = self.reference_lines(clip, facts, people, style)
        pieces["references"] = pieces["sources"]
        pieces["elements"] = subject_segments
        pieces["subjects"] = subject_segments
        pieces["goal"] = []
        single = facts.get("single_shot") if facts.get("single_shot") is not None else self.adapters.generic.get("single_shot")
        pieces["single_shot"] = [Segment(single)] if single and style != "wan" else []
        camera_segments = []
        if not guide:
            camera_segments = [Segment(camera_first)]
            if camera_move:
                static = facts.get("camera_static")
                if normalise_word(shot.get("move") or "static") == "static" and style == "h3":
                    # one camera sentence, in the wording testers found holds; a second camera line made cuts drift
                    # and the camera move (Project notes 42, W3)
                    camera_segments.append(Segment(self.phrase(
                        "h3", "camera_sentence",
                        default="The shot is static, on a tripod, with no camera movement whatsoever.")))
                elif normalise_word(shot.get("move") or "static") == "static" and static:
                    camera_segments.append(Segment(sentence(f"The camera {static}" if not static.startswith(("fixed", "holds")) else
                                                            ("Fixed camera" if static.startswith("fixed") else f"The camera {static}"))))
                    camera_segments.append(Segment(self.phrase("hold", "camera_does_not_move", default="The camera does not move.")))
                else:
                    camera_segments.append(Segment(camera_move))
        else:
            camera_segments = [Segment(self.phrase("guide_video", "lead", default=""))]
        pieces["camera"] = camera_segments
        pieces["keywords"] = camera_segments
        pieces["atmosphere"] = setting
        pieces["setting"] = setting
        pieces["world"] = setting + ([Segment(look_block, "key")] if look_block else []) + (
            [Segment(style_words + ("" if style_words.endswith(".") else "."), "key")] if style_words else [])
        pieces["look"] = [Segment(look_block, "key")] if look_block else []
        pieces["style"] = [Segment(style_words + ("" if style_words.endswith(".") else "."), "key")] if style_words else []
        if style == "h3":
            pieces["look"], pieces["style"] = [], []
        beat_segments = []
        spoken = {}
        for index, (identifier, item, entry) in enumerate(sent, start=1):
            when = self.speech_time(clip, item, entry, moments)
            spoken.setdefault(when, []).append(Segment(self.speaker_line(facts, style, clip, cast, identifier, item, entry, index), "speech"))
        placed = set()
        if motion_only and style not in ("omni",):
            beat_segments.append(Segment(self.phrase("start_picture", "lead", default="Starting from the opening picture,")
                                         .rstrip(",") + ":"))
        for index, (start, end, words) in enumerate(moments):
            text = words
            if marker and style != "wan":
                label = (marker.replace("{t0}", number_text(start)).replace("{t1}", number_text(end))
                         .replace("{mm_ss_t0}", mm_ss(start)).replace("{mm_ss_t1}", mm_ss(end))
                         .replace("{mm_ss_ms_t0}", mm_ss_ms(start)).replace("{ordinal}", ordinal(max(1, round(start)))))
                if style == "kling" and start < 0.5:
                    text = sentence(words)
                elif style == "kling":
                    text = f"{label} {lower_first(sentence(words))}"
                elif style == "h3":
                    text = sentence(f"{label} {words}") if start >= 0.5 else sentence(words)
                else:
                    text = f"{label} {sentence(words)}"
            else:
                text = sentence(("then " if index and style in ("wan", "ltx", "generic", "runway", "ray") else "") + words)
            beat_segments.append(Segment(text))
            for when in list(spoken):
                last = index == len(moments) - 1
                if when is not None and when not in placed and start - 1e-6 <= when and (when < end - 1e-6 or last):
                    beat_segments += spoken[when]
                    placed.add(when)
        for when, lines in spoken.items():
            if when not in placed:
                beat_segments += lines
        if motion_only:
            beat_segments += subject_segments
            pieces["elements"] = pieces["subjects"] = []
        pieces["beats"] = beat_segments
        pieces["timed_actions"] = beat_segments
        pieces["timed_stages"] = beat_segments
        pieces["dialogue"] = []
        end_label = facts.get("end_state")
        pieces["end_state"] = [Segment(f"{end_label} {sentence(end_state)}" if end_label else f"It ends: {lower_first(end_state).rstrip('.')}.")] if end_state else []
        if style not in ("seedance",) and end_state:
            beat_segments += pieces["end_state"]
            pieces["end_state"] = []
        audio_segments = []
        if not silent_model:
            veo = style == "veo"
            for words in effect_sentences:
                audio_segments.append(Segment(sentence(("SFX: " if veo else "The sound of ") + words)))
            if room:
                if veo:
                    audio_segments.append(Segment(sentence(f"Ambient noise: {room}")))
                elif style == "h3":
                    audio_segments.append(Segment(f"{self.phrase('audio', 'h3_labels', 'soundscape', default='overall_soundscape:')} {room}."))
                elif style == "omni":
                    audio_segments.append(Segment(sentence(f"{self.phrase('audio', 'omni_label', default='Sound design:')} {room}")))
                else:
                    audio_segments.append(Segment(sentence(self.phrase("audio", "room_sound", default="Room sound: {room}.").replace("{room}", room).rstrip("."))))
            if style == "h3":
                audio_segments.append(Segment(self.phrase("audio", "h3_labels", "music", default="non_diegetic_music: none.")))
            else:
                audio_segments.append(Segment(self.phrase("audio", "no_music", default="No background music.")))
        pieces["audio"] = audio_segments
        pieces["ambient"] = audio_segments
        pieces["soundscape"] = audio_segments
        pieces["music"] = []
        no_lines = []
        if not silent_model and not sent and (facts.get("invents_dialogue") or style == "omni"):
            no_lines.append(Segment(self.phrase("audio", "no_dialogue", default="No dialogue.")))
        if style == "omni":
            for line in facts.get("no_lines") or []:
                if line == "No dialogue." and sent:
                    continue
                if Segment(line) not in no_lines:
                    no_lines.append(Segment(line))
        pieces["no_lines"] = no_lines
        pieces["protect"] = ([Segment(sentence(f"Keep {person.label}'s face identical to the reference picture"))
                              for person in people if person.is_person and references and not motion_only][:1]
                             if style == "seedance" else [])
        pieces["role_line"] = [Segment(line) for line in self.role_lines(clip, facts)] if style == "omni" else []
        # write
        segments = []
        used = set()
        for slot in order:
            if slot in used:
                continue
            used.add(slot)
            for segment in pieces.get(slot) or []:
                if segment.text and segment not in segments:
                    segments.append(segment)
        if style == "wan" and single:
            segments.append(Segment(single))
        prompt = " ".join(segment.text.strip() for segment in segments if segment.text.strip())
        prompt = re.sub(r"\s{2,}", " ", prompt).replace(" .", ".").strip()
        clip.prompt = self.shorten_if_needed(prompt, segments, facts, clip)
        clip.spec = self.spec_of(clip, facts, camera_first, camera_move, people, setting, look_block, style_words,
                                 moments, end_state, sent, laid_in, room, effect_sentences, negative)

    def shorten_if_needed(self, prompt, segments, facts, clip):
        """Keep a prompt within the model's limits: verified limits are the checker's (GEN-01); an unverified limit is
        kept where it can be by leaving out words that are not keys, else noted."""
        limit = facts.get("prompt_limit") or facts.get("prompt_limit_unverified") or {}
        characters = limit.get("characters")
        words_limit = limit.get("words")
        tokens = limit.get("tokens")
        try:
            per_word = float(load_json(LIMITS_FILE).get("tokens_per_word_estimate", {}).get("value", 1.4))
        except (OSError, ValueError, AttributeError):
            per_word = 1.4

        def too_long(text):
            if characters and len(text) > characters:
                return True
            if words_limit and words_in(text) > words_limit:
                return True
            if tokens and math.ceil(words_in(text) * per_word) > tokens:
                return True
            return False
        if not too_long(prompt):
            return prompt
        kept = list(segments)
        # leave out the glass lines first, then the lines on how much a face shows; never keys or speech
        for predicate in (lambda segment: segment.kind == "words" and segment.text.startswith("The ") and ":" in segment.text,
                          lambda segment: segment.kind == "words" and "face and body show" in segment.text):
            kept = [segment for segment in kept if not predicate(segment)]
            text = re.sub(r"\s{2,}", " ", " ".join(segment.text for segment in kept)).replace(" .", ".").strip()
            if not too_long(text):
                clip.notes.append("some words about glass and about how much a face shows were left out to keep the "
                                  "prompt within the model's limit")
                return text
        unverified = facts.get("prompt_limit_unverified") and not facts.get("prompt_limit")
        if unverified:
            clip.notes.append(f"the prompt is {len(prompt)} characters, over the {characters or words_limit or tokens} the "
                              f"blueprint gives for {self.adapters.display(clip.model)} (the research could not confirm "
                              "that limit): check the limit on the day before sending")
        return prompt

    def inputs_for(self, clip, facts, people):
        """The pictures, guide video and voice takes the clip is made from, in C2's stack order."""
        plan = clip.plan
        scene_number = re.sub(r"^SC0*", "", plan.scene or "")
        shot_number_text = three_digits(plan.identifier)
        inputs = {"start_picture": None, "end_picture": None, "references": [], "guide_video": None, "audio": []}
        attach = []
        base = f"Scene {scene_number} - shot {shot_number_text}"
        number = clip.piece.number
        if plan.start_picture and number > 1 and clip.piece.chained:
            # no planned cutaway fits: the clip goes on from the last frame of the kept take before (8.4; C5 R31)
            inputs["start_picture"] = f"{plan.identifier}.{number - 1} last frame"
            attach.append({"file": f"{base} - clip {number - 1} - last frame.png",
                           "job": "the last frame of the kept take of the clip before, saved as a picture; this clip "
                                  "goes on from it (a flagged last resort)", "picture": None})
        elif plan.start_picture:
            identifier = f"PIC-{plan.identifier}-START-{number:02d}"
            inputs["start_picture"] = identifier
            job = "the first picture of the clip" if number == 1 else "the first picture of this clip, after the planned cutaway"
            if plan.mirror.route == "plate":
                job += (", made on the plate route: the place with its mirrored people as one picture, flipped, then "
                        "the others added unflipped with an edit model (8.5; C2 R5)")
            name = f"{base} - start picture.png" if number == 1 else f"{base} - clip {number} - start picture.png"
            attach.append({"file": name, "job": job, "picture": identifier})
        if plan.end_picture and number == clip.piece.count:
            identifier = f"PIC-{plan.identifier}-END-01"
            inputs["end_picture"] = identifier
            attach.append({"file": f"{base} - end picture.png",
                           "job": "the last picture of the clip, edited from the start picture (C2 Rule 15)", "picture": identifier})
        if plan.guide_video:
            level = number_of(plan.shot.get("previs_level"), 0) or 0
            identifier = f"PV-{plan.identifier}-V01"
            inputs["guide_video"] = identifier
            attach.append({"file": f"19 Grey previews/{base}/guide video.mp4",
                           "job": f"the grey preview the camera and blocking are copied from (grey preview level {int(level)})",
                           "picture": identifier})
        if not plan.start_picture and plan.route != "text":
            stack = []
            style = self.breakdown.singleton("STYLE")
            picture = style.get("style_picture") if style is not None else None
            if picture and not is_none(picture):
                stack.append(("style", None, f"{picture}", "the style picture: light, colour and texture only"))
            scene = self.breakdown.record(plan.scene, "SCENE")
            location = scene.get("location") if scene is not None else None
            faces = [person for person in people if person.is_person]
            for person in faces:
                name = person.name
                stack.append(("character", person.reference, f"Reference pictures/{name}{state_words_of(person.reference)}.png",
                              f"{name}'s face and clothes in this state"))
            things = []
            for written in plan.shot.get_all("thing"):
                item = split_item(written)
                reference = (item.first or "").strip()
                if not reference or is_none(reference) or reference.startswith(("MO-", "TX-")):
                    continue
                if (number_of(item.get("emphasis"), 0) or 0) >= 1:
                    element = element_of(reference)
                    name = element_name(self.breakdown, element)
                    things.append(("prop", reference, f"Reference pictures/{name[:1].upper() + name[1:]}{state_words_of(reference)}.png",
                                   f"{self.fixer.swap_words(lower_first(name))}"))
            location_entry = []
            if location and not is_none(location):
                name = element_name(self.breakdown, location)
                place_state = location_state(self.breakdown, plan.shot)
                place_reference = place_state.identifier if place_state is not None else location
                location_entry = [("location", place_reference,
                                   f"Reference pictures/{name[:1].upper() + name[1:]}{state_words_of(place_reference)}.png",
                                   f"the place: {self.fixer.swap_words(lower_first(name))}, empty")]
            most = (facts.get("inputs") or {}).get("references_max")
            ordered = stack[:1] + location_entry + stack[1:] + things
            if isinstance(most, int):
                while len(ordered) > most:
                    if things:
                        dropped = things.pop()
                    elif location_entry:
                        dropped = location_entry.pop()
                    elif stack and stack[0][0] == "style":
                        dropped = stack.pop(0)
                    else:
                        clip.notes.append(f"{self.adapters.display(clip.model)} takes {most} reference pictures and this shot has "
                                          f"{len(faces)} faces; faces are never dropped (C2 §6.6)")
                        break
                    ordered.remove(dropped)
                    clip.notes.append(f"left out of the reference pictures to stay within {most}: {dropped[3]} (C2 §6.6: props first, then the place, never faces)")
            tag = facts.get("reference_tag")
            for index, (kind, reference, file_name, job) in enumerate(ordered, start=1):
                identifier = (f"PIC-{reference}-REFERENCE-01" if reference and re.match(r"^(CH|PR|LOC|TX|CAM)-", reference)
                              else None)
                label = tag.replace("{n}", str(index)) if tag else f"picture {index}"
                entry = {"picture": identifier, "file": file_name, "job": job, "tag": label}
                if identifier and reference_turned(self, plan, reference):
                    entry.update({"file": turned_file(file_name), "unflipped_file": file_name, "flipped": True,
                                  "job": job + ", flipped left to right (the mirror world, 8.5)"})
                inputs["references"].append(entry)
                attach.append({"file": entry["file"], "job": f"{label}: {entry['job']}", "picture": identifier})
        if clip.speeches and (facts.get("inputs") or {}).get("audio_reference"):
            for identifier in clip.speeches:
                number = re.search(r"-D(\d+)$", identifier)
                file_name = f"Voices/Scene {scene_number} - speech {int(number.group(1)) if number else identifier} - picked take.wav"
                tag = facts.get("audio_tag")
                label = tag.replace("{n}", str(len(inputs['audio']) + 1)) if tag else "the audio reference"
                inputs["audio"].append({"voice_take": f"VT-{identifier}-T01", "file": file_name, "tag": label})
                attach.append({"file": file_name, "job": f"{label}: the line's picked voice take, so the mouth follows the locked voice (K16; D3 rule 21)",
                               "picture": None})
        elif clip.speeches and (facts.get("inputs") or {}).get("voice") and "bound" in str((facts.get("inputs") or {}).get("voice")):
            attach.append({"file": "the speaker's bound voice", "job": str(facts["inputs"]["voice"]), "picture": None})
        clip.attach = attach
        return inputs

    def reference_lines(self, clip, facts, people, style):
        """The line that names each attached picture's job, in the model's syntax (C3 §2B, §9C)."""
        inputs = clip.inputs
        references = inputs.get("references") or []
        lines = []
        if style == "veo" and references:
            names = and_list([reference["job"].split("'s face")[0] if "'s face" in reference["job"] else lower_first(reference["job"].split(":")[0]) for reference in references])
            lines.append(Segment((facts.get("reference_line") or "Using the provided images for {names}:").replace("{names}", names)))
        elif style == "omni" and (references or inputs.get("start_picture")):
            lines.append(Segment(facts.get("reference_line") or ""))
        elif references and style in ("kling", "seedance", "wan", "h3", "generic", "ltx"):
            described = []
            for reference in references:
                job = reference["job"]
                described.append(f"{reference['tag']} is {job}" if style != "h3" else f"{reference['tag'].capitalize()} controls {job}")
            lines.append(Segment(sentence("; ".join(described))))
        if style == "seedance" and inputs.get("guide_video"):
            tag = (facts.get("guide_tag") or "[Video{n}]").replace("{n}", "1")
            lines.append(Segment(self.phrase("guide_video", "seedance", default="").replace("{tag}", tag)))
        if style == "seedance" and inputs.get("audio"):
            for entry in inputs["audio"]:
                lines.append(Segment(sentence(f"{entry['tag']} is the recording of the line; the mouth follows it")))
        if inputs.get("end_picture") and style != "omni":
            lines.append(Segment(self.phrase("end_picture", "lead", default="")))
        return lines

    def role_lines(self, clip, facts):
        lines = []
        if clip.inputs.get("start_picture"):
            lines.append("Use Image1 as the starting frame.")
        if clip.inputs.get("references"):
            lines.append("Use Image2 as a reference for the video generation.")
        return lines

    def spec_of(self, clip, facts, camera_first, camera_move, people, setting, look_block, style_words, moments, end_state,
                sent, laid_in, room, effects, negative):
        """The model-neutral generation spec of 8.1 (C3 §15): every field filled, 'none' when empty."""
        plan = clip.plan
        shot = plan.shot
        return {
            "SHOT_ID": plan.identifier, "PURPOSE (never sent)": shot.get("purpose") or "none",
            "MODEL_TARGETS": [clip.model] + ([clip.routing.note] if clip.routing.override else []),
            "DURATION_S": clip.piece.length_s, "SHOT_MODE": "single",
            "INPUTS": {key: value for key, value in clip.inputs.items()},
            "CAMERA": "none" if plan.guide_video else f"{camera_first} {camera_move}".strip(),
            "SUBJECTS": [{"state": person.reference, "label": person.label, "fixed_description": person.fixed_description or "none",
                          "state_line": person.state_line or "none", "at": person.at or "none", "faces": person.faces or "none",
                          "prompt_side_flipped": person.flipped} for person in people] or "none",
            "SETTING": [segment.text for segment in setting] or "none",
            "LOOK": look_block or ("none (a start picture carries it)" if clip.motion_only else "none"),
            "STYLE_WORDS": style_words or "none",
            "BEATS": [f"{number_text(start)}-{number_text(end)}: {words}" for start, end, words in moments] or "none",
            "END_STATE": end_state or "none",
            "DIALOGUE": [identifier for identifier, _, _ in sent] or "none",
            "LAID_IN_FROM_VOICE_TAKES": laid_in or "none",
            "AUDIO": {"room": room or "none", "effects": effects or "none", "music": "none"},
            "TEXT_ON_SCREEN": "plain, unmarked surfaces" if text_in_frame(self.breakdown, shot) else "none",
            "EXCLUDE": negative or "none",
            "PHYSICS_NOTES (never sent)": shot.get("physics_note") or "none",
            "POST_OPS (never sent)": clip.post_ops or "none",
            "CONTENT_RISK (never sent)": shot.get("content_flags") or "none",
            "SEED": clip.seed or "none",
            "BUDGET (never sent)": None if clip.cost is None else round(clip.cost, 2),
        }


# ---------------------------------------------------------------- questions, takes and cost

def side_questions(compiler, plan):
    """The side questions of one shot: for each visible own-sided plot feature (a ring, a scar), which side it is on in
    the take, as the take is made: before the flip in the edit on routes a and b (8.5; C1 R22). Shared by the clip
    pack and the clip book (clip_book.py)."""
    shot = plan.shot
    questions = []
    try:
        sides = image_sides(compiler.breakdown, shot)
    except Exception:
        sides = []
    flipped_note = " (in the take as made, before the flip in the edit)" if plan.prompt_flipped_all else ""
    for entry in sides:
        person = next((person for person in plan.people if person.element == entry.get("element")), None)
        owner = person.name if person else element_name(compiler.breakdown, entry.get("element"))
        for feature in entry.get("features") or []:
            if not feature.get("own") or not feature_shown(shot, feature):
                continue
            if feature_hidden(compiler.breakdown, shot, feature.get("feature")):
                continue
            where = feature.get("prompt") if plan.prompt_flipped_all else feature.get("image")
            words = side_words(compiler.adapters, feature, where) if where and where != "open" else ""
            if words:
                questions.append(f"Is {owner}'s {feature['feature']} {words}{flipped_note}?")
    return questions


def check_questions(compiler, clip, facts):
    """Yes/no questions for the take, built from the records (8.9; B2 R24; C1 Rec11)."""
    phrase = compiler.adapters.phrase
    plan = clip.plan
    shot = plan.shot
    questions = []
    faces = [person for person in plan.people if person.is_person and person.faces != "away"]
    for person in [person for person in plan.people if person.is_person]:
        template = phrase("check_questions", "same_face", default="Is it the same face as {name}'s reference pictures?")
        questions.append(template.replace("{name}", person.name))
    for person in faces:
        if len(faces) > 1:
            questions.append(phrase("check_questions", "face", default="").replace("{name}", person.name))
        else:
            questions.append(f"Is {person.name}'s face readable and true in colour in this light?")
    questions += side_questions(compiler, plan)
    for identifier in clip.speeches:
        entry = next((entry for speech, _, entry in plan.on_screen if speech == identifier), {})
        speaker = element_of(entry.get("speaker") or "")
        person = next((person for person in plan.people if person.element == speaker), None)
        name = person.name if person else person_name(speaker)
        window = None
        for written in shot.get_all("moment"):
            item = split_item(written)
            span = parse_span(item.first)
            if span and re.search(r"\b(says?|asks?|answers?|speaks?|words?)\b", item.get("shows") or "", re.IGNORECASE):
                window = span
                break
        if window:
            questions.append(phrase("check_questions", "mouth", default="").replace("{whose}", f"{name}'s")
                             .replace("{t0}", number_text(window[0])).replace("{t1}", number_text(window[1])))
        else:
            questions.append(f"Does only {name}'s mouth move for the line?")
    if clip.speeches:
        questions.append(phrase("check_questions", "said_once", default="Is each line said once, by the right mouth?"))
    # Never ask whether something stays still: checks catch known failures, and a face that never moves between
    # the written actions is the failure testers found (Project notes 42, W10).
    for person in faces:
        questions.append(phrase("check_questions", "moves_between",
                                default="Does {name} move between the written actions: breathing, eyes, small shifts?")
                         .replace("{name}", person.name))
    if normalise_word(shot.get("move") or "static") == "static":
        questions.append(phrase("check_questions", "camera_holds",
                                default="Does the camera hold its framing, with no drift or zoom?"))
    if plan.held:
        questions.append(phrase("check_questions", "one_take", default="Is it one continuous take, with no cut inside it?"))
    if text_in_frame(compiler.breakdown, shot):
        questions.append(phrase("check_questions", "text_blank", default="Are the surfaces blank, with no letters?"))
    if not is_silent_model(facts):
        questions.append("Is there no music, and no voice but the lines written in this prompt?")
    end = shot.get("end")
    if end and not is_none(end) and clip.piece.number == clip.piece.count:
        questions.append(f"Does it end on this: {lower_first(str(end)).rstrip('.')}?")
    if clip.routing.override and compiler.current_scene_model:
        questions.append(f"Do the faces, clothes and the place match the scene's clips made on "
                         f"{compiler.adapters.display(compiler.current_scene_model)}? (this shot is made on another model, K29)")
    return list(dict.fromkeys(questions))


def takes_and_cost(compiler, clip, facts):
    """Planned draft and final takes (D13 §6.1) and their cost: clip length x (drafts x draft price + finals x price)."""
    table = (compiler.adapters.routing.get("takes") or {}).get("by_cost_class") or {}
    drafts, finals = table.get(clip.plan.cost_class, [2, 3])
    draft = None
    for need in (compiler.adapters.routing.get("need_order") or []) + list(clip.plan.needs):
        if need in clip.plan.needs:
            row = compiler.adapters.need(need)
            if row.get("draft"):
                draft = row["draft"]
                break
    draft = draft or compiler.adapters.routing.get("default_draft") or {}
    clip.draft = {"model": draft.get("model"), "resolution": draft.get("resolution")}
    clip.takes = (drafts, finals)
    clip.price = model_price(facts, clip.piece.resolution, clip.piece.audio_on)
    draft_facts = compiler.adapters.video.get(draft.get("model") or "")
    clip.draft_price = model_price(draft_facts, draft.get("resolution")) if draft_facts else None
    if clip.price is None:
        clip.cost = None
        clip.notes.append(f"{compiler.adapters.display(clip.model)} has no price in the model facts, so this clip is not priced")
        return
    cost = clip.piece.length_s * finals * clip.price
    if drafts:
        cost += clip.piece.length_s * drafts * (clip.draft_price if clip.draft_price is not None else clip.price)
    clip.cost = cost


# ---------------------------------------------------------------- one scene

@dataclass
class ScenePacks:
    scene: str
    label: str
    scene_model: str
    scores: dict
    plans: list
    clips: list
    stills: list
    graphics: list
    notes: list


class Compiler:
    """Everything one compile run shares: the breakdown, the adapters, the project's settings and today's date."""

    def __init__(self, breakdown, adapters, words, raw_speeches, today=None):
        self.breakdown = breakdown
        self.adapters = adapters
        self.words = words or {}
        self.raw = raw_speeches or {}
        self.today = today or datetime.date.today()
        project = breakdown.project
        self.project = project
        self.fixer = WordFixer(adapters, self.words, project)
        self.writer = PromptWriter(breakdown, adapters, self.fixer, self.raw, project)
        self.frame_shape = normalise_word(project.get("frame_shape") if project is not None else "") or "16_9"
        self.frame_shape = self.frame_shape.replace(":", "_")
        self.licensed_only = is_yes(project.get("licensed_data_only")) if project is not None else False
        cap = number_of(project.get("spend_cap_usd")) if project is not None else None
        self.spend_cap = cap
        self.rights = normalise_word(project.get("rights") or "") if project is not None else ""
        use = normalise_word(project.get("intended_use") or "") if project is not None else ""
        self.release = "public" if use in ("festival", "online_free", "online_monetised", "commercial") else "private"
        self.max_age = number_of(constant(breakdown.constants, "model_facts_max_age_days", 30), 30)
        self.age = adapters.age_days(self.today)
        self.current_scene_model = None

    @property
    def fresh(self):
        return self.age is not None and self.age <= self.max_age

    def compile_scene(self, scene_identifier, forced=None):
        breakdown = self.breakdown
        shots = breakdown.shots_of(scene_identifier)
        plans = [analyse_shot(breakdown, self.adapters, shot, self.raw) for shot in shots]
        scene_model, scores = choose_scene_model(self.adapters, plans, self.licensed_only)
        self.current_scene_model = scene_model
        notes = []
        clips = []
        longest_allowed = constant(breakdown.constants, "shot_screen_time_max_s", 600)
        for plan in plans:
            if not plan.video:
                continue
            if (plan.screen_time or 0) > longest_allowed:
                notes.append(f"shot {three_digits(plan.identifier)}: screen time {plan.screen_time:g} seconds is over the "
                             f"most one shot may last ({longest_allowed:g} seconds), so no prompt was made for it; "
                             f"check the value and compile again")
                continue
            routing = route_shot(self.adapters, plan, scene_model, forced, self.licensed_only)
            facts = self.adapters.video.get(routing.model) or {}
            if routing.warning:
                notes.append(f"shot {three_digits(plan.identifier)}: {routing.warning}")
            if routing.error:
                notes.append(f"shot {three_digits(plan.identifier)}: {routing.error}")
            silent = is_silent_model(facts)
            silence = normalise_word(plan.shot.get("silence") or "none")
            audio_on = not silent and silence != "true_silence"
            need = routing.need or (plan.needs[0] if plan.needs else "")
            pieces = plan_pieces(breakdown, self.adapters, plan, routing.model, facts, self.frame_shape,
                                 references=not plan.start_picture and plan.recurring, audio_on=audio_on, need=need)
            for piece in pieces:
                clip = Clip(piece.identifier, plan.identifier, plan.scene, routing.model, piece, plan, routing)
                if piece.chained:
                    clip.notes.append("no planned cutaway fits, so this clip starts from the last picture of the clip before: "
                                      "a flagged last resort (8.4; C5 R31)")
                elif piece.count > 1:
                    clip.notes.append(f"the shot is split at its planned cutaway into {piece.count} clips (8.4)")
                self.writer.build(clip, facts)
                clip.post_ops = self.post_ops(clip, facts)
                clip.seed = self.seed_note(facts, clip)
                takes_and_cost(self, clip, facts)
                clip.questions = check_questions(self, clip, facts)
                clips.append(clip)
        stills = [plan for plan in plans if plan.still_only]
        graphics = [plan for plan in plans if not plan.video and not plan.still_only]
        return ScenePacks(scene_identifier, scene_label(breakdown, scene_identifier), scene_model, scores, plans, clips,
                          stills, graphics, notes)

    def post_ops(self, clip, facts):
        from .derive_fields import post_operations
        try:
            found = list(post_operations(self.breakdown, clip.plan.shot))
        except Exception:
            found = []
        if clip.piece.shape.replace(":", "_") != self.frame_shape:
            found.append("crop")
        if clip.laid_in and any(identifier in clip.laid_in for identifier, _, _ in clip.plan.on_screen):
            found.append("lip_sync")
        for identifier, item, entry in clip.plan.on_screen + clip.plan.off_screen:
            path = normalise_word(item.get("path") or entry.get("path") or "direct")
            if path not in ("direct", "off_screen") and "voice_path" not in found:
                found.append("voice_path")
        return list(dict.fromkeys(found))

    def seed_note(self, facts, clip=None):
        """What to keep so a take can be made again (C3 R18, R24)."""
        seed = facts.get("seed")
        pictures = "start picture" if clip is not None and clip.plan.start_picture else "reference pictures"
        if isinstance(seed, dict):
            if seed.get("fal") is False:
                return f"no seed on fal: to repeat a take, reuse its {pictures} and prompt (C3 R24)"
            if any(value is True for value in seed.values()):
                return "record the seed of the kept take (C3 R18)"
        if seed is True:
            return "record the seed of the kept take (C3 R18)"
        return "no seed documented: record the settings of the kept take"


def routed_model(breakdown, shot, adapters=None):
    """The model compile routes one shot to (the scene model, or another with its reason), for the shot list's Model
    column and the estimate's clip lengths; "" for a shot that is not made as video or when the model facts are
    missing. The routing of each scene is worked out once per breakdown."""
    if shot is None:
        return ""
    scene_identifier = scene_of(shot.identifier)
    cache = getattr(breakdown, "_cache", None)
    key = ("routed_model", scene_identifier)
    if cache is not None and key in cache:
        return cache[key].get(shot.identifier, "")
    adapters = adapters or Adapters()
    table = {}
    if adapters.present:
        project = breakdown.project
        licensed_only = is_yes(project.get("licensed_data_only")) if project is not None else False
        plans = [analyse_shot(breakdown, adapters, each, {}) for each in breakdown.shots_of(scene_identifier)]
        scene_model, _ = choose_scene_model(adapters, plans, licensed_only)
        for plan in plans:
            if plan.video:
                table[plan.identifier] = route_shot(adapters, plan, scene_model, None, licensed_only).model or ""
    if cache is not None:
        cache[key] = table
    return table.get(shot.identifier, "")


# ---------------------------------------------------------------- packs as the GEN checks read them

def pack_file_name(scene, model):
    return f"{scene} - {model}.json"


def build_packs(compiler, scene_packs, forced=False):
    """{(scene, model): pack dict} in the shape checks_plan_generation_film reads."""
    packs = {}
    for scene in scene_packs:
        by_model = {}
        for clip in scene.clips:
            by_model.setdefault(clip.model, []).append(clip)
        for model, clips in by_model.items():
            total = sum(clip.cost for clip in clips if clip.cost is not None) if all(clip.cost is not None for clip in clips) else None
            pack = {
                "about": ("Compiled by stage.py compile from the records; never edit it. Change a record and compile again."
                          if not forced else "A syntax test: every shot compiled for one model (compile --force-model). Never sent as it is."),
                "scene": scene.scene, "scene_label": scene.label, "model": model,
                "model_name": compiler.adapters.display(model), "scene_model": scene.scene_model,
                "compiled_on": compiler.today.isoformat(),
                "model_facts_date": compiler.adapters.checked_on.isoformat() if compiler.adapters.checked_on else None,
                "model_facts_age_days": compiler.age, "paid": False, "not_paid_because": [],
                "release": compiler.release, "forced": bool(forced),
                "total_cost_usd": None if total is None or not compiler.fresh else round(total, 2),
                "clips": [clip.as_pack_entry() for clip in clips],
            }
            if not compiler.fresh:
                for entry in pack["clips"]:
                    entry["cost_usd"] = None
            packs[(scene.scene, model)] = pack
    return packs


def decide_paid(compiler, pack, problems):
    """A pack is marked paid (ready to spend) only on fresh model facts, under the spending cap, with no GEN error
    (8.2 freshness rule; 8.8 rule 1)."""
    reasons = []
    if not compiler.fresh:
        reasons.append(f"the model facts are {compiler.age if compiler.age is not None else 'of unknown'} days old, over "
                       f"{number_text(compiler.max_age)}: refresh them first (stage.py refresh-models)")
    if compiler.spend_cap is None:
        reasons.append("no spending cap is set yet in the project record: nothing is spent until it is")
    elif pack.get("total_cost_usd") is not None and pack["total_cost_usd"] > compiler.spend_cap:
        reasons.append(f"the pack's planned takes cost {money(pack['total_cost_usd'])}, over the cap of {money(compiler.spend_cap)}")
    if pack.get("forced"):
        reasons.append("a syntax test is never paid")
    unknown = sorted({identifier for entry in pack["clips"] for identifier in entry.get("words_unknown") or []})
    if unknown:
        reasons.append(f"{len(unknown)} spoken line{'s are' if len(unknown) != 1 else ' is'} missing from the prompts "
                       "because the story's speeches are missing: compile with the story first")
    clips = {entry["clip"] for entry in pack["clips"]}
    errors = [problem for problem in problems if getattr(problem, "level", "") == "E"
              and (getattr(problem, "record", "") in clips or str(problem).split(" ")[2] in clips)]
    if errors:
        reasons.append(f"{len(errors)} prompt check error{'s' if len(errors) != 1 else ''} to fix first")
    pack["paid"] = not reasons
    pack["not_paid_because"] = reasons
    return pack


def lint(compiler, record_files, story, project, packs, forced=False):
    """The GEN lines for these packs (checks_plan_generation_film.lint_packs); forced makes GEN-02 and GEN-10 notes."""
    from .check_records import CheckRun
    from .checks_plan_generation_film import lint_packs
    run = CheckRun(record_files, compiler.breakdown.schema, compiler.words, compiler.breakdown.constants, story=story,
                   project=project)
    return lint_packs(run, list(packs), forced=forced)


# ---------------------------------------------------------------- the pages the user reads

def three_digits(identifier):
    """A shot's number as the views say it ("150", "010"); a shot ID that is not well formed (FORM-02 reports it) is
    given as written, so one bad ID never stops the compile."""
    number = shot_number(identifier)
    return f"{number:03d}" if number is not None else str(identifier)


def shot_words(identifier):
    number = shot_number(identifier)
    scene = re.sub(r"^SC0*", "", scene_of(identifier) or "")
    return f"scene {scene}, shot {number:03d}" if number is not None else identifier


def clip_save_name(clip):
    scene = re.sub(r"^SC0*", "", clip.scene or "")
    middle = f" - clip {clip.piece.number}" if clip.piece.count > 1 else ""
    return f"Scene {scene} - shot {three_digits(clip.shot)}{middle} - take 01.mp4"


def list_item_line(breakdown, shot_identifier):
    shotlist = next(iter(breakdown.of_scene("SHOTLIST", scene_of(shot_identifier))), None)
    if shotlist is None:
        return ""
    for written in shotlist.get_all("item"):
        item = split_item(written)
        if (item.first or "").strip() == shot_identifier:
            return item.get("shows") or ""
    return ""


SIZE_WORDS = {"extreme_wide": "extreme wide shot", "wide": "wide shot", "medium_wide": "medium wide shot",
              "medium": "medium shot", "medium_close_up": "medium close-up", "close_up": "close-up",
              "extreme_close_up": "extreme close-up", "insert": "insert shot"}


def plain_size(shot):
    size = normalise_word(shot.get("size") or "")
    return SIZE_WORDS.get(size, size.replace("_", " "))


def setup_lines(compiler, model):
    """The one-time account setup of C1 Recipe 1, in plain words."""
    facts = compiler.adapters.video.get(model) or {}
    access = ", ".join(facts.get("access") or [])
    return [
        f"Where to make it: {access or 'see the model facts'}. If no account is connected yet, the easiest start is a "
        "sign-in connector (Runway or Higgsfield: add a custom connector in your chat app's settings, sign in, buy the "
        "smallest pack); for the lowest price, a fal account with one key (C1 Recipe 1).",
        "Test the connection with one cheap 4-second draft and check the charge before anything else.",
    ]


def pack_page(compiler, scene, model, pack, clips, forced=False):
    """The page one scene's pack for one model is read from (8.9)."""
    display = compiler.adapters.display(model)
    lines = [f"# {scene.label} - {display}{' - syntax test' if forced else ''}", ""]
    if forced:
        lines += ["A syntax test: every shot of this scene written for one model to check its words. The notes about "
                  "lengths and splits are expected here. Never send these as they are.", ""]
    lines += ["## How to use this page", ""]
    lines += [f"- {line}" for line in setup_lines(compiler, model)]
    age = compiler.age
    checked = compiler.adapters.checked_on.isoformat() if compiler.adapters.checked_on else "an unknown date"
    lines.append(f"- Model facts are {age if age is not None else 'of unknown age:'} day{'s' if age != 1 else ''} old (checked on {checked})."
                 + ("" if compiler.fresh else " They are too old to spend money on: refresh them first, and until then no money is shown."))
    lines.append("- For each shot: make the pictures under \"Attach, in this order\" first, paste the prompt, set the "
                 "settings, make the planned takes, answer the questions, and save the take you keep under its name.")
    lines.append("- Never change a prompt here. Change the shot in the breakdown and compile again.")
    if pack.get("paid"):
        lines.append(f"- Ready to spend: the planned takes cost {money(pack['total_cost_usd'])}, within your cap.")
    else:
        lines.append("- Not ready to spend yet: " + "; ".join(pack.get("not_paid_because") or ["see the notes"]) + ".")
    if pack.get("release") == "public":
        lines.append("- This film is for release, so every tool used must allow commercial use (D4).")
    lines.append("")
    for clip in clips:
        shot = clip.plan.shot
        seconds = number_text(number_of(shot.get("screen_time"), 0))
        heading = f"## Shot {three_digits(clip.shot)}"
        if clip.piece.count > 1:
            heading += f", clip {clip.piece.number} of {clip.piece.count}"
        lines += [heading, ""]
        description = list_item_line(compiler.breakdown, clip.shot)
        lines.append(f"{plain_size(shot).capitalize()}, {seconds} seconds on screen" + (f": {description}" if description else "."))
        purpose = shot.get("purpose")
        if purpose and not is_none(purpose):
            lines.append(f"What it is for: {purpose}")
        if clip.routing.override:
            lines.append(f"Why this model: {clip.routing.note}.")
        lines += ["", "Prompt:", "", "```text", clip.prompt, "```", ""]
        if clip.negative:
            lines += [f"Leave out (paste into the model's box for things to leave out): {clip.negative}", ""]
        if clip.attach:
            lines.append("Attach, in this order:")
            for index, entry in enumerate(clip.attach, start=1):
                lines.append(f"{index}. {entry['file']}: {entry['job']}")
            lines.append("")
        crop = ""
        if clip.piece.shape.replace(":", "_") != compiler.frame_shape:
            crop = f", cropped to {compiler.frame_shape.replace('_', ':')} in finishing"
        sound = "sound on" if clip.piece.audio_on else "sound off"
        lines.append(f"Settings: {number_text(clip.piece.length_s)} seconds, {clip.piece.resolution}, frame shape "
                     f"{clip.piece.shape}{crop}, {sound}; seed: {clip.seed}.")
        drafts, finals = clip.takes
        draft_name = compiler.adapters.display(clip.draft.get("model")) if clip.draft.get("model") else "the cheapest route"
        draft_size = f" at {clip.draft['resolution']}" if clip.draft.get("resolution") else ""
        cost = (f", about {money(clip.cost)}" if clip.cost is not None and compiler.fresh else
                ", not priced until the model facts are fresh" if not compiler.fresh else "")
        if drafts or finals:
            lines.append(f"Takes: {drafts} cheap draft{'s' if drafts != 1 else ''} on {draft_name}{draft_size} first, then "
                         f"{finals} final take{'s' if finals != 1 else ''}{cost}.")
        if clip.laid_in:
            laid = []
            for identifier in clip.laid_in:
                entry = speech_entry(compiler.breakdown, compiler.raw, identifier)
                laid.append(f"\"{entry.get('text', '')}\"")
            lines.append("Laid in during the edit from the voice takes, never sent to the model: " + ", ".join(laid) + ".")
        if clip.post_ops:
            lines.append("After the take: " + ", ".join(operation.replace("_", " ") for operation in clip.post_ops) + " (finishing jobs).")
        if clip.questions:
            lines += ["", "Check in the result:"]
            lines += [f"- {question}" for question in clip.questions]
        notes = clip.notes + clip.left_out
        if notes:
            lines += ["", "Notes:"]
            lines += [f"- {note}" for note in notes]
        lines += ["", f"Save the take as: {clip_save_name(clip)}", ""]
    return plain_page("\n".join(lines).rstrip() + "\n")


# ---------------------------------------------------------------- pictures to make first

def picture_model(compiler, use, plan=None):
    table = compiler.adapters.routing.get("pictures") or {}
    if use == "storyboard" and plan is not None:
        named = [person for person in plan.people if person.is_person]
        if len(named) >= 3:
            return table.get("storyboard_many_characters") or {}
        return table.get("storyboard_named" if named else "storyboard_other") or {}
    return table.get(use) or {}


def picture_size_words(compiler, entry):
    if compiler.frame_shape == "2.39" and entry.get("size_for_2_39"):
        width, height = entry["size_for_2_39"]
        return f"{width} x {height} pixels (the film's 2.39 frame; K24)"
    size = str(entry.get("size") or "")
    if size.startswith("same as"):
        return "the same size as" + size[len("same as"):]
    if size:
        return f"size {size}"
    return "the film's frame shape"


def description_prompt(compiler, plan, moment_words=""):
    """A full picture description of a shot's first instant: framing, people (keys word for word), place, look block,
    style words (C2 R4)."""
    writer = compiler.writer
    fake = Clip(plan.identifier + ".1", plan.identifier, plan.scene, "", ClipPiece(plan.identifier + ".1", 1, 1, 0.0,
                plan.screen_time, plan.needed_s, "", "", "", False), plan, Routing(""))
    cast = Cast(compiler.breakdown, compiler.adapters, plan, motion_only=False)
    first, _ = writer.camera_words(fake, cast, False)
    parts = [first]
    for person in plan.people:
        parts += [segment.text for segment in writer.subject_block(person, fake, cast, False, for_picture=True)]
    location = location_state_line(compiler.breakdown, plan.shot)
    if location and not is_none(location):
        parts.append(sentence(compiler.fixer.key_words(location)))
    parts += [segment.text for segment in writer.things_block(fake, cast)]
    look = look_of(compiler.breakdown, plan.shot)
    if look is not None and not is_none(look.get("look_block")):
        parts.append(compiler.fixer.key_words(look.get("look_block")))
    style = compiler.breakdown.singleton("STYLE")
    if style is not None and not is_none(style.get("style_words")):
        parts.append(sentence(style.get("style_words")))
    if moment_words:
        parts.append(sentence(moment_words))
    parts.append(sentence(compiler.adapters.phrase("text", "surfaces", default="plain, unmarked surfaces")))
    return " ".join(part for part in parts if part)


def thing_mirror_state(compiler, plan, reference):
    """mirrored, normal or open: how a thing in frame appears in this shot (derive_fields' mirror states)."""
    try:
        states = shot_mirror_states(compiler.breakdown, plan.shot)
    except Exception:  # the mirror states need the eras; a gap there must not stop the pictures
        return "open"
    return (states.get(element_of(reference)) or {}).get("mirror_state") or "open"


def plate_route_prompts(compiler, plan, moment_words=""):
    """(plate prompt, edit prompt) of a start picture on the plate route (8.5; C2 R5).

    The plate is one picture of the place with its mirrored people and mirrored things, described as the model makes
    it, before it is flipped: every image side is turned, and the people and things shown normally are left out.
    The edit prompt adds the people and things shown normally to the flipped plate, described as the finished
    picture shows them. The two are never one prompt: one picture cannot hold sides from before and after a flip.
    The edit prompt is "" when nobody and nothing is added (the flipped plate is then the start picture)."""
    writer = compiler.writer
    added = [person for person in plan.people if not person.flipped]
    added_elements = {person.element for person in added}
    try:
        facings = {entry["element"]: entry.get("facing") for entry in image_sides(compiler.breakdown, plan.shot)}
    except Exception:  # the sides need the set plan and eras; a gap there must not stop the pictures
        facings = {}
    in_plate = []
    for person in plan.people:
        if not person.flipped:
            continue
        if element_of(person.faces) in added_elements:
            # the one they face is added later: the plate says only which way they face, as the finished frame has it
            facing = facings.get(person.element)
            person = dataclass_replace(person, faces=facing if facing in ("camera", "away", "frame_left", "frame_right")
                                       else "")
        in_plate.append(person)
    plate_plan = dataclass_replace(plan, people=in_plate)
    plate_clip = Clip(plan.identifier + ".1", plan.identifier, plan.scene, "", ClipPiece(
        plan.identifier + ".1", 1, 1, 0.0, plan.screen_time, plan.needed_s, "", "", "", False), plate_plan, Routing(""))
    plate_cast = Cast(compiler.breakdown, compiler.adapters, plate_plan, motion_only=False)
    first, _ = writer.camera_words(plate_clip, plate_cast, False)
    parts = [first]
    for person in in_plate:
        parts += [segment.text for segment in writer.subject_block(person, plate_clip, plate_cast, False, for_picture=True)]
    location = location_state_line(compiler.breakdown, plan.shot)
    if location and not is_none(location):
        parts.append(sentence(compiler.fixer.key_words(location)))
    added_names = [name.lower() for person in added for name in (person.name, person_name(person.element)) if name]

    def in_the_plate(reference):
        """A mirrored thing goes in the plate, unless an added person holds it (its at names them): then it is added
        with them, in the finished picture's sides."""
        if thing_mirror_state(compiler, plan, reference) != "mirrored":
            return False
        for written in plan.shot.get_all("thing"):
            item = split_item(written)
            if (item.first or "").strip() == reference:
                where = (item.get("at") or "").lower()
                return not any(re.search(rf"\b{re.escape(name)}\b", where) for name in added_names)
        return True
    parts += [segment.text for segment in writer.things_block(plate_clip, plate_cast, keep=in_the_plate, turned=True)]
    look = look_of(compiler.breakdown, plan.shot)
    if look is not None and not is_none(look.get("look_block")):
        parts.append(compiler.fixer.key_words(look.get("look_block")))
    style = compiler.breakdown.singleton("STYLE")
    if style is not None and not is_none(style.get("style_words")):
        parts.append(sentence(style.get("style_words")))
    if not added and moment_words:
        parts.append(sentence(swap_image_sides(moment_words)))
    parts.append(sentence(compiler.adapters.phrase("text", "surfaces", default="plain, unmarked surfaces")))
    plate = " ".join(part for part in parts if part)
    full_clip = dataclass_replace(plate_clip, plan=plan)
    full_cast = Cast(compiler.breakdown, compiler.adapters, plan, motion_only=False)
    added_things = [segment.text for segment in writer.things_block(
        full_clip, full_cast, keep=lambda reference: not in_the_plate(reference), turned=False, glass=False)]
    if not added and not added_things:
        return plate, ""
    names = and_list([person.name for person in added if person.is_person]
                     + [lower_first(element_name(compiler.breakdown, person.element)) for person in added
                        if not person.is_person])
    edit = [sentence(f"Add {names} to the attached picture" if names else "Add to the attached picture")]
    for person in added:
        edit += [segment.text for segment in writer.subject_block(person, full_clip, full_cast, False, for_picture=True)]
    edit += added_things
    if moment_words:
        edit.append(sentence(moment_words))
    edit.append("Do not mirror them. Keep the background exactly as given.")
    return plate, " ".join(part for part in edit if part)


def reference_turned(compiler, plan, reference):
    """True when a reference picture is attached flipped left to right (8.5). A reference picture shows its element
    as its own words describe it (a person or a thing as not mirrored; a place as its stored set plan is drawn). The
    picture the model makes must show the element as the finished shot does, turned once more when the clip is
    flipped after (routes a and b): on the flip routes every element shown normally is made from flipped references
    (B1 method 1), on the direct route every mirrored element is. The plate route flips its plate instead."""
    route = plan.mirror.route
    if route not in ("flip_all", "flip_with_mirrored_references", "direct", "none"):
        return False
    state = thing_mirror_state(compiler, plan, reference)
    if state not in ("mirrored", "normal"):
        return False
    wanted = "reversed" if (state == "mirrored") != flipped_after(route) else "original"
    drawn = "original"
    element = element_of(reference)
    if element.startswith("LOC-"):
        stored = set_plan(compiler.breakdown, element)
        drawn = stored.orientation if stored is not None else "original"
    return wanted != drawn


def turned_file(file_name):
    """The file name of a picture's copy flipped left to right: 'Reference pictures/Iona.png' -> '... - flipped.png'."""
    path = Path(file_name)
    return str(path.with_name(f"{path.stem} - flipped{path.suffix}"))


def pictures_to_make(compiler, scene):
    """Every picture job the scene's clips and stills need: start and end pictures, reference pictures, stills."""
    jobs = []
    seen = set()
    plans = [clip.plan for clip in scene.clips] + scene.stills
    for plan in plans:
        if plan.identifier in seen:
            continue
        seen.add(plan.identifier)
        if plan.start_picture:
            model = picture_model(compiler, "still_with_move" if plan.still_only else "start")
            moments = [split_item(written) for written in plan.shot.get_all("moment")]
            first_moment = moments[0].get("shows") if moments else ""
            cast = Cast(compiler.breakdown, compiler.adapters, plan, motion_only=False)
            moment = compiler.fixer.fix(cast.rename(first_moment or ""))
            edit_prompt = None
            if plan.mirror.route == "plate":
                model = picture_model(compiler, "plate") or model
                prompt, edit_prompt = plate_route_prompts(compiler, plan, moment)
            else:
                prompt = description_prompt(compiler, plan, moment)
            jobs.append({"picture": f"PIC-{plan.identifier}-START-01", "use": "start",
                         "file": f"Scene {re.sub(r'^SC0*', '', plan.scene)} - shot {three_digits(plan.identifier)} - start picture.png",
                         "model": model.get("model"), "size": picture_size_words(compiler, model), "prompt": prompt,
                         "plate": plan.mirror.route == "plate", "edit_prompt": edit_prompt,
                         "edit_model": picture_model(compiler, "end").get("model"),
                         "why": plan.route_note, "for": plan.identifier})
        if plan.end_picture:
            model = picture_model(compiler, "end")
            end = compiler.fixer.fix(Cast(compiler.breakdown, compiler.adapters, plan, False).rename(plan.shot.get("end") or ""))
            jobs.append({"picture": f"PIC-{plan.identifier}-END-01", "use": "end",
                         "file": f"Scene {re.sub(r'^SC0*', '', plan.scene)} - shot {three_digits(plan.identifier)} - end picture.png",
                         "model": model.get("model"), "size": picture_size_words(compiler, model),
                         "prompt": f"Edit the attached start picture only where it must change: {lower_first(end).rstrip('.')}. Keep everything else exactly as it is.",
                         "why": "the end picture is edited from the start picture (C2 Rule 15)", "for": plan.identifier})
    for clip in scene.clips:
        piece = clip.piece
        identifier = clip.inputs.get("start_picture")
        if piece.number == 1 or piece.chained or not identifier or not str(identifier).startswith("PIC-"):
            continue
        plan = clip.plan
        moment_words = ""
        for written in plan.shot.get_all("moment"):
            item = split_item(written)
            span = parse_span(item.first)
            if span and span[0] <= piece.start + 1e-9 < span[1]:
                moment_words = re.sub(r"\s*\b(?:and|then)\s*$", "", CUTAWAY_WORDS.sub(" ", item.get("shows") or "").strip())
                break
        cast = Cast(compiler.breakdown, compiler.adapters, plan, motion_only=False)
        moment = compiler.fixer.fix(cast.rename(moment_words.strip(" ;,")))
        model = picture_model(compiler, "start")
        edit_prompt = None
        if plan.mirror.route == "plate":
            model = picture_model(compiler, "plate") or model
            prompt, edit_prompt = plate_route_prompts(compiler, plan, moment)
        else:
            prompt = description_prompt(compiler, plan, moment)
        file_name = next((entry["file"] for entry in clip.attach if entry.get("picture") == identifier),
                         f"{identifier}.png")
        jobs.append({"picture": identifier, "use": "start", "file": file_name, "model": model.get("model"),
                     "size": picture_size_words(compiler, model), "prompt": prompt,
                     "plate": plan.mirror.route == "plate", "edit_prompt": edit_prompt,
                     "edit_model": picture_model(compiler, "end").get("model"),
                     "why": f"the first picture of clip {piece.number}, where the shot comes back after its planned "
                            f"cutaway at {number_text(piece.start)} seconds; made like the shot's start picture",
                     "for": plan.identifier, "clip": piece.number})
    references = {}
    turned_copies = {}
    for clip in scene.clips:
        for entry in clip.inputs.get("references") or []:
            if entry.get("picture"):
                if entry.get("flipped"):
                    turned_copies.setdefault(entry["picture"], []).append(clip.plan.identifier)
                    entry = dict(entry, file=entry.get("unflipped_file") or entry.get("file"))
                references.setdefault(entry["picture"], entry)
        for person in clip.plan.people:
            identifier = f"PIC-{person.reference}-REFERENCE-01"
            if clip.plan.start_picture and person.is_person:
                references.setdefault(identifier, {"picture": identifier,
                                                   "file": f"Reference pictures/{person.name}{state_words_of(person.reference)}.png",
                                                   "job": f"{person.name}'s face and clothes in this state"})
    for identifier, entry in sorted(references.items()):
        reference = identifier[len("PIC-"):-len("-REFERENCE-01")]
        element = element_of(reference)
        record = compiler.breakdown.record(element)
        state = state_record(compiler.breakdown, reference)
        fixed = compiler.fixer.key_words(record.get("fixed_description") if record is not None else "")
        state_line = compiler.fixer.key_words(state.get("state_line") if state is not None else "")
        model = picture_model(compiler, "reference")
        if element.startswith("CH-"):
            prompt = ("Using the attached portrait as the exact identity reference, create a character turnaround sheet of "
                      "the same person: full body, front view, three-quarter view facing frame-left, side view facing "
                      f"frame-left, back view. {fixed} {state_line}. Flat, shadowless studio light on a plain, unmarked "
                      "mid-grey background. Keep the face, hair, body proportions and clothing identical in every view. "
                      "3:2 landscape.")
        elif element.startswith("LOC-"):
            look = next((record for record in compiler.breakdown.records_of("LOOK") if record.get("for") == element), None)
            prompt = (f"A wide establishing view of this empty place: {state_line or element_name(compiler.breakdown, element)}. "
                      f"{look.get('look_block') if look is not None else ''} Plain, unmarked surfaces. "
                      "Follow the attached floor plan for walls, doors and furniture.")
        else:
            prompt = (f"Product-style reference sheet of one object: {fixed}{', ' + state_line if state_line else ''}. Three "
                      "views side by side on plain mid-grey: front, three-quarter, top. 3:2.")
        job = {"picture": identifier, "use": "reference", "file": entry.get("file"), "model": model.get("model"),
               "size": model.get("size") and f"size {model['size']}" or "", "prompt": re.sub(r"\s{2,}", " ", prompt),
               "why": "reference pictures of every element state in frame, made once and reused (C2 Rule 1)", "for": reference}
        if identifier in turned_copies:
            shots = sorted(set(turned_copies[identifier]), key=sort_key_for_identifier)
            job["flipped_file"] = turned_file(entry.get("file"))
            job["flipped_for"] = shots
        jobs.append(job)
    for plan in scene.graphics:
        texts = text_in_frame(compiler.breakdown, plan.shot)
        if texts:
            jobs.append({"picture": None, "use": "text_graphic", "file": "Text graphics/", "model": "stage.py graphics",
                         "size": "", "prompt": "", "for": plan.identifier,
                         "why": "readable words are drawn as text graphics, never generated (K17): run stage.py graphics"})
    return jobs


def pictures_page(compiler, scene, jobs):
    lines = [f"# {scene.label} - pictures to make first", "",
             "Make these pictures before any clip: the clips are made from them. Show every start picture to the user "
             "before it is used (C2 §3.7).", ""]
    for job in jobs:
        if job["use"] == "text_graphic":
            lines += [f"## Text for {shot_words(job['for'])}", "", sentence(job["why"]), ""]
            continue
        title = {"start": "Start picture", "end": "End picture", "reference": "Reference pictures"}.get(job["use"], "Picture")
        target = shot_words(job["for"]) if job["use"] != "reference" else Path(job["file"]).stem
        if job.get("clip"):
            target += f", clip {job['clip']}"
        lines += [f"## {title}: {target}", ""]
        model = compiler.adapters.image.get(job.get("model") or "", {})
        lines.append(f"Make it with {model.get('name', job.get('model'))}" + (f", {job['size']}" if job.get("size") else "") + ".")
        lines.append(f"Why: {sentence(job['why'])}")
        lines += ["", "```text", job["prompt"], "```", ""]
        if job.get("plate"):
            if job.get("edit_prompt"):
                editor = compiler.adapters.image.get(job.get("edit_model") or "", {})
                lines += [f"This is the plate: the place as its own world shows it. Flip it left to right, then add the "
                          f"others with {editor.get('name', job.get('edit_model') or 'an image edit model')}: attach "
                          "the flipped plate and their reference pictures, and give it these words:", "",
                          "```text", job["edit_prompt"], "```", ""]
            else:
                lines += ["This is the plate: the place as its own world shows it. Flip it left to right: the flipped "
                          "picture is the start picture.", ""]
        lines.append(f"Save it as: {job['file']}")
        if job.get("flipped_file"):
            lines.append(f"Then save a copy flipped left to right as: {job['flipped_file']}. In the mirror world these "
                         f"shots attach the flipped copy: {'; '.join(shot_words(shot) for shot in job['flipped_for'])}.")
        lines.append("")
    lines += ["## For the records", "",
              "The picture jobs above, by the IDs their PIC records take in 20 Prompts for AI video/Pictures.md:"]
    lines += [f"- {job['picture']}: {job['file']}" for job in jobs if job.get("picture")]
    return plain_page("\n".join(lines).rstrip() + "\n")


# ---------------------------------------------------------------- storyboard frame prompts (add-on A)

def light_sentence(look_block):
    sentences = re.split(r"(?<=[.!?])\s+", str(look_block or "").strip())
    for text in sentences:
        if re.search(r"\b(lit|light|lamp|sun|window|glow|dark|shadow)", text, re.IGNORECASE):
            return text
    return sentences[0] if sentences else ""


def storyboard_prompts(compiler, scene_identifier):
    """The frame prompts for every shot with storyboard: yes (step 12, C2 R3)."""
    breakdown = compiler.breakdown
    style_line = ((compiler.adapters.image_document.get("storyboard_style_lines") or {}).get("default")
                  or "greyscale storyboard frame, charcoal and grey marker, 4 tonal values, strong light and shadow shapes, no color, no text, no arrows")
    frames = []
    for shot in breakdown.shots_of(scene_identifier):
        if not is_yes(shot.get("storyboard")):
            continue
        plan = analyse_shot(breakdown, compiler.adapters, shot, compiler.raw)
        cast = Cast(breakdown, compiler.adapters, plan, motion_only=False)
        fake = Clip(plan.identifier + ".1", plan.identifier, plan.scene, "", ClipPiece(plan.identifier + ".1", 1, 1, 0.0,
                    plan.screen_time, plan.needed_s, "", "", "", False), plan, Routing(""))
        first, _ = compiler.writer.camera_words(fake, cast, False)
        parts = [style_line[0].upper() + style_line[1:] + ".", first]
        for person in plan.people:
            segments = compiler.writer.subject_block(person, fake, cast, False, for_picture=True)
            parts += [segment.text for segment in segments]
        parts += [segment.text for segment in compiler.writer.things_block(fake, cast)]
        look = look_of(breakdown, shot)
        if look is not None:
            parts.append(light_sentence(compiler.fixer.key_words(look.get("look_block"))))
        middle = plan.screen_time / 2
        chosen = ""
        for written in shot.get_all("moment"):
            item = split_item(written)
            span = parse_span(item.first)
            if span and span[0] <= middle <= span[1]:
                chosen = item.get("shows") or ""
        if chosen:
            parts.append(sentence("The moment: " + compiler.fixer.fix(cast.rename(chosen), fake.left_out, "the moment")))
        model = picture_model(compiler, "storyboard", plan)
        scene_number = re.sub(r"^SC0*", "", scene_identifier)
        checks = [f"Is it the same face as {person.name}'s reference pictures?" for person in plan.people if person.is_person][:1]
        for person in plan.people[:1]:
            place = compiler.adapters.phrase("placement", person.at, default="") if person.at else ""
            facing = compiler.adapters.phrase("facing", person.faces, default="") if person.faces and not person.faces.startswith(("ch-", "pr-")) else ""
            if place or facing:
                checks.append(f"Is {person.name} {', '.join(part for part in (place, facing) if part)}?")
        angle = compiler.adapters.phrase("angle", normalise_word(shot.get("angle") or "eye_level"), default="at eye level")
        size_words = plain_size(shot)
        article = "an" if size_words[:1] in "aeiou" and size_words else "a"
        checks.append(f"Is it {article} {size_words}, {lower_first(angle)}?")
        references = []
        for person in plan.people:
            if person.is_person:
                references.append(f"Reference pictures/{person.name}{state_words_of(person.reference)}.png: "
                                  f"{person.name}'s face and clothes")
        frames.append({"shot": shot.identifier, "picture": f"PIC-{shot.identifier}-STORYBOARD-01",
                       "model": model.get("model"), "size": model.get("size"),
                       "prompt": re.sub(r"\s{2,}", " ", " ".join(part for part in parts if part)),
                       "references": references, "checks": checks[:3],
                       "save_as": f"{STORYBOARD_FOLDER}/Scene {scene_number} - shot {three_digits(shot.identifier)} - frame 01.png",
                       "line": list_item_line(breakdown, shot.identifier), "size_words": plain_size(shot),
                       "seconds": number_text(number_of(shot.get("screen_time"), 0)), "left_out": fake.left_out})
    return frames


def storyboard_page(compiler, scene_identifier, frames):
    label = scene_label(compiler.breakdown, scene_identifier)
    lines = [f"# {label} - frame prompts", "",
             "Grey storyboard frames, one per shot marked for a storyboard. Arrows, numbers and captions are added by "
             "the storyboard page, never drawn into a picture (C2 Rule 20). Never change a prompt here: change the shot "
             "and compile again.", ""]
    for frame in frames:
        lines += [f"## Shot {three_digits(frame['shot'])}", "",
                  f"{frame['size_words'].capitalize()}, {frame['seconds']} seconds" + (f": {frame['line']}" if frame['line'] else ".")]
        model = compiler.adapters.image.get(frame.get("model") or "", {})
        lines.append(f"Make it with {model.get('name', frame.get('model'))}" + (f" at {frame['size']}" if frame.get("size") else "") + ".")
        lines += ["", "```text", frame["prompt"], "```", ""]
        if frame["references"]:
            lines.append("Attach, in this order:")
            lines += [f"{index}. {reference}" for index, reference in enumerate(frame["references"], start=1)]
            lines.append("")
        lines.append("Check the frame:")
        lines += [f"- {check}" for check in frame["checks"]]
        if frame["left_out"]:
            lines += ["", "Left out of the prompt:"] + [f"- {note}" for note in frame["left_out"]]
        lines += ["", f"Save it as: {frame['save_as']}", ""]
    lines += ["## For the records", "", "The storyboard frames above, by the IDs their PIC records take in 18 Storyboard/Storyboard frames.md:"]
    lines += [f"- {frame['picture']}: {frame['save_as']}" for frame in frames]
    return plain_page("\n".join(lines).rstrip() + "\n")


# ---------------------------------------------------------------- the command

def read_scene_list(written, breakdown):
    """Scene IDs from --scene: one ID, a comma list or a range SC07..SC10 (7.1)."""
    known = breakdown.scene_identifiers()
    if not written:
        project = breakdown.project
        scope = project.get("scope") if project is not None else None
        if scope and not is_none(scope) and normalise_word(scope) != "all":
            written = scope
        else:
            return [scene for scene in known if breakdown.shots_of(scene)]
    chosen = []
    for piece in [piece.strip() for piece in str(written).split(",") if piece.strip()]:
        if ".." in piece:
            first, last = [part.strip().upper() for part in piece.split("..", 1)]
            low, high = sort_key_for_identifier(first), sort_key_for_identifier(last)
            chosen += [scene for scene in known if low <= sort_key_for_identifier(scene) <= high]
        else:
            chosen.append(piece.upper())
    return list(dict.fromkeys(chosen))


def raw_speeches_of(project_folder=None, story_path=None, constants=None):
    """Every speech as the reader wrote it (with its parenthetical), from speeches.json or a story file."""
    found = {}
    if project_folder is not None:
        path = Path(project_folder) / MACHINE_FOLDER / SPEECHES_FILE
        if path.is_file():
            try:
                with open(path, encoding="utf-8") as handle:
                    for entry in json.load(handle).get("speeches", []):
                        found[entry["id"]] = entry
            except (OSError, ValueError, KeyError):
                pass
    if story_path:
        from .read_story import load_story_file, read_story_lines, speeches_json
        reading = read_story_lines(load_story_file(story_path), constants)
        for entry in speeches_json(reading).get("speeches", []):
            found[entry["id"]] = entry
    return found


def add_compile_arguments(parser):
    parser.add_argument("--scene", help="the scenes to compile: one ID, a comma list, or a range such as SC07..SC10")
    parser.add_argument("--model", help="write packs only for shots routed to these models (a comma list)")
    parser.add_argument("--force-model", dest="force_model", help="compile every shot for one model, to test its words")
    parser.add_argument("--storyboard", action="store_true", help="write the storyboard frame prompts instead of video packs")
    parser.add_argument("--lint-only", dest="lint_only", action="store_true", help="route and lint without writing packs")
    parser.add_argument("--story", help="a story file to read the speeches from (default: the project's)")
    parser.add_argument("--route", help="make the clip book of a route, a model plus the place it runs (for example "
                        "h3-comfyui: MiniMax H3 in ComfyUI, Reference to Video)")


def write_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".part")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def run_compile(context):
    """stage.py compile: route, compile, price and lint the prompts of the scenes asked for, and write the packs."""
    from .project_files import Project, StageStop
    from .check_records import StorySource
    arguments = context.arguments
    folder = Path(context.project)
    adapters = Adapters()
    if not adapters.present:
        raise StageStop("The model facts (_config/adapters/video_models.json) are missing from the tools. Use a complete copy of the skill folder.")
    breakdown = Breakdown.from_project(folder, context.schema, context.words, context.constants)
    story_path = getattr(arguments, "story", None)
    if story_path:
        if not Path(story_path).is_file():
            raise StageStop(f'The story file "{Path(story_path).name}" was not found. Give the path of the story file.')
        breakdown.attach_story_file(story_path)
    raw = raw_speeches_of(folder, story_path, context.constants)
    compiler = Compiler(breakdown, adapters, context.words, raw)
    scenes = read_scene_list(getattr(arguments, "scene", None), breakdown)
    missing = [scene for scene in scenes if not breakdown.shots_of(scene)]
    if not scenes:
        raise StageStop("No shots to compile yet: write the scenes' shots first (step 8).")
    if missing and len(missing) == len(scenes):
        raise StageStop(f"No shots to compile in {', '.join(missing)}: write the scene's shots first (step 8).")
    scenes = [scene for scene in scenes if breakdown.shots_of(scene)]
    forced = None
    if getattr(arguments, "force_model", None):
        forced, facts, retired = adapters.find(arguments.force_model)
        if forced and is_route(facts):
            arguments.route, forced = forced, None
        elif not forced:
            raise StageStop(f"The model \"{arguments.force_model}\" is not in the model facts. Known models: "
                            + ", ".join(sorted(adapters.video)) + ".")
        if retired:
            context.say(f"{arguments.force_model} is retired; testing {adapters.display(forced)}, its replacement.")
    wanted_models = None
    if getattr(arguments, "model", None):
        wanted_models = []
        for written in [piece.strip() for piece in arguments.model.split(",") if piece.strip()]:
            name, _, _ = adapters.find(written)
            if not name:
                raise StageStop(f"The model \"{written}\" is not in the model facts. Known models: " + ", ".join(sorted(adapters.video)) + ".")
            wanted_models.append(name)
    project = Project(folder, context.schema, context.words)
    if getattr(arguments, "storyboard", False):
        return write_storyboards(context, compiler, project, scenes)
    route = chosen_route(adapters, breakdown, arguments, forced)
    if route:
        from .clip_book import compile_route
        return compile_route(context, compiler, project, scenes, route, lint_only=bool(getattr(arguments, "lint_only", False)))
    results = [compiler.compile_scene(scene, forced) for scene in scenes]
    for result in results:
        compiler.current_scene_model = result.scene_model
    packs = build_packs(compiler, results, forced=bool(forced))
    chosen = {key: pack for key, pack in packs.items() if wanted_models is None or key[1] in wanted_models}
    story = StorySource.from_file(story_path, context.constants) if story_path else StorySource.from_project(folder)
    problems = lint(compiler, breakdown.record_files, story, project, chosen.values(), forced=bool(forced))
    for pack in chosen.values():
        decide_paid(compiler, pack, problems)
    # say what happened
    age = compiler.age
    context.say(f"Model facts are {age if age is not None else 'of unknown age:'} day{'s' if age != 1 else ''} old"
                + (f" (checked on {adapters.checked_on.isoformat()})." if adapters.checked_on else "."))
    for result in results:
        by_model = {}
        for clip in result.clips:
            by_model.setdefault(clip.model, []).append(clip)
        spread = ", ".join(f"{adapters.display(model)} {len(clips)}" for model, clips in by_model.items())
        extra = []
        if result.stills:
            extra.append(f"{len(result.stills)} made from still{'s' if len(result.stills) != 1 else ''}")
        if result.graphics:
            extra.append(f"{len(result.graphics)} made in the edit or as text graphics")
        context.say(f"{result.label}: {len(result.clips)} clip{'s' if len(result.clips) != 1 else ''} ({spread})"
                    + (f"; {', '.join(extra)}" if extra else "") + "."
                    + (f" Scene model: {adapters.display(result.scene_model)}." if result.scene_model and not forced else ""))
        for clip in result.clips:
            if clip.routing.override and clip.piece.number == 1:
                context.say(f"  Shot {three_digits(clip.shot)} goes to {adapters.display(clip.model)} as "
                            f"{'one ' + number_text(clip.piece.length_s) + '-second take' if clip.piece.count == 1 else str(clip.piece.count) + ' clips'}: "
                            f"{plain_words(clip.routing.note)}.")
            elif clip.piece.count > 1 and clip.piece.number == 1:
                context.say(f"  Shot {three_digits(clip.shot)} is split into {clip.piece.count} clips on "
                            f"{adapters.display(clip.model)}: {plain_words(clip.notes[0]) if clip.notes else 'at its planned cutaway'}.")
        for note in result.notes:
            context.say(f"  {plain_words(note)}")
    unknown = sorted({identifier for result in results for clip in result.clips for identifier in clip.words_unknown})
    if unknown:
        context.say(f"The story's speeches are missing, so {len(unknown)} spoken line{'s were' if len(unknown) != 1 else ' was'} "
                    "left out of the prompts: read the story (stage.py read) or compile with --story, then compile again.")
    errors = [problem for problem in problems if getattr(problem, "level", "") == "E"]
    warnings = [problem for problem in problems if getattr(problem, "level", "") == "W"]
    for problem in problems:
        context.say(str(problem))
    context.say(f"Lint: {len(errors)} error{'s' if len(errors) != 1 else ''}, {len(warnings)} warning{'s' if len(warnings) != 1 else ''}"
                + (f", {len(problems) - len(errors) - len(warnings)} notes" if len(problems) - len(errors) - len(warnings) else "") + ".")
    if getattr(arguments, "lint_only", False):
        context.summary = f"compile --lint-only: {len(errors)} prompt check errors"
        return 1 if errors else 0
    written = write_packs(context, compiler, project, results, packs, chosen, forced, wanted_models)
    total = sum(pack["total_cost_usd"] for pack in chosen.values() if pack.get("total_cost_usd") is not None)
    if chosen and compiler.fresh and all(pack.get("total_cost_usd") is not None for pack in chosen.values()):
        context.say(f"Planned takes for these packs: about {money(total)} in all.")
    for name in written:
        context.say(f"Written: {name}")
    context.summary = f"compile: {sum(len(pack['clips']) for pack in chosen.values())} clips, {len(errors)} prompt check errors"
    return 1 if errors else 0


def chosen_route(adapters, breakdown, arguments, forced):
    """The route entry compile makes a clip book for: --route (a name or alias), else the project's video_route when
    it names a route and no model is asked for; None for the usual packs (Project notes 43, A2)."""
    from .project_files import StageStop
    written = getattr(arguments, "route", None)
    if written:
        name, facts, _ = adapters.find(written)
        if not name or not is_route(facts):
            routes = sorted(key for key, value in adapters.video.items() if is_route(value))
            raise StageStop(f'The route "{written}" is not in the model facts. Known routes: ' + ", ".join(routes) + ".")
        return name
    if forced or getattr(arguments, "model", None):
        return None
    project = breakdown.project
    value = normalise_word(project.get("video_route") or "") if project is not None else ""
    if value and value not in ("auto", "per_scene", "none", "open"):
        name, facts, _ = adapters.find(value)
        if name and is_route(facts):
            return name
    return None


def write_packs(context, compiler, project, results, packs, chosen, forced, wanted_models):
    folder = Path(project.folder)
    machine = folder / MACHINE_FOLDER / (SYNTAX_TEST_FOLDER if forced else PROMPTS_FOLDER)
    pages = folder / PACK_FOLDER / (SYNTAX_TEST_PAGES if forced else "")
    written = []
    with project.lock():
        machine.mkdir(parents=True, exist_ok=True)
        for result in results:
            for old in machine.glob(f"{result.scene} - *.json"):
                model = old.stem[len(result.scene) + 3:]
                if model.endswith(" pictures") or is_route(compiler.adapters.video.get(model)):
                    continue  # a route's clip book is kept: compile --route makes it
                if (result.scene, model) not in chosen and (wanted_models is None or model in wanted_models):
                    old.unlink()
            for (scene, model), pack in chosen.items():
                if scene != result.scene:
                    continue
                path = machine / pack_file_name(scene, model)
                write_text(path, json.dumps(pack, indent=1, ensure_ascii=False) + "\n")
                clips = [clip for clip in result.clips if clip.model == model]
                page = pages / f"{result.label} - {compiler.adapters.display(model)}.md"
                write_text(page, pack_page(compiler, result, model, pack, clips, forced=bool(forced)))
                written.append(str(page.relative_to(folder)))
            if not forced:
                jobs = pictures_to_make(compiler, result)
                if jobs:
                    write_text(machine / f"{result.scene} - pictures.json",
                               json.dumps({"scene": result.scene, "pictures": jobs}, indent=1, ensure_ascii=False) + "\n")
                    page = pages / f"{result.label} - pictures to make first.md"
                    write_text(page, pictures_page(compiler, result, jobs))
                    written.append(str(page.relative_to(folder)))
        if written and not forced:
            scenes = ", ".join(scene_words_plain(result.scene) for result in results)
            try:
                project.add_log_entry(f"Compiled the prompts for AI video for {scenes}.")
            except (OSError, ValueError):
                pass
    return written


def scene_words_plain(scene_identifier):
    return "scene " + re.sub(r"^SC0*", "", scene_identifier or "")


def write_storyboards(context, compiler, project, scenes):
    folder = Path(project.folder)
    written = []
    count = 0
    with project.lock():
        for scene in scenes:
            frames = storyboard_prompts(compiler, scene)
            if not frames:
                continue
            count += len(frames)
            label = scene_label(compiler.breakdown, scene)
            number = re.sub(r"^SC0*", "", scene)
            path = folder / STORYBOARD_FOLDER / f"Scene {number} - frame prompts.md"
            write_text(path, storyboard_page(compiler, scene, frames))
            written.append(str(path.relative_to(folder)))
            context.say(f"{label}: {len(frames)} frame prompt{'s' if len(frames) != 1 else ''}.")
    if not written:
        context.say("No shot in these scenes is marked for a storyboard (storyboard: yes).")
    for name in written:
        context.say(f"Written: {name}")
    context.summary = f"compile --storyboard: {count} frame prompts"
    return 0


def register_commands(table):
    table.add("compile", "Prompts and packs for AI video: routing, prompts, lint and cost", run_compile,
              add_compile_arguments)
