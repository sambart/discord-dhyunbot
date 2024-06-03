
class Cog(CogMixin, DPYCog, metaclass=DPYCogMeta):
    """
    Red's Cog base class

    This includes a metaclass from discord.py

    .. warning::

        None of your methods should start with ``red_`` or
        be dunder names which start with red (eg. ``__red_test_thing__``)
        unless to override behavior in a method designed to be overridden,
        as this prefix is reserved for future methods in order to be
        able to add features non-breakingly.

        Attributes and methods must remain compatible
        with discord.py and with any of red's methods and attributes.

    """

    __cog_commands__: Tuple[Command]

    @property
    def all_commands(self) -> Dict[str, Command]:
        """
        This does not have identical behavior to
        Group.all_commands but should return what you expect

        :meta private:
        """
        return {cmd.name: cmd for cmd in self.__cog_commands__}

