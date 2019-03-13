import pytest
import sys
import os
import time
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../test_sentinel.conf'))
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../lib')))
import misc
import config
from models import GovernanceObject, Proposal, Superblock, Vote


# clear DB tables before each execution
def setup():
    # clear tables first...
    Vote.delete().execute()
    Proposal.delete().execute()
    Superblock.delete().execute()
    GovernanceObject.delete().execute()


def teardown():
    pass


# list of proposal govobjs to import for testing
@pytest.fixture
def go_list_proposals():
    items = [
        {u'AbsoluteYesCount': 1000,
         u'AbstainCount': 7,
         u'CollateralHash': u'501d8b0110b318b413a444ace9ceeea3ce2972a1523baaa3e1614bd5a2a5a9b0',
         u'DataHex': u'5b5b2270726f706f73616c222c7b22656e645f65706f6368223a313532383430393634312c226e616d65223a2269616d67726f6f7432222c227061796d656e745f61646472657373223a226e46377433714433386351506a5847396e4447356537637036475447366f54663955222c227061796d656e745f616d6f756e74223a3130302c2273746172745f65706f6368223a313532383430363037362c2274797065223a312c2275726c223a2268747470733a2f2f676f627974652e6e6574776f726b227d5d5d',
         u'DataString': u'[["proposal", {"end_epoch": 2122520400, "name": "dean-miller-5493", "payment_address": "nLLGSuauCV21NBpHJpLHKevWpwE3t6CHGc", "payment_amount": 25.75, "start_epoch": 1474261086, "type": 1, "url": "http://gobytecentral.org/dean-miller-5493"}]]',
         u'Hash': u'e966911624df92b90582ef9cdd2b3d8c1ed5c06ee2847aadc68ad0442c22ea6a',
         u'IsValidReason': u'',
         u'NoCount': 25,
         u'YesCount': 1025,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1000,
         u'AbstainCount': 29,
         u'CollateralHash': u'283cce0ccc4793f202429bf3fd8233319c340f7d240a5cd6db26bfebaeefb7a7',
         u'DataHex': u'5b5b2270726f706f73616c222c7b22656e645f65706f6368223a313532383133313531352c226e616d65223a224c4f574b455931222c227061796d656e745f61646472657373223a226e4c4c4753756175435632314e4270484a704c484b65765770774533743643484763222c227061796d656e745f616d6f756e74223a3135302c2273746172745f65706f6368223a313532383132373935302c2274797065223a312c2275726c223a2268747470733a2f2f7777772e676f627974652e6e6574776f726b227d5d5d',
         u'DataString': u'[["proposal", {"end_epoch": 1528131515, "name": "fernandez-7625", "payment_address": "nLLGSuauCV21NBpHJpLHKevWpwE3t6CHGc", "payment_amount": 25.75, "start_epoch": 1528127950, "type": 1, "url": "http://gobytecentral.org/fernandez-7625"}]]',
         u'Hash': u'2b6b4aee7bea18b38a928ef8c50aa74dac58787e850d990881daf5c1341c9bf8',
         u'IsValidReason': u'',
         u'NoCount': 56,
         u'YesCount': 1056,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
    ]

    return items


# list of superblock govobjs to import for testing
@pytest.fixture
def go_list_superblocks():
    items = [
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2270726f706f73616c222c7b22656e645f65706f6368223a313532383133383034372c226e616d65223a224c4f574b455932222c227061796d656e745f61646472657373223a226e4259624c48453154544e504142725a466466473441525a484e584468615a546231222c227061796d656e745f616d6f756e74223a35302c2273746172745f65706f6368223a313532383133343438322c2274797065223a312c2275726c223a2268747470733a2f2f7777772e676f627974652e6e6574776f726b227d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "nBYbLHE1TTNPABrZFdfG4ARZHNXDhaZTb1|nBYbLHE1TTNPABrZFdfG4ARZHNXDhaZTb1", "payment_amounts": "25.75000000|25.7575000000", "type": 2}]]',
         u'Hash': u'667c4a53eb81ba14d02860fdb4779e830eb8e98306f9145f3789d347cbeb0721',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2270726f706f73616c222c7b22656e645f65706f6368223a313532383133383034372c226e616d65223a224c4f574b455932222c227061796d656e745f61646472657373223a226e4259624c48453154544e504142725a466466473441525a484e584468615a546231222c227061796d656e745f616d6f756e74223a35302c2273746172745f65706f6368223a313532383133343438322c2274797065223a312c2275726c223a2268747470733a2f2f7777772e676f627974652e6e6574776f726b227d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "nBYbLHE1TTNPABrZFdfG4ARZHNXDhaZTb1|nBYbLHE1TTNPABrZFdfG4ARZHNXDhaZTb1", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
         u'Hash': u'8f91ffb105739ec7d5b6c0b12000210fcfcc0837d3bb8ca6333ba93ab5fc0bdf',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
        {u'AbsoluteYesCount': 1,
         u'AbstainCount': 0,
         u'CollateralHash': u'0000000000000000000000000000000000000000000000000000000000000000',
         u'DataHex': u'5b5b2270726f706f73616c222c7b22656e645f65706f6368223a313532383133383034372c226e616d65223a224c4f574b455932222c227061796d656e745f61646472657373223a226e4259624c48453154544e504142725a466466473441525a484e584468615a546231222c227061796d656e745f616d6f756e74223a35302c2273746172745f65706f6368223a313532383133343438322c2274797065223a312c2275726c223a2268747470733a2f2f7777772e676f627974652e6e6574776f726b227d5d5d',
         u'DataString': u'[["trigger", {"event_block_height": 72696, "payment_addresses": "nBYbLHE1TTNPABrZFdfG4ARZHNXDhaZTb1|nBYbLHE1TTNPABrZFdfG4ARZHNXDhaZTb1", "payment_amounts": "25.75000000|25.75000000", "type": 2}]]',
         u'Hash': u'a10bab2993a11f206d8094024b254d36bf0c9a34ee34ce60f11bc75e44d70c93',
         u'IsValidReason': u'',
         u'NoCount': 0,
         u'YesCount': 1,
         u'fBlockchainValidity': True,
         u'fCachedDelete': False,
         u'fCachedEndorsed': False,
         u'fCachedFunding': False,
         u'fCachedValid': True},
    ]

    return items


