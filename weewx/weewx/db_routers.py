from stationregistry import models


class DBRouter(object):
    """
    Determine how to route database calls for an app's models (in this case, for an app named Example).
    All other models will be routed to the next router in the DATABASE_ROUTERS setting if applicable,
    or otherwise to the default database.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'old_db':
            return 'old_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'default':
            return 'default'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that the weewx station registry models get created on the right database."""
        if app_label == 'default':
            return db == 'default'
        elif db == 'old_db':
            # Ensure that the old database models do not migrate.
            return False

        # No opinion for all other scenarios
        return None
