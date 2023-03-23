import unittest
import warnings

import numpy as np
import pytest

import droneresponse_mathtools as mathtools


class TestNVector(unittest.TestCase):
    def test_to_pvector(self):
        nvec = mathtools.Nvector(0, 1, 0, 0)
        expected = mathtools.Pvector(0.0, 6.37813700E06, 0.0)
        actual = nvec.to_pvector()

        self.assertEqual(expected, actual)

    def test_to_lla(self):
        nvec = mathtools.Nvector(0, 1, 0, 0)
        expected = mathtools.Lla(0, 90, 0)
        actual = nvec.to_lla()

        self.assertEqual(expected, actual)

    def test_getters(self):
        nvec = mathtools.Nvector(0, 1, 1, -100)
        x = 0.0
        y = 1.0
        z = 1.0
        depth = -100.0

        self.assertEqual(x, nvec.get_x())
        self.assertEqual(x, nvec.x)

        self.assertEqual(y, nvec.get_y())
        self.assertEqual(y, nvec.y)

        self.assertEqual(z, nvec.get_z())
        self.assertEqual(z, nvec.z)

        self.assertEqual(depth, nvec.get_depth())
        self.assertEqual(depth, nvec.depth)

    def test_nvector_to_lla2(self):
        nvec = mathtools.Nvector(-0.42438554422796887, -0.667963499796372, 0.6113277948777666, -302.0)
        lla = nvec.to_lla()
        self.assertAlmostEqual(37.685573224035295, lla.lat, 1)
        self.assertAlmostEqual(-122.42952655042922, lla.lon, 1)
        self.assertAlmostEqual(302, lla.alt, 1)


class TestPVector(unittest.TestCase):
    def test_getters(self):
        pvec = mathtools.Pvector(0.0, 6.37813700E06, 0.0)
        x = 0.0
        y = 6.37813700E06
        z = 0.0

        self.assertEqual(x, pvec.get_x())
        self.assertEqual(x, pvec.x)

        self.assertEqual(y, pvec.get_y())
        self.assertEqual(y, pvec.y)

        self.assertEqual(z, pvec.get_z())
        self.assertEqual(z, pvec.z)

    def test_to_lla_for_warnings(self):

        pass


class TestLLA(unittest.TestCase):
    def test_getters(self):
        lla = mathtools.Lla(0, 90, 0)
        lat_deg = 0
        lon_deg = 90
        lat_rad = np.deg2rad(lat_deg)
        lon_rad = np.deg2rad(lon_deg)
        alt = 0

        self.assertEqual(lat_deg, lla.get_latitude())
        self.assertEqual(lat_deg, lla.latitude)
        self.assertEqual(lat_deg, lla.lat)

        self.assertEqual(lon_deg, lla.get_longitude())
        self.assertEqual(lon_deg, lla.longitude)
        self.assertEqual(lon_deg, lla.lon)

        self.assertEqual(alt, lla.get_altitude())
        self.assertEqual(alt, lla.altitude)
        self.assertEqual(alt, lla.alt)

        self.assertEqual(lat_rad, lla.get_latitude(as_rad=True))
        self.assertEqual(lon_rad, lla.get_longitude(as_rad=True))

    def test_round_trip(self):
        a = mathtools.Lla(41.71437875722079, -86.24183715080551, 220.7392)
        b = a.move_ned(100, 100, 100)
        n, e, d = b.distance_ned(a)

        self.assertAlmostEqual(n, -100, 2)
        self.assertAlmostEqual(e, -100, 2)
        self.assertAlmostEqual(d, -100, 2)

        a_actual = b.move_ned(-100, -100, -100)

        actual_lat, actual_lon, actual_alt = a_actual.lla
        a_lat, a_lon, a_alt = a.lla
        self.assertAlmostEqual(actual_lat, a_lat, 1)
        self.assertAlmostEqual(actual_lon, a_lon, 1)
        self.assertAlmostEqual(actual_alt, a_alt, 1)

    def test_north_moves_in_plus_lat_direction_northern_hemisphere(self):
        a = mathtools.Lla(41.71437875722079, -86.24183715080551, 220.7392)
        b = a.move_ned(100, 0, 0)
        self.assertGreater(b.lat, a.lat)

    def test_north_moves_in_plus_lat_direction_southern_hemisphere(self):
        a = mathtools.Lla(-41.71437875722079, -86.24183715080551, 220.7392)
        b = a.move_ned(100, 0, 0)
        self.assertGreater(b.lat, a.lat)

    def test_east_moves_in_plus_longitude_direction_northern_hemisphere(self):
        a = mathtools.Lla(41.71437875722079, -86.24183715080551, 220.7392)
        b = a.move_ned(0, 100, 0)
        self.assertGreater(b.lon, a.lon)

    def test_east_moves_in_plus_longitude_direction_southern_hemisphere(self):
        a = mathtools.Lla(-41.71437875722079, -86.24183715080551, 220.7392)
        b = a.move_ned(0, 100, 0)
        self.assertGreater(b.lon, a.lon)


