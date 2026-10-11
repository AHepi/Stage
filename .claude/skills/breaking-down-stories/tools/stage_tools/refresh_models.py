"""refresh_models.py: keep the dated model facts in _config/adapters/ fresh, and run the command refresh-models.

In plain words:
- the model facts (_config/adapters/video_models.json, image_models.json, audio_models.json, routing.json,
  phrasebook.json and prices.json) carry the date they were checked on; above model_facts_max_age_days
  (_config/rules/constants.json) compile marks no pack ready to spend and estimate prints no money (blueprint 8.2, the
  freshness rule; GEN-11; D13 R7);
- this tool never reads the web: an AI with web access re-reads the makers' pages and writes what it found in a
  findings file (the shape is below); `refresh-models --propose <findings file>` applies the findings to copies of
  the files, checks their shape, and writes the proposal to _config/adapters/proposal/ with a plain list of every change;
- the user approves any price change; `refresh-models --apply` then writes the proposal over the files with the new
  date, and keeps the files it replaced in _config/adapters/previous/<their date>/ so a refresh can be undone;
- `refresh-models --check` checks the shape of the files as they are; with no option it says how old they are and
  what to do.

The findings file (JSON):
    {"checked_on": "2026-10-27",
     "files_checked": ["video_models.json", "prices.json"],      (optional; default: every dated file)
     "changes": [
       {"file": "video_models.json", "path": "models/kling-3.0/price_usd_per_s/audio", "value": 0.18,
        "mark": "V", "source": "https://fal.ai/models/..."},
       {"file": "video_models.json", "path": "models/kling-3.0/status", "value": "retired", "mark": "V",
        "source": "https://..."},
       {"file": "video_models.json", "path": "models/old-model", "remove": true, "mark": "V", "source": "https://..."}]}
A mark is V (read on the maker's page), U (not confirmed) or J (a judgement), as in the research files (C1 section 0).
A change to a model's fact also writes its mark and source into the model's "marks"; a change inside prices.json
sets the entry's url and evidence. Paths use "/" between keys; a number is a list position.

Command: refresh-models [--propose <findings file>] [--apply [--prices-approved]] [--check] [--adapters <folder>].
Exit 0: done; 1: shape problems, or price changes waiting for the user's approval; 2: could not run.
Standard library only; no web requests.
"""

import copy
import datetime
import hashlib
import json
import re
import shutil
from pathlib import Path

from .record_format import ADAPTERS_FOLDER, SKILL_FOLDER

PROPOSAL_FOLDER = "proposal"
PREVIOUS_FOLDER = "previous"
PROPOSAL_FILE = "proposal.json"
PROPOSAL_PAGE = "proposal.md"
DATED_FILES = ("video_models.json", "image_models.json", "audio_models.json", "routing.json", "phrasebook.json",
               "prices.json")
MARK_LETTERS = ("V", "U", "J")
PRICE_KEY = re.compile(r"price|per_s|usd|per_image|per_minute|per_month|cost", re.IGNORECASE)
TEXT_KEYS_UNDER_PRICES = {"route", "note", "what", "unit", "url", "evidence", "source", "about", "model", "currency",
                          "plan", "name", "why"}
RESOLUTION = re.compile(r"^\d{3,4}p$|^\d[kK]$")
SHAPE = re.compile(r"^\d+(?:\.\d+)?:\d+(?:\.\d+)?$")
STATUS_VALUES = ("current", "preview", "test_first", "superseded_still_sold", "retired", "edit", "performance")
LIMIT_UNITS = ("characters", "tokens", "words")


def adapters_folder(written=None):
    return Path(written) if written else Path(SKILL_FOLDER) / ADAPTERS_FOLDER


def read_documents(folder):
    """{file name: document} for every JSON file directly in the adapters folder."""
    documents = {}
    for path in sorted(Path(folder).glob("*.json")):
        with open(path, encoding="utf-8") as handle:
            documents[path.name] = json.load(handle)
    return documents


