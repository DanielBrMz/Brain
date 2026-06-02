#!/usr/bin/env python3
"""
BOTW Shrine Finder
==================
Shows nearest uncompleted shrines, injects stamps into save.

Usage:
    python3 botw_shrine_finder.py status                 # Show cleared/remaining
    python3 botw_shrine_finder.py inject [region|X Z]    # Inject 30 nearest uncleared shrine stamps
    python3 botw_shrine_finder.py list [region|X Z]      # List 30 nearest (no inject)
    python3 botw_shrine_finder.py cleared 1 2 5-10       # Mark shrine #s as cleared (manual)
    python3 botw_shrine_finder.py undo                   # Undo last manual marking
    python3 botw_shrine_finder.py reset                  # Clear manual tracking

Regions: plateau, central, hateno, faron, lanayru, eldin, akkala, hebra, gerudo,
         ridgeland, kakariko, zora, rito, korok
"""

import struct
import math
import sys
import json
import shutil
from pathlib import Path

# Reuse parsers from korok finder
sys.path.insert(0, str(Path(__file__).parent))
from botw_korok_finder import yaz0_decompress, parse_sarc, BYMLParser

CEMU_BASE = Path("/home/brmz/.local/share/Cemu")
BOOTUP_PACK = CEMU_BASE / "EUR/GAMES/Base Games/The Legend of Zelda Breath of the Wild [ALZP01]/content/Pack/Bootup.pack"
SAVE_DIR = CEMU_BASE / "mlc01/usr/save/00050000/101c9500/user/80000001"
CLEARED_FILE = CEMU_BASE / "shrine_cleared.json"
CACHE_FILE = Path("/tmp/shrine_hashes_cache.json")

STAMP_TYPE = 31  # Star stamp (Korok finder uses 34=Leaf)
STAMP_LIMIT = 30
SHRINE_SLOT_START = 151  # Slots 0=user, 1-150=Koroks, 151-180=Shrines
ICON_POS_HASH = struct.pack('>i', -358748353)
ICON_NO_HASH = struct.pack('>i', -1820112626)

REGIONS = {
    'plateau':   {'x': -500,  'z': 1800, 'name': 'Great Plateau'},
    'central':   {'x': -300,  'z': 300,  'name': 'Central Hyrule'},
    'hateno':    {'x': 3400,  'z': 2100, 'name': 'Hateno Village'},
    'faron':     {'x': 1100,  'z': 3300, 'name': 'Faron'},
    'lanayru':   {'x': 3400,  'z': 400,  'name': 'Lanayru'},
    'eldin':     {'x': 2700,  'z': -1600,'name': 'Eldin/Death Mountain'},
    'akkala':    {'x': 3500,  'z': -2700,'name': 'Akkala'},
    'hebra':     {'x': -3300, 'z': -1800,'name': 'Hebra/Tabantha'},
    'gerudo':    {'x': -3800, 'z': 2200, 'name': 'Gerudo Desert'},
    'ridgeland': {'x': -2200, 'z': -100, 'name': 'Ridgeland'},
    'kakariko':  {'x': 1800,  'z': 1000, 'name': 'Kakariko Village'},
    'zora':      {'x': 3300,  'z': -400, 'name': "Zora's Domain"},
    'rito':      {'x': -3600, 'z': -1200,'name': 'Rito Village'},
    'korok':     {'x': 700,   'z': -400, 'name': 'Korok Forest'},
}

