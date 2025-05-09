"""Tasks for use with Invoke."""
import os
import sys
from invoke import task

try:
    import toml
except ImportError:
    sys.exit("Please make sure to `pip install toml` or enable the Poetry shell and run `poetry install`.")


def is_truthy(arg):
    """Convert "truthy" strings into Booleans.

    Examples:
        >>> is_truthy('yes')
        True
    Args:
        arg (str): Truthy string (True values are y, yes, t, true, on and 1; false values are n, no,
        f, false, off and 0. Raises ValueError if val is anything else.
    """
    if isinstance(arg, bool):
        return arg

    val = str(arg).lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    if val in ("n", "no", "f", "false", "off", "0"):
        return False
    raise ValueError(f"Invalid truthy value: `{arg}`")


PYPROJECT_CONFIG = toml.load("pyproject.toml")
TOOL_CONFIG = PYPROJECT_CONFIG["tool"]["poetry"]

# Can be set to a separate Python version to be used for launching or building image
PYTHON_VER = os.getenv("PYTHON_VER", "3.8")
# Name of the docker image/image
IMAGE_NAME = os.getenv("IMAGE_NAME", TOOL_CONFIG["name"])
# Tag for the image
IMAGE_VER = os.getenv("IMAGE_VER", f"{TOOL_CONFIG['version']}-py{PYTHON_VER}")
# Gather current working directory for Docker commands
PWD = os.getcwd()
# Local or Docker execution provide "local" to run locally without docker execution
INVOKE_LOCAL = is_truthy(os.getenv("INVOKE_LOCAL", False))  # pylint: disable=W1508


def run_cmd(context, exec_cmd, local=INVOKE_LOCAL):
    """Wrapper to run the invoke task commands.

    Args:
        context ([invoke.task]): Invoke task object.
        exec_cmd ([str]): Command to run.
        local (bool): Define as `True` to execute locally

    Returns:
        result (obj): Contains Invoke result from running task.
    """
    if is_truthy(local):
        print(f"LOCAL - Running command {exec_cmd}")
        result = context.run(exec_cmd, pty=True)
    else:
        print(f"DOCKER - Running command: {exec_cmd} container: {IMAGE_NAME}:{IMAGE_VER}")
        result = context.run(f"docker run -it -v {PWD}:/local {IMAGE_NAME}:{IMAGE_VER} sh -c '{exec_cmd}'", pty=True)

    return result


@task(
    help={
        "cache": "Whether to use Docker's cache when building images (default enabled)",
        "force_rm": "Always remove intermediate images",
        "hide": "Suppress output from Docker",
    }
)
def build(context, cache=True, force_rm=False, hide=False):
    """Build a Docker image."""
    print(f"Building image {IMAGE_NAME}:{IMAGE_VER}")
    command = f"docker build --tag {IMAGE_NAME}:{IMAGE_VER} --build-arg PYTHON_VER={PYTHON_VER} -f Dockerfile ."

    if not cache:
        command += " --no-cache"
    if force_rm:
        command += " --force-rm"

    result = context.run(command, hide=hide)
    if result.exited != 0:
        print(f"Failed to build image {IMAGE_NAME}:{IMAGE_VER}\nError: {result.stderr}")


@task
def clean(context):
    """Remove the project specific image."""
    print(f"Attempting to forcefully remove image {IMAGE_NAME}:{IMAGE_VER}")
    context.run(f"docker rmi {IMAGE_NAME}:{IMAGE_VER} --force")
    print(f"Successfully removed image {IMAGE_NAME}:{IMAGE_VER}")


@task
def rebuild(context):
    """Clean the Docker image and then rebuild without using cache."""
    clean(context)
    build(context, cache=False)


@task(help={"local": "Run locally or within the Docker container"})
def pytest(context, local=INVOKE_LOCAL):
    """Run pytest test cases."""
    exec_cmd = "pytest"
    run_cmd(context, exec_cmd, local)


@task(help={"local": "Run locally or within the Docker container"})
def black(context, path=".", local=INVOKE_LOCAL):
    """Run black to check that Python files adherence to black standards."""
    exec_cmd = f"black {path}"
    run_cmd(context, exec_cmd, local)


@task(help={"local": "Run locally or within the Docker container"})
def flake8(context, path=".", local=INVOKE_LOCAL):
    """Run flake8 code analysis."""
    exec_cmd = f"flake8 {path}"
    run_cmd(context, exec_cmd, local)


@task(help={"local": "Run locally or within the Docker container"})
def pylint(context, path=".", local=INVOKE_LOCAL):
    """Run pylint code analysis."""
    exec_cmd = f'find {path} -name "*.py" | xargs pylint'
    run_cmd(context, exec_cmd, local)


@task(help={"local": "Run locally or within the Docker container"})
def yamllint(context, path=".", local=INVOKE_LOCAL):
    """Run yamllint to validate formatting adheres to NTC defined YAML standards."""
    exec_cmd = f"yamllint {path}"
    run_cmd(context, exec_cmd, local)


@task(help={"local": "Run locally or within the Docker container"})
def pydocstyle(context, path=".", local=INVOKE_LOCAL):
    """Run pydocstyle to validate docstring formatting adheres to NTC defined standards."""
    exec_cmd = f"pydocstyle {path}"
    run_cmd(context, exec_cmd, local)


@task(help={"local": "Run locally or within the Docker container"})
def bandit(context, path=".", local=INVOKE_LOCAL):
    """Run bandit to validate basic static code security analysis."""
    exec_cmd = f"bandit --recursive ./{path} --configfile .bandit.yml"
    run_cmd(context, exec_cmd, local)


@task(help={"local": "Run locally or within the Docker container"})
def mypy(context, path=".", local=INVOKE_LOCAL):
    """Run mypy to validate type hinting."""
    exec_cmd = f"mypy {path}"
    run_cmd(context, exec_cmd, local)


@task
def cli(context):
    """Enter the image to perform troubleshooting or dev work."""
    dev = f"docker run -it -v {PWD}:/local {IMAGE_NAME}:{IMAGE_VER} /bin/bash"
    context.run(f"{dev}", pty=True)


@task(help={"local": "Run locally or within the Docker container"})
def tests(context, path=".", local=INVOKE_LOCAL):
    """Run all tests for this repository."""
    black(context, path, local)
    flake8(context, path, local)
    pylint(context, path, local)
    yamllint(context, path, local)
    pydocstyle(context, path, local)
    bandit(context, path, local)
    mypy(context, path, local)
    pytest(context, local)
    print("All tests have passed!")
