from numpy import sqrt, sin, cos, arctan2, array, cross, dot, ones
from numpy.linalg.linalg import norm
from scipy.interpolate import Rbf # Radial basis function interpolation.
from numpy.linalg import lstsq


def normalized_earth_radius(latitude_rad):
    wgs84_f = 1./298.257223563
    return 1.0/sqrt(cos(latitude_rad)**2 + ((1.0 - wgs84_f)**2)*(sin(latitude_rad)**2))

def geographic_from_xyz(xyz_m):
    r'''
    Compute lon, lat, and height
    '''
    wgs84_a = 6378137.0
    wgs84_f = 1./298.257223563
    wgs84_e2 = wgs84_f*(2.0 - wgs84_f)
    
    x_m, y_m, z_m = xyz_m
    lon_rad = arctan2(y_m, x_m)
    r_m = sqrt(x_m**2 + y_m**2)
    # Iterate to latitude solution
    phi_previous = 1e4
    phi = arctan2(z_m, r_m)
    while abs(phi -phi_previous) > 1.6e-12:
        phi_previous = phi
        phi = arctan2(z_m + wgs84_e2*wgs84_a*normalized_earth_radius(phi)*sin(phi),
                      r_m)
    lat_rad = phi
    height_m = r_m*cos(lat_rad) + z_m*sin(lat_rad) - wgs84_a*sqrt(1.0 - wgs84_e2*sin(lat_rad)**2)
    return {'lon_rad': lon_rad, 'lat_rad': lat_rad, 'height_m': height_m}

def normal_vector_ellipsoid(lon_rad, lat_rad):
    return array([cos(lat_rad)*cos(lon_rad),
                  cos(lat_rad)*sin(lon_rad),
                  sin(lat_rad)])

def normal_vector_meridian_plane(xyz_m):
    x_m, y_m, _ = xyz_m
    return array([y_m, -x_m, 0.0])/sqrt(x_m**2 + y_m**2)

def projection_matrix(xyz0_m, normal_vector):
    r_unit = normal_vector
    meridian_normal = normal_vector_meridian_plane(xyz0_m)
    q_unit = cross(meridian_normal, r_unit)
    q_unit /= norm(q_unit)
    p_unit = cross(q_unit, r_unit)
    p_unit /= norm(p_unit)
    return array([p_unit, q_unit, r_unit]).T

def transform(xyz_m, xyz0_m, mat):
    offsets = xyz_m  - xyz0_m
    return array([dot(mat, offset) for offset in offsets])

LOFAR_XYZ0_m = array([3826574.0, 461045.0, 5064894.5])
LOFAR_REF_MERIDIAN_NORMAL = normal_vector_meridian_plane(LOFAR_XYZ0_m)


def interpolation_function(pqr):
    '''
    Return an interpolation function fn(x, y, z), which returns the value at x, y.
    '''
    rbfi = Rbf(pqr[:,0], pqr[:,1], 0.0*pqr[:,2], pqr[:,2], function='linear')
    def interpolator(x_m, y_m):
        return rbfi(x_m, y_m, y_m*0.0)
    return interpolator


def fit_plane(xyz):
    # data_model z = ax +by +c
    # M colvec(a, b, c) = colvec(z)
    # M row i = (x_i, y_i, 1.0)
    mean_position = xyz.mean(axis=0)
    mat = array([xyz[:,0]- mean_position[0],
                 xyz[:,1]- mean_position[1],
                 ones(len(xyz[:,2]))]).T
    a, b, c = lstsq(mat, xyz[:,2] - mean_position[2])[0]
    normal_vector = array([-a, -b, 1.0])
    normal_vector /= norm(normal_vector)
    return {'mean': mean_position, 'normal': normal_vector}