def fingerprint(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() if Path(path).is_file() else None


def read_date(text):
    try:
        return datetime.date.fromisoformat(str(text)[:10])
    except (TypeError, ValueError):
        return None


def split_path(path):
    """'models/kling-3.0/length_s/max' -> ['models', 'kling-3.0', 'length_s', 'max']; a list is kept."""
    if isinstance(path, list):
        return [str(part) for part in path]
    return [part for part in str(path or "").split("/") if part != ""]


def get_at(document, parts):
    current = document
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return None, False
    return current, True


def set_at(document, parts, value, remove=False):
    """Set (or remove) the value at a path, making dictionaries on the way. Returns a problem in words, or ''."""
    current = document
    for index, part in enumerate(parts[:-1]):
        if isinstance(current, dict):
            if part not in current:
                if remove:
                    return f"nothing at {'/'.join(parts[:index + 1])} to remove"
                current[part] = {}
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return f"{'/'.join(parts[:index + 1])} is not a place a value can go"
    last = parts[-1]
    if isinstance(current, dict):
        if remove:
            if last not in current:
                return f"nothing at {'/'.join(parts)} to remove"
            del current[last]
        else:
            current[last] = value
        return ""
    if isinstance(current, list) and last.isdigit():
        position = int(last)
        if remove:
            if position >= len(current):
                return f"nothing at {'/'.join(parts)} to remove"
            del current[position]
        elif position < len(current):
            current[position] = value
        elif position == len(current):
            current.append(value)
        else:
            return f"{'/'.join(parts)} is past the end of its list"
        return ""
    return f"{'/'.join(parts[:-1])} is not a place a value can go"


def is_price_change(file_name, parts, old, new):
    if any(PRICE_KEY.search(part) for part in parts):
        return True
    if file_name == "prices.json" and (isinstance(old, (int, float)) or isinstance(new, (int, float))):
        return True
    return False


def walk(value, parts=()):
    """(path parts, key, value) for every value in a document."""
    if isinstance(value, dict):
        for key, inner in value.items():
            yield parts + (str(key),), str(key), inner
            yield from walk(inner, parts + (str(key),))
    elif isinstance(value, list):
        for index, inner in enumerate(value):
            yield parts + (str(index),), str(index), inner
            yield from walk(inner, parts + (str(index),))


# ---------------------------------------------------------------- the shape check

def shape_problems(documents, today=None):
    """Plain sentences, one per problem, for a set of adapter documents (the files as they are or as proposed)."""
    today = today or datetime.date.today()
    problems = []
    for file_name in DATED_FILES:
        if file_name not in documents:
            problems.append(f"{file_name} is missing")
    for file_name, document in documents.items():
        if not isinstance(document, dict):
            problems.append(f"{file_name} is not a JSON object")
            continue
        for key in ("checked_on", "price_date"):
            if key in document:
                date = read_date(document[key])
                if date is None:
                    problems.append(f"{file_name}: {key} \"{document[key]}\" is not a date written as YYYY-MM-DD")
                elif date > today + datetime.timedelta(days=1):
                    problems.append(f"{file_name}: {key} {date.isoformat()} is in the future")
        if file_name in DATED_FILES and "checked_on" not in document:
            problems.append(f"{file_name} has no checked_on date")
        for parts, key, value in walk(document):
            price_path = any(PRICE_KEY.search(part) for part in parts)
            if not price_path or key in TEXT_KEYS_UNDER_PRICES or parts[-1] == "marks" or "marks" in parts:
                continue
            if isinstance(value, bool):
                continue
            if isinstance(value, (int, float)) and value < 0:
                problems.append(f"{file_name}: the price at {'/'.join(parts)} is below zero")
            if isinstance(value, str) and re.fullmatch(r"\$?\s*-?\d+(?:\.\d+)?", value.strip()):
                problems.append(f"{file_name}: the price at {'/'.join(parts)} is written as text; write it as a number")
    video = documents.get("video_models.json")
    if isinstance(video, dict):
        problems += video_problems(video)
        known = set((video.get("models") or {}).keys())
        routing = documents.get("routing.json")
        if isinstance(routing, dict):
            problems += routing_problems(routing, video)
        for old, replacements in (video.get("retired") or {}).items():
            for name in replacements if isinstance(replacements, list) else [replacements]:
                if name and name not in known:
                    problems.append(f"video_models.json: the retired model {old} names a replacement that is not a "
                                    f"model: {name}")
    image = documents.get("image_models.json")
    if isinstance(image, dict):
        models = image.get("models")
        if not isinstance(models, dict) or not models:
            problems.append("image_models.json has no models")
        else:
            for name, facts in models.items():
                problems += common_model_problems("image_models.json", name, facts)
    phrasebook = documents.get("phrasebook.json")
    if isinstance(phrasebook, dict):
        for key in ("size", "move", "angle", "text_graphics"):
            if key not in phrasebook:
                problems.append(f"phrasebook.json has no {key} section")
    return problems


def common_model_problems(file_name, name, facts):
    problems = []
    if not isinstance(facts, dict):
        return [f"{file_name}: the model {name} is not a JSON object"]
    if not isinstance(facts.get("name"), str) or not facts.get("name"):
        problems.append(f"{file_name}: the model {name} has no name")
    marks = facts.get("marks")
    if not isinstance(marks, dict):
        problems.append(f"{file_name}: the model {name} has no marks (every fact carries V, U or J and its source)")
    else:
        for key, mark in marks.items():
            if not isinstance(mark, str) or not mark.strip()[:1] in MARK_LETTERS:
                problems.append(f"{file_name}: the mark of {name} {key} does not start with V, U or J")
    status = facts.get("status")
    if status is not None and status not in STATUS_VALUES:
        problems.append(f"{file_name}: the model {name} has the status \"{status}\"; use one of "
                        + ", ".join(STATUS_VALUES))
    return problems


def video_problems(video):
    problems = []
    models = video.get("models")
    if not isinstance(models, dict) or not models:
        return ["video_models.json has no models"]
    aliases = {}
    for name, facts in models.items():
        problems += common_model_problems("video_models.json", name, facts)
        if not isinstance(facts, dict):
            continue
        length = facts.get("length_s")
        if length is not None:
            if not isinstance(length, dict):
                problems.append(f"video_models.json: {name} length_s is not min, max and step, or a list of allowed lengths")
            elif "allowed" in length:
                allowed = length.get("allowed")
                if not isinstance(allowed, list) or not allowed or not all(isinstance(value, (int, float)) and value > 0 for value in allowed):
                    problems.append(f"video_models.json: {name} length_s allowed is not a list of lengths in seconds")
            else:
                low, high = length.get("min", 0), length.get("max")
                if not isinstance(high, (int, float)) or high <= 0 or not isinstance(low, (int, float)) or low > high:
                    problems.append(f"video_models.json: {name} length_s needs a max above its min")
        for key, pattern, words in (("resolution", RESOLUTION, "a size like 720p or 4K"),
                                    ("shapes", SHAPE, "a frame shape like 16:9")):
            values = facts.get(key)
            if values is None:
                continue
            if not isinstance(values, list) or not all(isinstance(value, str) and pattern.match(value) for value in values):
                problems.append(f"video_models.json: every {key} of {name} must be {words}")
        speaker = facts.get("speaker")
        if speaker is not None and (not isinstance(speaker, str) or "{line}" not in speaker):
            problems.append(f"video_models.json: the speaker form of {name} has no {{line}}")
        limit = facts.get("prompt_limit")
        if limit is not None:
            units = [unit for unit in LIMIT_UNITS if isinstance(limit, dict) and unit in limit]
            if len(units) != 1 or not isinstance(limit[units[0]], int) or limit[units[0]] <= 0:
                problems.append(f"video_models.json: the prompt limit of {name} needs one of characters, tokens or "
                                "words, as a whole number")
        for alias in facts.get("aliases") or []:
            other = aliases.get(str(alias).lower())
            if other and other != name:
                problems.append(f"video_models.json: the alias {alias} names both {other} and {name}")
            aliases[str(alias).lower()] = name
    return problems


def routing_problems(routing, video):
    problems = []
    models = video.get("models") or {}
    retired = video.get("retired") or {}
    for need, row in (routing.get("needs") or {}).items():
        if not isinstance(row, dict):
            continue
        for key in ("first", "backup", "draft"):
            names = row.get(key) or []
            for name in names if isinstance(names, list) else [names]:
                if isinstance(name, dict):
                    name = name.get("model")
                if not name or not isinstance(name, str):
                    continue
                if name in retired:
                    problems.append(f"routing.json: the {key} choice for {need} is the retired model {name}")
                elif name not in models:
                    problems.append(f"routing.json: the {key} choice for {need} is {name}, which is not in video_models.json")
    draft = (routing.get("default_draft") or {}).get("model") if isinstance(routing.get("default_draft"), dict) else None
    if draft and draft not in models:
        problems.append(f"routing.json: the default draft model {draft} is not in video_models.json")
    return problems


# ---------------------------------------------------------------- propose and apply

def read_findings(path):
    path = Path(path)
    if not path.is_file():
        return None, f"The findings file \"{path.name}\" was not found."
    try:
        with open(path, encoding="utf-8") as handle:
            findings = json.load(handle)
    except json.JSONDecodeError as error:
        return None, f"The findings file is not valid JSON (line {error.lineno}): {error.msg}."
    if not isinstance(findings, dict) or not isinstance(findings.get("changes", []), list):
        return None, "The findings file must be a JSON object with a list of changes."
    if read_date(findings.get("checked_on")) is None:
        return None, "The findings file needs checked_on: the date the pages were read, written as YYYY-MM-DD."
    return findings, ""


def propose(folder, findings, today=None):
    """Apply findings to copies of the adapter files. Returns (proposed documents, proposal summary)."""
    today = today or datetime.date.today()
    current = read_documents(folder)
    proposed = copy.deepcopy(current)
    checked_on = read_date(findings.get("checked_on"))
    changes = []
    problems = []
    for number, change in enumerate(findings.get("changes") or [], start=1):
        if not isinstance(change, dict):
            problems.append(f"change {number} is not a JSON object")
            continue
        file_name = str(change.get("file") or "")
        if file_name not in proposed:
            problems.append(f"change {number}: there is no adapter file called \"{file_name}\"")
            continue
        parts = split_path(change.get("path"))
        if not parts:
            problems.append(f"change {number}: it has no path")
            continue
        mark = str(change.get("mark") or "").strip()
        source = str(change.get("source") or "").strip()
        if mark[:1] not in MARK_LETTERS:
            problems.append(f"change {number} ({'/'.join(parts)}): its mark must be V, U or J")
        if mark[:1] == "V" and not source:
            problems.append(f"change {number} ({'/'.join(parts)}): a V mark needs the page it was read on (source)")
        remove = bool(change.get("remove"))
        if not remove and "value" not in change:
            problems.append(f"change {number} ({'/'.join(parts)}): it has no value (or remove: true)")
            continue
        old, existed = get_at(proposed[file_name], parts)
        new = None if remove else change.get("value")
        if existed and not remove and old == new:
            changes.append({"file": file_name, "path": "/".join(parts), "old": old, "new": new, "same": True,
                            "mark": mark, "source": source, "price": False})
            continue
        problem = set_at(proposed[file_name], parts, new, remove=remove)
        if problem:
            problems.append(f"change {number}: {problem}")
            continue
        write_mark(proposed[file_name], file_name, parts, mark, source, checked_on, remove)
        changes.append({"file": file_name, "path": "/".join(parts), "old": old if existed else None, "new": new,
                        "added": not existed, "removed": remove, "mark": mark, "source": source,
                        "price": is_price_change(file_name, parts, old, new)})
    files_checked = findings.get("files_checked") or [name for name in DATED_FILES if name in proposed]
    for file_name in files_checked:
        document = proposed.get(file_name)
        if not isinstance(document, dict):
            problems.append(f"files_checked names \"{file_name}\", which is not an adapter file")
            continue
        document["checked_on"] = checked_on.isoformat()
        if "price_date" in document:
            document["price_date"] = checked_on.isoformat()
    problems += shape_problems(proposed, today)
    changed_files = sorted(name for name in proposed if proposed[name] != current.get(name))
    summary = {
        "about": "A proposed refresh of the model facts, made by stage.py refresh-models --propose. Nothing is used "
                 "until refresh-models --apply writes it; any price change needs the user's approval first.",
        "made_on": today.isoformat(), "checked_on": checked_on.isoformat(),
        "files": changed_files,
        "base_fingerprints": {name: fingerprint(Path(folder) / name) for name in changed_files},
        "changes": changes,
        "price_changes": [change for change in changes if change.get("price") and not change.get("same")],
        "problems": problems, "shape_ok": not problems,
    }
    return proposed, summary


def write_mark(document, file_name, parts, mark, source, checked_on, removed):
    """Write the change's mark and source where the file keeps them: a model's marks, or a price entry's url."""
    if not mark:
        return
    words = f"{mark} {source}".strip() + f" (checked {checked_on.isoformat()})"
    if parts[0] == "models" and len(parts) >= 3 and isinstance(document.get("models"), dict):
        model = document["models"].get(parts[1])
        if isinstance(model, dict):
            model.setdefault("marks", {})
            if isinstance(model["marks"], dict):
                model["marks"][parts[2]] = words
            if source:
                sources = model.setdefault("sources", [])
                if isinstance(sources, list) and source not in sources:
                    sources.append(source)
        return
    if file_name == "prices.json" and not removed and len(parts) >= 2:
        parent, found = get_at(document, parts[:-1])
        if found and isinstance(parent, dict):
            if source:
                parent["url"] = source
            parent["evidence"] = {"V": "verified", "U": "research", "J": "judgement"}.get(mark[:1], parent.get("evidence"))


def short(value, limit=80):
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    return text if len(text) <= limit else text[:limit - 3] + "..."


def proposal_page(summary):
    lines = ["# Proposed refresh of the model facts", "",
             f"Pages read on {summary['checked_on']}; proposal made on {summary['made_on']}.", ""]
    if summary["problems"]:
        lines += ["## Problems to fix first", ""] + [f"- {problem}" for problem in summary["problems"]] + [""]
    prices = summary["price_changes"]
    if prices:
        lines += ["## Price changes the user approves", ""]
        lines += [f"- {change['file']} {change['path']}: {short(change['old'])} becomes {short(change['new'])} "
                  f"({change['mark']} {change['source']})".rstrip() for change in prices]
        lines.append("")
    others = [change for change in summary["changes"] if not change.get("price") and not change.get("same")]
    if others:
        lines += ["## Other changes", ""]
        for change in others:
            if change.get("removed"):
                what = "removed"
            elif change.get("added"):
                what = f"added: {short(change['new'])}"
            else:
                what = f"{short(change['old'])} becomes {short(change['new'])}"
            lines.append(f"- {change['file']} {change['path']}: {what} ({change['mark']} {change['source']})".rstrip())
        lines.append("")
    same = [change for change in summary["changes"] if change.get("same")]
    if same:
        lines += [f"Checked and unchanged: {len(same)} fact{'s' if len(same) != 1 else ''}.", ""]
    lines.append("To use it: stage.py refresh-models --apply" + (" --prices-approved, once the user has approved the "
                                                                  "price changes above" if prices else "") + ".")
    return "\n".join(lines).rstrip() + "\n"


def write_json(path, document):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".part")
    temporary.write_text(json.dumps(document, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def apply_proposal(folder, prices_approved=False, today=None):
    """(exit code, lines to print). Writes the proposal over the adapter files, keeping the replaced files."""
    folder = Path(folder)
    proposal_folder = folder / PROPOSAL_FOLDER
    summary_path = proposal_folder / PROPOSAL_FILE
    if not summary_path.is_file():
        return 2, ["There is no proposal to apply: run stage.py refresh-models --propose <findings file> first."]
    with open(summary_path, encoding="utf-8") as handle:
        summary = json.load(handle)
    if not summary.get("shape_ok"):
        return 1, ["The proposal has problems (see _config/adapters/proposal/proposal.md): fix the findings and propose again."]
    for name, print_ in (summary.get("base_fingerprints") or {}).items():
        if fingerprint(folder / name) != print_:
            return 1, [f"{name} changed after the proposal was made: propose again from the same findings."]
    proposed = read_documents(folder)
    for name in summary.get("files") or []:
        path = proposal_folder / name
        if not path.is_file():
            return 1, [f"The proposal is missing {name}: propose again."]
        with open(path, encoding="utf-8") as handle:
            proposed[name] = json.load(handle)
    problems = shape_problems(proposed, today)
    if problems:
        return 1, ["The proposed files do not pass the shape check:"] + [f"  {problem}" for problem in problems]
    prices = summary.get("price_changes") or []
    if prices and not prices_approved:
        lines = [f"{len(prices)} price change{'s wait' if len(prices) != 1 else ' waits'} for the user's approval:"]
        lines += [f"  {change['file']} {change['path']}: {short(change['old'])} becomes {short(change['new'])}" for change in prices]
        lines.append("Show them to the user. Once approved, run stage.py refresh-models --apply --prices-approved.")
        return 1, lines
    written = []
    for name in summary.get("files") or []:
        old_path = folder / name
        if old_path.is_file():
            with open(old_path, encoding="utf-8") as handle:
                old = json.load(handle)
            old_date = str(old.get("checked_on") or "undated") if isinstance(old, dict) else "undated"
            keep = folder / PREVIOUS_FOLDER / old_date / name
            keep.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(old_path, keep)
        write_json(old_path, proposed[name])
        written.append(name)
    shutil.rmtree(proposal_folder, ignore_errors=True)
    lines = [f"Model facts refreshed: {', '.join(written) or 'no file changed'}; dated {summary.get('checked_on')}.",
             f"The replaced files are kept in _config/adapters/{PREVIOUS_FOLDER}/."]
    if prices:
        lines.append(f"{len(prices)} price change{'s' if len(prices) != 1 else ''} applied with the user's approval.")
    return 0, lines


def ages(folder, today=None):
    today = today or datetime.date.today()
    found = []
    for name, document in read_documents(folder).items():
        if isinstance(document, dict) and "checked_on" in document:
            date = read_date(document.get("checked_on"))
            found.append((name, date, (today - date).days if date else None))
    return found


# ---------------------------------------------------------------- the command

def add_refresh_arguments(parser):
    parser.add_argument("--propose", metavar="FINDINGS", help="a findings file (JSON) written from the makers' pages")
    parser.add_argument("--apply", action="store_true", help="write the proposal over the model facts")
    parser.add_argument("--prices-approved", action="store_true",
                        help="the user has approved the proposal's price changes")
    parser.add_argument("--check", action="store_true", help="check the shape of the model facts as they are")
    parser.add_argument("--adapters", help="the adapters folder (default: the skill's _config/adapters/)")


def run_refresh(context):
    """stage.py refresh-models: propose, check or apply a dated refresh of the model facts (8.2)."""
    from .project_files import StageStop
    arguments = context.arguments
    folder = adapters_folder(getattr(arguments, "adapters", None))
    if not folder.is_dir() or not any(folder.glob("*.json")):
        raise StageStop("The model facts (the adapters folder) are missing. Use a complete copy of the skill folder.")
    from .derive_fields import constant
    # _config/rules/constants.json keeps its values under "constants" (and "from_blueprint_text"), never at the top level
    limit = constant(context.constants, "model_facts_max_age_days", 30) or 30
    if getattr(arguments, "propose", None):
        findings, problem = read_findings(arguments.propose)
        if findings is None:
            raise StageStop(problem)
        proposed, summary = propose(folder, findings)
        proposal_folder = folder / PROPOSAL_FOLDER
        if proposal_folder.exists():
            shutil.rmtree(proposal_folder)
        for name in summary["files"]:
            write_json(proposal_folder / name, proposed[name])
        write_json(proposal_folder / PROPOSAL_FILE, summary)
        (proposal_folder / PROPOSAL_PAGE).write_text(proposal_page(summary), encoding="utf-8")
        real = [change for change in summary["changes"] if not change.get("same")]
        context.say(f"Proposal written to _config/adapters/{PROPOSAL_FOLDER}/: {len(real)} change{'s' if len(real) != 1 else ''} "
                    f"in {len(summary['files'])} file{'s' if len(summary['files']) != 1 else ''}, dated {summary['checked_on']}.")
        if summary["price_changes"]:
            context.say(f"{len(summary['price_changes'])} of them change a price: show them to the user for approval "
                        f"(_config/adapters/{PROPOSAL_FOLDER}/{PROPOSAL_PAGE}).")
        for problem in summary["problems"]:
            context.say(f"  Problem: {problem}")
        context.summary = f"refresh-models --propose: {len(real)} changes, {len(summary['problems'])} problems"
        return 1 if summary["problems"] else 0
    if getattr(arguments, "apply", False):
        code, lines = apply_proposal(folder, prices_approved=getattr(arguments, "prices_approved", False))
        for line in lines:
            context.say(line)
        context.summary = f"refresh-models --apply: exit {code}"
        if code == 2:
            raise StageStop(lines[0])
        return code
    problems = shape_problems(read_documents(folder))
    for name, date, age in ages(folder):
        old = age is not None and age > limit
        context.say(f"{name}: checked on {date.isoformat() if date else 'an unknown date'}"
                    + (f", {age} day{'s' if age != 1 else ''} old" if age is not None else "")
                    + (" - too old to spend money on" if old else "") + ".")
    if getattr(arguments, "check", False) or problems:
        if problems:
            context.say(f"Shape check: {len(problems)} problem{'s' if len(problems) != 1 else ''}.")
            for problem in problems:
                context.say(f"  {problem}")
        else:
            context.say("Shape check: the model facts are in order.")
    if not getattr(arguments, "check", False):
        context.say("To refresh: an AI with web access re-reads the makers' pages named under \"sources\" in each "
                    "model, writes a findings file (its shape is in stage_tools/refresh_models.py), and runs "
                    "stage.py refresh-models --propose <findings file>; the user approves any price change; then "
                    "stage.py refresh-models --apply.")
    context.summary = f"refresh-models: {len(problems)} shape problems"
    return 1 if problems else 0


def register_commands(table):
    table.add("refresh-models", "Refresh the dated model facts: propose from the makers' pages, check, apply",
              run_refresh, add_refresh_arguments, uses_project=False)