@pytest.fixture
def superblock():
    sb = Superblock(
        event_block_height=62500,
        payment_addresses='nBYbLHE1TTNPABrZFdfG4ARZHNXDhaZTb1|nJUUwdV8JvDXjoMLhmqi9mQCgiA86xPL4h',
        payment_amounts='5|3',
        proposal_hashes='e8a0057914a2e1964ae8a945c4723491caae2077a90a00a2aabee22b40081a87|d1ce73527d7cd6f2218f8ca893990bc7d5c6b9334791ce7973bfa22f155f826e',
    )
    return sb


def test_superblock_is_valid(superblock):
    from gobyted import GoByteDaemon
    gobyted = GoByteDaemon.from_gobyte_conf(config.gobyte_conf)

    orig = Superblock(**superblock.get_dict())  # make a copy

    # original as-is should be valid
    assert orig.is_valid() is True

    # mess with payment amounts
    superblock.payment_amounts = '7|yyzx'
    assert superblock.is_valid() is False

    superblock.payment_amounts = '7,|yzx'
    assert superblock.is_valid() is False

    superblock.payment_amounts = '7|8'
    assert superblock.is_valid() is True

    superblock.payment_amounts = ' 7|8'
    assert superblock.is_valid() is False

    superblock.payment_amounts = '7|8 '
    assert superblock.is_valid() is False

    superblock.payment_amounts = ' 7|8 '
    assert superblock.is_valid() is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid() is True

    # mess with payment addresses
    superblock.payment_addresses = 'nJUUwdV8JvDXjoMLhmqi9mQCgiA86xPL4h|1234 Anywhere ST, Chicago, USA'
    assert superblock.is_valid() is False

    # leading spaces in payment addresses
    superblock.payment_addresses = ' nJUUwdV8JvDXjoMLhmqi9mQCgiA86xPL4h'
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid() is False

    # trailing spaces in payment addresses
    superblock.payment_addresses = 'nJUUwdV8JvDXjoMLhmqi9mQCgiA86xPL4h '
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid() is False

    # leading & trailing spaces in payment addresses
    superblock.payment_addresses = ' nJUUwdV8JvDXjoMLhmqi9mQCgiA86xPL4h '
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid() is False

    # single payment addr/amt is ok
    superblock.payment_addresses = 'nJUUwdV8JvDXjoMLhmqi9mQCgiA86xPL4h'
    superblock.payment_amounts = '5.00'
    assert superblock.is_valid() is True

    # ensure number of payment addresses matches number of payments
    superblock.payment_addresses = 'nJUUwdV8JvDXjoMLhmqi9mQCgiA86xPL4h'
    superblock.payment_amounts = '37.00|23.24'
    assert superblock.is_valid() is False

    superblock.payment_addresses = 'nBYbLHE1TTNPABrZFdfG4ARZHNXDhaZTb1|nJUUwdV8JvDXjoMLhmqi9mQCgiA86xPL4h'
    superblock.payment_amounts = '37.00'
    assert superblock.is_valid() is False

    # ensure amounts greater than zero
    superblock.payment_addresses = 'nJUUwdV8JvDXjoMLhmqi9mQCgiA86xPL4h'
    superblock.payment_amounts = '-37.00'
    assert superblock.is_valid() is False

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid() is True

    # mess with proposal hashes
    superblock.proposal_hashes = '7|yyzx'
    assert superblock.is_valid() is False

    superblock.proposal_hashes = '7,|yyzx'
    assert superblock.is_valid() is False

    superblock.proposal_hashes = '0|1'
    assert superblock.is_valid() is False

    superblock.proposal_hashes = '0000000000000000000000000000000000000000000000000000000000000000|1111111111111111111111111111111111111111111111111111111111111111'
    assert superblock.is_valid() is True

    # reset
    superblock = Superblock(**orig.get_dict())
    assert superblock.is_valid() is True


