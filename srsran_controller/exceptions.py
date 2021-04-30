class SrsranControllerException(Exception):
    """ Domain exception for srsran controller errors. """
    pass


class MissionIdNotFoundError(SrsranControllerException):
    """ Raise when a mission with a given id is missing from missions folder. """
    pass


class MissionAlreadyRunningError(SrsranControllerException):
    """ Raise when trying to launch a mission while another mission is running. """
    pass
