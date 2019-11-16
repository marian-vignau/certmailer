"""
Unit test of all command line interface
"""
import unittest
import logging
import shutil
import pathlib
import sys
from unittest import mock

from click.testing import CliRunner
import yaml
import json


sys.path.append("..")
import certmailer

cwd = pathlib.Path("./test_data")
cwd = cwd.absolute().resolve()
if cwd.exists():
    shutil.rmtree(str(cwd))
cwd.mkdir()
logging.basicConfig(filename='./test_data/log.log', level=logging.DEBUG)

SAMPLE_DATA = pathlib.Path("./data")
SAMPLE_DATA = SAMPLE_DATA.absolute().resolve()


class FakeApp(object):
    user_config_dir = str(cwd)
    user_cache_dir = str(cwd)
    user_data_dir = str(cwd)


certmailer.app = FakeApp()
certmailer.main(certmailer.app)


from certmailer import cli_config
from certmailer import cli_jobs
from certmailer import cli_edit_run


cli_config.base = certmailer.base
cli_jobs.jobs.base = certmailer.base
cli_edit_run.jobs.base = certmailer.base


def runner(command, data):
    r = CliRunner()
    result = r.invoke(command, data)
    logging.debug("\n>>>> " + ' '.join(data))
    logging.debug(result.output)
    return result


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_00start(self):
        self.assertEqual(certmailer.base.cache_basedir, cwd)
        self.assertEqual(certmailer.base.config_basedir, cwd)
        self.assertEqual(certmailer.base.data_basedir, cwd)
        self.assertTrue(SAMPLE_DATA.exists())

    def test_01config(self):
        cli = cli_config.cli
        result = runner(cli, ['config', "--api_key", "ff", "--secret_key", "EE"])
        self.assertEqual(result.exit_code, 2)
        result = runner(cli, ['config', "--api_key", "x" * 32, "--secret_key", "E" * 32])
        self.assertEqual(result.exit_code, 2)
        result = runner(cli, ['config', "--api_key", "f" * 32, "--secret_key", "e" * 32])
        self.assertEqual(result.exit_code, 0)

    def test_02new_job(self):
        self.assertEqual(cli_jobs.jobs.base.data_basedir, cwd)
        result = runner(cli_jobs.cli, ['job', "new", "test_job",
                                    "-t", "MyNewJob",
                                    "-e", "sample@email.com",
                                     "-n", "John Doe",
                                     "-s", "Certification as attendee {name}",
                                     "-f", "2018-01-01",
                                     "-d", "2019-10-02"])
        self.assertEqual(result.exit_code, 0)
        result = runner(cli_jobs.cli, ['job', "list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("test_job", result.output)
        result = runner(cli_jobs.cli, ['job', "use", "test_job"])
        for filename in SAMPLE_DATA.iterdir():
            if filename.is_file():
                dst = cli_jobs.jobs.current_job.path.joinpath(filename.name)
                shutil.copyfile(str(filename), str(dst))

    def test_03attach(self):
        to_attach = ["PIE.png", "LOGO.png", "sample_job invitation.pdf"]
        for filename in to_attach:
            cmd = ['attach', "add", str(SAMPLE_DATA.joinpath("attach").joinpath(filename))]
            result = runner(cli_jobs.cli, cmd)
            self.assertEqual(result.exit_code, 0)
        result = runner(cli_jobs.cli, ['attach', "list"])
        self.assertEqual(result.exit_code, 0)
        for filename in to_attach:
            self.assertIn(filename, result.output)

    def test_04data(self):
        add_to_data = ["Activity-2019-05-28.yaml",
                     "Attendee-2019-05-28.yaml",
                     "Collaborator-2019-05-28.yaml",
                     "Installer-2019-05-28.yaml"]
        for filename in add_to_data:
            cmd = ["data", "add", str(SAMPLE_DATA.joinpath("data").joinpath(filename))]
            result = runner(cli_jobs.cli, cmd)
            self.assertEqual(result.exit_code, 0)
        result = runner(cli_jobs.cli, ["data", "list"])
        self.assertEqual(result.exit_code, 0)
        for filename in add_to_data:
            self.assertIn(filename, result.output)

    def test_05template(self):
        result = runner(cli_edit_run.cli, ['do', "template"])
        self.assertEqual(result.exit_code, 0)

    def test_06makelist(self):
        result = runner(cli_edit_run.cli, ['do', "list"])
        self.assertEqual(result.exit_code, 0)

    def test_07generate_certificate(self):
        result = runner(cli_edit_run.cli, ['do', "certificates"])
        self.assertEqual(result.exit_code, 0)

    def test_08sendmails(self):
        class Result:
            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                return {"data": "my mock"}

        import certmailer.send_mails
        certmailer.send_mails.jobs = certmailer.jobs.Jobs()

        cli_jobs.jobs = certmailer.jobs.Jobs()
        with mock.patch("mailjet_rest.client.api_call") as mymock:
            mymock.return_value = Result(200)
            result = runner(cli_edit_run.cli, ['do', "send"])
            calls = [yaml.safe_dump(json.loads(c[2]["data"])) for c in mymock.mock_calls]
            logging.debug('\n\n\n API CALLS \n' + '\n___________\n'.join(calls))

            self.assertEqual(result.exit_code, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