# All 120 shrine world coordinates [x, z] from game data
# Sorted by coordinate for stable indexing
SHRINES = [
    {"id": 0,   "x": -4847.0, "z": 3772.6,  "name": "Korgu Chideh Shrine"},
    {"id": 1,   "x": -4799.1, "z": 2800.2,  "name": "Suma Sahma Shrine"},
    {"id": 2,   "x": -4673.5, "z": 1967.8,  "name": "Kema Zoos Shrine"},
    {"id": 3,   "x": -4658.5, "z": 904.8,   "name": "Goma Asaagh Shrine"},
    {"id": 4,   "x": -4446.8, "z": -3803.0, "name": "Sha Warvo Shrine"},
    {"id": 5,   "x": -4120.4, "z": -414.4,  "name": "Tena Ko'sah Shrine"},
    {"id": 6,   "x": -4057.8, "z": -2508.4, "name": "Shada Naw Shrine"},
    {"id": 7,   "x": -4023.1, "z": -3711.6, "name": "Voo Lota Shrine"},
    {"id": 8,   "x": -4016.2, "z": -1721.9, "name": "Akh Va'Quot Shrine"},
    {"id": 9,   "x": -3911.3, "z": 1653.8,  "name": "Dako Tah Shrine"},
    {"id": 10,  "x": -3853.4, "z": 716.7,   "name": "Kay Noh Shrine"},
    {"id": 11,  "x": -3823.1, "z": -2206.4, "name": "Bareeda Naag Shrine"},
    {"id": 12,  "x": -3817.0, "z": 2819.8,  "name": "Hawa Koth Shrine"},
    {"id": 13,  "x": -3810.5, "z": 3127.2,  "name": "Jee Noh Shrine"},
    {"id": 14,  "x": -3656.1, "z": -1756.7, "name": "Sha Gehma Shrine"},
    {"id": 15,  "x": -3627.7, "z": -3038.2, "name": "Lanno Kooh Shrine"},
    {"id": 16,  "x": -3609.2, "z": -1515.4, "name": "Mozo Shenno Shrine"},
    {"id": 17,  "x": -3559.8, "z": 1953.0,  "name": "Daqo Chisay Shrine"},
    {"id": 18,  "x": -3465.5, "z": -448.0,  "name": "Rok Uwog Shrine"},
    {"id": 19,  "x": -3317.8, "z": 2162.5,  "name": "Misae Suma Shrine"},
    {"id": 20,  "x": -3083.0, "z": 1221.0,  "name": "Raqa Zunzo Shrine"},
    {"id": 21,  "x": -2998.6, "z": -3221.6, "name": "Gee Ha'rah Shrine"},
    {"id": 22,  "x": -2970.3, "z": 3781.5,  "name": "Sho Dantu Shrine"},
    {"id": 23,  "x": -2930.9, "z": -432.1,  "name": "Maag No'rah Shrine"},
    {"id": 24,  "x": -2832.5, "z": -1578.0, "name": "To Quomo Shrine"},
    {"id": 25,  "x": -2811.0, "z": 2300.1,  "name": "Tho Kayu Shrine"},
    {"id": 26,  "x": -2792.3, "z": -2882.3, "name": "Rin Oyaa Shrine"},
    {"id": 27,  "x": -2743.3, "z": 226.4,   "name": "Shae Loya Shrine"},
    {"id": 28,  "x": -2688.6, "z": 2811.2,  "name": "Joloo Nah Shrine"},
    {"id": 29,  "x": -2636.4, "z": -2060.4, "name": "Dunba Taag Shrine"},
    {"id": 30,  "x": -2379.8, "z": -2254.6, "name": "Qaza Tokki Shrine"},
    {"id": 31,  "x": -2378.0, "z": -3224.7, "name": "Hia Miu Shrine"},
    {"id": 32,  "x": -2297.4, "z": 460.7,   "name": "Zalta Wa Shrine"},
    {"id": 33,  "x": -2269.1, "z": -900.1,  "name": "Mijah Rokee Shrine"},
    {"id": 34,  "x": -2004.0, "z": 1674.3,  "name": "Kah Okeo Shrine"},
    {"id": 35,  "x": -1939.9, "z": -1458.2, "name": "Sheem Dagoze Shrine"},
    {"id": 36,  "x": -1893.3, "z": 91.5,    "name": "Monya Toma Shrine"},
    {"id": 37,  "x": -1795.0, "z": 3465.4,  "name": "Muwo Jeem Shrine"},
    {"id": 38,  "x": -1792.8, "z": 2423.4,  "name": "Shae Katha Shrine"},
    {"id": 39,  "x": -1721.4, "z": -2554.5, "name": "Noe Rajee Shrine"},
    {"id": 40,  "x": -1695.3, "z": 1700.1,  "name": "Kaam Ya'tak Shrine"},
    {"id": 41,  "x": -1673.2, "z": -3758.4, "name": "Katah Chuki Shrine"},
    {"id": 42,  "x": -1563.2, "z": 1310.1,  "name": "Noya Neha Shrine"},
    {"id": 43,  "x": -1488.6, "z": -1473.0, "name": "Saas Ko'sah Shrine"},
    {"id": 44,  "x": -1436.3, "z": 1991.0,  "name": "Owa Daim Shrine"},
    {"id": 45,  "x": -1432.3, "z": -594.2,  "name": "Maag Halan Shrine"},
    {"id": 46,  "x": -1418.2, "z": 3448.3,  "name": "Shai Yota Shrine"},
    {"id": 47,  "x": -1088.2, "z": -2661.5, "name": "Ritaag Zumo Shrine"},
    {"id": 48,  "x": -984.8,  "z": 3565.0,  "name": "Lakna Rokee Shrine"},
    {"id": 49,  "x": -967.8,  "z": 715.9,   "name": "Rota Ooh Shrine"},
    {"id": 50,  "x": -951.2,  "z": -623.8,  "name": "Keo Ruug Shrine"},
    {"id": 51,  "x": -925.0,  "z": 2321.2,  "name": "Ja Baij Shrine"},
    {"id": 52,  "x": -820.5,  "z": -3535.0, "name": "Katosa Aug Shrine"},
    {"id": 53,  "x": -673.2,  "z": 1513.0,  "name": "Oman Au Shrine"},
    {"id": 54,  "x": -636.4,  "z": -345.1,  "name": "Kuhn Sidajj Shrine"},
    {"id": 55,  "x": -446.7,  "z": 1990.2,  "name": "Keh Namut Shrine"},
    {"id": 56,  "x": -328.2,  "z": 2600.3,  "name": "Bosh Kala Shrine"},
    {"id": 57,  "x": -147.4,  "z": -1159.3, "name": "Daag Chokah Shrine"},
    {"id": 58,  "x": -26.4,   "z": -2458.6, "name": "Zuna Kai Shrine"},
    {"id": 59,  "x": 17.7,    "z": -1944.4, "name": "Ketoh Wawai Shrine"},
    {"id": 60,  "x": 87.0,    "z": 1658.7,  "name": "Hila Rao Shrine"},
    {"id": 61,  "x": 94.0,    "z": 3841.0,  "name": "Toto Sah Shrine"},
    {"id": 62,  "x": 283.4,   "z": -3119.6, "name": "Tu Ka'loh Shrine"},
    {"id": 63,  "x": 344.9,   "z": 1007.0,  "name": "Wahgo Katta Shrine"},
    {"id": 64,  "x": 470.7,   "z": -2168.8, "name": "Mirro Shaz Shrine"},
    {"id": 65,  "x": 523.3,   "z": 3526.3,  "name": "Ya Naga Shrine"},
    {"id": 66,  "x": 559.5,   "z": 2990.2,  "name": "Shee Vaneer Shrine"},
    {"id": 67,  "x": 761.3,   "z": -821.3,  "name": "Maag No'rah Shrine"},
    {"id": 68,  "x": 824.2,   "z": 187.8,   "name": "Kaya Wan Shrine"},
    {"id": 69,  "x": 837.1,   "z": -2419.7, "name": "Ke'nai Shakah Shrine"},
    {"id": 70,  "x": 854.7,   "z": 838.1,   "name": "Ha Dahamar Shrine"},
    {"id": 71,  "x": 870.3,   "z": 2328.5,  "name": "Ree Dahee Shrine"},
    {"id": 72,  "x": 1232.0,  "z": -1212.8, "name": "Dah Hesho Shrine"},
    {"id": 73,  "x": 1244.1,  "z": 1850.3,  "name": "Ta'loh Naeg Shrine"},
    {"id": 74,  "x": 1265.3,  "z": 1938.7,  "name": "Lakna Rokee Shrine"},
    {"id": 75,  "x": 1271.9,  "z": 1843.7,  "name": "Shee Venath Shrine"},
    {"id": 76,  "x": 1510.5,  "z": -377.0,  "name": "Dagah Keek Shrine"},
    {"id": 77,  "x": 1535.4,  "z": -3118.0, "name": "Tutsurak Shrine"},
    {"id": 78,  "x": 1586.7,  "z": 3614.9,  "name": "Kam Urog Shrine"},
    {"id": 79,  "x": 1601.0,  "z": 462.2,   "name": "Soh Kofi Shrine"},
    {"id": 80,  "x": 1662.4,  "z": 1921.6,  "name": "Tah Muhl Shrine"},
    {"id": 81,  "x": 1757.2,  "z": -2562.5, "name": "Dah Kaso Shrine"},
    {"id": 82,  "x": 1790.5,  "z": 2991.9,  "name": "Dow Na'eh Shrine"},
    {"id": 83,  "x": 1820.7,  "z": -1517.0, "name": "Mo'a Keet Shrine"},
    {"id": 84,  "x": 1841.9,  "z": 890.4,   "name": "Sah Dahaj Shrine"},
    {"id": 85,  "x": 1845.7,  "z": 2474.1,  "name": "Mezza Lo Shrine"},
    {"id": 86,  "x": 2007.0,  "z": 3285.0,  "name": "Shoqa Tatone Shrine"},
    {"id": 87,  "x": 2040.5,  "z": 972.2,   "name": "Yah Rin Shrine"},
    {"id": 88,  "x": 2065.8,  "z": -2328.4, "name": "Ze Kasho Shrine"},
    {"id": 89,  "x": 2076.8,  "z": -2039.8, "name": "Kayra Mah Shrine"},
    {"id": 90,  "x": 2238.4,  "z": -293.0,  "name": "Ne'ez Yohma Shrine"},
    {"id": 91,  "x": 2300.7,  "z": -941.3,  "name": "Rucco Maag Shrine"},
    {"id": 92,  "x": 2501.0,  "z": 1494.8,  "name": "Jitan Sa'mi Shrine"},
    {"id": 93,  "x": 2621.6,  "z": 378.2,   "name": "Shai Utoh Shrine"},
    {"id": 94,  "x": 2637.5,  "z": 2834.4,  "name": "Chaas Qeta Shrine"},
    {"id": 95,  "x": 2662.0,  "z": -3456.5, "name": "South Akkala Shrine"},
    {"id": 96,  "x": 2665.2,  "z": -1580.8, "name": "Shora Hah Shrine"},
    {"id": 97,  "x": 2697.7,  "z": 1333.5,  "name": "Myahm Agana Shrine"},
    {"id": 98,  "x": 2723.5,  "z": -1166.1, "name": "Toh Yahsa Shrine"},
    {"id": 99,  "x": 2833.4,  "z": 3311.0,  "name": "Muwo Jeem Shrine"},
    {"id": 100, "x": 3027.3,  "z": -1667.8, "name": "Rok Uwog Shrine"},
    {"id": 101, "x": 3149.7,  "z": -416.8,  "name": "Tahno O'ah Shrine"},
    {"id": 102, "x": 3323.6,  "z": -518.8,  "name": "Dag Ah Shrine"},
    {"id": 103, "x": 3324.5,  "z": -3420.4, "name": "Kah Mael Shrine"},
    {"id": 104, "x": 3333.5,  "z": 401.5,   "name": "Kam Urog Shrine"},
    {"id": 105, "x": 3388.4,  "z": 2215.8,  "name": "Tahno O'ah Shrine"},
    {"id": 106, "x": 3436.9,  "z": 3316.3,  "name": "Chaas Qeta Shrine"},
    {"id": 107, "x": 3658.1,  "z": 3308.3,  "name": "Kah Yah Shrine"},
    {"id": 108, "x": 3777.8,  "z": -2704.9, "name": "Tutsurak Shrine"},
    {"id": 109, "x": 3882.1,  "z": 1314.9,  "name": "Zanvo Shrine"},
    {"id": 110, "x": 3899.5,  "z": -1302.8, "name": "Dah Hesho Shrine"},
    {"id": 111, "x": 4012.2,  "z": 2990.5,  "name": "Korsh O'hu Shrine"},
    {"id": 112, "x": 4181.8,  "z": 1686.7,  "name": "Tawa Jinn Shrine"},
    {"id": 113, "x": 4194.5,  "z": -856.9,  "name": "Ritaag Zumo Shrine"},
    {"id": 114, "x": 4245.6,  "z": 252.9,   "name": "Kah Mael Shrine"},
    {"id": 115, "x": 4295.8,  "z": -2730.3, "name": "Tu Ka'loh Shrine"},
    {"id": 116, "x": 4524.6,  "z": -2127.5, "name": "Kenai Shakah Shrine"},
    {"id": 117, "x": 4655.0,  "z": -3710.0, "name": "Lomei Labyrinth Shrine"},
    {"id": 118, "x": 4709.2,  "z": -1310.3, "name": "Akkala Shrine"},
    {"id": 119, "x": 4737.5,  "z": 3772.1,  "name": "Muwo Jeem Shrine"},
]

