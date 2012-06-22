# -*- coding: utf-8 -*-


import kobo.client
import pyfaf

class Pull_Tags(kobo.client.ClientCommand):
    """Pulls tags for given operating system"""
    enabled = True
    admin = False # admin type account required

    def options(self):
        # specify command usage
        # normalized name contains a lower-case class name with underscores converted to dashes
        self.parser.usage = "%%prog %s [options] <args>" % self.normalized_name

        # specify command options as in optparse.OptionParser
        """
        self.parser.add_option(
            "--long-option",
            default=None,
            action="store",
            help=""
        )
        """

    def run(self, *args, **kwargs):
        # load from config file
        config_username = None
        config_password = None
        try:
            if self.container.conf["AUTH_METHOD"] == "password":
                config_username = self.container.conf["USERNAME"]
                config_password = self.container.conf["PASSWORD"]
        except (AttributeError, KeyError, TypeError):
            pass

        # optparser output is passed via *args (args) and **kwargs (opts)
        username = kwargs.pop("username", None)
        password = kwargs.pop("password", None)

        # None is not taken from the default in kwargs.pop
        # but it's the actual value of kwargs["username"]
        if username is None:
            username = config_username
        # same here
        if password is None:
            password = config_password

        if len(args) != 1:
            self.parser.error("You must specify an operating system")

        # login to the hub
        self.set_hub(username, password)
        kwargs = {
            "owner_name": username,
            "label": "Pull tags for {0}".format(args[0]),
            "method": "PullTags",
            "args": {
                "os": args[0],
            },
            "weight": 0,
            "arch_name": "noarch",
            "channel_name": "default",
        }

        self.hub.client.create_task(kwargs)
