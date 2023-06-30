import uuid
from base import Shape

import config

class site(Shape):

    def __init__(self, zone_type, shape):

        super().__init__(shape)

        self._zone_type = zone_type
        self._reciever_connections = []
        self._sender_connections = []
        self._survival_time = 10
        self._id = uuid.uuid4()
        self._zone = None
        self._residents = []

        self.set_display_repr(config.SITE_BLOCK[self._zone_type.name])

    def set_zone(self, zone):
        self._zone = zone

    def get_id(self):
        return self._id

    def get_corner_coordinates(self):
        return self._object.exterior.coords[0]

    def get_coord_points(self):
        return list(self.iter_points())

    def get_zone_type(self):
        return self._zone_type

    def add_resident(self, resident):
        self._residents.append(resident)

    def add_receiver_connection(self, other):
        self._reciever_connections.append(other)

    def add_sender_connection(self, other):
        self._sender_connections.append(other)


