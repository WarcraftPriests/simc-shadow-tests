from statistics import mean


def generate_apl(action_name, shadowform=False, mastery=False, dark_ascension=False, void_eruption=False):
    apl = f"actions={action_name}"
    if shadowform:
        apl = f"actions.precombat=shadowform\nactions={action_name}"
    if mastery:
        apl = f"actions=vampiric_touch,if=refreshable\nactions+=/shadow_word_pain,if=refreshable\nactions+=/{action_name},if=dot.shadow_word_pain.ticking&dot.vampiric_touch.ticking"
    if dark_ascension:
        apl = f"actions=dark_ascension\nactions+=/{action_name}"
    if void_eruption:
        apl = f"actions=void_eruption\nactions+=/{action_name}"

    return apl


def close_enough(a, b, error):
    print(f"actual: {a} expected:{b}")
    return abs(a - b) <= error


def spell_avg_matches(damage_events, expected_dmg):
    return close_enough(mean(damage_events), expected_dmg, 2)


def spell_max_matches(damage_events, expected_dmg):
    return close_enough(max(damage_events), expected_dmg, 2)


def affected_by_shadowform(damage_events, base_dmg_events):
    return close_enough(mean(damage_events), (mean(base_dmg_events) * 1.1), 1)


def affected_by_mastery(damage_events, base_dmg_events, dots):
    dot_increase = 1 + (dots * 0.04)
    return close_enough(mean(damage_events), (mean(base_dmg_events) * dot_increase), 1)


def affected_by_dark_ascension(damage_events, base_dmg_events):
    return close_enough(max(damage_events), (mean(base_dmg_events) * 1.25), 1)


def affected_by_voidform(damage_events, base_dmg_events, dots=3, error=1):
    dot_increase = 1 + (dots * 0.04)
    return close_enough(max(damage_events), (mean(base_dmg_events) * dot_increase), error)
