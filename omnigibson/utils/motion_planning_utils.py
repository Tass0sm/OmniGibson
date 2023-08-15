import numpy as np
from math import ceil

import omnigibson as og
from omnigibson.object_states import ContactBodies
import omnigibson.utils.transform_utils as T
from pxr import PhysicsSchemaTools, Gf

def plan_base_motion(
    robot,
    end_conf,
    context,
    planning_time = 100.0,
    **kwargs
):
    """
    Plans a base motion to a 2d pose

    Args:
        robot (omnigibson.object_states.Robot): Robot object to plan for
        end_conf (Iterable): [x, y, yaw] 2d pose to plan to
        context (UndoableContext): Context to plan in that includes the robot copy
        planning_time (float): Time to plan for
    
    Returns:
        Array of arrays: Array of 2d poses that the robot should navigate to
    """
    from ompl import base as ob
    from ompl import geometric as ompl_geo

    ANGLE_DIFF = 0.3
    DIST_DIFF = 0.1

    class CustomStateSpace(ob.RealVectorStateSpace):

        def __init__(self, dim):
            super(CustomStateSpace, self).__init__(dim)

        def getX(self):
            return self[0]
        
        def setX(self, x):
            self[0] = float(x)

        def getY(self):
            return self[1]
        
        def setY(self, y):
            self[1] = float(y)

        def getYaw(self):
            return self.yaw

        def setYaw(self, yaw):
            self.yaw = float(yaw)

    class CustomMotionValidator(ob.MotionValidator):
        """
        Rotate towards goal position, then move in a straight line and rotate to goal orientation
        """

        def __init__(self, si, space):
            super(CustomMotionValidator, self).__init__(si)
            self.space = space

        def create_state(self, x, y, yaw):
            state = ob.State(self.space)
            state.getSpace().setX(x)
            state.getSpace().setY(y)
            state.getSpace().setYaw(yaw)
            return state
        
        def checkMotion(self, s1, s2):
            if not si.isValid(s2):
                return False
            
            start = np.array([s1.getSpace().getX(), s1.getSpace().getY(), s1.getSpace().getYaw()])
            goal = np.array([s2.getSpace().getX(), s2.getSpace().getY(), s2.getSpace().getYaw()])
            segment = goal[:2] - start[:2]
            segment_theta = np.arctan2(segment[1], segment[0])

            # Start rotation
            diff = T.wrap_angle(segment_theta - start[2])
            direction = np.sign(diff)
            diff = abs(diff)
            num_points = ceil(diff / ANGLE_DIFF) + 1
            nav_angle = np.linspace(0.0, diff, num_points) * direction
            angles = nav_angle + start[2]
            for i in range(num_points):
                state = self.create_state(start[0], start[1], angles[i])
                if not si.isValid(state()):
                    return False

            # Navigation
            dist = np.linalg.norm(segment)
            num_points = ceil(dist / DIST_DIFF) + 1
            nav_x = np.linspace(start[0], goal[0], num_points).tolist()
            nav_y = np.linspace(start[1], goal[1], num_points).tolist()
            for i in range(num_points):
                state = self.create_state(nav_x[i], nav_y[i], segment_theta)
                if not si.isValid(state()):
                    return False
                
            # Goal rotation
            # diff = T.wrap_angle(goal[2] - segment_theta)
            # direction = np.sign(diff)
            # diff = abs(diff)
            # num_points = ceil(diff / ANGLE_DIFF) + 1
            # nav_angle = np.linspace(0.0, diff, num_points) * direction
            # angles = nav_angle + segment_theta
            # for i in range(num_points):
            #     state = self.create_state(goal[0], goal[1], angles[i])
            #     if not si.isValid(state()):
            #         return False
                
            s2().setYaw(T.wrap_angle(segment_theta))
            return True

    def state_valid_fn(q):
        x = q.getSpace().getX()
        y = q.getSpace().getY()
        yaw = q.getSpace().getYaw()
        pose = ([x, y, 0.0], T.euler2quat((0, 0, yaw)))
        return not set_base_and_detect_collision(context, pose)

    pos = robot.get_position()
    yaw = T.quat2euler(robot.get_orientation())[2]
    start_conf = (pos[0], pos[1], yaw)

    # create an R2 state space
    dim = 2
    space = CustomStateSpace(dim)

    # set lower and upper bounds
    bbox_vals = []
    for floor in filter(lambda o: o.category == "floors", og.sim.scene.objects):
        bbox_vals += floor.aabb[0][:2].tolist()
        bbox_vals += floor.aabb[1][:2].tolist()
    bounds = ob.RealVectorBounds(dim)
    bounds.setLow(min(bbox_vals))
    bounds.setHigh(max(bbox_vals))
    space.setBounds(bounds)

    # create a simple setup object
    ss = ompl_geo.SimpleSetup(space)
    ss.setStateValidityChecker(ob.StateValidityCheckerFn(state_valid_fn))

    si = ss.getSpaceInformation()
    si.setMotionValidator(CustomMotionValidator(si, space))
    planner = ompl_geo.RRTConnect(si)
    ss.setPlanner(planner)

    start = ob.State(space)
    from IPython import embed; embed()
    start.getSpace().setX(start_conf[0])
    start.getSpace().setY(start_conf[1])
    start.getSpace().setYaw(T.wrap_angle(start_conf[2]))
    print(start)

    goal = ob.State(space)
    goal.getSpace().setX(end_conf[0])
    goal.getSpace().setY(end_conf[1])
    goal.getSpace().setYaw(T.wrap_angle(end_conf[2]))
    print(goal)

    ss.setStartAndGoalStates(start, goal)

    # this will automatically choose a default planner with
    # default parameters
    solved = ss.solve(planning_time)

    if solved:
        # try to shorten the path
        ss.simplifySolution()
        # print the simplified path
        sol_path = ss.getSolutionPath()
        return_path = []

        # for i in range(sol_path.getStateCount()):
        #     point = [sol_path.getState(i)[j] for j in range(dim)]
        #     point.append(sol_path.getState(i).yaw)
        #     return_path.append(point)
        # return return_path
    
        for i in range(sol_path.getStateCount()):
            x = sol_path.getState(i).getX()
            y = sol_path.getState(i).getY()
            yaw = sol_path.getState(i).getYaw()
            return_path.append([x, y, yaw])
        return return_path
    return None

