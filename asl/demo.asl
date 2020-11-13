/**
 * @author	Patrick Gavigan
 * @date	16 October 2020
 */

/**
 * +battery(low)
 * When the battery(low) perception is received, we need to pickup the goal
 * of !chargeBattery, if we haven't already.
 */
// Check if I'm on a mailMission, if so, I'll need to launch the mission again
// once the battery is charged.
// Also need to confirm that I'm not already charging the battery. 
+battery(low)
	:	(not charging) & 
		dockStation(DOCK) &
		mailMission(SENDER,RECEIVER)
	<-	+charging;
		.drop_all_intentions;
		.broadcast(tell, battery(chargingNeeded));
		.broadcast(tell, battery(intentionsDropped));
		!chargeBattery;
		-charging;
		.broadcast(tell, battery(chargingFinished));
		.broadcast(tell, battery(returnToMission));
		!collectAndDeliverMail(SENDER,RECEIVER).

// No mailMission on the go, just need to charge the battery if I'm not already
// dealing with it.
+battery(low)
	:	(not charging) &
		dockStation(DOCK) &
		not mailMission(SENDER,RECEIVER)
	<-	+charging;
		.broadcast(tell, battery(chargingNeeded));
		.broadcast(tell, battery(noMissionToInterrupt));
		!chargeBattery;
		-charging;
		.broadcast(tell, battery(chargingFinished)).

+battery(low)
	:	not dockStation(DOCK)
	<-	.broadcast(tell, battery(chargingNeeded));
		.broadcast(tell, battery(noDockFound)).
		
/**
 * !chargeBattery
 * The plan for getting the battery to battery(full) if needed.
 */
 // Battery isn't full and I'm not docked. Go to the docking station and dock.
 // This is rerursiuve as we need to wait for the battery to charge.
 +!chargeBattery
	:	(not battery(full)) &
		dockStation(DOCK) &
		(not docked)
	<-	.broadcast(tell, battery(chargingNeeded));
		!goTo(DOCK,1);
		.broadcast(tell, battery(atDock));
		station(dock);
		.broadcast(tell, battery(docked));
		+docked;
		!chargeBattery.
		
// Battery is full, undock the robot
+!chargeBattery
	: 	battery(full) & docked
	<-	.broadcast(tell, battery(charged));
		station(undock);
		-docked;
		.broadcast(tell, battery(unDocked)).
		
/**
 * Primary mission: collect and deliver mail
 * Plan is simple: 
 * (1) Make mental note that I have a mail mission
 * (2) Collect the mail
 * (3) Deliver the mail
 * (4) Delete mental note about mail mission
 * Updating the user at every step.
 *
 * NOTE: The robot must start with a post point visible!
 */
+!collectAndDeliverMail(SENDER,RECEIVER)
	:	(not charging)
	<-	+mailMission(SENDER,RECEIVER);
		.broadcast(tell, mailUpdate(receivedMission,SENDER,RECEIVER));
		!collectMail(SENDER);
		.broadcast(tell, mailUpdate(gotMail,SENDER,RECEIVER));
		!deliverMail(RECEIVER);
		.broadcast(tell, mailUpdate(delivered,RECEIVER));
		-mailMission(SENDER,RECEIVER).

/**
 * !collectMail(SENDER)
 * Go get the mail from the sender
 */
 // I do not yet have the mail, go get it.
+!collectMail(SENDER)
	:	not haveMail
	<-	.broadcast(tell, collectMail(goToSender,SENDER));
		!goTo(SENDER,1);
		.broadcast(tell, collectMail(atSender,SENDER));
		+haveMail;
		.broadcast(tell, collectMail(haveMail,SENDER)).

// I already have the mail.
+!collectMail(SENDER)
	:	haveMail
	<-	.broadcast(tell, collectMail(alreadyHaveMail,SENDER)).

/**
 * !deliverMail(RECEIVER)
 * Give the mail to the receiver
 */
 // Case where I have the mail.
+!deliverMail(RECEIVER)
	:	haveMail
	<-	.broadcast(tell, deliverMail(goToReceiver,RECEIVER));
		!goTo(RECEIVER,1);
		.broadcast(tell, deliverMail(arrivedAtReceiver,RECEIVER));
		-haveMail;
		.broadcast(tell, deliverMail(delivered,RECEIVER)).
		
// Case where there is no mail to deliver.
+!deliverMail(RECEIVER)
	:	not haveMail
	<-	.broadcast(tell, deliverMail(noMail,RECEIVER)).

/** 
 * !goTo(LOCATION,WATCHDOG)
 * Used for navigating the robot via the post points. Decide if the robot needs 
 * to turn or drive forward. Uses the sub goal of !followPath to move between 
 * post points.
 *
 * WATCHDOG is a counter to help keep us from getting stuck (in a scenario where
 * we can't see a postPoint. When adopting this goal, always set this to 1 on
 * the first iteration.
 * Example: !goTo(post3,1)
 * 
 * LOCATION: The location we want to go to
 * SET_DESTINATION: The location that the agent has set itself to navigate to
 * DIRECTION: The direction that the agent needs to go in order to move toward 
 *				setDestination
 */

 // Case where the robot has not yet set a destination to navigate to. Need to 
 // set the destination.
