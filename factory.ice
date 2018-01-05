// -*- mode:c++ -*-

#include "drobots.ice"

module drobots {
  interface RobotControllerFactory {
    RobotController* make(Robot* robot, int identifier);
  };
};
