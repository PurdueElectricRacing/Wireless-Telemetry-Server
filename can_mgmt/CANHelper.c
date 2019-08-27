/* 
* Generated on 2019-08-27 14:44:41.156965
* This file creates a list of functions used to send
* CAN messages with abstracted IDs and messages.
*/

#include "CANHelper.h"


 // GENERATED FUCTION
void sendWheelSpeedFront(int16_t wheelSpeedFrontL, int16_t wheelSpeedFrontR)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = WHEEL_SPEED_FRONT_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = wheelSpeedFrontL & 0xFF;
	tx.Data[1] = wheelSpeedFrontL >> 8;

	tx.Data[2] = wheelSpeedFrontR & 0xFF;
	tx.Data[3] = wheelSpeedFrontR >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendWheelSpeedRear(int16_t wheelSpeedRearL, int16_t wheelSpeedRearR)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = WHEEL_SPEED_REAR_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = wheelSpeedRearL & 0xFF;
	tx.Data[1] = wheelSpeedRearL >> 8;

	tx.Data[2] = wheelSpeedRearR & 0xFF;
	tx.Data[3] = wheelSpeedRearR >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendTireTempFront(int16_t tireTempFrontR, int16_t tireTempFrontL)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = TIRE_TEMP_FRONT_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = tireTempFrontR & 0xFF;
	tx.Data[1] = tireTempFrontR >> 8;

	tx.Data[2] = tireTempFrontL & 0xFF;
	tx.Data[3] = tireTempFrontL >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendTireTempRear(int16_t tireTempRearR, int16_t tireTempRearL)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = TIRE_TEMP_REAR_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = tireTempRearR & 0xFF;
	tx.Data[1] = tireTempRearR >> 8;

	tx.Data[2] = tireTempRearL & 0xFF;
	tx.Data[3] = tireTempRearL >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendCoolant(int16_t coolantMotor, int16_t coolantFlow, int16_t coolantRad, int16_t coolantMc)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = COOLANT_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = coolantMotor & 0xFF;
	tx.Data[1] = coolantMotor >> 8;

	tx.Data[2] = coolantFlow & 0xFF;
	tx.Data[3] = coolantFlow >> 8;

	tx.Data[4] = coolantRad & 0xFF;
	tx.Data[5] = coolantRad >> 8;

	tx.Data[6] = coolantMc & 0xFF;
	tx.Data[7] = coolantMc >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendShockPotFront(int16_t shockPotFrontL, int16_t shockPotFrontR)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = SHOCK_POT_FRONT_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = shockPotFrontL & 0xFF;
	tx.Data[1] = shockPotFrontL >> 8;

	tx.Data[2] = shockPotFrontR & 0xFF;
	tx.Data[3] = shockPotFrontR >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendShockPotRear(int16_t shockPotRearR, int16_t shockPotRearL)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = SHOCK_POT_REAR_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = shockPotRearR & 0xFF;
	tx.Data[1] = shockPotRearR >> 8;

	tx.Data[2] = shockPotRearL & 0xFF;
	tx.Data[3] = shockPotRearL >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendDropLink(int16_t dropLinkLeft, int16_t dropLinkRight)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = DROP_LINK_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = dropLinkLeft & 0xFF;
	tx.Data[1] = dropLinkLeft >> 8;

	tx.Data[2] = dropLinkRight & 0xFF;
	tx.Data[3] = dropLinkRight >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendLcaFront(int16_t lcaFrontLb, int16_t lcaFrontRf, int16_t lcaFrontLf, int16_t lcaFrontRb)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = LCA_FRONT_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = lcaFrontLb & 0xFF;
	tx.Data[1] = lcaFrontLb >> 8;

	tx.Data[2] = lcaFrontRf & 0xFF;
	tx.Data[3] = lcaFrontRf >> 8;

	tx.Data[4] = lcaFrontLf & 0xFF;
	tx.Data[5] = lcaFrontLf >> 8;

	tx.Data[6] = lcaFrontRb & 0xFF;
	tx.Data[7] = lcaFrontRb >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendLcaRear(int16_t lcaRearLf, int16_t lcaRearRf, int16_t lcaRearLb, int16_t lcaRearRb)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = LCA_REAR_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = lcaRearLf & 0xFF;
	tx.Data[1] = lcaRearLf >> 8;

	tx.Data[2] = lcaRearRf & 0xFF;
	tx.Data[3] = lcaRearRf >> 8;

	tx.Data[4] = lcaRearLb & 0xFF;
	tx.Data[5] = lcaRearLb >> 8;

	tx.Data[6] = lcaRearRb & 0xFF;
	tx.Data[7] = lcaRearRb >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendUcaFront(int16_t ucaFrontRb, int16_t ucaFrontLb, int16_t ucaFrontRf, int16_t ucaFrontLf)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = UCA_FRONT_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = ucaFrontRb & 0xFF;
	tx.Data[1] = ucaFrontRb >> 8;

	tx.Data[2] = ucaFrontLb & 0xFF;
	tx.Data[3] = ucaFrontLb >> 8;

	tx.Data[4] = ucaFrontRf & 0xFF;
	tx.Data[5] = ucaFrontRf >> 8;

	tx.Data[6] = ucaFrontLf & 0xFF;
	tx.Data[7] = ucaFrontLf >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendUcaRear(int16_t ucaRearLf, int16_t ucaRearRb, int16_t ucaRearLb, int16_t ucaRearRf)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = UCA_REAR_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = ucaRearLf & 0xFF;
	tx.Data[1] = ucaRearLf >> 8;

	tx.Data[2] = ucaRearRb & 0xFF;
	tx.Data[3] = ucaRearRb >> 8;

	tx.Data[4] = ucaRearLb & 0xFF;
	tx.Data[5] = ucaRearLb >> 8;

	tx.Data[6] = ucaRearRf & 0xFF;
	tx.Data[7] = ucaRearRf >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendFrontTorsionalArb(int16_t frontTorsionalArb)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = FRONT_TORSIONAL_ARB_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = frontTorsionalArb & 0xFF;
	tx.Data[1] = frontTorsionalArb >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendRearTorsionalArb(int16_t rearTorsionalArb)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = REAR_TORSIONAL_ARB_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = rearTorsionalArb & 0xFF;
	tx.Data[1] = rearTorsionalArb >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendSteering(int16_t steeringTorsion, int16_t steeringAngle)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = STEERING_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = steeringTorsion & 0xFF;
	tx.Data[1] = steeringTorsion >> 8;

	tx.Data[2] = steeringAngle & 0xFF;
	tx.Data[3] = steeringAngle >> 8;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}

 // GENERATED FUCTION
void sendImu(int8_t imuType, int16_t imuData, int32_t imuTime)
{
	CanTxMsgTypeDef tx;                        	tx.IDE = CAN_ID_STD;                        	tx.RTR = CAN_RTR_DATA;                        	tx.StdId = IMU_CAN_ID;                        	tx.DLC = 1;

	tx.Data[0] = imuType & 0xFF;

	tx.Data[1] = imuData & 0xFF;
	tx.Data[2] = imuData >> 8;

	tx.Data[3] = imuTime & 0xFF;
	tx.Data[4] = imuTime >> 8;
	tx.Data[5] = imuTime >> 16;

	xQueueSendToBack(car.q_tx_dcan, &tx, 100);
}
