from pathlib import Path


def yaml2dict(pod_f: Path) -> dict:
    """
    Read YAML front matter and convert it into a dict.

    Parameters
    ----------
    pod_f : Path
        Path to the file with yaml front matter.

    Returns
    -------
    dict
        Dict made from the YAML front matter.
    """
    yaml_dict = {}
    with open(pod_f, "r") as f:
        lines = [i.strip() for i in f.readlines() if i.strip()][1:-1]

    for line in lines:
        line_split = line.split(":", 1)
        yaml_dict[line_split[0].strip()] = line_split[1].strip()

    return yaml_dict


def dict2yaml(yaml_dict: dict) -> str:
    """
    Convert the YAML dict into the YAML front matter string.

    Parameters
    ----------
    yaml_dict : dict
        Dict made from the YAML front matter.

    Returns
    -------
    str
        YAML front matter into string.
    """
    yaml_text = "---\n"
    for i in yaml_dict:
        line = f"{i}: {yaml_dict[i]}"
        yaml_text += f"{line.strip()}\n"
    yaml_text += "---\n"
    return yaml_text


def write_yaml(filepath: Path, yaml: str) -> None:
    """
    Write the YAML front matter string to the provided file.

    Parameters
    ----------
    filepath : Path
    yaml : str
        YAML front matter string
    """
    with open(filepath, "w") as f:
        f.write(yaml)
