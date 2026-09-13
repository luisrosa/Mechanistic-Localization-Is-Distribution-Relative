#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
import tempfile
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
        raise SystemExit(
            f"zip manifest mismatch for {archive}: missing={missing}, extra={extra}"
        )


def reject_private_dependencies(path):
    bad = ("mechanistic_interpretability", "mechanistic_localization_tmlr")
    for p in path.rglob("*"):
        if not p.is_file() or p.suffix not in {".tex", ".bib", ".md", ".py", ".sh"}:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        for token in bad:
            if token in text:
                raise SystemExit(f"private development dependency {token!r} found in {p}")


def compare_shared_science(arxiv, iclr):
    shared_roots = ("sections", "appendices")
    for root in shared_roots:
        aroot = arxiv / root
        iroot = iclr / root
        afiles = files_under(aroot)
        ifiles = files_under(iroot)
        if afiles != ifiles:
            raise SystemExit(f"shared scientific file set drift in {root}")
        for rel in sorted(afiles):
            if (aroot / rel).read_bytes() != (iroot / rel).read_bytes():
                raise SystemExit(f"shared scientific source drift: {root}/{rel}")
    if (arxiv / "references.bib").read_bytes() != (iclr / "references.bib").read_bytes():
        raise SystemExit("bibliography drift between arXiv and ICLR packages")


def compile_extracted_zip(archive):
    if shutil.which("latexmk") is None:
        raise SystemExit("latexmk is required to verify standalone submission ZIPs")
    with tempfile.TemporaryDirectory(prefix="mldr_zip_") as td:
        td = Path(td)
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(td)
        proc = subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            cwd=td,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if proc.returncode != 0:
            tail = "\n".join(proc.stdout.splitlines()[-80:])
            raise SystemExit(f"standalone ZIP failed to compile: {archive}\n{tail}")
        if not (td / "main.pdf").exists():
            raise SystemExit(f"standalone ZIP did not produce main.pdf: {archive}")


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
    if "Luis F. Rosario Freytes" in iclr_main:
        raise SystemExit("author identity leaked into ICLR main source")
    if "Luis F. Rosario Freytes" not in arxiv_main:
        raise SystemExit("arXiv package is not identified")

    compare_shared_science(arxiv, iclr)
    check_zip(arxiv, zips / "mldr_arxiv.zip")
    check_zip(iclr, zips / "mldr_iclr2027.zip")

    compile_extracted_zip(zips / "mldr_arxiv.zip")
    compile_extracted_zip(zips / "mldr_iclr2027.zip")
    print("submission packages: VERIFIED AND STANDALONE")


if __name__ == "__main__":
    main()
