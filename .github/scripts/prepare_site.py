"""Stage only explicitly public assets; run from the repository root."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
PUBLIC = (
    'index.html', '404.html', 'sitemap.xml',
    'privacy/index.html', 'contact/index.html',
    'aramtermeles/index.html', 'paks/index.html', 'import-export/index.html',
    'assets/styles.css', 'assets/favicon.svg', 'assets/social-card.png',
    'assets/app-overview.png', 'assets/app-mix.png', 'assets/app-solar.png',
)

def prepare(destination):
    destination = Path(destination).resolve()
    if destination == ROOT or not destination.is_relative_to(ROOT):
        raise ValueError('Destination must be a dedicated directory inside the repository')
    if destination.exists():
        raise FileExistsError('Use a fresh staging directory to prevent stale files')
    for name in PUBLIC:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    print(f'Staged {len(PUBLIC)} public files in {destination.name}')

if __name__ == '__main__':
    import sys
    prepare(sys.argv[1] if len(sys.argv) > 1 else ROOT / '_site')
