#!/usr/bin/env python3
import sys
import json
from pathlib import Path

src_dir = str(Path(__file__).parent.parent.resolve())
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from quikrun.metadata.cmd_templates import cmd_templates  # noqa: E402

NAME_MAP = {
    "linux": "Linux",
    "darwin": "macOS",
    "win": "Windows",
    "posix": "POSIX",
    "cmd": "CMD",
    "pwsh": "PowerShell",
}


def extract_branches(val):
    if not isinstance(val, dict):
        return None
    if "compile" in val and "run" in val:
        return None

    res = {}
    for k, v in val.items():
        if k in NAME_MAP:
            res[NAME_MAP[k]] = v

    return res if res else None


def format_interpreted(val):
    if isinstance(val, str):
        return f"`{val}`"
    elif isinstance(val, list):
        return " → ".join(format_interpreted(v) for v in val)
    elif isinstance(val, dict):
        branches = extract_branches(val)
        if branches:
            formatted_groups = {}
            for name, branch_val in branches.items():
                fmt = format_interpreted(branch_val)
                if fmt not in formatted_groups:
                    formatted_groups[fmt] = []
                formatted_groups[fmt].append(name)

            if len(formatted_groups) == 1:
                return list(formatted_groups.keys())[0]

            parts = []
            for fmt, names in formatted_groups.items():
                # Sort names for consistency
                parts.append(f"{fmt} ({'/'.join(names)})")
            return "<br>".join(parts)
    return str(val)


def is_compiled(val):
    if isinstance(val, dict):
        if "compile" in val and "run" in val:
            return True
        branches = extract_branches(val)
        if branches:
            for branch_val in branches.values():
                if is_compiled(branch_val):
                    return True
    return False


def main():
    interpreted = {}
    compiled = {}

    for ext, val in cmd_templates.items():
        resolved_val = val
        if isinstance(val, str) and val.startswith("@"):
            target = val[1:]
            if target in cmd_templates:
                resolved_val = cmd_templates[target]

        # Enforce Schema: OS platforms must be nested inside shell families
        if isinstance(resolved_val, dict) and not (
            "compile" in resolved_val or "run" in resolved_val
        ):
            invalid_root_keys = [
                k for k in ["linux", "darwin", "win"] if k in resolved_val
            ]
            if invalid_root_keys:
                print(
                    f"Schema Error: OS platforms {invalid_root_keys} are not allowed at the root of '.{ext}'. They must be nested inside a shell family (posix, cmd, pwsh).",
                    file=sys.stderr,
                )
                sys.exit(1)

        val_str = json.dumps(resolved_val, sort_keys=True)

        if is_compiled(resolved_val):
            if val_str not in compiled:
                compiled[val_str] = {"exts": [], "val": resolved_val}
            compiled[val_str]["exts"].append(ext)
        else:
            if val_str not in interpreted:
                interpreted[val_str] = {"exts": [], "val": resolved_val}
            interpreted[val_str]["exts"].append(ext)

    # Build Interpreted Table
    interpreted_md = "| Extension | Command |\n| --- | --- |\n"
    for k in sorted(interpreted.keys(), key=lambda x: interpreted[x]["exts"][0]):
        exts = " / ".join(f"`.{e}`" for e in interpreted[k]["exts"])
        cmd = format_interpreted(interpreted[k]["val"])
        interpreted_md += f"| {exts} | {cmd} |\n"

    # Build Compiled Table
    compiled_md = "| Extension | Compile Command | Run Command |\n| --- | --- | --- |\n"
    for k in sorted(compiled.keys(), key=lambda x: compiled[x]["exts"][0]):
        exts = " / ".join(f"`.{e}`" for e in compiled[k]["exts"])

        resolved_val = compiled[k]["val"]
        branches = extract_branches(resolved_val)

        if branches:
            c_dict = {}
            r_dict = {}

            # Flatten to pass into format_interpreted to resolve inner OS branches
            # Because format_interpreted recursively detects them
            def populate_cr(v, c, r, root):
                b = extract_branches(v)
                if b:
                    for name, inner_v in b.items():
                        c[name] = {}
                        r[name] = {}
                        populate_cr(inner_v, c[name], r[name], False)
                        if not c[name]:
                            c[name] = inner_v.get("compile", inner_v)
                        if not r[name]:
                            r[name] = inner_v.get("run", inner_v)
                elif root:
                    c.update(v.get("compile", v))
                    r.update(v.get("run", v))

            c_dict = {
                k: v.get("compile", v) if isinstance(v, dict) else v
                for k, v in resolved_val.items()
                if k in NAME_MAP
            }
            r_dict = {
                k: v.get("run", v) if isinstance(v, dict) else v
                for k, v in resolved_val.items()
                if k in NAME_MAP
            }

            c = format_interpreted(c_dict)
            r = format_interpreted(r_dict)
        else:
            c = format_interpreted(resolved_val["compile"])
            r = format_interpreted(resolved_val["run"])

        compiled_md += f"| {exts} | {c} | {r} |\n"

    # Inject into supported-languages.md
    md_path = (
        Path(__file__).parent.parent.parent / "docs" / "md" / "supported-languages.md"
    )

    if not md_path.exists():
        print(f"Error: Could not find {md_path}")
        sys.exit(1)

    content = md_path.read_text("utf-8")

    # Replace interpreted
    import re

    content = re.sub(
        r"<!-- DYNAMIC_INTERPRETED_START -->.*?<!-- DYNAMIC_INTERPRETED_END -->",
        f"<!-- DYNAMIC_INTERPRETED_START -->\n\n{interpreted_md.strip()}\n\n<!-- DYNAMIC_INTERPRETED_END -->",
        content,
        flags=re.DOTALL,
    )

    # Replace compiled
    content = re.sub(
        r"<!-- DYNAMIC_COMPILED_START -->.*?<!-- DYNAMIC_COMPILED_END -->",
        f"<!-- DYNAMIC_COMPILED_START -->\n\n{compiled_md.strip()}\n\n<!-- DYNAMIC_COMPILED_END -->",
        content,
        flags=re.DOTALL,
    )

    md_path.write_text(content, "utf-8")
    print("Successfully synchronized docs/md/supported-languages.md")


if __name__ == "__main__":
    main()
