import yaml
import numpy as np
import argparse

import omnigibson as og
from omnigibson.macros import gm
from omnigibson.action_primitives.starter_semantic_action_primitives import StarterSemanticActionPrimitives, UndoableContext
import omnigibson.utils.transform_utils as T
from omnigibson.objects.dataset_object import DatasetObject
from omnigibson.utils.motion_planning_utils import set_arm_and_detect_collision, set_base_and_detect_collision

import cProfile, pstats, io
import time
import os
import argparse

def pause(time):
    for _ in range(int(time*100)):
        og.sim.render()

def pause_step(time):
    for _ in range(int(time*100)):
        og.sim.step()

def main():
    # Load the config
    config_filename = "test_tiago.yaml"
    config = yaml.load(open(config_filename, "r"), Loader=yaml.FullLoader)

    config["scene"]["load_object_categories"] = ["floors", "walls", "coffee_table"]

    # Load the environment
    env = og.Environment(configs=config)
    scene = env.scene
    robot = env.robots[0]

    # Allow user to move camera more easily
    og.sim.enable_viewer_camera_teleoperation()

    def set_start_pose():
        control_idx = np.concatenate([robot.trunk_control_idx])
        robot.set_joint_positions([0.1], control_idx)
        og.sim.step()


    pose_2d = [-1.0, 0.0, 0.1]
    pose = StarterSemanticActionPrimitives._get_robot_pose_from_2d_pose(pose_2d)
    pose = StarterSemanticActionPrimitives._get_robot_pose_from_2d_pose([-0.433881, -0.230183, -1.87])
    robot.set_position_orientation(*pose)
    set_start_pose()
    pause_step(4)

    controller = StarterSemanticActionPrimitives(None, scene, robot)

    # for position in positions:
    #     with UndoableContext(controller.robot, controller.robot_copy, "original", True) as context:
    #         print(set_base_and_detect_collision(context,(position, [0, 0, 0, 1])))
    #         print("--------------------")

    # pause(100)

    # joint_combined_idx = np.concatenate([robot.trunk_control_idx, robot.arm_control_idx["combined"]])
    # initial_joint_pos = np.array(robot.get_joint_positions()[joint_combined_idx])

    def get_random_joint_position():
        import random
        joint_positions = []
        joint_control_idx = np.concatenate([robot.trunk_control_idx, robot.arm_control_idx[robot.default_arm]])
        joints = np.array([joint for joint in robot.joints.values()])
        arm_joints = joints[joint_control_idx]
        for i, joint in enumerate(arm_joints):
            val = random.uniform(joint.lower_limit, joint.upper_limit)
            joint_positions.append(val)
        return joint_positions, joint_control_idx


    joint_control_idx = np.concatenate([robot.trunk_control_idx, robot.arm_control_idx[robot.default_arm]])
    joint_combined_idx = np.concatenate([robot.trunk_control_idx, robot.arm_control_idx["combined"]])
    initial_joint_pos = np.array(robot.get_joint_positions()[joint_combined_idx])
    control_idx_in_joint_pos = np.where(np.in1d(joint_combined_idx, joint_control_idx))[0]
    # joint_pos = initial_joint_pos
    # joint_pos[control_idx_in_joint_pos] = [0.0133727 ,0.216775 ,0.683931 ,2.04371 ,1.88204 ,0.720747 ,1.23276 ,1.72251]
    # from IPython import embed; embed()

    # def print_link():
    #     for link in robot.links.values():
    #         link_name = link.prim_path.split("/")[-1]
    #         for mesh_name, mesh in link.collision_meshes.items():
    #             if link_name == "arm_right_1_link":
    #                 pose = T.relative_pose_transform(*link.get_position_orientation(), *robot.get_position_orientation())
    #                 print(pose[0], T.quat2euler(pose[1]))
    #                 print("-------")
    # while True:
    #     joint_pos, joint_control_idx = get_random_joint_position()
    #     robot.set_joint_positions(joint_pos, joint_control_idx)
    #     pause_step(2)
    #     # print_link()
    #     # from IPython import embed; embed()
    #     with UndoableContext(controller.robot, controller.robot_copy, "original") as context:
    #         # from IPython import embed; embed()
    #         initial_joint_pos[control_idx_in_joint_pos] = joint_pos
    #         # initial_joint_pos = np.array(robot.get_joint_positions()[joint_combined_idx])
    #         print(set_arm_and_detect_collision(context, initial_joint_pos))
    #         print("--------------------")
    #         from IPython import embed; embed()
    
    inter_path = [[0.09997262060642242, -1.0293538570404053, 1.4700201749801636, 2.709970235824585, 1.749015212059021, -1.5699917078018188, 1.3900072574615479, -4.500867362366989e-06], [0.11691628270503057, -0.8830267327942037, 1.3513760662081975, 2.544509606147747, 1.7484604307752005, -1.5653005250323326, 1.3170965590802435, -0.054800000852916544], [0.13385994480363872, -0.7366996085480022, 1.2327319574362314, 2.379048976470909, 1.74790564949138, -1.5606093422628464, 1.2441858606989389, -0.10959550083847072], [0.15080360690224687, -0.5903724843018008, 1.1140878486642654, 2.213588346794071, 1.7473508682075598, -1.55591815949336, 1.1712751623176345, -0.16439100082402489], [0.16774726900085501, -0.44404536005559925, 0.9954437398922993, 2.048127717117233, 1.7467960869237393, -1.5512269767238738, 1.09836446393633, -0.21918650080957908], [0.18469093109946316, -0.2977182358093978, 0.8767996311203332, 1.882667087440395, 1.7462413056399189, -1.5465357939543876, 1.0254537655550255, -0.27398200079513324], [0.2016345931980713, -0.1513911115631964, 0.7581555223483671, 1.717206457763557, 1.7456865243560984, -1.5418446111849013, 0.9525430671737212, -0.3287775007806874], [0.21857825529667946, -0.005063987316994867, 0.6395114135764011, 1.5517458280867191, 1.745131743072278, -1.5371534284154151, 0.8796323687924167, -0.38357300076624157], [0.2355219173952876, 0.14126313692920678, 0.520867304804435, 1.386285198409881, 1.7445769617884577, -1.5324622456459287, 0.8067216704111121, -0.4383685007517958], [0.25246557949389575, 0.2875902611754082, 0.4022231960324689, 1.220824568733043, 1.7440221805046372, -1.5277710628764425, 0.7338109720298077, -0.49316400073734995], [0.2694092415925039, 0.4339173854216096, 0.28357908726050285, 1.055363939056205, 1.7434673992208167, -1.5230798801069563, 0.6609002736485032, -0.5479595007229041], [0.2783637696421741, 0.47426669293427165, 0.31462729394691785, 1.116599611260824, 1.6978851495815748, -1.4143148289833873, 0.4303872927273669, -0.5602623084353068], [0.28731829769184425, 0.5146160004469337, 0.3456755006333329, 1.1778352834654429, 1.6523028999423328, -1.3055497778598182, 0.1998743118062306, -0.5725651161477093], [0.2962728257415144, 0.5549653079595958, 0.3767237073197479, 1.2390709556700619, 1.606720650303091, -1.196784726736249, -0.030638669114905648, -0.584867923860112], [0.3052273537911846, 0.5953146154722577, 0.4077719140061629, 1.3003066278746809, 1.5611384006638491, -1.08801967561268, -0.261151650036042, -0.5971707315725147], [0.3141818818408548, 0.6356639229849199, 0.438820120692578, 1.3615423000792997, 1.5155561510246072, -0.979254624489111, -0.4916646309571784, -0.6094735392849172], [0.323136409890525, 0.6760132304975819, 0.469868327378993, 1.4227779722839187, 1.4699739013853654, -0.870489573365542, -0.7221776118783145, -0.6217763469973199], [0.3320909379401952, 0.7163625380102439, 0.500916534065408, 1.4840136444885377, 1.4243916517461233, -0.761724522241973, -0.9526905927994511, -0.6340791547097225], [0.34104546598986535, 0.7567118455229059, 0.531964740751823, 1.5452493166931565, 1.3788094021068815, -0.6529594711184039, -1.1832035737205873, -0.6463819624221251], [0.3499999940395355, 0.797061153035568, 0.563012947438238, 1.6064849888977755, 1.3332271524676396, -0.5441944199948349, -1.4137165546417236, -0.6586847701345278]]

    for p in inter_path:
        with UndoableContext(controller.robot, controller.robot_copy, "original") as context:
            # from IPython import embed; embed()
            initial_joint_pos[control_idx_in_joint_pos] = p
            # initial_joint_pos = np.array(robot.get_joint_positions()[joint_combined_idx])
            print(set_arm_and_detect_collision(context, initial_joint_pos))
            print("--------------------")
            pause(0.1)
            from IPython import embed; embed()

    pause(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run test script")
    parser.add_argument(
        "--profile",
        action="store_true",
        help="If set, profile code and generate .prof file",
    )
    args = parser.parse_args()
    if args.profile:
        pr = cProfile.Profile()
        pr.enable()
        main()
        pr.disable()
        results = pstats.Stats(pr)
        filename = f'profile-{os.path.basename(__file__)}-{time.strftime("%Y%m%d-%H%M%S")}'
        results.dump_stats(f"./profiles/{filename}.prof")
        os.system(f"flameprof ./profiles/{filename}.prof > ./profiles/{filename}.svg")
        # Run `snakeviz ./profiles/<filename>.prof` to visualize stack trace or open <filename>.svg in a browser
    else:
        main()