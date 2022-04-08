from sqlalchemy.exc import IntegrityError

from photoric import db


# Photoric base model class provides common properties
# and methods
class PhotoricMixin():

    @classmethod
    def get_by_id(cls, id=None):
        if id is None:
            return False
        try:
            instance = cls.query.get(id)
        except IntegrityError:
            return False
        return instance

    @classmethod
    def get_by_name(cls, name=None):
        if name is None:
            return False
        instance = cls.query.filter_by(name=name).first()
        if instance:
            return instance
        return False

    @classmethod
    def create_from_json(cls, data):

        # check if object with such name already exists
        if cls.get_by_name(name=data["name"]):
            msg = "%s with such name already exists." % cls.__name__
            return {"message": msg}, 400
            
        obj = cls()
        for key, value in data.items():
            setattr(obj, key, value)

        db.session.add(obj)
        db.session.commit()

        return cls.get_by_name(obj.name)

    @classmethod
    def update_from_json(cls, data, id):

	    # check if requested object exists
        obj = cls.get_by_id(id=id)
        if not object:
            msg = "%s was not found" % cls.__name__
            return {"message": msg}, 404
            
        if "name" in data and data["name"] != obj.name and cls.get_by_name(name=data["name"]):
            return {"message": "This name is already in use. Please use a different name."}, 400
        
        for key, value in data.items():
            setattr(obj, key, value)	
        db.session.commit()

        return obj

    @classmethod
    def delete(cls, id=None):
        if id is None:
            return False
        instance = cls.query.get(id)
        if not instance:
            return False
        db.session.delete(instance)
        db.session.commit()
        return True
        
    def _build_relationship(self, rel, data, rel_cls, create=False):
        missed = []
        for item in data:
            existing_item = rel_cls.get_by_name(name=item["name"])
            if existing_item:
                getattr(self, rel).append(existing_item)
            elif create:
                new_item = rel_cls.create_from_json(item)
                getattr(self, rel).append(new_item)
            else:
                missed.append(item["name"])
        return missed