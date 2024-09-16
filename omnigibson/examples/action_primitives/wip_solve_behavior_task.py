import os

import torch as th
import yaml

import omnigibson as og
from omnigibson.action_primitives.starter_semantic_action_primitives import (
    StarterSemanticActionPrimitives,
    StarterSemanticActionPrimitiveSet,
)
from omnigibson.macros import gm

# Don't use GPU dynamics and use flatcache for performance boost
# gm.USE_GPU_DYNAMICS = True
# gm.ENABLE_FLATCACHE = True


def execute_controller(ctrl_gen, env):
    for action in ctrl_gen:
        env.step(action)


def main():
    """
    Demonstrates how to use the action primitives to solve a simple BEHAVIOR-1K task.

    It loads Benevolence_1_int with a Fetch robot, and the robot attempts to solve the
    picking_up_trash task using a hardcoded sequence of primitives.
    """
    # Load the config
    config_filename = os.path.join(og.example_config_path, "fetch_primitives.yaml")
    config = yaml.load(open(config_filename, "r"), Loader=yaml.FullLoader)

    # Update it to run a grocery shopping task
    config["scene"]["scene_model"] = "Benevolence_1_int"
    config["scene"]["load_task_relevant_only"] = True
    config["scene"]["not_load_object_categories"] = ["ceilings"]
    config["task"] = {
        "type": "BehaviorTask",
        "activity_name": "picking_up_trash",
        "activity_definition_id": 0,
        "activity_instance_id": 0,
        "predefined_problem": None,
        "online_object_sampling": False,
    }

    # Load the environment
    env = og.Environment(configs=config)
    scene = env.scene
    robot = env.robots[0]

    # Allow user to move camera more easily
    og.sim.enable_viewer_camera_teleoperation()

    controller = StarterSemanticActionPrimitives(env, enable_head_tracking=False)

    # Grasp can of soda
    grasp_obj = env.task.object_scope["can__of__soda.n.01_2"]
    print("Executing controller")
    # TODO: use task scope to get the right object
    execute_controller(controller.apply_ref(StarterSemanticActionPrimitiveSet.GRASP, grasp_obj), env)
    print("Finished executing grasp")

    # Place can in trash can
    print("Executing controller")
    # TODO: use task scope to get the right object

    trash = env.task.object_scope["ashcan.n.01_1"]
    execute_controller(controller.apply_ref(StarterSemanticActionPrimitiveSet.PLACE_INSIDE, trash), env)
    print("Finished executing place")


if __name__ == "__main__":
    main()
