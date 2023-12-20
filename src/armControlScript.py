import json  # Reading json
import time  # Used to set delay time to control moving distance

from adafruit_servokit import ServoKit

# ARM
kit = ServoKit(channels=16, address=0x41)

# ARM COMPONENTS: Maps string names of joints to arms
JOINT_DICT = {
    "S0": kit.servo[0],  # Turntable
    "S1": kit.servo[1],  # Shoulder
    "S2": kit.servo[2],  # Elbow
    "S3": kit.servo[3],  # Wrist
    "S5": kit.servo[8],  # Gripper. 60 is maxish open, 180 is max closed
}

# CONSTANTS
FILENAME = "armInstructions.json"  # File name
WAIT_TIME = 2  # Time between each instruction

S5_CLOSED = 150  # Closed claw S5 position
S5_OPEN = 80  # Open claw S5 position

# Map the provided input angles (in the code) to the actual angles
# according to space frame
RESCALE_DICT = {
    "S0": [{"input": 90, "actual": 0}, {"input": 0, "actual": -70}],
    "S1": [{"input": 90, "actual": -5}, {"input": 170, "actual": +65}],
    "S2": [{"input": 90, "actual": -100}, {"input": 180, "actual": -40}],
    "S3": [{"input": 0, "actual": -45}, {"input": 180, "actual": 90}],
    "S5": [
        {"input": S5_OPEN, "actual": 0},
        {
            "input": S5_CLOSED,
            "actual": 180,
        },
    ],
}


# Given input-actual pairs from the rescaleDict, rescale an actual to an input
# Order of rescale pairs doesn't matter
def rescaleActualToInput(jointName, actual):
    pairList = list(RESCALE_DICT[jointName])
    pair1 = pairList[0]
    pair2 = pairList[1]

    # Calculate the slope of (input = m*actual + b)
    slope = (pair2["input"] - pair1["input"]) /\
        (pair2["actual"] - pair1["actual"])
    # print("slope = ", slope)

    # Calculate the y-intercept
    yIntercept = pair1["input"] - slope * pair1["actual"]
    # print("yIntercept = ", yIntercept)

    # Return actual transformed to input
    return slope * actual + yIntercept


# Returns the instruction list
def readInstructionsList():
    # Opening JSON file
    file = open(FILENAME)

    instructionsDictionary = json.load(file)

    # Closing file
    file.close()

    return instructionsDictionary["instructions"]


# Moves all the joints to a given configuration
# If a joint angle is not provided, then it is left the same as before
DELAY = 2
NUM_DIVISIONS = 1


def executeInstruction(instruction):
    name = instruction["name"]
    configuration = instruction["configuration"]
    seconds = instruction["seconds"]

    # Print the name
    print("Executing " + name)

    # Calculate the needed change in each angle
    incrementDict = {}
    for jointName in configuration.keys():
        # Calculate the increment needed (in terms of inputs)
        oldAngle = JOINT_DICT[jointName].angle
        newAngle = rescaleActualToInput(jointName, configuration[jointName])

        print(
            "\tMoving joint "
            + jointName
            + " to "
            + str(configuration[jointName])
            + " degrees over "
            + str(seconds)
            + " seconds"
        )

        increment = (newAngle - oldAngle) / NUM_DIVISIONS
        incrementDict[jointName] = increment

    # For every increment
    for division in range(1, NUM_DIVISIONS):
        # Increment each in increment dictionary
        for jointName in incrementDict:
            JOINT_DICT[jointName].angle = (
                JOINT_DICT[jointName].angle + incrementDict[jointName]
            )

        # Sleep
        time.sleep(seconds / NUM_DIVISIONS * 0.5)

    # Wait the remaining time
    print("Waiting for " + str(DELAY) + " seconds...")
    time.sleep(DELAY)

    return


# Loops and execute each instruction, with a delay inbetween
def readControl():
    instructionList = readInstructionsList()

    for instruction in instructionList:
        executeInstruction(instruction)
        print("\n---\n")

    return


# Choose manual or read control
def main():

    readControl()

    return


# Execute main with interrupt
if __name__ == "__main__":
    try:
        print("Starting main()!\n")
        main()
        print("\nEnded main()!")
    except KeyboardInterrupt:
        print("\nStopped main() prematurely.")
