from internal import simc
from internal import utils


def test_mind_blast():
    """tests mind blast damage"""
    # base
    apl = utils.generate_apl("mind_blast")
    mb_base_dmg = simc.run_sim("", "", apl, "base.simc", "mind_blast")
    assert utils.spell_avg_matches(mb_base_dmg, 2043)

    # shadowform
    apl = utils.generate_apl("mind_blast", shadowform=True)
    mb_sf_dmg = simc.run_sim("", "", apl, "base.simc", "mind_blast")
    assert utils.spell_avg_matches(mb_sf_dmg, 2248)

    # mastery
    apl = utils.generate_apl("mind_blast", mastery=True)
    mb_mastery_dmg = simc.run_sim("", "", apl, "base.simc", "mind_blast")
    assert utils.affected_by_mastery(mb_mastery_dmg, mb_base_dmg)
    assert utils.spell_avg_matches(mb_mastery_dmg, 2207)

    # dark_ascension
    apl = utils.generate_apl("mind_blast", dark_ascension=True)
    st = "spec_talents=dark_ascension:1"
    mb_da_dmg = simc.run_sim("", st, apl, "base.simc", "mind_blast")
    assert utils.affected_by_dark_ascension(mb_da_dmg, mb_base_dmg)
    assert utils.spell_max_matches(mb_da_dmg, 2554)

    # void_eruption
    apl = utils.generate_apl("mind_blast", void_eruption=True)
    st = "spec_talents=void_eruption:1"
    mb_vf_dmg = simc.run_sim("", st, apl, "base.simc", "mind_blast")
    assert utils.affected_by_voidform(mb_vf_dmg, mb_sf_dmg)
    assert utils.spell_max_matches(mb_vf_dmg, 2517)
