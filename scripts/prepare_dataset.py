"""Verify the published files and restore the exact original JSONL bytes."""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def verify(path, spec):
    with path.open('rb') as f:
        actual = hashlib.file_digest(f, 'sha256').hexdigest()
    if path.stat().st_size != spec['bytes'] or actual != spec['sha256']:
        raise ValueError(f'Integrity check failed: {path}')

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'data')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    specs = manifest['files']
    source_gz = ROOT / 'data/cargo_dataset.jsonl.gz'
    source_drivers = ROOT / 'data/drivers.json'
    verify(source_gz, specs['data/cargo_dataset.jsonl.gz'])
    verify(source_drivers, specs['data/drivers.json'])
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    target = output / 'cargo_dataset.jsonl'
    if target.exists():
        verify(target, specs['data/cargo_dataset.jsonl'])
    else:
        temp = None
        try:
            with tempfile.NamedTemporaryFile(dir=output, prefix='.cargo-', delete=False) as out:
                temp = Path(out.name)
                with gzip.open(source_gz, 'rb') as inp:
                    shutil.copyfileobj(inp, out)
            verify(temp, specs['data/cargo_dataset.jsonl'])
            temp.replace(target)
        finally:
            if temp and temp.exists():
                temp.unlink()
    drivers = output / 'drivers.json'
    if drivers.exists():
        verify(drivers, specs['data/drivers.json'])
    elif drivers != source_drivers:
        shutil.copyfile(source_drivers, drivers)
    print(f'Verified: {target} (500000 cargo records)')
    print(f'Verified: {drivers} (10 driver records)')

if __name__ == '__main__':
    main()
