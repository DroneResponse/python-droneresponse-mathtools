import os

import numpy as np
import nvector as nv
from pygeodesy.geoids import GeoidPGM

__version__ = '0.3.0'

SEMI_MAJOR = np.float64(6378137.0)
SEMI_MINOR = np.float64(6356752.31)

NV_A = SEMI_MAJOR
NV_F = 1 - (SEMI_MINOR / SEMI_MAJOR)


_egm96_data_path = os.path.join(os.path.dirname(__file__), 'geoids', 'egm96-5.pgm')
_egm96 = GeoidPGM(_egm96_data_path, kind=-3)


class Position(object):
    def __getitem__(self, item):
        return self.as_array()[item]

    def as_array(self, flat=True):
        a = self._as_array()
        if not flat:
            a = a.reshape(-1, 1)

        return a

    # noinspection PyTypeChecker
    def distance(self, other):
        p1 = self.to_pvector().as_array()
        p2 = other.to_pvector().as_array()

        resid = p1 - p2
        resid_sq = resid ** 2
        resid_sum_sq = resid_sq.sum()
        dist = np.sqrt(resid_sum_sq)

        return dist

    def coerce(self, other):
        if isinstance(other, Position):
            if isinstance(self, Lla):
                return other.to_lla()
            elif isinstance(self, Nvector):
                return other.to_nvector()
            else:
                return other.to_pvector()
        else:
            return other

    def n_E2R_EN(self):
        n_E = self.to_nvector().get_xyz(shape=(3, 1))
        R_EN = nv.n_E2R_EN(n_E)

        return R_EN

    def move_ned(self, north, east, down):
        p_EA_E = self.to_pvector().get_xyz()

        R_NE = self.n_E2R_EN()
        p_delta_E = R_NE.dot([north, east, down])

        p_EA_E_delta = p_EA_E + p_delta_E

        return self.coerce(Pvector(*p_EA_E_delta))

    def distance_ned(self, other):
        R_NE = self.n_E2R_EN().T

        p_AB_E = other.to_pvector().as_array() - self.to_pvector().as_array()
        p_AB_N = R_NE.dot(p_AB_E)

        return p_AB_N

    def __repr__(self):
        return '{}'.format(','.join(self.as_array().astype(str)))

    def __str__(self):
        return repr(self)

    # noinspection PyTypeChecker
    def __eq__(self, other):
        other_ = self.coerce(other)
        if isinstance(other_, self.__class__):
            return np.isclose(self.as_array(), other_.as_array()).all()
        return False

    def to_lla(self):
        raise NotImplementedError

    def to_nvector(self):
        raise NotImplementedError

    def to_pvector(self):
        raise NotImplementedError

    def _as_array(self):
        raise NotImplementedError


class Lla(Position):
    def __init__(self, latitude, longitude, altitude):
        self.lla = np.array([latitude, longitude, altitude], dtype=np.float64)

    def get_latitude(self, as_rad=False):
        lat = self.lla[0]
        if as_rad:
            lat = np.deg2rad(lat)

        return lat

    def get_longitude(self, as_rad=False):
        lon = self.lla[1]
        if as_rad:
            lon = np.deg2rad(lon)

        return lon

    def get_altitude(self):
        return self.lla[-1]

    latitude = property(get_latitude)
    lat = property(get_latitude)
    longitude = property(get_longitude)
    lon = property(get_longitude)
    altitude = property(get_altitude)
    alt = property(get_altitude)

    def to_nvector(self):
        lat = self.get_latitude(as_rad=True)
        lon = self.get_longitude(as_rad=True)
        alt = self.get_altitude()
        n_EB_E = nv.lat_lon2n_E(lat, lon)
        x, y, z = n_EB_E.ravel()

        return Nvector(x, y, z, -alt)

    def to_pvector(self):
        return self.to_nvector().to_pvector()

    def to_lla(self):
        return self

    def _as_array(self):
        return self.lla


class Nvector(Position):
    def __init__(self, x, y, z, depth):
        self.n_EB_E = np.array([x, y, z], dtype=np.float64).reshape(-1, 1)
        self._depth = depth

    def get_x(self):
        return self.n_EB_E[0, 0]

    def get_y(self):
        return self.n_EB_E[1, 0]

    def get_z(self):
        return self.n_EB_E[2, 0]

    def get_xyz(self, shape=(3,)):
        return self.n_EB_E.ravel().reshape(shape)

    def get_depth(self):
        return self._depth

    x = property(get_x)
    y = property(get_y)
    z = property(get_z)
    xyz = property(get_xyz)
    depth = property(get_depth)

    def to_nvector(self):
        return self

    def to_pvector(self):
        x, y, z = nv.n_EB_E2p_EB_E(
            self.n_EB_E, depth=self.depth, a=NV_A, f=NV_F).ravel()

        return Pvector(x, y, z)

    def to_lla(self):
        lat, lon = np.ravel(nv.n_E2lat_lon(self.n_EB_E))

        return Lla(np.rad2deg(lat), np.rad2deg(lon), -self.depth)

    def _as_array(self):
        x, y, z = self.n_EB_E.ravel()
        return np.array([x, y, z, self.depth])


class Pvector(Position):
    def __init__(self, x, y, z):
        self.p_EB_E = np.array([x, y, z], dtype=np.float64).reshape(-1, 1)

    def __sub__(self, other):
        return self.p_EB_E.ravel() - other.p_EB_E.ravel()

    def get_x(self):
        return self.p_EB_E[0, 0]

    def get_y(self):
        return self.p_EB_E[1, 0]

    def get_z(self):
        return self.p_EB_E[2, 0]

    def get_xyz(self, shape=(3,)):
        xyz = self.p_EB_E.ravel().reshape(shape)
        return xyz

    x = property(get_x)
    y = property(get_y)
    z = property(get_z)
    xyz = property(get_xyz)

    def to_nvector(self):
        n_EB_E, depth = nv.p_EB_E2n_EB_E(self.p_EB_E, a=NV_A, f=NV_F)
        n_EB_E = n_EB_E.ravel()
        depth = depth[0]

        x = n_EB_E[0]
        y = n_EB_E[1]
        z = n_EB_E[2]

        return Nvector(x, y, z, depth)

    def to_pvector(self):
        return self

    def to_lla(self):
        return self.to_nvector().to_lla()

    def _as_array(self):
        return self.p_EB_E.ravel()


def mean_position(positions):
    nvecs = np.array([pos.to_nvector().as_array() for pos in positions]).T
    n_EM_E = nv.mean_horizontal_position(nvecs[:-1, :]).ravel()
    m_Z = np.mean(nvecs[-1, :])

    return positions[0].coerce(Nvector(n_EM_E[0], n_EM_E[1], n_EM_E[2], m_Z))


def geoid_height(lat, lon):
    """Calculates AMSL to ellipsoid conversion offset.
    Uses EGM96 data with 5' grid and cubic interpolation.

    The value returned can help you convert from meters above mean sea level (AMSL) to meters above
    the WGS84 ellipsoid.

    If you want to go from AMSL to ellipsoid height, add the value.
    And to go from ellipsoid height to AMSL, subtract this value.
    """
    return _egm96.height(lat, lon)
