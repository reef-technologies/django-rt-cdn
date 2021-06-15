# type: ignore
import nox


PYTHON_VERSION = '3.8'
PY_PATHS = ['django_rt_cdn', 'tests', 'noxfile.py']

REQUIREMENT_SELF = '.[imagekit,ninja]'
REQUIREMENTS_FORMAT = ['black==20.8b1', 'isort==5.6.4', 'docformatter==1.3.1']
REQUIREMENTS_LINT = [*REQUIREMENTS_FORMAT, 'flake8==3.8.4']
REQUIREMENTS_TEST = ['Pillow', 'pytest==6.1.1', 'pytest-django==4.1.0']

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ['lint', 'test']


@nox.session(name='format', python=PYTHON_VERSION)
def format_(session):
    """Format the code."""
    session.install(*REQUIREMENTS_FORMAT)
    session.run('black', '-l', '100', '-t', 'py38', '-S', '--exclude=.*/migrations/.*', *PY_PATHS)
    session.run('isort', *PY_PATHS)
    session.run(
        'docformatter',
        '--in-place',
        '--recursive',
        '--wrap-summaries=100',
        '--wrap-descriptions=100',
        *PY_PATHS,
    )


@nox.session(python=PYTHON_VERSION)
def lint(session):
    """Run linters."""
    session.install('-e', REQUIREMENT_SELF, *REQUIREMENTS_LINT)
    session.run(
        'black',
        '-l',
        '100',
        '-t',
        'py38',
        '-S',
        '--exclude=.*/migrations/.*',
        '--check',
        *PY_PATHS,
    )
    session.run('isort', '--check', *PY_PATHS)
    session.run(
        'docformatter',
        '--check',
        '--recursive',
        '--wrap-summaries=100',
        '--wrap-descriptions=100',
        *PY_PATHS,
    )
    session.run('flake8', *PY_PATHS)


@nox.session(python=PYTHON_VERSION)
def test(session):
    """Run tests."""
    session.install('-e', REQUIREMENT_SELF, *REQUIREMENTS_TEST)
    session.run('pytest', *session.posargs)
