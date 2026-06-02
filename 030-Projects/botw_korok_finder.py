#!/usr/bin/env python3
"""
BOTW Korok Stamp Manager
=========================
Finds Koroks, tracks collected ones, injects stamps into save.

Usage:
    python3 botw_korok_finder.py status                 # Show collected/remaining
    python3 botw_korok_finder.py inject [region|X Z]    # Inject 150 nearest uncollected stamps
    python3 botw_korok_finder.py collected 1 2 5-10     # Mark stamp #s as collected (manual)
    python3 botw_korok_finder.py undo                   # Undo last collected marking
    python3 botw_korok_finder.py list [region|X Z]      # List nearest uncollected (no inject)
    python3 botw_korok_finder.py reset                  # Clear all collected tracking

Regions: plateau, central, hateno, faron, lanayru, eldin, akkala, hebra, gerudo,
         ridgeland, kakariko, zora, rito, korok
"""

import struct
import math
import sys
import json
import shutil
from pathlib import Path

CEMU_BASE = Path("/home/brmz/.local/share/Cemu")
BOOTUP_PACK = CEMU_BASE / "EUR/GAMES/Base Games/The Legend of Zelda Breath of the Wild [ALZP01]/content/Pack/Bootup.pack"
CACHE_FILE = Path("/tmp/korok_900_cache.json")
COLLECTED_FILE = CEMU_BASE / "korok_collected.json"
SAVE_DIR = CEMU_BASE / "mlc01/usr/save/00050000/101c9500/user/80000001"

STAMP_TYPE = 34
STAMP_LIMIT = 150
ICON_POS_HASH = struct.pack('>i', -358748353)
ICON_NO_HASH = struct.pack('>i', -1820112626)
HASH_CACHE_FILE = Path("/tmp/korok_hash_cache.json")

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


# ── Binary parsers (Yaz0, SARC, BYML) ─────────────────────────────────

def yaz0_decompress(data):
    ds = struct.unpack('>I', data[4:8])[0]
    o = bytearray(ds); sp = 16; dp = 0
    while dp < ds:
        cb = data[sp]; sp += 1
        for bit in range(8):
            if dp >= ds: break
            if cb & (0x80 >> bit):
                o[dp] = data[sp]; sp += 1; dp += 1
            else:
                b1 = data[sp]; b2 = data[sp+1]; sp += 2
                d = ((b1 & 0xF) << 8) | b2; rp = dp - d - 1
                l = b1 >> 4
                if l == 0: l = data[sp] + 0x12; sp += 1
                else: l += 2
                for j in range(l):
                    if dp >= ds: break
                    o[dp] = o[rp + j]; dp += 1
    return bytes(o)


def parse_sarc(data):
    hl = struct.unpack('>H', data[4:6])[0]
    bom = struct.unpack('>H', data[6:8])[0]
    fmt = '>' if bom == 0xFEFF else '<'
    do = struct.unpack(f'{fmt}I', data[12:16])[0]
    nc = struct.unpack(f'{fmt}H', data[hl+6:hl+8])[0]
    sns = hl + 12; sts = sns + nc * 16 + 8; files = {}
    for i in range(nc):
        no = sns + i * 16
        attrs = struct.unpack(f'{fmt}I', data[no+4:no+8])[0]
        hn = (attrs >> 24) & 0xFF == 0x01
        noff = (attrs & 0xFFFFFF) * 4
        ds2 = struct.unpack(f'{fmt}I', data[no+8:no+12])[0]
        de = struct.unpack(f'{fmt}I', data[no+12:no+16])[0]
        name = ''
        if hn:
            ns = sts + noff; ne = data[ns:].index(b'\x00') + ns
            name = data[ns:ne].decode('utf-8')
        files[name] = data[do + ds2:do + de]
    return files


