import argparse
import subprocess
import webbrowser
from datetime import date, datetime, timedelta

from jinja2 import Template
from work_log_handler import read_defaults, read_log, write_asciidoc, write_log

from work_day import WorkDay


def latest_workday():
    worklog: list = read_log()
    latest_workday: WorkDay = WorkDay.from_dict(worklog.pop())

    return latest_workday


def calc_working_hours(start: datetime, stop: datetime):
    delta = stop - start
    working_hours = round(delta.total_seconds() / 3600, 2)

    return working_hours


def calc_flex(working_hours, default_working_hours):
    flex = round(working_hours - default_working_hours, 2)
    return flex


def check_work_day():
    worklog: list = read_log()
    try:
        latest_workday = WorkDay.from_dict(worklog[-1])
    except IndexError:
        print("Index error")

    today = date.today()

    start_day = latest_workday.start[:-6]
    start_day_date = datetime.strptime(start_day, "%Y-%m-%d")

    if today.__eq__(start_day_date):
        print("Error: Start time for work day has already been logged.")

    return today.__eq__(start_day_date)


def start():
    start: datetime = datetime.now()
    stop: datetime = datetime.now() + timedelta(hours=8)

    default_values: dict = read_defaults()
    print(default_values)
    # workday_defaults = yaml_data.get("work_day", {})
    # print(workday_defaults)
    # print(yaml_data.defaults.breaks)
    breaks: int = (
        default_values.get("work_day", {}).get("defaults", {}).get("breaks", 1)
    )
    # working_hours = (yaml_data.get("work_day", {}).get("defaults", {}).get("working_hours", 8))
    # Default to 1 if 'breaks' key is missing
    # working_hours = workday_defaults.get("working_hours", 8)  # Default to 8 if 'working_hours' key is missing
    # print(workday_defaults.breaks)
    # print(workday_defaults.working_hours)

    working_hours = calc_working_hours(start, stop)

    work_day = WorkDay(
        start=start,
        stop=stop,
        breaks=breaks,
        working_hours=working_hours,
        flex=0,
        comments=[],
    )

    working_hours -= work_day.breaks

    worklog: dict = read_log()
    worklog.append(work_day.__dict__)

    print(f"Stop working at {work_day.stop}")
    # print(f"Stop working at {work_day.stop}" + breaks)

    write_log(worklog)


def stop():
    stop = datetime.now()
    stop_str = stop.strftime("%Y-%m-%d %H:%M")

    work_day: WorkDay = latest_workday()
    print(work_day)

    work_day.stop = stop_str
    start = datetime.strptime(work_day.start, "%Y-%m-%d %H:%M")

    working_hours = calc_working_hours(start, stop)

    working_hours -= work_day.breaks

    work_day.working_hours = working_hours

    default_values: dict = read_defaults()
    default_working_hours: int = (
        default_values.get("work_day", {}).get("defaults", {}).get("working_hours", 8)
    )
    work_day.flex = calc_flex(
        working_hours=working_hours, default_working_hours=default_working_hours
    )
    print(work_day)
    worklog: dict = read_log()
    worklog[-1] = work_day.__dict__

    write_log(worklog)


def add_comment(comment: str):

    work_day = latest_workday()
    comment: list = comment.split(",")
    comments: list = work_day.comments

    for com in comment:
        comments.append(com)

    work_day.comments = comments

    worklog: dict = read_log()
    worklog[-1] = work_day.__dict__
    write_log(worklog)


def print_work_log():
    template_str = """
.Work Day table
[%autowidth]
|===
| Start Time | Stop Time | Breaks | Working Hours | Flex | Comments

{% for entry in worklog %}
| {{ entry._start }} | {{ entry._stop }} | {{ entry._breaks }} | {{ entry._working_hours }} | {{ entry._flex }} | \n\n&bull; {% if entry._comments %}{{ entry._comments | join("\n\n&bull; ") }}{% endif %}
{% endfor %}
|===
"""
    worklog_data = read_log()

    template = Template(template_str)

    # Render the template with the data
    result = template.render(worklog=worklog_data)
    write_asciidoc(result)
    asciidoc_html()


def asciidoc_html():
    # Define the command you want to run
    command = "asciidoctor worklog.adoc"

    # Run the command
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Wait for the command to finish and get the output
    output, error = process.communicate()

    # Check if there was an error
    if error:
        print("Error:", error.decode())
    else:
        # Print the output
        webbrowser.open("worklog.html", 1)


def commands(parser: argparse.ArgumentParser):
    parser.add_argument("action", choices=["start", "stop", "update", "print"])
    parser.add_argument("-c", "--comment")
    parser.add_argument("-b", "--breaks")

    args = parser.parse_args()

    if args.action == "start" and not check_work_day():
        start()
    elif args.action == "stop":
        stop()
    elif args.action == "update":
        add_comment(args.comment)
    elif args.action == "print":
        print_work_log()


def main():
    parser = argparse.ArgumentParser(
        prog="Work Day",
        description="Logs times and activites during a work day.",
        epilog="Work Day at your service",
    )

    commands(parser)


if __name__ == "__main__":
    main()
