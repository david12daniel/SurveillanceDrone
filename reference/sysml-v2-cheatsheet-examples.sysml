/* SysML v2 Textual Notation Cheat Sheet - Example Code
 *
 * This file contains working examples of all SysML v2 constructs shown in the
 * cheat sheet. Sections are organized to match the cheat sheet structure.
 *
 * Note: Some examples require supporting type definitions which are provided
 * in the "Supporting Definitions" section at the top.
 *
 * ----------------------------------------------------------------------------
 *
 * Excerpts and examples in this cheat sheet are derived from the OMG (R)
 * SysML (R) v2.0 Beta 4 specification (C) 2019-2025 Object Management Group,
 * Inc. and its contributors). All rights reserved.
 *
 * Cheat sheet complies with the SysML version 2.0 Beta 4 specification,
 * prepared for INCOSE IS 2025. (C) 2025 Sensmetry
 *
 * Source: https://sensmetry.com/sysml-cheatsheet/
 * Vendored into this repo as a live, extension-validated syntax reference.
 */

package 'Cheat sheet examples' {
    // Import standard libraries used throughout examples
    private import ScalarValues::*;
    private import ISQ::*;
    private import SI::*;

    // ========================================================================
    // SUPPORTING DEFINITIONS
    // These types are used by multiple examples below to avoid SysML errors
    // ========================================================================

    package 'Supporting definitions' {
        // Used in Parts examples
        part def Engine;
        part def FuelTank {
            attribute fuelLevel : VolumeValue;
            attribute maxFuelLevel : VolumeValue;
        }

        // Used in Items examples
        item def MainSwitch;
        item def SensorFeed;

        // Used in Connections examples
        part def Hub;
        part def Device;

        // Used in Actions examples
        action def EngineStatus;
        action def Accelerate;
    }

    // Helper package used in Packages section examples
    package VehicleParts {
        doc
        /* Package with vehicle part models */
        part vehiclePartA;
        part vehiclePartB;
        part vehiclePartC;
    }

    // ========================================================================
    // PACKAGES
    // ========================================================================

    package 'Package examples' {
        // Package Imports
        public import VehicleParts;
        private import ISQ::MassValue;
        private import SI::*;

        // Alias
        alias MV for ISQ::MassValue;
    }

    // ========================================================================
    // PARTS
    // ========================================================================

    package 'Part examples' {
        private import 'Supporting definitions'::*;

        // Part Definition
        part def Engine;
        part def Vehicle {
            attribute mass : MassValue;
            attribute wheels : Integer;
        }

        // Specialization
        part def SportsCar :> Vehicle {
            :>> wheels = 4;
        }

        // Part Usage
        part vehicle : Vehicle {
            :>> mass = 1500 [kg];
            part engine : Engine;
        }
    }

    // ========================================================================
    // ITEMS
    // ========================================================================

    package 'Item examples' {
        // Item Definition
        item def Fuel {
            attribute fuelMass :> ISQ::mass;
        }
    }

    // ========================================================================
    // CONNECTIONS
    // ========================================================================

    package 'Connection examples' {
        private import 'Supporting definitions'::*;

        // Connection Definition
        connection def DeviceConn {
            end part hub : Hub;
            end part device : Device;
            attribute bandwidth : Real;
        }

        // Connection Usage
        // (requires item instances for the connection ends)
        item mainSwitch : MainSwitch;
        item sensorFeed : SensorFeed;

        connection conn : DeviceConn {
            end part hub ::> mainSwitch;
            end part device ::> sensorFeed;
        }
    }

    // ========================================================================
    // PORTS
    // ========================================================================

    package 'Port examples' {
        private import 'Item examples'::Fuel;

        // Port Definition
        port def FuelingPort {
            attribute flowRate : Real;
            out fuelOut : Fuel;
            in fuelIn : Fuel;
        }

        // Port Usage
        port fuelTankPort : FuelingPort;
    }

    // ========================================================================
    // ACTIONS
    // ========================================================================

    package 'Action examples' {
        private import 'Supporting definitions'::*;
        private import 'Part examples'::Vehicle;

        // Action Definition
        action def StartEngine {
            in ignitionSignal : Boolean;
            out status : EngineStatus;
        }

        // Composite Action
        action def Drive {
            action accelerate : Accelerate;
            first start then accelerate;
        }

        // Perform Action
        part vehicle : Vehicle {
            action driveVehicle : Drive;
            action pressGas {
                perform driveVehicle;
            }
        }

        // State Definition
        state def EngineStates {
            state Off;
            state Running;
        }
    }

    // ========================================================================
    // CONSTRAINTS & REQUIREMENTS
    // ========================================================================

    package 'Constraint & requirement examples' {
        private import 'Supporting definitions'::FuelTank;
        private import 'Part examples'::Vehicle;

        // Constraint Definition
        constraint def IsFull {
            in tank : FuelTank;
            tank.fuelLevel == tank.maxFuelLevel
        }

        // Constraint Usage
        part def VehicleWithConstraint {
            part fuelTank : FuelTank;
            constraint tankIsFull : IsFull {
                in tank = fuelTank;
            }
        }

        // Requirement Definition
        requirement def MassRequirement {
            subject vehicle : Vehicle;
            attribute massActual : ISQ::MassValue;
            attribute massLimit : ISQ::MassValue;
            require constraint { massActual <= massLimit }
        }

        // Requirement Usage
        part vehicle : Vehicle {
            :>> mass = 1500 [kg];
        }

        requirement <R1> vehicleMass : MassRequirement {
            attribute :>> massActual = vehicle.mass;
            attribute :>> massLimit = 1800 [kg];
        }

        // Satisfy Requirement
        satisfy R1 by vehicle;
    }
}
