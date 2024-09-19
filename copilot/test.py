from compas_timber.parts import TimberPart
from compas_timber.joints import Joint

class CustomJoint(Joint):
    def __init__(self, name, part1, part2):
        super(CustomJoint, self).__init__(name)
        self.part1 = part1
        self.part2 = part2

    def create_joint(self):
        # Define how the joint is created between part1 and part2
        pass

# Example usage
part1 = TimberPart(name="Part1")
part2 = TimberPart(name="Part2")

joint = CustomJoint(name="Joint1", part1=part1, part2=part2)
joint.create_joint()

