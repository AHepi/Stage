"""The package behind stage.py: one module per job (blueprint 7.1).

record_format.py reads and writes record files (grammar G1-G13); checks_form.py holds the grammar checks
FORM-01 to FORM-13; project_files.py makes projects, finds their files, keeps the manifest, the log and the
save ZIPs, and runs the commands new, status, apply, pack and unpack. The other modules (read_story,
adopt_folder, derive_fields, check_records, film_pass, make_handout, make_views, make_exports, estimate,
compile_prompts, make_text_graphics, make_previs_plans, refresh_models, build_kit) are added by later work
packages; each one registers its commands through a register_commands function (see stage.py).

Standard library only.
"""
