package DroneSystemModel {

 package Requirements {
 requirement R1 {
 doc /* The system shall operate at a nominal cruising altitude relative to ground level between 90 meters and 120 meters. */
 }

 requirement R2 {
 doc /* The drone shall maintain a steady ground speed of 2.23 meters/second. */
 }

 requirement R3 {
 doc /* The infrared camera shall have a minimum resolution of 320x240. */
 }

 requirement R4 {
 doc /* The total cost for the entire integrated system shall be under $2,500. */
 }

 requirement R5 {
 doc /* The system shall minimize DIY soldering. */
 }

 requirement R6 {
 doc /* Minimum sustained flight time: 30 minutes in non-wind (0 m/s) conditions. */
 }

 requirement R7 {
 doc /* Minimum linear distance during surveillance: 2800 meters when performing surveillance at 2.2 m/s in sustained wind conditions of 4.5 m/s. */
 }

 requirement R8 {
 doc /* Stretch Goal: sustained flight time of 60 minutes in non-wind (0 m/s) conditions. */
 }
 }

 package Architecture {

 part def Battery {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute energy : ISQThermodynamics::EnergyValue;

 // Derived specific energy
 attribute specificEnergy : ISQMechanics::SpecificEnergyValue =
 energy / mass;

 port power_out;
 }

 part def Airframe {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;

 port power_battery;
 port power_sbc;
 port power_tp;
 port data_sbc;
 }

 part def ThermalPayload {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;

 port video_out;
 port power;
 }

 part def SingleBoardComputerPayload {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;

 port video_in;
 port data_af;
 port power;
 }

 part def GroundControlStation {
 attribute cost_USD : ScalarValues::Real;
 attribute mass : ISQBase::MassValue;
 attribute power : ISQMechanics::PowerValue;
 attribute batteryEnergy : ISQThermodynamics::EnergyValue;

 port video_in;
 port user_interface;
 port status_and_control;
 }

 part def SurveillanceDrone {

 part platform : Airframe;
 part battery : Battery;
 part camera : ThermalPayload;
 part sbc : SingleBoardComputerPayload;

 interface connect battery.power_out to platform.power_battery;
 interface connect platform.power_tp to camera.power;
 interface connect platform.power_sbc to sbc.power;
 interface connect sbc.data_af to platform.data_sbc;
 interface connect sbc.video_in to camera.video_out;

 // Derived total electrical load
 attribute totalPower : ISQMechanics::PowerValue =
 platform.power + camera.power + sbc.power;
 }

 part def AerialThermalObservationSystem {

 part drone : SurveillanceDrone;
 part gcs : GroundControlStation;

 connection connect drone.camera.video_out to gcs.video_in;

 // Derived total acquisition cost
 attribute totalCost : ScalarValues::Real =
 drone.platform.cost_USD
 + drone.battery.cost_USD
 + drone.camera.cost_USD
 + drone.sbc.cost_USD
 + gcs.cost_USD;
 }
 }

 package Analysis {

 constraint def BudgetLimit {

 in attribute total_cost : ScalarValues::Real;
 in attribute limit : ScalarValues::Real;

 total_cost <= limit
 }

 constraint def FlightTimeCalc {

 in attribute batteryEnergy : ISQThermodynamics::EnergyValue;
 in attribute totalPower : ISQMechanics::PowerValue;

 out attribute flightTime : ISQBase::DurationValue =
 batteryEnergy / totalPower;
 }

 constraint def ScoreCalc {

 in attribute flightTime : ISQBase::DurationValue;
 in attribute totalCost : ScalarValues::Real;

 out attribute score : ScalarValues::Real =
 flightTime.num / totalCost;
 }

 part MinFlightTimeCheck {

 part system : Architecture::AerialThermalObservationSystem;

 attribute computed_flight_time : ISQBase::DurationValue;

 constraint budget_check : BudgetLimit {
 in total_cost = system.totalCost;
 in limit = 2500.0; // R4: $2,500 max
 }

 constraint ft_calc : FlightTimeCalc {
 in batteryEnergy = system.drone.battery.energy;
 in totalPower = system.drone.totalPower;
 out flightTime = computed_flight_time;
 }

 constraint flight_time_meets_req {
 computed_flight_time >= 1800.0; // R6: 30 min minimum
 }
 }

 analysis def TradeSpaceEvaluation {

 in part candidate : Architecture::AerialThermalObservationSystem;

 attribute flight_time : ISQBase::DurationValue;
 attribute score : ScalarValues::Real;

 constraint ft_calc : FlightTimeCalc {
 in batteryEnergy = candidate.drone.battery.energy;
 in totalPower = candidate.drone.totalPower;
 out flightTime = flight_time;
 }

 constraint score_calc : ScoreCalc {
 in flightTime = flight_time;
 in totalCost = candidate.totalCost;
 out score = score;
 }
 }
 }
}