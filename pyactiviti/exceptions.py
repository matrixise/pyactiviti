class AlreadyExists(Exception):
    pass


class UserAlreadyExists(AlreadyExists):
    pass


class NotFound(Exception):
    pass


class GroupNotFound(NotFound):
    pass


class UserNotFound(NotFound):
    pass


class DeploymentNotFound(NotFound):
    pass


class BadQueryParameters(Exception):
    pass


class MissingID(Exception):
    pass


class GroupMissingID(MissingID):
    pass


class UserMissingID(MissingID):
    pass


class UpdatedSimultaneous(Exception):
    pass


class GroupUpdatedSimultaneous(UpdatedSimultaneous):
    pass


class UserUpdatedSimultaneous(UpdatedSimultaneous):
    pass


class UserAlreadyMember(Exception):
    pass