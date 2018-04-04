import pytest
from click.testing import CliRunner
from flask.cli import ScriptInfo


class FlaskCliRunner(CliRunner):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

    def invoke(self, cli=None, args=None, **kwargs):
        if cli is None:
            cli = self.app.cli
        if 'obj' not in kwargs:
            kwargs['obj'] = ScriptInfo(create_app=lambda _: self.app)
        return super().invoke(cli, args, **kwargs)


@pytest.fixture()
def cli_runner(app):
    yield FlaskCliRunner(app)


@pytest.mark.skip(reason="doesn't do anything")
def test_cli(cli_runner):
    cli_runner.invoke(args=['test'])
    cli_runner.invoke(args=['seed-db'])