def plan_arm_motion(
        
    robot,
    end_conf,
    context,
    planning_time = 100.0,
    **kwargs
):
    """
    Plans an arm motion to a final joint position

    Args:
        robot (BaseRobot): Robot object to plan for
        end_conf (Iterable): Final joint position to plan to
        context (UndoableContext): Context to plan in that includes the robot copy
        planning_time (float): Time to plan for
    
    Returns:
        Array of arrays: Array of joint positions that the robot should navigate to
    """
    from ompl import base as ob
    from ompl import geometric as ompl_geo

    joint_control_idx = np.concatenate([robot.trunk_control_idx, robot.arm_control_idx[robot.default_arm]])
    dim = len(joint_control_idx)

    if "combined" in robot.robot_arm_descriptor_yamls:
        joint_combined_idx = np.concatenate([robot.trunk_control_idx, robot.arm_control_idx["combined"]])
        initial_joint_pos = np.array(robot.get_joint_positions()[joint_combined_idx])
        control_idx_in_joint_pos = np.where(np.in1d(joint_combined_idx, joint_control_idx))[0]
    else:
        initial_joint_pos = np.array(robot.get_joint_positions()[joint_control_idx])
        control_idx_in_joint_pos = np.arange(dim)

    def state_valid_fn(q):
        joint_pos = initial_joint_pos
        joint_pos[control_idx_in_joint_pos] = [q[i] for i in range(dim)]
        return not set_arm_and_detect_collision(context, joint_pos)
    
    # create an SE2 state space
    space = ob.RealVectorStateSpace(dim)

    # set lower and upper bounds
    bounds = ob.RealVectorBounds(dim)
    joints = np.array([joint for joint in robot.joints.values()])
    arm_joints = joints[joint_control_idx]
    for i, joint in enumerate(arm_joints):
        if end_conf[i] > joint.upper_limit:
            end_conf[i] = joint.upper_limit
        if end_conf[i] < joint.lower_limit:
            end_conf[i] = joint.lower_limit
        bounds.setLow(i, float(joint.lower_limit))
        bounds.setHigh(i, float(joint.upper_limit))
    space.setBounds(bounds)

    # create a simple setup object
    ss = ompl_geo.SimpleSetup(space)
    ss.setStateValidityChecker(ob.StateValidityCheckerFn(state_valid_fn))

    si = ss.getSpaceInformation()
    planner = ompl_geo.BITstar(si)
    ss.setPlanner(planner)

    start_conf = robot.get_joint_positions()[joint_control_idx]
    start = ob.State(space)
    for i in range(dim):
        start[i] = float(start_conf[i])

    goal = ob.State(space)
    for i in range(dim):
        goal[i] = float(end_conf[i])
    ss.setStartAndGoalStates(start, goal)

    # this will automatically choose a default planner with
    # default parameters
    solved = ss.solve(planning_time)

    if solved:
        # try to shorten the path
        # ss.simplifySolution()

        sol_path = ss.getSolutionPath()
        return_path = []
        for i in range(sol_path.getStateCount()):
            joint_pos = [sol_path.getState(i)[j] for j in range(dim)]
            return_path.append(joint_pos)
        return return_path
    return None

