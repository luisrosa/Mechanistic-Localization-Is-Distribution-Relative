#!/usr/bin/env python3
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def files_under(path):
    return {
        p.relative_to(path).as_posix()
        for p in path.rglob("*")
        if p.is_file() and p.name != "main.pdf"
    }


def check_zip(directory, archive):
    expected = files_under(directory)
    with zipfile.ZipFile(archive) as zf:
        actual = {n.rstrip("/") for n in zf.namelist() if not n.endswith("/")}
    if expected != actual:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise SystemExit(f"zip manifest mismatch for {archive}: missing={missing}, extra={extra}")


def reject_private_dependencies(path):
    bad = ("mechanistic_interpretability", "mechanistic_localization_tmlr")
    for p in path.rglob("*"):
        if not p.is_file() or p.suffix not in {".tex", ".bib", ".md", ".py", ".sh"}:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for token in bad:
            if token in text:
                raise SystemExit(f"private development dependency {token!r} found in {p}")


def main():
    arxiv = ROOT / "arxiv"
    iclr = ROOT / "iclr2027"
    zips = ROOT / "submission-zips"
    required = [
        arxiv / "main.tex",
        arxiv / "references.bib",
        iclr / "main.tex",
        iclr / "references.bib",
        iclr / "iclr2027_conference.sty",
        iclr / "iclr2027_conference.bst",
        zips / "mldr_arxiv.zip",
        zips / "mldr_iclr2027.zip",
    ]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        raise SystemExit(f"missing package files: {missing}")

    reject_private_dependencies(arxiv)
    reject_private_dependencies(iclr)

    iclr_main = (iclr / "main.tex").read_text(encoding="utf-8")
    arxiv_main = (arxiv / "main.tex").read_text(encoding="utf-8")
    if "Anonymous authors" not in iclr_main:
        raise SystemExit("ICLR package is not anonymous")
    if "Luis F. Rosario Freytes" not in arxiv_main:
        raise SystemExit("arXiv package is not identified")

    check_zip(arxiv, zips / "mldr_arxiv.zip")
    check_zip(iclr, zips / "mldr_iclr2027.zip")
    print("submission packages: VERIFIED")


if __name__ == "__main__":
    main()
