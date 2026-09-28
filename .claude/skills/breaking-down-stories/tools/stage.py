#!/usr/bin/env python3
"""stage.py: the one command of the Stage kit (blueprint 7.1). It reads the command, finds the project, calls
the module that does the work, prints plain lines and exits 0 (finished, no error), 1 (finished, errors
printed) or 2 (could not run; one plain line says what to do), as blueprint 7.3 says.

Usage, from any folder:
    python <skill folder>/tools/stage.py <command> [options] [--project "<project folder>"]
    python <skill folder>/tools/stage.py help

stage.py finds its own schema, rules, steps, cards and templates through its own location, so the same
command works in Claude Code, in the Claude website's skill folder and in ChatGPT's unpacked tools ZIP.

HOW A MODULE ADDS ITS COMMANDS (for the builders of later work packages)
1. In the module (for example stage_tools/read_story.py) write one function:

       def register_commands(table):
           table.add("read", "Read and number the story", run_read, add_read_arguments)
           table.add("lines", "Every source line mentioning an element", run_lines, add_lines_arguments)

   - run_read(context) does the work and returns 0 (no error) or 1 (error lines printed). When the command
     cannot run at all, raise project_files.StageStop("one plain line saying what to do"): that exits 2.
   - add_read_arguments(parser) adds the command's options to an argparse parser (it may be None).
   - uses_project=False (a keyword of table.add) marks a command that needs no project (new, unpack).
   - context gives: context.arguments (the parsed options), context.project (the project folder, found on
     first use by 7.1's rule or from --project), context.schema, context.words, context.constants,
     context.skill_folder, context.say(line) to print a line, context.summary (one line for log.jsonl) and
     context.project_folder (set it when a command makes or opens a project).
2. Add the module's name to COMMAND_MODULES below, one line. Nothing else in this file changes.
   A module listed there that does not exist yet is skipped, and its planned commands say so plainly.

Every command writes one line in "For machines - do not edit/log.jsonl" of its project (7.3).
Standard library only.
"""

import argparse
import importlib
import os
import sys
import traceback
from pathlib import Path

TOOLS_FOLDER = Path(__file__).resolve().parent
if str(TOOLS_FOLDER) not in sys.path:
    sys.path.insert(0, str(TOOLS_FOLDER))

from stage_tools.project_files import Project, StageStop, find_project  # noqa: E402
from stage_tools.record_format import SKILL_FOLDER, load_skill_data  # noqa: E402

# The modules that register commands, in the order their commands are listed. Add one line per module.
COMMAND_MODULES = [
    "stage_tools.project_files",      # new, status, apply, pack, unpack (WP2)
    "stage_tools.read_story",         # read, lines, selftest (WP3)
    "stage_tools.check_records",      # check (WP4b)
    "stage_tools.derive_fields",      # build (WP4a)
    "stage_tools.adopt_folder",       # adopt, impact, questions (WP4f)
    "stage_tools.make_handout",       # next, handout (WP5)
    "stage_tools.make_exports",       # export (WP6)
    "stage_tools.estimate",           # estimate (WP7)
    "stage_tools.compile_prompts",    # compile (WP8)
    "stage_tools.make_text_graphics", # graphics (WP8)
    "stage_tools.refresh_models",     # refresh-models (WP8)
    "stage_tools.make_previs_plans",  # previs (WP9)
    "stage_tools.build_kit",          # build-kit, lib, import-json, replay (WP13, WP14)
]

# Every command of blueprint 7.1 and the module expected to provide it, for a plain message while a module
# is still missing.
PLANNED_COMMANDS = {
    "new": "project_files", "status": "project_files", "apply": "project_files", "pack": "project_files",
    "unpack": "project_files", "read": "read_story", "lines": "read_story", "selftest": "read_story",
    "adopt": "adopt_folder", "check": "check_records", "build": "derive_fields", "impact": "adopt_folder",
    "questions": "adopt_folder", "next": "make_handout", "handout": "make_handout", "export": "make_exports",
    "estimate": "estimate", "compile": "compile_prompts", "graphics": "make_text_graphics",
    "refresh-models": "refresh_models", "previs": "make_previs_plans", "build-kit": "build_kit",
    "lib": "build_kit", "import-json": "build_kit", "replay": "build_kit",
}


class CommandTable:
    """The commands every module registered: name -> (summary, run, add_arguments, uses_project)."""

    def __init__(self):
        self.commands = {}
        self.module_of = {}
        self.current_module = None

    def add(self, name, summary, run, add_arguments=None, uses_project=True):
        if name in self.commands:
            raise ValueError(f"The command {name} is registered twice ({self.module_of[name]} and {self.current_module}).")
        self.commands[name] = (summary, run, add_arguments, uses_project)
        self.module_of[name] = self.current_module


