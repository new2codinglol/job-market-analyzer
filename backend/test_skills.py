import sys
sys.path.insert(0, "scripts")
from fetch_seed import fix_mojibake, is_garbled
from skills import count_skills

assert fix_mojibake("Singapore") == "Singapore"  # ascii: no-op
assert fix_mojibake("BayamÃ³n") == "Bayamón"  # double-encoded: repaired
assert fix_mojibake("中山市") == "中山市"  # real multi-byte: can't latin-1-encode, no-op
assert fix_mojibake("") == ""
assert fix_mojibake(None) is None
assert not is_garbled("Bayamón")
assert is_garbled("\x8aabc")

jobs = [
    {"title": "Senior R Developer", "description": "5 years experience required, strong communicator."},
    {"title": "Backend Engineer", "description": "We use C++ and Go daily, going forward."},
]
counts = count_skills(jobs)
assert counts["R"] == 1, counts  # not matched inside "years"/"experience"/"required"
assert counts["Go"] == 1, counts  # matched once in "Go daily", not inside "going"
assert counts["C++"] == 1, counts
