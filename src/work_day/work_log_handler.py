# Save the list of dictionaries to a JSON file
import json
import os

import yaml


def write_log(workday):
    work_day_dir = os.path.dirname(os.path.abspath(__file__))
    worklog_path = os.path.join(work_day_dir, "log", "worklog.json")

    with open(worklog_path, "w") as json_file:

        json.dump({"worklog": workday}, json_file, default=str, indent=2)


def write_asciidoc(asciidoc_content):
    with open("worklog.adoc", "w") as worklog_asciidoc:
        worklog_asciidoc.write(asciidoc_content)


def read_log():

    work_day_dir = os.path.dirname(os.path.abspath(__file__))
    worklog_path = os.path.join(work_day_dir, "log", "worklog.json")

    with open(worklog_path, "r") as json_file:
        data = json.load(json_file)
        worklog = data.get("worklog")

    return worklog


def read_defaults():

    work_day_dir = os.path.dirname(os.path.abspath(__file__))
    settings_path = os.path.join(work_day_dir, "config", "workday_settings.yml")

    with open(settings_path, "r") as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


def create_log():

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the relative path to the log file
    log_file_path = os.path.join(script_dir, "log", "worklog.log")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