def set_base_and_detect_collision(context, pose):
    """
    Moves the robot and detects robot collisions with the environment and itself

    Args:
        context (UndoableContext): Context to plan in that includes the robot copy
        pose (Array): Pose in the world frame to check for collisions at
    
    Returns:
        bool: Whether the robot is in collision
    """
    robot_copy = context.robot_copy
    robot_copy_type = context.robot_copy_type

    translation = pose[0]
    orientation = pose[1]
    # context.robot_copy.prim.set_local_poses(np.array([translation]), np.array([orientation]))
    translation = Gf.Vec3d(*np.array(translation, dtype=float))
    robot_copy.prims[robot_copy_type].GetAttribute("xformOp:translate").Set(translation)

    orientation = np.array(orientation, dtype=float)[[3, 0, 1, 2]]
    robot_copy.prims[robot_copy_type].GetAttribute("xformOp:orient").Set(Gf.Quatd(*orientation)) 

    return detect_robot_collision(context)

def set_arm_and_detect_collision(context, joint_pos):
    """
    Sets joint positions of the robot and detects robot collisions with the environment and itself

    Args:
        context (UndoableContext): Context to plan in that includes the robot copy
        joint_pos (Array): Joint positions to set the robot to
    
    Returns:
        bool: Whether the robot is in a valid state i.e. not in collision
    """
    robot_copy = context.robot_copy
    robot_copy_type = context.robot_copy_type
    
    arm_links = context.robot.manipulation_link_names
    link_poses = context.fk_solver.get_link_poses(joint_pos, arm_links)

    for link in arm_links:
        pose = link_poses[link]
        if link in robot_copy.meshes[robot_copy_type].keys():
            for mesh, relative_pose in zip(robot_copy.meshes[robot_copy_type][link].values(), robot_copy.relative_poses[robot_copy_type][link].values()):
                mesh_pose = T.pose_transform(*pose, *relative_pose)
                translation = Gf.Vec3d(*np.array(mesh_pose[0], dtype=float))
                mesh.GetAttribute("xformOp:translate").Set(translation)
                orientation = np.array(mesh_pose[1], dtype=float)[[3, 0, 1, 2]]
                mesh.GetAttribute("xformOp:orient").Set(Gf.Quatd(*orientation))

    return detect_robot_collision(context)

def detect_robot_collision(context):
    """
    Detects robot collisions

    Args:
        context (UndoableContext): Context to plan in that includes the robot copy
    
    Returns:
        bool: Whether the robot is in collision
    """
    robot_copy = context.robot_copy
    robot_copy_type = context.robot_copy_type

    # Define function for checking overlap
    valid_hit = False
    mesh_path = None

    def overlap_callback(hit):
        nonlocal valid_hit
        nonlocal mesh_path

        valid_hit = hit.rigid_body not in context.disabled_collision_pairs_dict[mesh_path]

        return not valid_hit

    for meshes in robot_copy.meshes[robot_copy_type].values():
        for mesh in meshes.values():
            if valid_hit:
                return valid_hit
            mesh_path = mesh.GetPrimPath().pathString
            mesh_id = PhysicsSchemaTools.encodeSdfPath(mesh_path)
            if mesh.GetTypeName() == "Mesh":
                og.sim.psqi.overlap_mesh(*mesh_id, reportFn=overlap_callback)
            else:
                og.sim.psqi.overlap_shape(*mesh_id, reportFn=overlap_callback)
        
    return valid_hit

def detect_robot_collision_in_sim(robot, filter_objs=[], ignore_obj_in_hand=True):
    """
    Detects robot collisions with the environment, but not with itself using the ContactBodies API

    Args:
        robot (BaseRobot): Robot object to detect collisions for
        filter_objs (Array of StatefulObject): Objects to ignore collisions with
        ignore_obj_in_hand (bool): Whether to ignore collisions with the object in the robot's hand
    
    Returns:
        bool: Whether the robot is in collision
    """
    filter_categories = ["floors"]
    
    obj_in_hand = robot._ag_obj_in_hand[robot.default_arm]
    if obj_in_hand is not None and ignore_obj_in_hand:
        filter_objs.append(obj_in_hand)

    collision_prims = list(robot.states[ContactBodies].get_value(ignore_objs=tuple(filter_objs)))

    for col_prim in collision_prims:
        tokens = col_prim.prim_path.split("/")
        obj_prim_path = "/".join(tokens[:-1])
        col_obj = og.sim.scene.object_registry("prim_path", obj_prim_path)
        if col_obj.category in filter_categories:
            collision_prims.remove(col_prim)
    return len(collision_prims) > 0
    

def remove_unnecessary_rotations(path):
    """
    Removes unnecessary rotations from a path for the base where the yaw for each pose in the path is in the direction of the
    the position of the next pose in the path

    Args:
        path (Array of arrays): Array of 2d poses
    
    Returns:
        Array of arrays: Array of 2d poses with unnecessary rotations removed
    """
    for start_idx in range(len(path) - 1):
        start = np.array(path[start_idx][:2])
        end = np.array(path[start_idx + 1][:2])
        segment = end - start
        theta = np.arctan2(segment[1], segment[0])
        path[start_idx] = (start[0], start[1], theta)
    return path