class SrsranControllerException(Exception):
    """ Domain exception for srsran controller errors. """
    pass


class MissionIdNotFoundError(SrsranControllerException):
    """ Raise when a mission with a given id is missing from missions folder. """
    pass


class MissionAlreadyRunningError(SrsranControllerException):
    """ Raise when trying to launch a mission while another mission is running. """
    pass


class ScanAlreadyRunningError(SrsranControllerException):
    """ Raise when trying to launch a scan while another scan is running. """
    pass


class MissionIsNotRunningError(SrsranControllerException):
    """ Raise when trying to stop a mission while no mission is running. """
    pass