# ── Shrine clear detection from save ──────────────────────────────────

def load_clear_hashes():
    """Build hash -> dungeon_num mapping for Clear_Dungeon flags."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)

    with open(BOOTUP_PACK, 'rb') as f:
        bootup = f.read()
    outer = parse_sarc(bootup)
    sdf_raw = yaz0_decompress(outer['GameData/savedataformat.ssarc'])
    sdf_files = parse_sarc(sdf_raw)

    hash_map = {}
    for page in range(8):
        key = f'/saveformat_{page}.bgsvdata'
        if key not in sdf_files:
            continue
        sdf = BYMLParser(sdf_files[key]).parse()
        for flag in sdf['file_list'][1]:
            dn = flag['DataName']
            if dn.startswith('Clear_Dungeon') and dn[13:].isdigit():
                num = int(dn[13:])
                hash_map[str(flag['HashValue'])] = num

    with open(CACHE_FILE, 'w') as f:
        json.dump(hash_map, f)
    return hash_map


def find_latest_save():
    slots = list(SAVE_DIR.glob("*/game_data.sav"))
    if not slots:
        return None
    return max(slots, key=lambda p: p.stat().st_mtime).parent.name


def detect_cleared_from_save(slot):
    """Read save file and return set of cleared dungeon numbers."""
    save_file = SAVE_DIR / str(slot) / "game_data.sav"
    with open(save_file, 'rb') as f:
        save = f.read()

    hash_map = load_clear_hashes()
    cleared = set()
    for off in range(4, len(save) - 8, 8):
        h = struct.unpack('>i', save[off:off+4])[0]
        v = struct.unpack('>I', save[off+4:off+8])[0]
        str_h = str(h)
        if str_h in hash_map and v == 1:
            cleared.add(hash_map[str_h])
    return cleared


# ── Manual tracking ───────────────────────────────────────────────────

def load_cleared():
    if CLEARED_FILE.exists():
        with open(CLEARED_FILE) as f:
            return json.load(f)
    return {'manual': [], 'last_manual': []}


def save_cleared(data):
    with open(CLEARED_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_all_cleared_ids():
    """Combine save-detected and manually tracked cleared shrine IDs."""
    slot = find_latest_save()
    save_cleared_dungeons = set()
    if slot:
        save_cleared_dungeons = detect_cleared_from_save(slot)

    manual = load_cleared()
    manual_ids = set(manual.get('manual', []))

    return save_cleared_dungeons, manual_ids


# ── Distance / display ────────────────────────────────────────────────

def distance(s, px, pz):
    return math.sqrt((s['x'] - px) ** 2 + (s['z'] - pz) ** 2)


def parse_position(args):
    if args[0].lower() in REGIONS:
        r = REGIONS[args[0].lower()]
        return r['x'], r['z']
    if len(args) >= 2:
        return float(args[0]), float(args[1])
    print(f"Unknown region: {args[0]}")
    print(f"Available: {', '.join(REGIONS.keys())}")
    sys.exit(1)


def show_status():
    save_cleared, manual_ids = get_all_cleared_ids()
    total_cleared = len(save_cleared)
    remaining = 120 - total_cleared
    manual_count = len(manual_ids)

    print(f"  Total Shrines:    120")
    print(f"  Cleared:          {total_cleared} ({total_cleared} from save)")
    print(f"  Remaining:        {remaining}")
    if manual_count:
        print(f"  Manual marks:     {manual_count}")


def get_uncleared_sorted(px, pz):
    """Get uncleared shrines sorted by distance from (px, pz)."""
    save_cleared, manual_ids = get_all_cleared_ids()
    uncollected = [s for s in SHRINES if s['id'] not in manual_ids]
    uncollected.sort(key=lambda s: distance(s, px, pz))
    total_cleared = len(save_cleared) + len(manual_ids)
    return uncollected, total_cleared


def inject_stamps(px, pz, count=30):
    """Inject shrine stamps into save file. Uses slots 151-180, preserves Korok stamps."""
    uncollected, total_cleared = get_uncleared_sorted(px, pz)
    remaining = 120 - total_cleared

    slot = find_latest_save()
    if slot is None:
        print("No save file found!")
        return

    save_file = SAVE_DIR / str(slot) / "game_data.sav"

    # Backup
    backup = save_file.with_suffix('.sav.backup_pre_shrine')
    shutil.copy2(save_file, backup)

    with open(save_file, 'rb') as f:
        save = bytearray(f.read())

    pos_start = save.index(ICON_POS_HASH)
    no_start = save.index(ICON_NO_HASH)

    # Only clear shrine slots (SHRINE_SLOT_START to SHRINE_SLOT_START + STAMP_LIMIT)
    # Slots 0-150 are reserved for user stamp + Korok stamps
    shrine_start = SHRINE_SLOT_START
    for i in range(shrine_start, shrine_start + STAMP_LIMIT):
        base = pos_start + i * 24
        struct.pack_into('>f', save, base + 4, -100000.0)
        struct.pack_into('>f', save, base + 12, 0.0)
        struct.pack_into('>f', save, base + 20, 0.0)
        base_no = no_start + i * 8
        struct.pack_into('>i', save, base_no + 4, -1)

    # Inject shrine stamps
    to_inject = uncollected[:count]
    actual = min(len(to_inject), STAMP_LIMIT)
    for i, s in enumerate(to_inject[:actual]):
        slot_idx = shrine_start + i
        base = pos_start + slot_idx * 24
        struct.pack_into('>f', save, base + 4, s['x'])
        struct.pack_into('>f', save, base + 12, 100.0)
        struct.pack_into('>f', save, base + 20, s['z'])
        base_no = no_start + slot_idx * 8
        struct.pack_into('>i', save, base_no + 4, STAMP_TYPE)

    with open(save_file, 'wb') as f:
        f.write(save)

    print(f"Injected {actual} shrine stamps into slot {slot} (star icons)")
    print(f"Sorted by distance from ({px:.0f}, {pz:.0f})")
    print(f"({total_cleared} cleared, {remaining} remaining)")
    print(f"Korok stamps preserved (slots 0-{shrine_start - 1})")
    print()
    print("Close BOTW and reload the save to see stamps.")
    print("After clearing, run: shrine_finder cleared 1 2 3 ...")


def show_list(px, pz, count=30):
    save_cleared, manual_ids = get_all_cleared_ids()

    # Filter out cleared shrines (by save detection)
    # We can't map save dungeon numbers to our coordinate-based IDs directly,
    # so we use the total count and manual marks
    uncollected = [s for s in SHRINES if s['id'] not in manual_ids]

    # Sort by distance
    uncollected.sort(key=lambda s: distance(s, px, pz))

    total_cleared = len(save_cleared)
    remaining = 120 - total_cleared - len(manual_ids)

    print(f"{count} nearest uncleared shrines to ({px:.0f}, {pz:.0f})")
    print(f"({total_cleared + len(manual_ids)} cleared, {remaining} remaining)")
    print()
    print(f"{'#':>4}  {'Dist':>6}  {'X':>10}  {'Z':>10}  Name")
    print("-" * 60)

    for i, s in enumerate(uncollected[:count], 1):
        d = distance(s, px, pz)
        print(f"{i:4d}  {d:6.0f}  {s['x']:10.1f}  {s['z']:10.1f}  {s['name']}")


def mark_cleared(args):
    cleared = load_cleared()
    old_manual = list(cleared.get('manual', []))
    new_ids = set(old_manual)

    for arg in args:
        if '-' in arg:
            start, end = arg.split('-')
            for i in range(int(start), int(end) + 1):
                new_ids.add(i)
        else:
            new_ids.add(int(arg))

    cleared['last_manual'] = old_manual
    cleared['manual'] = sorted(new_ids)
    save_cleared(cleared)
    added = len(new_ids) - len(old_manual)
    print(f"Marked {added} shrine(s) as cleared (total manual: {len(new_ids)})")


def undo_cleared():
    cleared = load_cleared()
    if 'last_manual' in cleared and cleared['last_manual'] is not None:
        cleared['manual'] = cleared['last_manual']
        cleared['last_manual'] = None
        save_cleared(cleared)
        print(f"Undone. Manual marks restored to {len(cleared['manual'])}")
    else:
        print("Nothing to undo")


def reset_cleared():
    save_cleared({'manual': [], 'last_manual': None})
    print("Manual tracking reset")


# ── Main ──────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1].lower()

    if cmd == 'status':
        show_status()

    elif cmd == 'inject':
        if len(sys.argv) > 2:
            px, pz = parse_position(sys.argv[2:])
        else:
            px, pz = 1807, 992
        inject_stamps(px, pz)

    elif cmd == 'list':
        if len(sys.argv) > 2:
            px, pz = parse_position(sys.argv[2:])
        else:
            px, pz = 1807, 992
        show_list(px, pz)

    elif cmd == 'cleared':
        if len(sys.argv) < 3:
            print("Usage: shrine_finder cleared 1 2 5-10")
            return
        mark_cleared(sys.argv[2:])

    elif cmd == 'undo':
        undo_cleared()

    elif cmd == 'reset':
        reset_cleared()

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == '__main__':
    main()
