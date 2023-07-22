class FormattedSeconds:
    """Formats seconds to a more readable time stamp
            E.g: 1 day 1 hour 4 minutes 20 seconds
    """

    def __init__(self, seconds_) -> None:
        """Initialises the calculations for each time scale (day, hour etc.)

        Args:
            seconds_ (float): Seconds
        """
        self.raw_seconds = seconds_
        self.seconds = seconds_

        self.day: int = int(divmod(self.seconds, 24 * 3600)[0])
        self.seconds: int = divmod(self.seconds, 24 * 3600)[1]
        self.hour: int = int(divmod(self.seconds, 3600)[0])
        self.seconds: int = divmod(self.seconds, 3600)[1]
        self.minute: int = int(divmod(self.seconds, 60)[0])
        self.seconds: int = int(divmod(self.seconds, 60)[1])

        # divmod() is used because it's faster

    @staticmethod
    def get_suffix(time_frame, word) -> str:
        """Checks if the time frame's value is singular (1) to change the suffix of the time frame
                E.g: if it's 1 day, then it doesn't return 1 days, rather 1 day

        Args:
            time_frame (int): i.e: `5` days
            word (str): The word accompanying the time frame i.e day, hour etc.

        Returns:
            str: The formatted phrase i.e 1 day, 5 minutes etc.
        """
        if time_frame == 0:
            return ''
        elif time_frame != 1:
            return f'{time_frame} {word}s '
        else:
            return f'{time_frame} {word} '

    def return_formatted_secs(self) -> str:
        """Actually returns the full sentence

        Returns:
            str: The full time stamp
        """
        days: str = FormattedSeconds.get_suffix(self.day, 'day')
        hours: str = FormattedSeconds.get_suffix(self.hour, 'hour')
        minutes: str = FormattedSeconds.get_suffix(self.minute, 'minute')
        seconds: str = FormattedSeconds.get_suffix(self.seconds, 'second')

        if self.raw_seconds < 1:
            return f'{round(self.raw_seconds, 2)} seconds'
            # If the float value is less than 1, it normally returns "" instead of "0" so if statement is needed to amend that
        else:
            return f'{days}{hours}{minutes}{seconds}'.strip()
            # Strips because of blank spaces whenever values are 0
