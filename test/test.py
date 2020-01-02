"""
Unit test of all command line interface
"""
import json
import logging
import pathlib
import shutil
import sys
import unittest
from unittest import mock

import yaml
from click.testing import CliRunner

p1, p2 = pathlib.Path.cwd(), pathlib.Path(__file__).parent.absolute().resolve()
if p1 != p2:
    print("bad path:\n", p1, "\n", p2)
    sys.exit(1)


cwd = pathlib.Path("./test_data")
cwd = cwd.absolute().resolve()
if cwd.exists():
    shutil.rmtree(str(cwd))
cwd.mkdir()
# logging.basicConfig(filename="./test_data/log.log", level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

SAMPLE_DATA = pathlib.Path("./data")
SAMPLE_DATA = SAMPLE_DATA.absolute().resolve()


sys.path.append("..")
import certmailer


certmailer.app = certmailer.FakeApp(cwd)
certmailer.main()


from certmailer import cli_jobs, cli_config, cli_edit_run


cli_config.base = certmailer.base
cli_jobs.jobs.base = certmailer.base
cli_edit_run.jobs.base = certmailer.base


def runner(command, data):
    r = CliRunner()
    result = r.invoke(command, data)
    logging.debug("\n>>>> " + " ".join(data))
    logging.debug(result.output)
    return result


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_00start(self):
        # self.assertEqual(certmailer.base.cache_basedir, cwd)
        self.assertEqual(certmailer.base.config_basedir, cwd)
        self.assertEqual(certmailer.base.data_basedir, cwd)
        self.assertTrue(SAMPLE_DATA.exists())

    def test_01config(self):
        cli = cli_config.cli
        result = runner(cli, ["config", "--api_key", "ff", "--secret_key", "EE"])
        self.assertEqual(result.exit_code, 2)
        result = runner(
            cli, ["config", "--api_key", "x" * 32, "--secret_key", "E" * 32]
        )
        self.assertEqual(result.exit_code, 2)
        result = runner(
            cli, ["config", "--api_key", "f" * 32, "--secret_key", "e" * 32]
        )
        self.assertEqual(result.exit_code, 0)
        from certmailer.jobs import jobs

        self.assertEqual(jobs.key_pair, ("f" * 32, "e" * 32))

    def test_02new_job(self):
        self.assertEqual(cli_jobs.jobs.base.data_basedir, cwd)
        result = runner(
            cli_jobs.cli,
            [
                "job",
                "new",
                "test_job",
                "-t",
                "MyNewJob",
                "-e",
                "sample@email.com",
                "-n",
                "John Doe",
                "-s",
                "Certification as attendee {name}",
                "-f",
                "2018-01-01",
                "-d",
                "2019-10-02",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        result = runner(cli_jobs.cli, ["job", "list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("test_job", result.output)
        result = runner(cli_jobs.cli, ["job", "use", "test_job"])
        for filename in SAMPLE_DATA.iterdir():
            if filename.is_file():
                dst = cli_jobs.jobs.current_job.path.joinpath(filename.name)
                shutil.copyfile(str(filename), str(dst))

    def test_03attach(self):
        to_attach = ["PIE.png", "LOGO.png", "sample_job invitation.pdf"]
        for filename in to_attach:
            cmd = [
                "attach",
                "add",
                str(SAMPLE_DATA.joinpath("attach").joinpath(filename)),
            ]
            result = runner(cli_jobs.cli, cmd)
            self.assertEqual(result.exit_code, 0)
        result = runner(cli_jobs.cli, ["attach", "list"])
        self.assertEqual(result.exit_code, 0)
        for filename in to_attach:
            self.assertIn(filename, result.output)

    def test_04data(self):
        result = runner(cli_jobs.cli, ["job", "use"])
        add_to_data = [
            "Activity-2019-05-28.yaml",
            "Attendee-2019-05-28.yaml",
            "Collaborator-2019-05-28.yaml",
            "Installer-2019-05-28.yaml",
        ]
        for filename in add_to_data:
            cmd = ["data", "add", str(SAMPLE_DATA.joinpath("data").joinpath(filename))]
            result = runner(cli_jobs.cli, cmd)
            self.assertEqual(result.exit_code, 0)
        result = runner(cli_jobs.cli, ["data", "list"])
        self.assertEqual(result.exit_code, 0)
        for filename in add_to_data:
            self.assertIn(filename, result.output)

    def test_06import(self):
        result = runner(cli_edit_run.cli, ["import"])
        self.assertEqual(result.exit_code, 0)
        result = runner(cli_jobs.cli, ["job", "use"])

    def test_07send(self):
        class Result:
            def __init__(self, status_code):
                self.status_code = status_code

            def json(self):
                return {"data": "my mock"}

        def mock_pdf(call_args):
            """Creates a fake pdf file for testing."""
            which = ["export-pdf=" in n for n in call_args].index(True)
            pdf_filename = call_args[which].split("=")[1]
            certificates_files.append(pdf_filename)
            with open(pdf_filename, "w") as fh:
                fh.write("something")

        # result = runner(cli_jobs.cli, ["job", "use"])
        # mock certg, I can't create pdf without inkscape
        with mock.patch("subprocess.check_call", new=mock_pdf) as mock_sp:
            certificates_files = []
            with mock.patch("mailjet_rest.client.api_call") as mock_mailjet:
                mock_mailjet.return_value = Result(200)
                result = runner(cli_edit_run.cli, ["send"])
                calls = [
                    yaml.safe_dump(json.loads(c[2]["data"]))
                    for c in mock_mailjet.mock_calls
                ]
                # logging.debug("\n\n\n API CALLS \n" + "\n___________\n".join(calls))

                self.assertEqual(result.exit_code, 0)
                for line in result.output:
                    if line.startswith("Total"):
                        how_many = max([int(w) for w in line.split()])
                        if "mails" in line:
                            self.assertEqual(len(calls), how_many)
                        if "certificates" in line:
                            self.assertEqual(len(certificates_files), how_many)


if __name__ == "__main__":
    unittest.main(verbosity=2)
