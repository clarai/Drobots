// -*- mode:c++ -*-

#include "drobots.ice"

module factory {
  interface RobotControllerFactory {
    ::drobots::RobotController* make(::drobots::Robot* robot_prx, int pid);
  };
  interface RobotControllerAttacker extends ::drobots::RobotController{
  	void location(::drobots::Point coordinates);
  	void objective(::drobots::Point coordinates);
  };
  interface RobotControllerDefender extends ::drobots::RobotController{
	void location(::drobots::Point coordinates);
  };
};