class BYMLParser:
    def __init__(self, data):
        self.data = data; self.big_endian = data[:2] == b'BY'
        self.fmt = '>' if self.big_endian else '<'
        nnt = struct.unpack(f'{self.fmt}I', data[4:8])[0]
        svt = struct.unpack(f'{self.fmt}I', data[8:12])[0]
        self.root_off = struct.unpack(f'{self.fmt}I', data[12:16])[0]
        self.node_names = self._st(nnt) if nnt else []
        self.string_values = self._st(svt) if svt else []

    def _st(self, off):
        if not off: return []
        c = self._u24(off+1)
        ofs = [struct.unpack(f'{self.fmt}I', self.data[off+4+i*4:off+8+i*4])[0] for i in range(c+1)]
        return [self.data[off+ofs[i]:self.data.index(b'\x00', off+ofs[i])].decode('utf-8') for i in range(c)]

    def _u24(self, off):
        b = self.data[off:off+3]
        return (b[0]<<16|b[1]<<8|b[2]) if self.big_endian else (b[0]|b[1]<<8|b[2]<<16)

    def parse(self): return self._node(self.root_off) if self.root_off else None

    def _node(self, off):
        nt = self.data[off]
        if nt == 0xC0: return self._array(off)
        if nt == 0xC1: return self._dict(off)

    def _array(self, off):
        c = self._u24(off+1); ts = off+4; vs = ts+((c+3)&~3)
        return [self._val(self.data[ts+i], struct.unpack(f'{self.fmt}I', self.data[vs+i*4:vs+(i+1)*4])[0]) for i in range(c)]

    def _dict(self, off):
        c = self._u24(off+1); r = {}
        for i in range(c):
            eo = off+4+i*8; ni = self._u24(eo); tb = self.data[eo+3]
            vr = struct.unpack(f'{self.fmt}I', self.data[eo+4:eo+8])[0]
            r[self.node_names[ni]] = self._val(tb, vr)
        return r

    def _val(self, tb, vr):
        if tb == 0xA0: return self.string_values[vr] if vr < len(self.string_values) else f"str#{vr}"
        if tb in (0xC0, 0xC1): return self._node(vr)
        if tb == 0xD0: return bool(vr)
        if tb == 0xD1: return struct.unpack(f'{self.fmt}i', struct.pack(f'{self.fmt}I', vr))[0]
        if tb == 0xD2: return struct.unpack(f'{self.fmt}f', struct.pack(f'{self.fmt}I', vr))[0]
        if tb == 0xD3: return vr
        return vr


# ── Korok database ────────────────────────────────────────────────────

def load_koroks():
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)

    print("Extracting Korok data from game files (first run only)...")
    with open(BOOTUP_PACK, 'rb') as f:
        bootup = f.read()
    outer = parse_sarc(bootup)
    static_raw = yaz0_decompress(outer['Map/MainField/Static.smubin'])
    raw_koroks = BYMLParser(static_raw).parse()['KorokLocation']

    db = []
    for k in raw_koroks:
        t = k['Translate']
        db.append({
            'flag': k['Flag'],
            'x': round(t['X'], 1),
            'y': round(t['Y'], 1),
            'z': round(t['Z'], 1),
            'type': k['PlacementType'],
        })

    with open(CACHE_FILE, 'w') as f:
        json.dump(db, f)
    return db


# ── Korok hash database (for save detection) ─────────────────────────

def load_korok_hashes():
    """Build hash→flag mapping from savedataformat for detecting collected Koroks."""
    if HASH_CACHE_FILE.exists():
        with open(HASH_CACHE_FILE) as f:
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
            if 'Npc_HiddenKorok' in flag['DataName']:
                hash_map[str(flag['HashValue'])] = flag['DataName']

    with open(HASH_CACHE_FILE, 'w') as f:
        json.dump(hash_map, f)
    return hash_map


