import json
from pathlib import Path
import shutil
from typing import *
import pytest  # type: ignore
from pinit.pinit import set_up_venv_and_project  # type: ignore


@pytest.fixture
def tdir() -> str:
    return "/tmp/"


@pytest.fixture
def tenv() -> str:
    return "test_pinit_test"


@pytest.fixture
def ccpath() -> str:
    return "/home/osboxes/proj/BET/"


@pytest.fixture
def cookiec_json(tenv) -> Dict:
    return {
        "full_name": "Chris Smith",
        "email": "smitty1e@gmail.com",
        "project_name": tenv,
        "repo_name": tenv,
        "project_short_description": "Refreshingly simple static site generator.",
        "release_date": "2020-05-23",
        "year": "2020",
        "version": "0.1",
    }


def test_set_up_venv_and_project(tdir: str, tenv: str, ccpath: str, cookiec_json: Dict):
    # blow away previous tests
    p = Path(tdir + tenv)
    try:
        shutil.rmtree(p)
    except FileNotFoundError:
        pass

    # stage cookiecutter.json
    with open(ccpath + "cookiecutter.json", "w") as f:
        f.write(json.dumps(cookiec_json))

    assert set_up_venv_and_project(p, tenv, Path(ccpath)) = "Complete"