def load_command_table():
    """Import every module of COMMAND_MODULES that exists and let it register its commands."""
    table = CommandTable()
    broken = {}
    for module_name in dict.fromkeys(COMMAND_MODULES):  # a module listed twice registers once
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError as error:
            if error.name == module_name:
                continue
            broken[module_name] = f"{type(error).__name__}: {error}"
            continue
        except Exception as error:  # a module with a fault must not stop every other command
            broken[module_name] = f"{type(error).__name__}: {error}"
            continue
        register = getattr(module, "register_commands", None)
        if register is None:
            continue
        table.current_module = module_name
        register(table)
    table.current_module = None
    return table, broken


class CommandContext:
    """What a command's run function receives (see the note at the top of this file)."""

    def __init__(self, arguments, command_name):
        self.arguments = arguments
        self.command_name = command_name
        self.skill_folder = SKILL_FOLDER
        self.schema, self.words, self.constants = load_skill_data()
        self.summary = ""
        self.project_folder = None
        self.lines = []

    @property
    def project(self):
        """The project folder (7.1): --project, else found from the current folder. Stops with exit 2 if none."""
        if self.project_folder is None:
            self.project_folder = find_project(getattr(self.arguments, "project", None))
        return self.project_folder

    def say(self, line=""):
        self.lines.append(line)
        print(line, flush=True)


def build_parser(table):
    parser = argparse.ArgumentParser(prog="stage.py", description="The Stage kit's one command (blueprint 7.1).",
                                     add_help=True)
    parser.add_argument("--project", help="the project folder (default: found from the current folder)")
    sub_parsers = parser.add_subparsers(dest="command", metavar="<command>")
    sub_parsers.add_parser("help", help="list the commands")
    for name, (summary, _, add_arguments, _) in table.commands.items():
        command_parser = sub_parsers.add_parser(name, help=summary, description=summary)
        command_parser.add_argument("--project", default=argparse.SUPPRESS,
                                    help="the project folder (default: found from the current folder)")
        if add_arguments is not None:
            add_arguments(command_parser)
    return parser


def logged_arguments(arguments):
    """The options of a command for log.jsonl, with every path reduced to its file name (privacy)."""
    logged = {}
    for key, value in vars(arguments).items():
        if key == "command" or value is None:
            continue
        if isinstance(value, str) and (os.sep in value or "/" in value):
            value = Path(value).name
        logged[key] = value
    return logged


def print_help(table, broken):
    print("stage.py <command> [options]   (python stage.py <command> --help for a command's options)")
    for name, (summary, _, _, _) in table.commands.items():
        print(f"  {name:<15} {summary}")
    missing = sorted(name for name, module in PLANNED_COMMANDS.items() if name not in table.commands)
    if missing:
        print("Not in this copy of the tools yet: " + ", ".join(missing) + ".")
    for module_name, reason in broken.items():
        print(f"Could not load {module_name}: {reason}")


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    argv = list(sys.argv[1:] if argv is None else argv)
    table, broken = load_command_table()
    first_word = next((word for word in argv if not word.startswith("-")), None)
    if first_word and first_word not in table.commands and first_word != "help" and first_word in PLANNED_COMMANDS:
        module = PLANNED_COMMANDS[first_word]
        reason = broken.get(f"stage_tools.{module}")
        if not reason and (TOOLS_FOLDER / "stage_tools" / f"{module}.py").is_file():
            print(f"The command {first_word} is planned but not built yet (stage_tools/{module}.py does not provide "
                  "it). Use what the house rules give for it when you cannot run code.")
            return 2
        detail = f" (loading it failed: {reason})" if reason else f" (stage_tools/{module}.py is missing)"
        print(f"The command {first_word} is not available in this copy of the tools{detail}. "
              "Use a complete copy of the skill folder.")
        return 2
    parser = build_parser(table)
    try:
        arguments = parser.parse_args(argv)
    except SystemExit as stop:
        return 0 if stop.code == 0 else 2
    if arguments.command in (None, "help"):
        print_help(table, broken)
        return 0 if arguments.command == "help" else 2
    summary, run, _, uses_project = table.commands[arguments.command]
    context = CommandContext(arguments, arguments.command)
    exit_code = 2
    try:
        if uses_project:
            context.project
        exit_code = run(context)
        exit_code = 0 if exit_code is None else int(exit_code)
    except StageStop as stop:
        print(stop.message)
        context.summary = context.summary or stop.message
        exit_code = 2
    except BrokenPipeError:
        raise
    except KeyboardInterrupt:
        print("Stopped before the command finished. Nothing half-written was kept; run it again.")
        exit_code = 2
    except Exception as error:  # every failure ends with one plain line and exit 2 (7.3)
        print(f"stage.py could not finish {arguments.command}: {type(error).__name__}: {error}. "
              "Run it again; if it happens again, report this line.")
        if os.environ.get("STAGE_DEBUG"):
            traceback.print_exc()
        context.summary = context.summary or f"{type(error).__name__}: {error}"
        exit_code = 2
    if context.project_folder is not None:
        try:
            Project(context.project_folder, context.schema, context.words).log_command(
                arguments.command, logged_arguments(arguments), exit_code, context.summary)
        except OSError:
            pass
    return exit_code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # The reader of the output stopped early (for example "| head"); stop quietly.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(0)
