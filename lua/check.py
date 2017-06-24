from ai import TASKFORCES, TEAMS

for team in TEAMS.values():
    assert "trigger" in team

    assert team["faction"] == "allies" or \
           team["faction"] == "soviet" or team["faction"] == "mutants"

    tf = TASKFORCES[team["tf"]]
    assert len(tf["units"]) > 0
