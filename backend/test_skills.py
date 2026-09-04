from skills import count_skills

jobs = [
    {"title": "Senior R Developer", "description": "5 years experience required, strong communicator."},
    {"title": "Backend Engineer", "description": "We use C++ and Go daily, going forward."},
]
counts = count_skills(jobs)
assert counts["R"] == 1, counts  # not matched inside "years"/"experience"/"required"
assert counts["Go"] == 1, counts  # matched once in "Go daily", not inside "going"
assert counts["C++"] == 1, counts
