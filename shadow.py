from internal import simc
from internal import utils
import yaml

with open("config.yml", "r", encoding="utf8") as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)


def test_mind_blast():
    """tests mind blast damage"""
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
    assert utils.affected_by_mastery(mastery_dmg, base_dmg)
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
    assert utils.affected_by_mastery(mastery_dmg, base_dmg)
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
