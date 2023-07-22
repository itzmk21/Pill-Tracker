import config

class Notification:
    def __init__(self, title=' ', body=' ') -> None:
        """Initialises the title of the notification and body

        Args:
            title (str, optional): Can be anything the title should be. Defaults to ' '.
            body (str, optional): Can be anything the body should be. Defaults to ' '.
        """
        self.title: str = title
        self.body: str = body

    def phone(self) -> None:
        """Uses Pushbullet to send a message thus sending a notification to phone

        Raises:
            Exception: If the status code isn't 200 i.e successful then raises "Error" with the status code
        """
        from json import dumps
        from requests import post

        data = dumps({
            "type": "note",
            "title": self.title,
            "body": self.body
        })        

        resp = post('https://api.pushbullet.com/v2/pushes',
                    data=data,
                    headers={
                        "Authorization": "Bearer " + config.TOKEN,
                        "Content-Type": "application/json"
                    })
        if resp.status_code != 200:
            raise Exception('Error', resp.status_code)

    def win10(self) -> None:
        """Sends a toast notification and is only applicable if user is on Windows 10
        """
        from win10toast import ToastNotifier

        ToastNotifier().show_toast(self.title,
                                   self.body)
