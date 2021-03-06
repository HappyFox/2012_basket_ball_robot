import unittest

import mock

import drive


def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    else:
        return([])


class TestDrive(unittest.TestCase):

    def setUp(self):
        self.robot_drive = mock.RobotDrive()

        self.joy = mock.JoyStick()
        self.photo_sensors = [ mock.PhotoSensor() for x in range(5)]
        self.hs_button = mock.Button()
        self.align_button = mock.Button()

        self.drive = drive.Drive(self.robot_drive, self.joy, self.photo_sensors,
                                 self.hs_button, self.align_button)

    def tearDown(self):
        pass

    def test_throttle(self):
        self.joy.x = 0.0

        # Sweep forward
        for y in seq(-1.0, 1.0, 0.1):
            self.joy.y = y

            self.drive.tick()

            self.assertEquals(self.robot_drive.speed, self.joy.y)
            self.assertEquals(self.robot_drive.rotation, self.joy.x)

        # Sweep back
        for y in seq(1.0, -1.0, -0.1):
            self.joy.y = y

            self.drive.tick()

            self.assertEquals(self.robot_drive.speed, self.joy.y)
            self.assertEquals(self.robot_drive.rotation, self.joy.x)

    def test_steering(self):
        self.joy.y = 0.0

        # Sweep forward
        for x in seq(-1.0, 1.0, 0.1):
            self.joy.x = x

            self.drive.tick()

            self.assertEquals(self.robot_drive.speed, self.joy.y)
            self.assertEquals(self.robot_drive.rotation, self.joy.x)

        # Sweep back
        for x in seq(1.0, -1.0, -0.1):
            self.joy.x = x

            self.drive.tick()

            self.assertEquals(self.robot_drive.speed, self.joy.y)
            self.assertEquals(self.robot_drive.rotation, self.joy.x)

    def test_half_speed_throttle(self):
        self.hs_button.pressed = True

        self.joy.x = 0.0

        # Sweep forward
        for y in seq(-1.0, 1.0, 0.1):
            self.joy.y = y

            self.drive.tick()

            self.assertEquals(self.robot_drive.speed, self.joy.y/2)
            self.assertEquals(self.robot_drive.rotation, self.joy.x)

        # Sweep back
        for y in seq(1.0, -1.0, -0.1):
            self.joy.y = y

            self.drive.tick()

            self.assertEquals(self.robot_drive.speed, self.joy.y/2)
            self.assertEquals(self.robot_drive.rotation, self.joy.x)

    def test_half_speed_steering(self):
        self.hs_button.pressed = True

        self.joy.y = 0.0

        # Sweep forward
        for x in seq(-1.0, 1.0, 0.1):
            self.joy.x = x

            self.drive.tick()

            self.assertEquals(self.robot_drive.speed, self.joy.y)
            self.assertEquals(self.robot_drive.rotation, self.joy.x/2)

        # Sweep back
        for x in seq(1.0, -1.0, -0.1):
            self.joy.x = x

            self.drive.tick()

            self.assertEquals(self.robot_drive.speed, self.joy.y)
            self.assertEquals(self.robot_drive.rotation, self.joy.x/2)

if __name__ == '__main__':
        unittest.main()
