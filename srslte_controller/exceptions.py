class SrslteControllerException(Exception):
    """ Domain exception for srslte controller errors. """
    pass


class MissionIdNotFoundError(SrslteControllerException):
    """ Raise when a mission with a given id is missing from missions folder. """
    pass


class MissionAlreadyRunningError(SrslteControllerException):
    """ Raise when trying to launch a mission while another mission is running. """
    pass
