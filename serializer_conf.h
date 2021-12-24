/**
 * @file serializer_conf.h
 * @author Altamash Abdul Rahim (altamash@vecmocon.com)
 * @brief Serializes data to a compact form for logging purposes.
 * @version 0.1
 * @date 2020-08-22
 * 
 * @copyright Copyright (c) 2020
 * 
 */
#ifndef __SERIALIZER_CONF_H__
#define __SERIALIZER_CONF_H__


#include "stdint.h"
#include "stdlib.h"
#include "stdio.h"
#include "stdbool.h"
#include "string.h"

/**
 * @brief This structure contains very high priority data
 * 
 */
# pragma pack (1)
typedef struct
{
    int16_t imuAxes[6];/*!<Acc and Gyro 3-axis value*/
    uint32_t epoch;/*!<Timestamp*/
}veryHighPriorityData_t;

/**
 * @brief This structure contains high priority data
 * 
 */
# pragma pack (1)
typedef struct
{
    uint16_t rpm;/*!<Vehicle rpm*/
    int32_t batteryShuntCurrent;/*!<Battery Current measurement*/
    uint32_t batteryShuntCurrentTimestamp;/*!<Current timestamp*/
    int16_t  buckCurrent;/*!<vehicle Buck current*/
    uint16_t throttle;/*!<Throttle adc reading*/
}highPriorityData_t;

/**
 * @brief This structure contains normal priority data
 * 
 */
# pragma pack (1)
typedef struct
{
    uint32_t batteryThermistorTempTimestamp;/*!<Battery Group-2 timestamp*/
    int16_t batteryThermistorTemp[36];/*!<Battery Thermistor temperature*/
    int16_t batteryIcTemp;/*!<Battery BMS IC temperature*/
    int16_t batteryMosfetTemp;/*!<Battery Mosfet temperature*/
    uint16_t distance;/*!<Vehicle Trip Distance*/
    uint8_t   brake;/*!<Brake pressed or not*/
    float  coordinates[2];/*!<Vehicle coordinates*/
}normalPriorityData_t;

/**
 * @brief This structure contains low priority data
 * 
 */
# pragma pack (1)
typedef struct
{
    uint32_t batteryCellVoltagesTimestamp;/*!<Battery Group one Timestamp*/
    uint16_t batteryCellVoltages[72];/*!<Battery Cell voltages*/
    uint32_t batteryStackVoltage[4];/*!<Battery Stack voltage*/
    float  batterySoc;/*!<Battery soc*/
    float  batterySoh;/*!<Battery soh*/
    float estimatedRange;/*!<Range left in the pack. Predcited from ML model*/
    int32_t  vimIcTemp;/*!<Vim IC temperature*/
}lowPriorityData_t;

/**
 * @brief This structure contains very low priority data
 * 
 */
# pragma pack (1)
typedef struct
{
   uint32_t batteryG4Timestamp;/*!<Battery Group-4 data*/
   uint8_t batteryChgMosStatus;/*!<Battery charging mosfet status*/
   uint8_t batteryDsgMosStatus;/*!<Battery Discharging status*/
   uint8_t batteryPreMosStatus;/*!<Battery precharge mosfet status*/
   uint16_t batteryBalancingStatus;/*!<Battery balancing status*/
}veryLowPriorityData_t;

/**
 * @brief This structure contains asynchronous data
 * 
 */
# pragma pack (1)
typedef struct
{
	uint32_t fault;/*!<Battery fault code*/
	uint8_t batteryId[12];/*!<Unique Battery Id*/
}asyncData_t;


#endif