class SrslteControllerException(Exception):
    """ Domain exception for srslte controller errors. """
    pass


class MissionIdNotFoundError(SrslteControllerException):
    """ Raise when a mission with a given id is missing from missions folder. """
