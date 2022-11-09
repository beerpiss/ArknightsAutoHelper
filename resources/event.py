from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from imgreco.item import RecognizedItem

EXTRA_KNOWN_ITEMS = [
    "trap_oxygen_3",
    "31044",
    "charm_coin_4",
    "charm_coin_1",
    "randomMaterial_5",
    "4001_1500",
    "31054",
    "31053",
    "furni",
    "4005",
    "4001_2000",
    "charm_coin_3",
    "4001_1000",
    "charm_r1",
    "31043",
    "charm_coin_2",
    "charm_r2",
    "randomMaterial_1",
]

FIXED_QUANTITY = [
    "Quantum Firecracker",
    "Canteen Soup Ticket",
    "Anonymous Tags",
    "Best-selling Peterheim Cookies",
    "Aristocrat's Antique Aureus",
    "Mechanical Parts",
    "Discarded Clock Dial",
    "Bounty Coin",
    "Mieszko Sports Securities",
    "Factory Steel",
    "Wondrous Postcard",
    "Dusk Inkstick",
    "Rhodes Island Resource Allocation Certificate",
    "Scattered Sketches",
    "Corrupted Iberian Record",
    "Clearance Permit",
    "Competition Medals",
    "Rusted Compass"
    "'Imagini'",
]

# ONE_OR_NONE = [
#     '应急理智小样',
#     '罗德岛物资补给',
#     '岁过华灯',
#     '32h战略配给',
#     '感谢庆典物资补给',
# ]

# report_types = {'MATERIAL', 'CARD_EXP', 'VOUCHER_MGACHA', 'furni', 'special_report_item', None}


def event_preprocess(
    stage: str, items: list[tuple[str, RecognizedItem]], exclude_from_validation: list
):
    # [('常规掉落', '固源岩', 1), ...]
    for itemrecord in items:
        group, item = itemrecord
        if item.name in FIXED_QUANTITY or item.name.startswith("@"):
            # 不加入汇报列表
            continue

        # if name in ONE_OR_NONE:
        #     # 不使用企鹅数据验证规则进行验证
        #     exclude_from_validation.append(itemrecord)
        #     if qty != 1:
        #         raise ValueError('%sx%d' % (name, qty))

        # 加入汇报列表
        yield itemrecord
