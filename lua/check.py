from evo import TEAMS

for team in TEAMS.values():
    assert "trigger" in team

    assert team["faction"] == "allies" or \
           team["faction"] == "soviet" or team["faction"] == "mutants"

    assert len(team["units"]) > 0
    assert len(team["cnts"]) > 0
    assert len(team["cnts"]) == len(team["units"])