+!goTo(LOCATION,_)
	:	direction(unknown,_)
	<-	.broadcast(tell, navigationUpdate(setDestination,LOCATION));
		setDestination(LOCATION);	// Set the destination in the navigation module
		!goTo(LOCATION,1).

 // The robot has a different destination than the one we need to go to.
 +!goTo(LOCATION,_)
	:	direction(OLD,_) &
		(not (OLD = LOCATION))
	<-	.broadcast(tell, navigationUpdate(updateDestination,LOCATION));
		setDestination(LOCATION);	// Set the destination in the navigation module
		!goTo(LOCATION,1).
		
// Case where the robot has arrived at the destination.
+!goTo(LOCATION,_)
	:	direction(LOCATION,arrived)
	<-	.broadcast(tell, navigationUpdate(arrived));
		drive(stop).
	
// Destination is behind us: turn and start following the path.
+!goTo(LOCATION,_)
	:	direction(LOCATION,behind)
	<-	.broadcast(tell, navigationUpdate(behind));
		turn(left);
		!followPath;
		!goTo(LOCATION,1).
		
// Destiantion is forward. Drive forward, follow the path.
+!goTo(LOCATION,_)
	:	direction(LOCATION,forward)
	<-	.broadcast(tell, navigationUpdate(forward));
		drive(forward);
		!followPath;
		!goTo(LOCATION,1).

// Destiantion is either left or right. Turn and then follow the path.
+!goTo(LOCATION,_)
	:	direction(LOCATION,DIRECTION) &
		((DIRECTION = left) | (DIRECTION = right))
	<-	.broadcast(tell, navigationUpdate(DIRECTION));
		turn(DIRECTION);
		!followPath;
		!goTo(LOCATION,1).
		
// If WATCHDOG increaments past 20 we may be stuck. Try !followPath to see if
// we can find a postPoint. Reset WATCHDOG.
+!goTo(LOCATION,WATCHDOG)
	:	WATCHDOG > 20
	<-	.broadcast(tell, navigationUpdate(watchdogOverflow));
		!followPath;
		!goTo(LOCATION,1).

/** 
 * !followPath
 * Follow the line until a post point is visible, then stop.
 * Search for the line if it is not visible, adjust course if the line is 
 * drifting to the left or right.
 */
 
 // Case where the postPoint is visible, no driving.
 +!followPath
 	:	postPoint(_,_) | 
		direction(_,_)
	<-	.broadcast(tell, followPath(PostPointStop));
		drive(stop).
 
 
// Line is center, no post point, drive forward
+!followPath
	:	line(center) &
		(not postPoint(_,_)) &
		(not direction(_,_))
	<-	.broadcast(tell, followPath(center));
		drive(forward);
		!followPath.
		
// Line is lost, use the spiral action to try and find it.
+!followPath
	:	line(lost) & 
		(not postPoint(_,_)) &
		(not direction(_,_))
	<-	.broadcast(tell, followPath(lost));
		drive(spiral);
		!followPath.
		
// Line is accross, use the turn(left) action to re center it
+!followPath
	:	line(across) & 
		(not postPoint(_,_)) &
		(not direction(_,_))
	<-	.broadcast(tell, followPath(across));
		drive(left);
		!followPath.

// Handle cases for left and right turns.
+!followPath
	:	line(DIRECTION) & 
		((DIRECTION = left) | (DIRECTION = right)) &
		(not postPoint(_,_)) &
		(not direction(_,_))
	<-	.broadcast(tell, followPath(DIRECTION));
		drive(DIRECTION);
		!followPath.

/**
 * Default plans.
 * These can run when unrelated perceptions are received, resulting in a 
 * reasoning cycle where no plan context is applicable for that reasoning cycle.
 */
 // Ensure recursion and remember the parameters.
 // Note: This plan should never run as there are no context guards in the 
 // main plan for this goal above. If this plan runs, something strange 
 // happened.
+!collectAndDeliverMail(SENDER,RECEIVER)
	<-	.broadcast(tell, collectAndDeliverMail(default));
		!collectAndDeliverMail(SENDER,RECEIVER).

// Deal with the scenario where the reasoning cycle runs on a perception other 
// than a post point. Increment WATCHDOG and try again.
+!goTo(LOCATION,WATCHDOG)
	<-	.broadcast(tell, goTo(default, LOCATION, WATCHDOG));
		!goTo(LOCATION, (WATCHDOG + 1)).
		
// Ensure recursion. For example, if only a battery perception is received, you
// don't want to lose the followPath intention.
+!followPath
	<-	.broadcast(tell, followPath(default));
		drive(stop);	// Safest thing to do is not drive anywhere until something more useful is perceived.
		!followPath. 

// Ensure recursion while we are waiting for the battery to charge.
+!chargeBattery
	<-	.broadcast(tell, manageBattery(waitingToCharge));
		!chargeBattery.

// Default plan for collect mail. Should not be possible to get here.
+!collectMail(SENDER)
	<-	.broadcast(tell, collectMail(error,SENDER)).
		
// Default plan for deliver mail. Should not be possible to get here.
+!deliverMail(RECEIVER)
	<-	.broadcast(tell, deliverMail(error,RECEIVER)).
