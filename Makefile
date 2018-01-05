#!/usr/bin/make
# -*- mode:makefile -*-
SERVER=drobots2

all: factoriesContainer robotsContainer factory run

run:
	python Player.py --Ice.Config=player.config $(SERVER) AnCla1

secondPlayer:
	python Player.py --Ice.Config=player.config $(SERVER) AnCla2

factoriesContainer:
	gnome-terminal --tab -e "python Container.py --Ice.Config=container1.config"

robotsContainer:
	gnome-terminal --tab -e "python Container.py --Ice.Config=container2.config"

factory:
		gnome-terminal --tab -e "python Factory.py --Ice.Config=factory1.config"
		gnome-terminal --tab -e "python Factory.py --Ice.Config=factory2.config"
		gnome-terminal --tab -e "python Factory.py --Ice.Config=factory3.config"
