/************************************************************************
Copyright (c) 2020, Unitree Robotics.Co.Ltd. All rights reserved.
Use of this source code is governed by the MPL-2.0 license, see LICENSE.
************************************************************************/

#include "unitree_legged_sdk/unitree_legged_sdk.h"
#include <math.h>
#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <fstream>
#include <string.h>
#include <vector>

#define PORT 61626
#define MAX 2
#define SA struct sockaddr
int connfd;

using namespace UNITREE_LEGGED_SDK;
using namespace std;

class Custom
{
	public:
	Custom(uint8_t level): safe(LeggedType::A1), udp(level){
	udp.InitCmdData(cmd);
}
	void UDPRecv();
	void UDPSend();
	void RobotControl();

	Safety safe;
	UDP udp;
	HighCmd cmd = {0};
	HighState state = {0};
	int motiontime = 0;
	float dt = 0.002;     // 0.001~0.01
};


void Custom::UDPRecv()
{
	udp.Recv();
}

void Custom::UDPSend()
{  
	udp.Send();
}

string chat(){
	char buff[MAX];	
	string s = "";
	
	bzero(buff, MAX);
	read(connfd, buff, MAX);
	
	for( int j = 0; j < MAX; j++){
		s = s + buff[j];
	}
	
	cout << "String received" << s << endl;
	return s;
}

void Custom::RobotControl() 
{
	cmd.forwardSpeed = 0.0f;
	cmd.sideSpeed = 0.0f;
	cmd.rotateSpeed = 0.0f;
	cmd.bodyHeight = 0.0f;

	cmd.mode = 0;      // 0:idle, default stand      1:forced stand     2:walk continuously
	cmd.roll  = 0;
	cmd.pitch = 0;
	cmd.yaw = 0;
	
	udp.SetSend(cmd);
	float buffer = 0.5;
	
	while (true) {
		string command = chat();
		cout << command << endl;
		
		if (!isdigit(command[0])) { // make sure sting is not empty
			command = "99";
		}
		
		float turnSpeed = 0;
		int angle = stoi(command);
		cout << "Angle: " << angle << endl;
		
		if(angle == 99) { // 99 edge case when robot to close 
			cmd.mode = 1;
			cmd.forwardSpeed = 0.0f;
			cmd.rotateSpeed = 0.0f;
			cout << "STOP" << endl;
		
		} else if((angle > 32) && (angle < 52)) { // approx in the middle so no need to move
			cmd.mode = 2;
			cmd.forwardSpeed = 0.25f;
			cmd.rotateSpeed = 0.0f;
			cout << "WALK" << endl;

		} else { // Else turn and move
			cout << "TURN" << endl;
			cmd.mode = 2;
			cmd.forwardSpeed = 0.25f;
			
			angle = angle - 42;
			cmd.yaw = 3.14 * angle / 180;
			
			// method 1
			//turnSpeed = 0.25f;
			//turnSpeed = -1 * (3.14 * angle / 180) / buffer;
			
			if (turnSpeed >= -1 && turnSpeed <= 1) {
				cmd.rotateSpeed = turnSpeed;
			} else if (turnSpeed < -1) {
				cmd.rotateSpeed = -1;
			} else if (turnSpeed > 1) {
				cmd.rotateSpeed = 1;
			}
			
			
			// method 2
			if (angle > 0) {
				cmd.rotateSpeed = -0.25f;
			} else if (angle < 0) {
				cmd.rotateSpeed = 0.25f;
			}
		}
		
		udp.SetSend(cmd);
		sleep(buffer);
		
		// for testing
		/*
		cmd.rotateSpeed = 0;
		udp.SetSend(cmd);
		sleep(1);
		*/
	}
}

int main(void) 
{
	//Socket setup
	int sockfd;
	unsigned int len;
	struct sockaddr_in servaddr, client;

	if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1){
		printf("socket failed");
		exit(EXIT_FAILURE);
	}

	bzero(&servaddr, sizeof(servaddr));

	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(PORT);

	if(bind(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0){
		printf("bind failed");
		exit(EXIT_FAILURE);
	}

	if(listen(sockfd, 1) != 0){
		printf("listen failed");
		exit(EXIT_FAILURE);
	}
	cout << "Accepted" << endl;
	len = sizeof(client);
	connfd = accept(sockfd, (SA*)&client, &len);
	
	
	//Unitree
	std::cout << "Communication level is set to HIGH-level." << std::endl
	      << "WARNING: Make sure the robot is standing on the ground." << std::endl
	      << "Press Enter to continue..." << std::endl;
	std::cin.ignore();

	Custom custom(HIGHLEVEL);
	InitEnvironment();
	LoopFunc loop_control("control_loop", custom.dt,    boost::bind(&Custom::RobotControl, &custom));
	LoopFunc loop_udpSend("udp_send",     custom.dt, 3, boost::bind(&Custom::UDPSend,      &custom));
	LoopFunc loop_udpRecv("udp_recv",     custom.dt, 3, boost::bind(&Custom::UDPRecv,      &custom));

	loop_udpSend.start();
	loop_udpRecv.start();
	loop_control.start();

	while(1){
		sleep(10);
	};

	close(sockfd);

	return 0; 
}
