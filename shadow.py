from internal import simc
from internal import utils
import yaml

with open("config.yml", "r", encoding="utf8") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def test_mind_blast():
    """tests mind blast damage"""
    # TODO: cooldown check, insanity check (base+whispers), coalescing shadows, insidious ire, execute_time
    action = "mind_blast"
    # base
    apl = utils.generate_apl(action)
    base_dmg = simc.run_sim("", "", apl, "base.simc", action).direct
    assert utils.spell_avg_matches(base_dmg, config["spells"][action]["base"])

    # shadowform
    apl = utils.generate_apl(action, shadowform=True)
    sf_dmg = simc.run_sim("", "", apl, "base.simc", action).direct
    assert utils.affected_by_shadowform(sf_dmg, base_dmg)
    assert utils.spell_avg_matches(
        sf_dmg, config["spells"][action]["shadowform"])

    # mastery
    apl = utils.generate_apl(action, mastery=True)
    mastery_dmg = simc.run_sim("", "", apl, "base.simc", action).direct
    assert utils.affected_by_mastery(mastery_dmg, base_dmg, 2)
    assert utils.spell_avg_matches(
        mastery_dmg, config["spells"][action]["mastery"])

    # dark_ascension
    apl = utils.generate_apl(action, dark_ascension=True)
    st = "spec_talents=dark_ascension:1"
    da_dmg = simc.run_sim("", st, apl, "base.simc", action).direct
    assert utils.affected_by_dark_ascension(da_dmg, base_dmg)
    assert utils.spell_max_matches(
        da_dmg, config["spells"][action]["dark_ascension"])

    # void_eruption
    apl = utils.generate_apl(action, void_eruption=True)
    st = "spec_talents=void_eruption:1"
    vf_dmg = simc.run_sim("", st, apl, "base.simc", action).direct
    assert utils.affected_by_voidform(vf_dmg, sf_dmg)
    assert utils.spell_max_matches(
        vf_dmg, config["spells"][action]["voidform"])


def test_mind_flay():
    """tests mind flay damage"""
    action = "mind_flay"
    # base
    apl = utils.generate_apl(action)
    base_dmg = simc.run_sim("", "", apl, "base.simc", action).periodic
    assert utils.spell_avg_matches(base_dmg, config["spells"][action]["base"])

    # shadowform
    apl = utils.generate_apl(action, shadowform=True)
    sf_dmg = simc.run_sim("", "", apl, "base.simc", action).periodic
    assert utils.affected_by_shadowform(sf_dmg, base_dmg)
    assert utils.spell_avg_matches(
        sf_dmg, config["spells"][action]["shadowform"])

    # mastery
    apl = utils.generate_apl(action, mastery=True)
    mastery_dmg = simc.run_sim("", "", apl, "base.simc", action).periodic
    assert utils.affected_by_mastery(mastery_dmg, base_dmg, 2)
    assert utils.spell_avg_matches(
        mastery_dmg, config["spells"][action]["mastery"])

    # dark_ascension
    apl = utils.generate_apl(action, dark_ascension=True)
    st = "spec_talents=dark_ascension:1"
    da_dmg = simc.run_sim("", st, apl, "base.simc", action).periodic
    assert not utils.affected_by_dark_ascension(da_dmg, base_dmg)
    assert utils.spell_max_matches(
        da_dmg, config["spells"][action]["dark_ascension"])

    # void_eruption
    apl = utils.generate_apl(action, void_eruption=True)
    st = "spec_talents=void_eruption:1"
    vf_dmg = simc.run_sim("", st, apl, "base.simc", action).periodic
    assert utils.affected_by_voidform(vf_dmg, sf_dmg)
    assert utils.spell_max_matches(
        vf_dmg, config["spells"][action]["voidform"])


