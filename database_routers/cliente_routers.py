#Router encargado de especificar que migraciones de los modelos corresponden
#a la base de datos presuweb

class cliente_router:
    router_app_labels = {'cliente'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.router_app_labels:
            return 'clientes_presupuesto'
        return None

    #def db_for_write(self, model, **hints):
    #    if model._meta.app_label in self.router_app_labels:
    #        return 'clientes_presupuesto'
    #    return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
                obj1._meta.app_label in self.router_app_labels or
                obj2._meta.app_label in self.router_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.router_app_labels:
            return db == 'clientes_presupuesto'
        return None