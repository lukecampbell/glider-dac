import os

from glider_mission import db
from datetime import datetime
from flask.ext.mongokit import Document
from bson.objectid import ObjectId

@db.register
class Mission(Document):
    __collection__ = 'missions'
    use_dot_notation = True
    use_schemaless = True

    structure = {
        'name'                      : unicode,
        'user_id'                   : ObjectId,
        'mission_dir'               : unicode,
        'estimated_deploy_date'     : datetime,
        'estimated_deploy_location' : unicode,  # WKT text
        'wmo_id'                    : unicode,
        'completed'                 : bool,
        'created'                   : datetime,
        'updated'                   : datetime
    }

    default_values = {
        'created': datetime.utcnow,
        'completed': False
    }

    def sync(self):
        if not os.path.exists(self.mission_dir):
            os.makedirs(self.mission_dir)

        # Keep the WMO file updated if it is edited via the web form
        if self.wmo_id is not None and self.wmo_id != "":
            wmo_id_file = os.path.join(self.mission_dir, "wmoid.txt")
            with open(wmo_id_file, 'w') as f:
                f.write(self.wmo_id)
   
        # Save a file called "completed.txt" to tell TDS server it is completed
        completed_file = os.path.join(self.mission_dir, "completed.txt")
        if self.completed is True:
            with open(completed_file, 'w') as f:
                f.write(" ")
        else:
            try:
                os.remove(completed_file)
            except BaseException:
                pass

