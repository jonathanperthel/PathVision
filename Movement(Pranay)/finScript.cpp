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
#include <string.h>
#include <string>
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>

#define PORT 61626
#define MAX 90
#define SA struct sockaddr
#define int connfd

using namespace UNITREE_LEGGED_SDK;

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
	string buff;

	bzero(buff, MAX);

	read(connfd, buff, sizeof(buff));

	return buff;
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
		
	while (1) {
		string command = chat();

		if(command[0] == 'm') {
			cmd.mode = 2;
		} else if (command[0] == 's') {
			cmf.mode = 1;
		}
		
		float angle;
		if(command[2] == 'l') {
			angle = stoi(angle.substr(3,5));
			cmd.yaw = -1 * angle / 180;
		} else if (command[2] == 'r') {
			angle = stoi(angle.substr(3,5));
			cmd.yaw = 1 * angle / 180;
		}
		udp.SetSend(cmd);
	}
}


int main(void) 
{
	//Socket setup
	int sockfd, len;
	struct sockaddr_in, servaddr, client;

	if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) == -1){
		printf("socket failed");
		exit(EXIT_FAILURE);
	}

	bzero(&servaddr, sizeof(servaddr));

	servaddr.sin_famil = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(PORT);

	if(bind(sockfd, (SA*)&servaddr, sizeof(servaddr)) != 0){
		printf("bind failed");
		exit(EXIT_FAILURE);
	}

	if(listen(sockfd, 10) != 0){
		printf("listen failed");
		exit(EXIT_FAILURE);
	}
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