def test_serialisable_fields():
    s1 = ['event_block_height', 'payment_addresses', 'payment_amounts', 'proposal_hashes']
    s2 = Superblock.serialisable_fields()

    s1.sort()
    s2.sort()

    assert s2 == s1


def test_deterministic_superblock_creation(go_list_proposals):
    import gobytelib
    import misc
    from gobyted import GoByteDaemon
    gobyted = GoByteDaemon.from_gobyte_conf(config.gobyte_conf)
    for item in go_list_proposals:
        (go, subobj) = GovernanceObject.import_gobject_from_gobyted(gobyted, item)

    max_budget = 60
    prop_list = Proposal.approved_and_ranked(proposal_quorum=1, next_superblock_max_budget=max_budget)

    sb = gobytelib.create_superblock(prop_list, 72000, max_budget, misc.now())

    assert sb.event_block_height == 72000
    assert sb.payment_addresses == 'nLLGSuauCV21NBpHJpLHKevWpwE3t6CHGc|nLLGSuauCV21NBpHJpLHKevWpwE3t6CHGc'
    assert sb.payment_amounts == '25.75000000|32.01000000'
    assert sb.proposal_hashes == 'e966911624df92b90582ef9cdd2b3d8c1ed5c06ee2847aadc68ad0442c22ea6a|2b6b4aee7bea18b38a928ef8c50aa74dac58787e850d990881daf5c1341c9bf8'

    assert sb.hex_hash() == '5534e9fa4a51423820b9e19fa6d4770c12ea0a5663e8adff8223f5e8b6df641c'


def test_deterministic_superblock_selection(go_list_superblocks):
    from gobyted import GoByteDaemon
    gobyted = GoByteDaemon.from_gobyte_conf(config.gobyte_conf)

    for item in go_list_superblocks:
        (go, subobj) = GovernanceObject.import_gobject_from_gobyted(gobyted, item)

    # highest hash wins if same -- so just order by hash
    sb = Superblock.find_highest_deterministic('22a5f429c5ffb2b79b1b30c3ac30751284e3efa4e710bc7fd35fbe7456b1e485')

    assert sb.object_hash == 'a10bab2993a11f206d8094024b254d36bf0c9a34ee34ce60f11bc75e44d70c93'