class TestDistance(unittest.TestCase):
    def test_distance_1(self):
        a = mathtools.Lla(41.697987, -86.233922, 261.9)
        b = mathtools.Lla(41.698811, -86.233933, 261.9)

        expected = 91.44
        actual = a.distance(b)
        self.assertAlmostEqual(expected, actual, delta=0.25)

    def test_distance_2(self):
        a = mathtools.Lla(41.697987, -86.233922, 261.9).to_nvector()
        b = mathtools.Lla(41.698811, -86.233933, 261.9)

        expected = 91.44
        actual = a.distance(b)
        self.assertAlmostEqual(expected, actual, delta=0.25)

    def test_distance_3(self):
        a = mathtools.Lla(41.697987, -86.233922, 261.9).to_nvector()
        b = mathtools.Lla(41.698811, -86.233933, 261.9).to_pvector()

        expected = 91.44
        actual = a.distance(b)
        self.assertAlmostEqual(expected, actual, delta=0.25)


class TestGeoidHeight(unittest.TestCase):
    def test_the_case_that_caused_us_to_need_this_function_in_the_first_place(self):
        """
        In simulation the drone was sent to the target position but when it got there, it reported a
        position that was 47.2 meters too high. Here is the exact data:

                          LATITUDE           LONGITUDE          ALTITUDE
        current position: 47.3978429,        8.545869,          597.5515792976987
        target position:  47.39784293752265, 8.545869057172045, 550.3417375283871

        distance: 47.21 meters

        The difference in altitude accounted for all the distance. This test checks this posiiton.
        """
        expected_height = 47.2206
        actual_height = mathtools.geoid_height(47.3978429, 8.545869)
        self.assertAlmostEqual(expected_height, actual_height, places=3)

    def test_at_sim_landed_pos(self):
        """
        This test is noisy because the data was reported at different times.

        At time 1
        mavros/global_position/global reports:
            latitude: 47.3977504
            longitude: 8.5456074
            altitude: 535.321900855022

        At time 2
        /birdy0/mavros/altitude reports:
            monotonic: 487.572265625
            amsl: 488.1198425292969
            local: 0.01881488598883152
            relative: -0.1408376693725586
        """
        amsl = 488.1198425292969
        ellipsoid = 535.321900855022

        expected_height = ellipsoid - amsl
        actual_height = mathtools.geoid_height(47.3978429, 8.545869)

        self.assertAlmostEqual(expected_height, actual_height, places=1)


class TestWarnings(unittest.TestCase):
    def test_there_is_no_warning_when_going_to_or_from_lla_pvec_and_nvec(self):
        a = mathtools.Lla(41.71437875722079, -86.24183715080551, 220.7392)

        # b = a.move_ned(100, 100, 100)
        with warnings.catch_warnings(record=True) as record:
            a.to_pvector().to_lla()
            a.to_pvector().to_nvector()

            a.to_nvector().to_lla()
            a.to_nvector().to_pvector()

            a.to_lla().to_nvector()
            a.to_lla().to_pvector()

        for x in record:
            print(x)
        self.assertEqual(len(record), 0)
