#!/usr/bin/env python3
import re
import json
import hashlib
import sys
import ast

# parse odoo log to find list of missing modules
# output:
#   gl-code-quality-report.json (merge request widget)
#   modules_missing.txt: list of missing modules (one module per line)

WORKDIR = "shared"

def parse(log_content):
    errors = []
    warnings = []

    #use cases:
    # installed module missing
    # installed module, new dependency missing
    # module to install not found
    # module to install, dependency missing

    # there is trailing space at the end of each line
    patt_missing_modules_error = r"odoo.modules.loading: Some modules are not loaded, some dependencies or manifest may be missing: (\[.*?\]) "
    patt_missing_modules_error_dep = r"odoo.modules.graph: module (.*?): Unmet dependencies: (.*?) "
    patt_missing_modules_warning = r"odoo.modules.loading: Some modules have inconsistent states, some dependencies may be missing: (\[.*?\]) "

    for match in re.finditer(patt_missing_modules_error, log_content):
        try:
            # ast.literal_eval: str"['a', 'b']" -> dict['a', 'b']
            deps = ast.literal_eval(match.group(1))
            for dep in deps:
                errors.append(dep)
        except (ValueError, SyntaxError) as e:
            continue

    for match in re.finditer(patt_missing_modules_error_dep, log_content):
        # group1: name of the module
        # group2: names of it's missing dependency
        # str"a, b" -> dict['a', 'b']
        deps = match.group(2).split(",")
        for dep in deps:
            errors.append(dep)

    for match in re.finditer(patt_missing_modules_warning, log_content):
        try:
            # ast.literal_eval: str"['a', 'b']" -> dict['a', 'b']
            deps = ast.literal_eval(match.group(1))
            for dep in deps:
                warnings.append(dep)
        except (ValueError, SyntaxError) as e:
            continue

    return warnings, errors

def generate_list_of_missing_modules(warnings, errors):
    modules = list(set(warnings) | set(errors))
    modules.sort()
    with open(f"{WORKDIR}/modules_missing.txt", "w") as f:
        print(*modules, sep="\n", file=f)

def generate_gl_code_quality(warnings, errors):
    issues = []

    for dep in errors:
        description = f"Missing dependency: {dep}"
        fingerprint = hashlib.md5(description.encode()).hexdigest()

        issues.append({
            "description": description,
            "check_name": "missing_dependency",
            "fingerprint": fingerprint,
            "severity": "critical",
            "location": {
                "path": "odoo/spec.yaml",
                "lines": {"begin": 1}
            }
        })

    for dep in warnings:
        if dep in errors:
            continue
        description = f"Not installable dependency: {dep}"
        fingerprint = hashlib.md5(description.encode()).hexdigest()

        issues.append({
            "description": description,
            "check_name": "not_installable_dep",
            "fingerprint": fingerprint,
            "severity": "major",
            "location": {
                "path": "odoo/spec.yaml",
                "lines": {"begin": 1}
            }
        })

    with open(f"{WORKDIR}/gl-code-quality-report.json", "w") as f:
        json.dump(issues, f, indent=2)

if __name__ == "__main__":
    input_data = sys.stdin.read()
    if not input_data:
        print("Nothing to parse", file=sys.stderr)
        sys.exit(1)
    warnings, errors = parse(input_data)
    generate_gl_code_quality(warnings, errors)
    generate_list_of_missing_modules(warnings, errors)
