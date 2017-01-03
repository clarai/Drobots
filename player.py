#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-

import math
import sys
import Ice

Ice.loadSlice('drobots.ice')
from drobots import (
    GameInProgress, GamePrx, Player, PlayerPrx, Point, RobotPrx,
    RobotController, RobotControllerPrx)


class ControllerI(RobotController):
    def __init__(self, robot, destination):
        self.robot = robot
        self.destination = destination
        self.current_drive = (0, 0)

    def __repr__(self):
        return "Controller for {0}".format(self.robot)

    def turn(self, current=None):
        pos = self.robot.location()

        print('ControllerI %s' % pos)

        relative_x = self.destination.x - pos.x
        relative_y = self.destination.y - pos.y

        distance = math.hypot(relative_x, relative_y)
        print('Distance to destination: %s' % distance)

        if relative_x == 0 and relative_y == 0:
            self.robot.drive(0, 0)
            return

        angle = int(math.degrees(math.atan2(relative_y, relative_x)) % 360.0)

        speed = 100

        if distance < 10:
            speed = max(min(100, self.robot.speed() / (10 - distance)), 1)

        if self.current_drive != (angle, speed):
            print('drive %s %s' % (angle, speed))
            self.robot.drive(angle, speed)
            self.current_drive = (angle, speed)

    def gameover(self, current=None):
        print('ControllerI.gameover')


class PlayerI(Player):
    def __init__(self, adapter):
        self.adapter = adapter

    def makeController(self, robot_prx, current=None):
        print('PlayerI.makeController')
        print('robot proxy: %s' % robot_prx)

        controller = ControllerI(robot_prx, Point(x=500, y=500))
        prx = self.adapter.addWithUUID(controller)

        return RobotControllerPrx.uncheckedCast(prx)

    def win(self, current=None):
        print('I win!!!!')
        current.adapter.getCommunicator().shutdown()

    def lose(self, current=None):
        print('I lose :-( !!!')
        current.adapter.getCommunicator().shutdown()

    def gameAbort(self, current=None):
        print('Game aborted. Exiting')
        current.adapter.getCommunicator().shutdown()


class PlayerApp(Ice.Application):
    def run(self, args):
        adapter = self.communicator().createObjectAdapter("PlayerAdapter")

        servant = PlayerI(adapter)
        player_prx = PlayerPrx.uncheckedCast(adapter.addWithUUID(servant))
        adapter.activate()

        game_prx = GamePrx.checkedCast(self.communicator().stringToProxy(
            args[1]))

        try:
            game_prx.login(player_prx, str('profesor'))

        except GameInProgress:
            print('Game in progress. Try again later')
            return 1

        self.shutdownOnInterrupt()
        self.communicator().waitForShutdown()

        return 0


if __name__ == '__main__':
    sys.exit(PlayerApp().main(sys.argv))
