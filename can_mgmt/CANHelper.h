/* 
* Generated on 2019-08-27 14:48:30.380368
* This file creates a list of functions used to send
* CAN messages with abstracted IDs and messages.
*
*/

#include "CANProcess.h"
#include "CANID.h"

#ifndef CANHelper_H
#define CANHelper_H

void sendWheelSpeedFront(int16_t wheelSpeedFrontL, int16_t wheelSpeedFrontR);
void sendWheelSpeedRear(int16_t wheelSpeedRearL, int16_t wheelSpeedRearR);
void sendTireTempFront(int16_t tireTempFrontR, int16_t tireTempFrontL);
void sendTireTempRear(int16_t tireTempRearR, int16_t tireTempRearL);
void sendCoolant(int16_t coolantMotor, int16_t coolantFlow, int16_t coolantRad, int16_t coolantMc);
void sendShockPotFront(int16_t shockPotFrontL, int16_t shockPotFrontR);
void sendShockPotRear(int16_t shockPotRearR, int16_t shockPotRearL);
void sendDropLink(int16_t dropLinkLeft, int16_t dropLinkRight);
void sendLcaFront(int16_t lcaFrontLb, int16_t lcaFrontRf, int16_t lcaFrontLf, int16_t lcaFrontRb);
void sendLcaRear(int16_t lcaRearLf, int16_t lcaRearRf, int16_t lcaRearLb, int16_t lcaRearRb);
void sendUcaFront(int16_t ucaFrontRb, int16_t ucaFrontLb, int16_t ucaFrontRf, int16_t ucaFrontLf);
void sendUcaRear(int16_t ucaRearLf, int16_t ucaRearRb, int16_t ucaRearLb, int16_t ucaRearRf);
void sendFrontTorsionalArb(int16_t frontTorsionalArb);
void sendRearTorsionalArb(int16_t rearTorsionalArb);
void sendSteering(int16_t steeringTorsion, int16_t steeringAngle);
void sendImu(int8_t imuType, int16_t imuData, int32_t imuTime);

#endif