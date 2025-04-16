from datetime import datetime


class WorkDay:
    def __init__(
        self,
        start: datetime,
        stop: datetime,
        breaks=1,
        working_hours=8,
        flex=0,
        comments=None,
    ):
        self._start = datetime.strftime(start, "%Y-%m-%d %H:%M")
        self._stop = datetime.strftime(stop, "%Y-%m-%d %H:%M")
        self._breaks = breaks
        self._working_hours = working_hours
        self._flex = flex
        self._comments = comments

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    @property
    def breaks(self):
        return self._breaks

    @property
    def working_hours(self):
        return self._working_hours

    @property
    def flex(self):
        return self._flex

    @property
    def comments(self):
        return self._comments

    @start.setter
    def start(self, value):
        self._start = value

    @stop.setter
    def stop(self, value):
        self._stop = value

    @breaks.setter
    def breaks(self, value):
        self._breaks = value

    @working_hours.setter
    def working_hours(self, value):
        self._working_hours = value

    @flex.setter
    def flex(self, value):
        self._flex = value

    @comments.setter
    def comments(self, value):
        self._comments = value

    @classmethod
    def from_dict(cls, input_dict):
        start_datetime = datetime.strptime(input_dict["_start"], "%Y-%m-%d %H:%M")
        stop_datetime = datetime.strptime(input_dict["_stop"], "%Y-%m-%d %H:%M")

        return cls(
            start=start_datetime,
            stop=stop_datetime,
            breaks=input_dict["_breaks"],
            working_hours=input_dict["_working_hours"],
            flex=input_dict["_flex"],
            comments=input_dict["_comments"],
        )

    def __str__(self):
        return f"WorkDay(start={self.start}, stop={self.stop}, breaks={self.breaks}, working_hours={self.working_hours}, flex={self.flex}, comments={self.comments})"
