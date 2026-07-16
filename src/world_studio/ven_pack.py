"""VEN export/import via ~/.aidm/ven-collector/*.ven packs.

Supports:
  - **prime** packs — portable idea (desc, lore, wiki soft-links, template book pages)
  - **instance** packs — a lived copy (title/desc overrides, instance lore, book pages)
    always carries the prime definition so the target world can rehydrate both.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .db import get_meta
from .ids import (
    cute_name,
    digits_from_short_ref,
    normalize_formal_name,
    parse_ven_code,
    slugify,
)

PACK_FORMAT = "aidm.ven"
PACK_VERSION = 2
_SEQ_RE = re.compile(r"^(\d{4})-", re.IGNORECASE)


def aidm_home() -> Path:
    """User-level AIDM data root: ~/.aidm"""
    return Path.home() / ".aidm"


def ven_collector_dir(*, create: bool = True) -> Path:
    """Shared cartridge library: ~/.aidm/ven-collector"""
    d = aidm_home() / "ven-collector"
    if create:
        d.mkdir(parents=True, exist_ok=True)
    return d


def world_label(world: Any, world_path: Path | None = None) -> str:
    """Human origin stamp for packs (Imported.To, The Void, …)."""
    name = get_meta(world.conn, "world_name")
    if name and str(name).strip():
        return str(name).strip()
    if world_path is not None:
        return world_path.name
    return "unknown-world"


def next_collector_seq(collector: Path | None = None) -> int:
    root = collector or ven_collector_dir()
    max_n = 0
    for p in root.glob("*.ven"):
        m = _SEQ_RE.match(p.name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return max_n + 1


def _slug_fs(slug: str) -> str:
    slug_part = cute_name(slug or "unnamed").lower().replace("_", "-")
    return re.sub(r"[^a-z0-9-]+", "-", slug_part).strip("-") or "unnamed"


def pack_filename(seq: int, code: str, slug: str) -> str:
    """``0001-EVT-001-the-knock.ven`` — seq, code, cute slug."""
    code_part = (parse_ven_code(code) or code or "OTH-000").upper()
    return f"{seq:04d}-{code_part}-{_slug_fs(slug)}.ven"


def pack_filename_instance(
    seq: int, code: str, digits: str, title_slug: str
) -> str:
    """``0002-BOK-001-0001-ritual-notes.ven`` — seq, code, copy digits, title."""
    code_part = (parse_ven_code(code) or code or "OTH-000").upper()
    dig = digits_from_short_ref(digits) or "0001"
    return f"{seq:04d}-{code_part}-{dig}-{_slug_fs(title_slug)}.ven"


def _pages_from_instance(world: Any, inst_id: str) -> list[dict[str, Any]]:
    try:
        pages = world.list_book_pages(inst_id)
    except Exception:  # noqa: BLE001
        return []
    return [
        {
            "position": int(p["position"] or 0),
            "title": p["title"] or "",
            "body": p["body"] or "",
        }
        for p in pages
    ]


def _book_pages_for_ven(world: Any, ven_id: str) -> list[dict[str, Any]]:
    """Template pages from the first book instance that has any."""
    for inst in world.list_instances_of_ven(ven_id):
        if (inst.ven_kind or "").lower() not in ("folio", "book"):
            continue
        pages = _pages_from_instance(world, inst.id)
        if pages:
            return pages
    return []


def _lore_list(world: Any, subject_type: str, subject_id: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for r in world.lore_for(subject_type, subject_id):
        out.append(
            {
                "title": r["title"] or "",
                "body": r["body"] or "",
                "when_label": r["when_label"],
                "author": r["author"] or "builder",
            }
        )
    return out


def _prime_payload(world: Any, ven: Any) -> dict[str, Any]:
    parent = world.parent_of(ven.id) if hasattr(world, "parent_of") else None
    wiki_soft: list[dict[str, str]] = []
    for wid in world.get_wiki_links(ven.id):
        wven = world.get_ven(wid)
        if wven is None:
            continue
        wiki_soft.append(
            {
                "code": wven.code or "",
                "slug": wven.slug or "",
                "name": wven.name or "",
                "kind": wven.kind or "",
            }
        )
    parent_soft = None
    if parent is not None:
        parent_soft = {
            "code": parent.code or "",
            "slug": parent.slug or "",
            "name": parent.name or "",
            "kind": parent.kind or "",
        }
    book_pages = (
        _book_pages_for_ven(world, ven.id)
        if (ven.kind or "").lower() in ("folio", "book")
        else []
    )
    return {
        "name": ven.name,
        "slug": ven.slug,
        "code": ven.code or "",
        "kind": ven.kind,
        "subtype": ven.subtype,
        "description": ven.description or "",
        "tags": list(ven.tags or []),
        "meta": dict(ven.meta or {}) if ven.meta else {},
        "parent": parent_soft,
        "lore": _lore_list(world, "ven", ven.id),
        "wiki_links": wiki_soft,
        "book_pages": book_pages,
    }


def build_export_pack(
    world: Any,
    ven: Any,
    *,
    origin_world: str,
    seq: int,
) -> dict[str, Any]:
    """Serialize a prime VEN for the collector."""
    prime = _prime_payload(world, ven)
    return {
        "format": PACK_FORMAT,
        "version": PACK_VERSION,
        "pack_kind": "prime",
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "seq": seq,
        "provenance": {
            "origin_world": origin_world,
            "home_code": ven.code or "",
            "export_seq": seq,
            "pack_kind": "prime",
        },
        "prime": {k: v for k, v in prime.items() if k not in ("lore", "wiki_links", "book_pages")},
        "lore": prime["lore"],
        "wiki_links": prime["wiki_links"],
        "book_pages": prime["book_pages"],
    }


def build_export_instance_pack(
    world: Any,
    inst: Any,
    *,
    origin_world: str,
    seq: int,
) -> dict[str, Any]:
    """Serialize a lived instance + its prime definition."""
    ven = world.get_ven(inst.ven_id)
    if ven is None:
        raise ValueError("Instance has no prime VEN")
    prime = _prime_payload(world, ven)
    dig = digits_from_short_ref(world.short_ref_of(inst.id)) or "0001"
    try:
        desc_ov = world.get_description_override(inst.id)
    except Exception:  # noqa: BLE001
        desc_ov = None
    name_ov = world.get_name_override(inst.id)
    # Prefer explicit override; if title differs from prime, store display title
    if not name_ov and display_differs(inst.name, ven.name):
        name_ov = inst.name

    pages = (
        _pages_from_instance(world, inst.id)
        if (inst.ven_kind or "").lower() in ("folio", "book")
        else []
    )

    return {
        "format": PACK_FORMAT,
        "version": PACK_VERSION,
        "pack_kind": "instance",
        "exported_at": datetime.now(timezone.utc).isoformat(),
        "seq": seq,
        "provenance": {
            "origin_world": origin_world,
            "home_code": ven.code or "",
            "home_instance_ref": world.short_ref_of(inst.id),
            "home_instance_digits": dig,
            "export_seq": seq,
            "pack_kind": "instance",
        },
        "prime": {
            k: v for k, v in prime.items() if k not in ("lore", "wiki_links", "book_pages")
        },
        "lore": prime["lore"],
        "wiki_links": prime["wiki_links"],
        # Prime-level template pages (may be empty); instance pages below win on import
        "book_pages": prime["book_pages"],
        "instance": {
            "name_override": name_ov,
            "description_override": desc_ov,
            "short_ref_digits": dig,
            "lore": _lore_list(world, "instance", inst.id),
            "book_pages": pages,
        },
    }


def display_differs(a: str | None, b: str | None) -> bool:
    return (a or "").strip().casefold() != (b or "").strip().casefold()


def write_pack(pack: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(pack, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return path


def export_ven(
    world: Any,
    ven: Any,
    *,
    origin_world: str,
    collector: Path | None = None,
) -> Path:
    """Export prime to collector; returns path written."""
    root = collector or ven_collector_dir()
    seq = next_collector_seq(root)
    code = ven.code or "OTH-000"
    slug = ven.slug or cute_name(ven.name)
    fname = pack_filename(seq, code, slug)
    pack = build_export_pack(world, ven, origin_world=origin_world, seq=seq)
    _stamp_prime_ie(world, ven, pack, origin_world, seq)
    return write_pack(pack, root / fname)


def export_instance(
    world: Any,
    inst: Any,
    *,
    origin_world: str,
    collector: Path | None = None,
) -> Path:
    """Export instance + prime definition to collector."""
    ven = world.get_ven(inst.ven_id)
    if ven is None:
        raise ValueError("Instance has no prime VEN")
    root = collector or ven_collector_dir()
    seq = next_collector_seq(root)
    code = ven.code or "OTH-000"
    dig = digits_from_short_ref(world.short_ref_of(inst.id)) or "0001"
    title_slug = cute_name(inst.name or ven.name)
    fname = pack_filename_instance(seq, code, dig, title_slug)
    pack = build_export_instance_pack(
        world, inst, origin_world=origin_world, seq=seq
    )
    _stamp_prime_ie(world, ven, pack, origin_world, seq)
    return write_pack(pack, root / fname)


def _stamp_prime_ie(
    world: Any, ven: Any, pack: dict[str, Any], origin_world: str, seq: int
) -> None:
    meta = dict(ven.meta or {})
    ie = dict(meta.get("ie") or {})
    ie["last_export_seq"] = seq
    ie["last_export_at"] = pack["exported_at"]
    ie["home_code"] = ven.code or ""
    ie["origin_world"] = origin_world
    ie["last_pack_kind"] = pack.get("pack_kind") or "prime"
    meta["ie"] = ie
    world._set_ven_meta(ven.id, meta)  # noqa: SLF001


@dataclass
class PackInfo:
    path: Path
    seq: int
    code: str
    slug: str
    name: str
    kind: str
    origin_world: str
    pack_kind: str = "prime"  # prime | instance
    instance_title: str = ""


def list_packs(collector: Path | None = None) -> list[PackInfo]:
    root = collector or ven_collector_dir()
    out: list[PackInfo] = []
    for p in sorted(root.glob("*.ven")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("format") != PACK_FORMAT:
            continue
        prime = data.get("prime") or {}
        prov = data.get("provenance") or {}
        inst = data.get("instance") or {}
        pack_kind = str(
            data.get("pack_kind") or prov.get("pack_kind") or "prime"
        )
        display_name = str(prime.get("name") or p.stem)
        inst_title = ""
        if pack_kind == "instance":
            inst_title = str(
                inst.get("name_override") or display_name
            )
            display_name = inst_title
        out.append(
            PackInfo(
                path=p,
                seq=int(data.get("seq") or 0),
                code=str(prime.get("code") or ""),
                slug=str(prime.get("slug") or ""),
                name=display_name,
                kind=str(prime.get("kind") or ""),
                origin_world=str(prov.get("origin_world") or ""),
                pack_kind=pack_kind,
                instance_title=inst_title,
            )
        )
    return out


def load_pack_file(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("format") != PACK_FORMAT:
        raise ValueError(f"Not an AIDM VEN pack: {path.name}")
    return data


def _ensure_prime(
    world: Any,
    pack: dict[str, Any],
    *,
    target_world_label: str,
) -> tuple[str, str, str | None, bool]:
    """
    Ensure prime exists in world. Returns (ven_id, local_code, remap_note, created).
    """
    from .world import KINDS

    prime = pack.get("prime") or {}
    name = normalize_formal_name(prime.get("name") or "Imported")
    kind = (prime.get("kind") or "other").lower()
    if kind not in KINDS:
        kind = "other"
    home_code = (
        parse_ven_code(str(prime.get("code") or ""))
        or str(prime.get("code") or "").strip()
    )
    slug_hint = prime.get("slug") or slugify(name)

    # Reuse existing prime by code or unique slug
    existing = world.get_ven_by_code(home_code) if home_code else None
    if existing is None and slug_hint:
        by_slug = world.find_ven(str(slug_hint))
        if by_slug and by_slug.kind == kind:
            existing = by_slug
    if existing is not None:
        return existing.id, existing.code or home_code or "", None, False

    subtype = prime.get("subtype")
    description = prime.get("description") or ""
    tags = list(prime.get("tags") or [])
    base_meta = dict(prime.get("meta") or {})
    base_meta.pop("ie", None)
    if subtype:
        base_meta["subtype"] = subtype

    prov = pack.get("provenance") or {}
    origin_world = str(prov.get("origin_world") or "")
    export_seq = prov.get("export_seq") or pack.get("seq")

    local_code = (
        home_code if home_code and world.get_ven_by_code(home_code) is None else None
    )
    remap_note = None
    if home_code and local_code is None:
        local_code = world.allocate_ven_code(kind)
        remap_note = f"code remapped {home_code} → {local_code}"

    parent_id = None
    parent_soft = prime.get("parent")
    if isinstance(parent_soft, dict):
        parent_id = _resolve_soft_ven(world, parent_soft)

    ie_meta = {
        "home_code": home_code or "",
        "origin_world": origin_world,
        "imported_into": target_world_label,
        "imported_at": datetime.now(timezone.utc).isoformat(),
        "export_seq": export_seq,
        "pack_format": PACK_VERSION,
    }
    if remap_note:
        ie_meta["code_remap"] = remap_note
    base_meta["ie"] = ie_meta

    ven_id = world.create_ven(
        name,
        kind,
        description=description,
        slug=slug_hint,
        tags=tags,
        meta=base_meta,
        parent_ven_id=parent_id,
        code=local_code,
    )

    for entry in pack.get("lore") or []:
        if not isinstance(entry, dict):
            continue
        body = entry.get("body") or ""
        if not str(body).strip():
            continue
        world.add_lore(
            "ven",
            ven_id,
            body=str(body),
            title=str(entry.get("title") or ""),
            when_label=entry.get("when_label"),
            author=str(entry.get("author") or "import"),
        )

    for link in pack.get("wiki_links") or []:
        if not isinstance(link, dict):
            continue
        target = _resolve_soft_ven(world, link)
        if target and target != ven_id:
            try:
                world.add_wiki_link(ven_id, target)
            except Exception:  # noqa: BLE001
                pass

    ven = world.get_ven(ven_id)
    final_code = (ven.code if ven else None) or local_code or ""
    return ven_id, final_code, remap_note, True


def import_pack(
    world: Any,
    pack: dict[str, Any],
    *,
    target_world_label: str,
    place_instance_id: str | None = None,
) -> tuple[str, str, str | None, str | None]:
    """
    Import pack into *world*.

    Returns (ven_id, local_code, instance_id|None, remap_note).

    - prime pack: ensures prime; book template pages → unplaced catalog instance
    - instance pack: ensures prime; creates a new instance (into place if given
      and kind is not place)
    """
    pack_kind = str(
        pack.get("pack_kind")
        or (pack.get("provenance") or {}).get("pack_kind")
        or "prime"
    )
    ven_id, local_code, remap, created = _ensure_prime(
        world, pack, target_world_label=target_world_label
    )
    ven = world.get_ven(ven_id)
    kind = (ven.kind if ven else "other") or "other"

    if pack_kind != "instance":
        # Prime-only: optional template book pages if we just created the prime
        pages = pack.get("book_pages") or []
        inst_id = None
        if kind in ("folio", "book") and pages and created:
            inst_id = world.instantiate(ven_id)
            _apply_book_pages(world, inst_id, pages)
        return ven_id, local_code, inst_id, remap

    # Instance pack
    inst_data = pack.get("instance") or {}
    prov = pack.get("provenance") or {}
    origin_world = str(prov.get("origin_world") or "")
    home_ref = str(
        prov.get("home_instance_ref")
        or f"{local_code}-{inst_data.get('short_ref_digits') or '0001'}"
    ).strip()

    # Idempotent re-import: same origin instance key → reuse, do not duplicate
    existing_inst = world.find_instance_by_import_key(
        home_instance_ref=home_ref,
        origin_world=origin_world,
    )
    if existing_inst is not None:
        note = "already imported (same origin instance — skipped duplicate)"
        if remap:
            note = f"{remap}  ·  {note}"
        return ven_id, local_code, existing_inst.id, note

    name_ov = inst_data.get("name_override")
    desc_ov = inst_data.get("description_override")
    dig = digits_from_short_ref(str(inst_data.get("short_ref_digits") or "")) or None
    # Prefer home digits only if free for this prime; otherwise allocate next
    taken = world._short_ref_digits_taken(ven_id)  # noqa: SLF001
    if dig and dig in taken:
        dig = None

    loc = place_instance_id
    realm_id = timeline_id = None
    if loc:
        place = world.get_instance(loc)
        if place:
            realm_id = place.realm_instance_id
            timeline_id = place.timeline_instance_id

    state: dict[str, Any] = {
        "ie": {
            "home_instance_ref": home_ref,
            "home_code": str(prov.get("home_code") or local_code or ""),
            "origin_world": origin_world,
            "export_seq": prov.get("export_seq") or pack.get("seq"),
            "imported_into": target_world_label,
            "imported_at": datetime.now(timezone.utc).isoformat(),
            "pack_kind": "instance",
        }
    }
    if dig:
        state["short_ref"] = dig

    inst_id = world.instantiate(
        ven_id,
        name_override=name_ov if name_ov else None,
        description_override=desc_ov,
        realm_instance_id=realm_id,
        timeline_instance_id=timeline_id,
        state=state,
    )

    # Place free-standing; everything else into current place when available
    if kind != "place" and loc:
        from .world import default_inner_slot, is_inner_life_kind

        slot = default_inner_slot(kind) if is_inner_life_kind(kind) else "interior"
        world.put_in(inst_id, loc, slot=slot)

    for entry in inst_data.get("lore") or []:
        if not isinstance(entry, dict):
            continue
        body = entry.get("body") or ""
        if not str(body).strip():
            continue
        world.add_lore(
            "instance",
            inst_id,
            body=str(body),
            title=str(entry.get("title") or ""),
            when_label=entry.get("when_label"),
            author=str(entry.get("author") or "import"),
        )

    pages = inst_data.get("book_pages") or []
    if kind in ("folio", "book") and pages:
        _apply_book_pages(world, inst_id, pages)

    return ven_id, local_code, inst_id, remap


def _apply_book_pages(world: Any, inst_id: str, pages: list) -> None:
    for page in sorted(pages, key=lambda p: int((p or {}).get("position") or 0)):
        if not isinstance(page, dict):
            continue
        world.add_book_page(
            inst_id,
            str(page.get("title") or ""),
            str(page.get("body") or ""),
        )


def _resolve_soft_ven(world: Any, soft: dict[str, Any]) -> str | None:
    code = soft.get("code") or ""
    if code:
        v = world.get_ven_by_code(str(code))
        if v:
            return v.id
    slug = soft.get("slug") or ""
    if slug:
        v = world.find_ven(str(slug))
        if v:
            return v.id
    name = soft.get("name") or ""
    if name:
        v = world.find_ven(str(name))
        if v:
            return v.id
    return None


def find_pack(query: str, collector: Path | None = None) -> Path | None:
    """Resolve a pack by filename stem, code, or unique substring."""
    q = (query or "").strip()
    if not q:
        return None
    root = collector or ven_collector_dir()
    path = Path(q)
    if path.is_file():
        return path
    direct = root / q
    if direct.is_file():
        return direct
    if not q.lower().endswith(".ven"):
        direct = root / f"{q}.ven"
        if direct.is_file():
            return direct
    packs = list_packs(root)
    q_low = q.casefold()
    hits = [
        p
        for p in packs
        if q_low in p.path.name.casefold()
        or q_low == (p.code or "").casefold()
        or q_low in (p.slug or "").casefold()
        or q_low in (p.name or "").casefold()
        or q_low in (p.instance_title or "").casefold()
    ]
    if len(hits) == 1:
        return hits[0].path
    return None