def detect_collected_from_save(slot):
    """Read save file and return set of collected Korok flag names.
    Scans the ENTIRE file as 8-byte (hash, value) pairs because
    Korok flags are scattered across multiple sections."""
    save_file = SAVE_DIR / str(slot) / "game_data.sav"
    with open(save_file, 'rb') as f:
        save = f.read()

    hash_map = load_korok_hashes()

    collected = set()
    for off in range(4, len(save) - 8, 8):
        h = struct.unpack('>i', save[off:off+4])[0]
        v = struct.unpack('>I', save[off+4:off+8])[0]
        str_h = str(h)
        if str_h in hash_map and v == 1:
            collected.add(hash_map[str_h])

    return collected


# ── Collected tracking ────────────────────────────────────────────────

def load_collected():
    if COLLECTED_FILE.exists():
        with open(COLLECTED_FILE) as f:
            return json.load(f)
    return {'flags': [], 'last_inject': []}


def save_collected(data):
    with open(COLLECTED_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def get_uncollected(koroks, collected_flags):
    return [k for k in koroks if k['flag'] not in collected_flags]


def sync_collected_from_save():
    """Merge save-detected collections into our tracking file."""
    slot = find_latest_save()
    if slot is None:
        return set()

    from_save = detect_collected_from_save(slot)
    collected = load_collected()

    existing = set(collected['flags'])
    new_from_save = from_save - existing

    if new_from_save:
        collected['flags'].extend(new_from_save)
        save_collected(collected)

    return from_save


# ── Save file operations ─────────────────────────────────────────────

def find_latest_save():
    """Find the most recently modified save slot."""
    latest = None
    latest_mtime = 0
    for slot in range(6):
        save_file = SAVE_DIR / str(slot) / "game_data.sav"
        if save_file.exists():
            mtime = save_file.stat().st_mtime
            if mtime > latest_mtime:
                latest_mtime = mtime
                latest = slot
    return latest


def read_current_stamps(slot):
    """Read existing stamps from a save slot. Returns list of (x, y, z, type)."""
    save_file = SAVE_DIR / str(slot) / "game_data.sav"
    with open(save_file, 'rb') as f:
        save = f.read()

    pos_start = save.index(ICON_POS_HASH)
    no_start = save.index(ICON_NO_HASH)

    stamps = []
    for i in range(200):
        base = pos_start + i * 24
        x = struct.unpack('>f', save[base+4:base+8])[0]
        y = struct.unpack('>f', save[base+12:base+16])[0]
        z = struct.unpack('>f', save[base+20:base+24])[0]
        base_no = no_start + i * 8
        t = struct.unpack('>i', save[base_no+4:base_no+8])[0]
        stamps.append({'x': x, 'y': y, 'z': z, 'type': t, 'slot': i})
    return stamps


def detect_player_position(stamps):
    """Find player's manual stamp (non-Korok, non-empty) to use as position."""
    # User stamps have valid coords but might have any type
    # Our injected stamps also have type 34, so look at slot 0 specifically
    # (user's manual stamps go in the first available slot)
    for s in stamps:
        if s['x'] > -99999 and s['type'] != -1:
            return s['x'], s['z']
    return None, None


def inject_stamps(slot, koroks_to_inject):
    """Write Korok stamps into save file, preserving slot 0 (user stamp)."""
    save_file = SAVE_DIR / str(slot) / "game_data.sav"

    # Backup
    backup = save_file.with_suffix('.sav.backup_pre_korok')
    if not backup.exists():
        shutil.copy2(save_file, backup)

    with open(save_file, 'rb') as f:
        save = bytearray(f.read())

    pos_start = save.index(ICON_POS_HASH)
    no_start = save.index(ICON_NO_HASH)

    # Read slot 0 to preserve user's manual stamp
    s0_x = struct.unpack('>f', save[pos_start+4:pos_start+8])[0]
    has_user_stamp = s0_x > -99999

    # Clear Korok stamp slots only (0-150), preserve shrine slots (151+)
    for i in range(151):
        base = pos_start + i * 24
        struct.pack_into('>f', save, base + 4, -100000.0)
        struct.pack_into('>f', save, base + 12, 0.0)
        struct.pack_into('>f', save, base + 20, 0.0)
        base_no = no_start + i * 8
        struct.pack_into('>i', save, base_no + 4, -1)

    # Restore user stamp at slot 0 if it existed
    start_slot = 0
    if has_user_stamp:
        # Re-read from the backup to get original user stamp
        with open(backup, 'rb') as f:
            orig = f.read()
        orig_pos = orig.index(ICON_POS_HASH)
        orig_no = orig.index(ICON_NO_HASH)
        ox = struct.unpack('>f', orig[orig_pos+4:orig_pos+8])[0]
        if ox > -99999:
            save[pos_start+4:pos_start+8] = orig[orig_pos+4:orig_pos+8]
            save[pos_start+12:pos_start+16] = orig[orig_pos+12:orig_pos+16]
            save[pos_start+20:pos_start+24] = orig[orig_pos+20:orig_pos+24]
            save[no_start+4:no_start+8] = orig[orig_no+4:orig_no+8]
            start_slot = 1

    # Inject Koroks (up to STAMP_LIMIT)
    count = min(len(koroks_to_inject), STAMP_LIMIT, 200 - start_slot)
    for i, k in enumerate(koroks_to_inject[:count]):
        slot_idx = start_slot + i
        base = pos_start + slot_idx * 24
        struct.pack_into('>f', save, base + 4, k['x'])
        struct.pack_into('>f', save, base + 12, k['y'])
        struct.pack_into('>f', save, base + 20, k['z'])
        base_no = no_start + slot_idx * 8
        struct.pack_into('>i', save, base_no + 4, STAMP_TYPE)

    with open(save_file, 'wb') as f:
        f.write(save)

    return count


# ── Position parsing ──────────────────────────────────────────────────

def parse_position(args):
    """Parse position from args: region name or 'X Z' coordinates."""
    if not args:
        return None, None, None

    if args[0].lower() in REGIONS:
        r = REGIONS[args[0].lower()]
        return r['x'], r['z'], r['name']

    try:
        cx = float(args[0])
        cz = float(args[1]) if len(args) > 1 else 0.0
        return cx, cz, f"({cx:.0f}, {cz:.0f})"
    except (ValueError, IndexError):
        return None, None, None


def parse_numbers(args):
    """Parse stamp numbers from args like '1 2 5-10 15'."""
    nums = set()
    for a in args:
        if '-' in a:
            parts = a.split('-')
            try:
                start, end = int(parts[0]), int(parts[1])
                nums.update(range(start, end + 1))
            except (ValueError, IndexError):
                pass
        else:
            try:
                nums.add(int(a))
            except ValueError:
                pass
    return sorted(nums)


# ── Commands ──────────────────────────────────────────────────────────

def cmd_status():
    koroks = load_koroks()

    # Auto-sync from save
    from_save = sync_collected_from_save()
    collected = load_collected()
    all_collected = set(collected['flags'])
    uncollected = get_uncollected(koroks, all_collected)

    print(f"  Total Koroks:     900")
    print(f"  Collected:        {len(all_collected)} ({len(from_save)} detected from save)")
    print(f"  Remaining:        {len(uncollected)}")

    if collected['last_inject']:
        print(f"  Last inject:      {len(collected['last_inject'])} stamps")

    slot = find_latest_save()
    if slot is not None:
        stamps = read_current_stamps(slot)
        active = sum(1 for s in stamps if s['x'] > -99999)
        print(f"  Active stamps:    {active} (save slot {slot})")


def cmd_list(pos_args):
    koroks = load_koroks()
    sync_collected_from_save()
    collected = load_collected()
    uncollected = get_uncollected(koroks, set(collected['flags']))

    cx, cz, label = parse_position(pos_args)
    if cx is None:
        # Try to detect from save
        slot = find_latest_save()
        if slot is not None:
            stamps = read_current_stamps(slot)
            cx, cz = detect_player_position(stamps)
            label = f"player position ({cx:.0f}, {cz:.0f})" if cx else None

    if cx is None:
        cx, cz, label = -500, 1800, "Great Plateau (default)"

    for k in uncollected:
        k['dist'] = math.sqrt((k['x'] - cx)**2 + (k['z'] - cz)**2)
    uncollected.sort(key=lambda k: k['dist'])

    nearest = uncollected[:STAMP_LIMIT]
    print(f"\n{STAMP_LIMIT} nearest uncollected Koroks to {label}")
    print(f"({len(collected['flags'])} collected, {len(uncollected)} remaining)\n")
    print(f"{'#':>4}  {'Dist':>6}  {'X':>9}  {'Z':>9}  {'Y':>7}  Type")
    print("-" * 60)
    for i, k in enumerate(nearest, 1):
        print(f"{i:4d}  {k['dist']:6.0f}  {k['x']:9.1f}  {k['z']:9.1f}  {k['y']:7.1f}  {k['type']}")


def cmd_inject(pos_args):
    koroks = load_koroks()
    sync_collected_from_save()
    collected = load_collected()
    uncollected = get_uncollected(koroks, set(collected['flags']))

    cx, cz, label = parse_position(pos_args)
    if cx is None:
        slot = find_latest_save()
        if slot is not None:
            stamps = read_current_stamps(slot)
            cx, cz = detect_player_position(stamps)
            label = f"player position ({cx:.0f}, {cz:.0f})" if cx else None

    if cx is None:
        cx, cz, label = -500, 1800, "Great Plateau (default)"

    for k in uncollected:
        k['dist'] = math.sqrt((k['x'] - cx)**2 + (k['z'] - cz)**2)
    uncollected.sort(key=lambda k: k['dist'])

    nearest = uncollected[:STAMP_LIMIT]

    slot = find_latest_save()
    if slot is None:
        print("No save file found!")
        return

    count = inject_stamps(slot, nearest)

    # Track what we injected (for the 'collected' command)
    collected['last_inject'] = [k['flag'] for k in nearest[:count]]
    save_collected(collected)

    print(f"Injected {count} Korok stamps into slot {slot}")
    print(f"Sorted by distance from {label}")
    print(f"({len(collected['flags'])} collected, {len(uncollected)} remaining)")
    print(f"\nClose BOTW and reload the save to see stamps.")
    print(f"After collecting, run: korok collected 1 2 3 ...")


def cmd_collected(num_args):
    collected = load_collected()

    if not collected['last_inject']:
        print("No stamps injected yet. Run 'inject' first.")
        return

    nums = parse_numbers(num_args)
    if not nums:
        print("Usage: collected 1 2 5-10 15")
        print("Use stamp numbers from the last inject (1-indexed).")
        return

    newly_collected = []
    for n in nums:
        idx = n - 1  # 1-indexed to 0-indexed
        if 0 <= idx < len(collected['last_inject']):
            flag = collected['last_inject'][idx]
            if flag not in collected['flags']:
                collected['flags'].append(flag)
                newly_collected.append(n)

    save_collected(collected)
    print(f"Marked {len(newly_collected)} Koroks as collected: {newly_collected}")
    print(f"Total collected: {len(collected['flags'])}/900")
    print(f"Run 'inject' again to refresh stamps with remaining Koroks.")


def cmd_undo():
    collected = load_collected()
    if not collected['flags']:
        print("Nothing to undo.")
        return

    removed = collected['flags'].pop()
    save_collected(collected)
    print(f"Unmarked: {removed}")
    print(f"Total collected: {len(collected['flags'])}/900")


def cmd_reset():
    save_collected({'flags': [], 'last_inject': []})
    print("Cleared all collected tracking.")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        cmd_status()
        return

    cmd = args[0].lower()
    rest = args[1:]

    if cmd == 'status':
        cmd_status()
    elif cmd == 'list':
        cmd_list(rest)
    elif cmd == 'inject':
        cmd_inject(rest)
    elif cmd == 'collected':
        cmd_collected(rest)
    elif cmd == 'undo':
        cmd_undo()
    elif cmd == 'reset':
        cmd_reset()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)


if __name__ == '__main__':
    main()
