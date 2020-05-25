from pathlib import Path
import json
import logging
import shutil
import subprocess
import venv  # type: ignore
from cookiecutter.main import cookiecutter  # type: ignore


def set_up_venv_and_project(epath: Path, name: str, ccpath: Path):
    """Go to EPATH and set up the venv NAME
       TODO: check for PATH writabiilty and throw a suitable error if not writable.
             check for presense of git binary
             todo add optional argument to set up the git remote
       Set up the virtual environment
         upgrade pip immediately
       Run cookiecutter in the venv to lay out the project from the Best Ever Template (BET)
       Initialize a git repository for the project
       Install standard dependencies
    """
    ACTIVATE_AND_UPGRADE = (
        f"source {epath}/bin/activate && python -m pip install --upgrade pip"
    )
    INSTALL_STD_DEPENDS = f"source {epath}/bin/activate && python -m pip install -r ./etc/requirements.txt"
    v = venv.EnvBuilder(
        system_site_packages=False,
        clear=False,
        symlinks=False,
        upgrade=False,
        with_pip=True,
        prompt=None,
    )
    v.create(epath)  # make the environment
    subprocess.run(ACTIVATE_AND_UPGRADE, shell=True, cwd=epath)
    cookiecutter(str(ccpath) + "/", no_input=True, output_dir=epath)
    full_proj_path = Path(f"{epath}/{name}")  # TODO: fix path sep
    subprocess.run("git init", shell=True, cwd=full_proj_path)
    subprocess.run(INSTALL_STD_DEPENDS, shell=True, cwd=full_proj_path)
    return "Complete"

if __name__=='__main__':
    tdir='/home/osboxes/proj/'
    tenv='gmuform1'
    p = Path(tdir + tenv)
    ccpath="/home/osboxes/proj/BET/"
    cookiec_json = {
        "full_name": "Chris Smith",
        "email": "smitty1e@gmail.com",
        "project_name": tenv,
        "repo_name": tenv,
        "project_short_description": "System to manage the Form 1.",
        "release_date": "2020-05-23",
        "year": "2020",
        "version": "0.1",
    }
    try:
        shutil.rmtree(p)
    except FileNotFoundError:
        pass
    with open(ccpath + "cookiecutter.json", "w") as f:
        f.write(json.dumps(cookiec_json))

    set_up_venv_and_project(p, tenv, Path(ccpath))
