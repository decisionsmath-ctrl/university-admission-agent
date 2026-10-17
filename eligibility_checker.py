import json


def load_programs(path="data/programs.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def check_eligibility(student, program):
    """Rule-based check. Returns a list of (requirement, status, detail)."""
    results = []

    # Years of education (HEC: 16 years for MS/MPhil)
    need = program.get("min_years_education")
    have = student.get("years_education")
    if need is None:
        results.append(("Years of education", "Cannot determine", "Not provided by university data"))
    elif have is None:
        results.append(("Years of education", "Cannot determine", "Applicant did not provide"))
    elif have >= need:
        results.append(("Years of education", "Satisfied", f"{have} years (needs {need})"))
    else:
        results.append(("Years of education", "Not satisfied", f"{have} years (needs {need})"))

    # Degree
    accepted = [d.lower() for d in program.get("accepted_degrees", [])]
    degree = (student.get("degree") or "").lower()
    if not accepted:
        results.append(("Degree", "Cannot determine", "No accepted degrees listed"))
    elif degree in accepted:
        results.append(("Degree", "Satisfied", student["degree"]))
    else:
        results.append(("Degree", "Not satisfied", f"{student.get('degree')} not in accepted list"))

    # CGPA (normalize to the program's scale)
    min_cgpa = program.get("min_cgpa")
    cgpa = student.get("cgpa")
    if min_cgpa is None or cgpa is None:
        results.append(("CGPA", "Cannot determine", "Missing data"))
    else:
        scale_in = student.get("cgpa_scale", 4.0)
        scale_req = program.get("cgpa_scale", 4.0)
        normalized = cgpa / scale_in * scale_req
        status = "Satisfied" if normalized >= min_cgpa else "Not satisfied"
        results.append(("CGPA", status, f"{normalized:.2f} (needs {min_cgpa})"))

    # Entry test
    test = program.get("entry_test")
    if test:
        score = student.get("test_score")
        if score is None:
            results.append((test["name"], "Cannot determine", "No score provided"))
        else:
            status = "Satisfied" if score >= test["min_score"] else "Not satisfied"
            results.append((test["name"], status, f"{score} (needs {test['min_score']})"))

    # Overall
    statuses = [r[1] for r in results]
    if "Not satisfied" in statuses:
        overall = "Not eligible based on supplied information"
    elif "Cannot determine" in statuses:
        overall = "Needs verification"
    else:
        overall = "Eligible based on supplied information"

    return overall, results
