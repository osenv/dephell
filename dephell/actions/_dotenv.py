import shlex
from codecs import decode
from pathlib import Path
from string import Template
from typing import Dict


def read_dotenv(path: Path, vars: Dict[str, str] = None) -> Dict[str, str]:
    if vars is None:
        vars = dict()
    else:
        vars = vars.copy()

    if path.is_dir():
        path = path / '.env'
    if not path.exists():
        return vars

    with path.open('r', encoding='utf-8') as stream:
        for line in stream:
            line = line.strip()
            if not line or line[0] == '#':
                continue
            key, value = line.split('=', 1)

            # clean key
            key = key.strip()
            if key.startswith('export '):
                key = key.replace('export ', '', 1)
                key = key.strip()
            if key[0] == '$':
                key = key[1:]

            # clean and substitute value
            value = ' '.join(shlex.split(value, comments=True))
            value = decode(value, 'unicode-escape')
            if '$' in value:
                value = value.replace(r'\$', '$$')  # escaping
                value = Template(value).safe_substitute(vars)

            vars[key] = value

    return vars