def test_shadow_word_pain():
    """tests shadow_word_pain damage"""
    action = "shadow_word_pain"
    # base
    apl = utils.generate_apl(action)
    data = simc.run_sim("", "", apl, "base.simc", action)
    base_dd = data.direct
    base_td = data.periodic
    assert utils.spell_avg_matches(
        base_dd, config["spells"][action]["base"]["direct"])
    assert utils.spell_avg_matches(
        base_td, config["spells"][action]["base"]["periodic"])

    # shadowform
    apl = utils.generate_apl(action, shadowform=True)
    data = simc.run_sim("", "", apl, "base.simc", action)
    sf_dd = data.direct
    sf_td = data.periodic
    assert utils.spell_avg_matches(
        sf_dd, config["spells"][action]["shadowform"]["direct"])
    assert utils.spell_avg_matches(
        sf_td, config["spells"][action]["shadowform"]["periodic"])
    assert utils.affected_by_shadowform(sf_dd, base_dd)
    assert utils.affected_by_shadowform(sf_td, base_td)

    # mastery
    apl = utils.generate_apl(action, mastery=True)
    data = simc.run_sim("", "", apl, "base.simc", action)
    mastery_dd = data.direct
    mastery_td = data.periodic
    assert utils.spell_avg_matches(
        mastery_dd, config["spells"][action]["mastery"]["direct"])
    assert utils.spell_avg_matches(
        mastery_td, config["spells"][action]["mastery"]["periodic"])
    assert utils.affected_by_mastery(mastery_dd, base_dd, 1)
    assert utils.affected_by_mastery(mastery_td, base_td, 1)

    # dark_ascension
    apl = utils.generate_apl(action, dark_ascension=True)
    st = "spec_talents=dark_ascension:1"
    data = simc.run_sim("", st, apl, "base.simc", action)
    da_dd = data.direct
    da_td = data.periodic
    assert utils.spell_max_matches(
        da_dd, config["spells"][action]["dark_ascension"]["direct"])
    assert utils.spell_max_matches(
        da_td, config["spells"][action]["dark_ascension"]["periodic"])
    assert utils.affected_by_dark_ascension(da_dd, base_dd)
    assert not utils.affected_by_dark_ascension(da_td, base_td)

    # void_eruption
    apl = utils.generate_apl(action, void_eruption=True)
    st = "spec_talents=void_eruption:1"
    data = simc.run_sim("", st, apl, "base.simc", action)
    vf_dd = data.direct
    vf_td = data.periodic
    assert utils.spell_max_matches(
        vf_dd, config["spells"][action]["voidform"]["direct"])
    assert utils.spell_max_matches(
        vf_td, config["spells"][action]["voidform"]["periodic"])
    assert utils.affected_by_voidform(vf_dd, sf_dd, 2, 5)
    assert utils.affected_by_voidform(vf_td, sf_td, 2, 5)


def test_vampiric_touch():
    """tests vampiric_touch damage"""
    action = "vampiric_touch"
    # base
    apl = utils.generate_apl(action)
    data = simc.run_sim("", "", apl, "base.simc", action)
    base_td = data.periodic
    assert utils.spell_avg_matches(
        base_td, config["spells"][action]["base"])

    # shadowform
    apl = utils.generate_apl(action, shadowform=True)
    data = simc.run_sim("", "", apl, "base.simc", action)
    sf_td = data.periodic
    assert utils.spell_avg_matches(
        sf_td, config["spells"][action]["shadowform"])
    assert utils.affected_by_shadowform(sf_td, base_td)

    # mastery
    apl = utils.generate_apl(action, mastery=True)
    data = simc.run_sim("", "", apl, "base.simc", action)
    mastery_td = data.periodic
    assert utils.spell_avg_matches(
        mastery_td, config["spells"][action]["mastery"])
    assert utils.affected_by_mastery(mastery_td, base_td, 1, 5)

    # dark_ascension
    apl = utils.generate_apl(action, dark_ascension=True)
    st = "spec_talents=dark_ascension:1"
    data = simc.run_sim("", st, apl, "base.simc", action)
    da_td = data.periodic
    assert utils.spell_max_matches(
        da_td, config["spells"][action]["dark_ascension"])
    assert not utils.affected_by_dark_ascension(da_td, base_td)

    # void_eruption
    apl = utils.generate_apl(action, void_eruption=True)
    st = "spec_talents=void_eruption:1"
    data = simc.run_sim("", st, apl, "base.simc", action)
    vf_td = data.periodic
    assert utils.spell_max_matches(
        vf_td, config["spells"][action]["voidform"])
    assert utils.affected_by_voidform(vf_td, sf_td, 2, 5)


