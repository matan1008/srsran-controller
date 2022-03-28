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


class ScanIsNotRunningError(SrsranControllerException):
    """ Raise when trying to stop a scan while no scan is running. """
    pass


class ScanInterruptedError(SrsranControllerException):
    """ Raise when scan is interrupted. """
    pass


class EntityControlError(SrsranControllerException):
    """ Raise when a control command fails. """
    pass


class UnknownScriptError(SrsranControllerException):
    """ Raise when trying to get script class of an unknown script. """
    pass
