#!/usr/bin/env python3
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "releases" / "v1.0" / "SHA256SUMS.txt"


def digest(path: Path) -> str:
    h = sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    targets = [
        ROOT / "mechanistic_localization_is_distribution_relative.pdf",
        ROOT / "submission-zips" / "mldr_arxiv.zip",
        ROOT / "submission-zips" / "mldr_iclr2027.zip",
        ROOT / "source" / "arxiv_main.tex",
        ROOT / "source" / "iclr_main.tex",
        ROOT / "source" / "references.bib",
    ]
    targets += sorted((ROOT / "source" / "sections").glob("*.tex"))
    targets += sorted((ROOT / "source" / "appendices").glob("*.tex"))

    missing = [p for p in targets if not p.exists()]
    if missing:
        raise SystemExit("cannot hash missing release files: " + ", ".join(str(p) for p in missing))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{digest(p)}  {p.relative_to(ROOT).as_posix()}" for p in targets]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"release hashes: {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