def test_devouring_plague():
    """tests devouring_plague damage"""
    action = "devouring_plague"
    # base
    apl = utils.generate_apl(action, insanity=True)
    st = "spec_talents=devouring_plague:1"
    data = simc.run_sim("", st, apl, "base.simc", action)
    base_dd = data.direct
    base_td = data.periodic
    assert utils.spell_avg_matches(
        base_dd, config["spells"][action]["base"]["direct"])
    assert utils.spell_avg_matches(
        base_td, config["spells"][action]["base"]["periodic"])

    # shadowform
    apl = utils.generate_apl(action, shadowform=True, insanity=True)
    st = "spec_talents=devouring_plague:1"
    data = simc.run_sim("", st, apl, "base.simc", action)
    sf_dd = data.direct
    sf_td = data.periodic
    assert utils.spell_avg_matches(
        sf_dd, config["spells"][action]["shadowform"]["direct"])
    assert utils.spell_avg_matches(
        sf_td, config["spells"][action]["shadowform"]["periodic"])
    assert utils.affected_by_shadowform(sf_dd, base_dd)
    assert utils.affected_by_shadowform(sf_td, base_td)

    # mastery
    apl = utils.generate_apl(action, mastery=True, insanity=True)
    st = "spec_talents=devouring_plague:1"
    data = simc.run_sim("", st, apl, "base.simc", action)
    mastery_dd = data.direct
    mastery_td = data.periodic
    assert utils.spell_avg_matches(
        mastery_dd, config["spells"][action]["mastery"]["direct"])
    assert utils.spell_avg_matches(
        mastery_td, config["spells"][action]["mastery"]["periodic"])
    assert utils.affected_by_mastery(mastery_dd, base_dd, 2, 5)
    assert utils.affected_by_mastery(mastery_td, base_td, 2, 5)

    # dark_ascension
    apl = f"actions=dark_ascension\nactions+=/{action}\nactions+=/mind_flay"
    st = "spec_talents=devouring_plague:1/dark_ascension:1"
    data = simc.run_sim("", st, apl, "base.simc", action)
    da_dd = data.direct
    da_td = data.periodic
    assert utils.spell_max_matches(
        da_dd, config["spells"][action]["dark_ascension"]["direct"])
    assert utils.spell_max_matches(
        da_td, config["spells"][action]["dark_ascension"]["periodic"])
    assert utils.affected_by_dark_ascension(da_dd, base_dd)
    assert not utils.affected_by_dark_ascension(da_td, base_td)

    # void_eruption
    apl = f"actions=void_eruption\nactions+=/{action}\nactions+=/mind_flay"
    st = "spec_talents=devouring_plague:1/void_eruption:1"
    data = simc.run_sim("", st, apl, "base.simc", action)
    vf_dd = data.direct
    vf_td = data.periodic
    assert utils.spell_max_matches(
        vf_dd, config["spells"][action]["voidform"]["direct"])
    assert utils.spell_max_matches(
        vf_td, config["spells"][action]["voidform"]["periodic"])
    assert utils.affected_by_voidform(vf_dd, sf_dd, 2, 10)
    assert utils.affected_by_voidform(vf_td, sf_td, 2, 10)


def test_shadow_word_death():
    """tests shadow_word_death damage"""
    action = "shadow_word_death"
    # base
    apl = utils.generate_apl(action)
    ct = "class_talents=shadow_word_death:1"
    base_dmg = simc.run_sim(ct, "", apl, "base.simc", action).direct
    assert utils.spell_min_matches(
        base_dmg, config["spells"][action]["base"]["normal"])
    assert utils.spell_max_matches(
        base_dmg, config["spells"][action]["base"]["execute"])

    # shadowform
    apl = utils.generate_apl(action, shadowform=True)
    ct = "class_talents=shadow_word_death:1"
    sf_dmg = simc.run_sim(ct, "", apl, "base.simc", action).direct
    assert utils.spell_min_matches(
        sf_dmg, config["spells"][action]["shadowform"]["normal"])
    assert utils.spell_max_matches(
        sf_dmg, config["spells"][action]["shadowform"]["execute"])

    # mastery
    apl = utils.generate_apl(action, mastery=True)
    ct = "class_talents=shadow_word_death:1"
    mastery_dmg = simc.run_sim(ct, "", apl, "base.simc", action).direct
    assert utils.spell_min_matches(
        mastery_dmg, config["spells"][action]["mastery"]["normal"])
    assert utils.spell_max_matches(
        mastery_dmg, config["spells"][action]["mastery"]["execute"])

    # dark_ascension
    apl = utils.generate_apl(action, dark_ascension=True)
    ct = "class_talents=shadow_word_death:1"
    st = "spec_talents=dark_ascension:1"
    da_dmg = simc.run_sim(ct, st, apl, "base.simc", action).direct
    assert utils.spell_min_matches(
        da_dmg, config["spells"][action]["dark_ascension"]["normal"])
    assert utils.spell_max_matches(
        da_dmg, config["spells"][action]["dark_ascension"]["execute"])

    # void_eruption
    apl = utils.generate_apl(action, void_eruption=True)
    ct = "class_talents=shadow_word_death:1"
    st = "spec_talents=void_eruption:1"
    vf_dmg = simc.run_sim(ct, st, apl, "base.simc", action).direct
    assert utils.spell_min_matches(
        vf_dmg, config["spells"][action]["voidform"]["normal"])
    assert utils.spell_max_matches(
        vf_dmg, config["spells"][action]["voidform"]["execute"])
