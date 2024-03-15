# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin

from configs.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO

class Go2ConstraintTransRoughPhase2Cfg( LeggedRobotCfg ):
    class env(LeggedRobotCfg.env):
        num_envs = 4096

        n_scan = 132
        n_priv_latent = 4 + 1 + 12 + 12 + 6 + 1 + 4
        n_proprio = 42
        history_len = 5
        num_observations = n_proprio + n_scan + history_len*n_proprio + n_priv_latent + history_len*12 + history_len*(n_proprio-12)

    class init_state( LeggedRobotCfg.init_state ):
        pos = [0.0, 0.0, 0.42] # x,y,z [m]
        """
          unitree go2 sdk order:
               -0.1 <-3 FR_hip_joint 0 -> 0.0
               0.8 <- 4 FR_thigh_joint 1 -> 0.9
               -1.5 <- 5 FR_calf_joint 2 -> -1.8
               0.1 <- 0 FL_hip_joint 3 -> 0.0
               0.8 <- 1 FL_thigh_joint 4 -> 0.9
               -1.5 <- 2 FL_calf_joint 5 -> -1.8
               -0.1 <- 9 RR_hip_joint 6 -> 0.0
               1 <- 10 RR_thigh_joint 7 -> 0.9
               -1.5 <- 11 RR_calf_joint 8 -> -1.8
               0.1 <- 6 RL_hip_joint 9 -> 0.0
               1 <- 7 RL_thigh_joint 10 -> 0.9
               -1.5 <- 8 RL_calf_joint 11 -> -1.8
        """
        # default_joint_angles = { # = target angles [rad] when action = 0.0
        #     'FL_hip_joint': 0.1,   # [rad]
        #     'RL_hip_joint': 0.1,   # [rad]
        #     'FR_hip_joint': -0.1 ,  # [rad]
        #     'RR_hip_joint': -0.1,   # [rad]

        #     'FL_thigh_joint': 0.8,     # [rad]
        #     'RL_thigh_joint': 1.,   # [rad]
        #     'FR_thigh_joint': 0.8,     # [rad]
        #     'RR_thigh_joint': 1.,   # [rad]

        #     'FL_calf_joint': -1.5,   # [rad]
        #     'RL_calf_joint': -1.5,    # [rad]
        #     'FR_calf_joint': -1.5,  # [rad]
        #     'RR_calf_joint': -1.5,    # [rad]
        # }

        default_joint_angles = { # = target angles [rad] when action = 0.0
            'FL_hip_joint': 0.0,   # [rad]
            'RL_hip_joint': 0.0,   # [rad]
            'FR_hip_joint': 0.0 ,  # [rad]
            'RR_hip_joint': 0.0,   # [rad]

            'FL_thigh_joint': 0.9,     # [rad]
            'RL_thigh_joint': 0.9,   # [rad]
            'FR_thigh_joint': 0.9,     # [rad]
            'RR_thigh_joint': 0.9,   # [rad]

            'FL_calf_joint': -1.8,   # [rad]
            'RL_calf_joint': -1.8,    # [rad]
            'FR_calf_joint': -1.8,  # [rad]
            'RR_calf_joint': -1.8,    # [rad]
        }


    class control( LeggedRobotCfg.control ):
        # PD Drive parameters:
        control_type = 'P'
        stiffness = {'joint': 20.}  # [N*m/rad]
        damping = {'joint': 0.5}     # [N*m*s/rad]
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.25
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 4
        hip_scale_reduction = 0.25
        use_filter = False

    class asset( LeggedRobotCfg.asset ):
        file = '{ROOT_DIR}/resources/go2/urdf/go2.urdf'
        foot_name = "foot"
        name = "go2"
        penalize_contacts_on = ["thigh", "calf"]
        terminate_after_contacts_on = ["base"]
        self_collisions = 0 # 1 to disable, 0 to enable...bitwise filter
        flip_visual_attachments = True
  
    class rewards( LeggedRobotCfg.rewards ):
        soft_dof_pos_limit = 0.9
        base_height_target = 0.3
        class scales( LeggedRobotCfg.rewards.scales ):
            # torques = -0.0001
            # termination = 0.0
            # tracking_lin_vel = 1.0
            # tracking_ang_vel = 0.5
            # lin_vel_z = -2.0
            # ang_vel_xy = -0.05
            # orientation = 0.0
            # dof_vel = 0.0
            # dof_acc = 0.0
            # base_height = 0.0
            # feet_air_time = 1.0
            # collision = 0.0
            # feet_stumble = 0.0
            # action_rate = 0.0
            # stand_still = 0.0

            torques = -0.0002
            termination = 0.0
            tracking_lin_vel = 1.0
            tracking_ang_vel = 0.5
            lin_vel_z = -2.0
            ang_vel_xy = -0.05
            orientation = 0.0
            dof_vel = 0.0
            dof_acc = 0.0
            base_height = 0.0
            feet_air_time = 1.0
            collision = 0.0
            feet_stumble = 0.0
            action_rate = -0.01
            stand_still = 0.0

    class domain_rand( LeggedRobotCfg.domain_rand):
        randomize_friction = True
        friction_range = [0.05, 4.5]
        randomize_base_mass = True
        added_mass_range = [-1., 3.]
        randomize_base_com = True
        added_com_range = [-0.1, 0.1]
        push_robots = True
        push_interval_s = 15
        max_push_vel_xy = 1

        randomize_motor = True
        motor_strength_range = [0.9, 1.1]

        randomize_lag_timesteps = False
        lag_timesteps = 6
    
    class depth( LeggedRobotCfg.depth):
        use_camera = False
        camera_num_envs = 192
        camera_terrain_num_rows = 10
        camera_terrain_num_cols = 20

        position = [0.27, 0, 0.03]  # front camera
        angle = [-5, 5]  # positive pitch down

        update_interval = 1  # 5 works without retraining, 8 worse

        original = (106, 60)
        resized = (87, 58)
        horizontal_fov = 87
        buffer_len = 2
        
        near_clip = 0
        far_clip = 2
        dis_noise = 0.0
        
        scale = 1
        invert = True
    
    class costs:
        class scales:
            pos_limit = 0.1
            torque_limit = 0.1
            dof_vel_limits = 0.1
            vel_smoothness = 1
            acc_smoothness = 1
            collision = 0.1
            # feet_contact_forces = 0.1
            #feet_air_time = 1
            #torques= 1
            #action_rate= 1
            base_height=1
            stand_still=1
            hip_pos=1
 
        class d_values:
            pos_limit = 0.0
            torque_limit = 0.0
            dof_vel_limits = 0.0
            vel_smoothness = 0.0
            acc_smoothness = 0.0
            collision = 0.0
            # feet_contact_forces = 0.0
            #feet_air_time = 0.06
            #torques = 0.025
            #action_rate=0.07
            base_height=0.0
            stand_still=0.0
            hip_pos=0.0
    

    class cost:
        num_costs = 9
    
    class terrain(LeggedRobotCfg.terrain):
        mesh_type = 'trimesh'  # "heightfield" # none, plane, heightfield or trimesh
        measure_heights = True
        include_act_obs_pair_buf = True

class Go2ConstraintTransRoughPhase2CfgPPO( LeggedRobotCfgPPO ):
    class algorithm( LeggedRobotCfgPPO.algorithm ):
        entropy_coef = 0.01
        learning_rate = 5.e-4
        max_grad_norm = 0.01
        num_learning_epochs = 5
        num_mini_batches = 4 # mini batch size = num_envs*nsteps / nminibatches
        cost_value_loss_coef = 0.1
        cost_viol_loss_coef = 0.1

    class policy( LeggedRobotCfgPPO.policy):
        init_noise_std = 1.0
        continue_from_last_std = True
        scan_encoder_dims = [128, 64, 32]
        actor_hidden_dims = [512, 256, 128]
        critic_hidden_dims = [512, 256, 128]
        priv_encoder_dims = []
        activation = 'elu' # can be elu, relu, selu, crelu, lrelu, tanh, sigmoid
        # only for 'ActorCriticRecurrent':
        rnn_type = 'lstm'
        rnn_hidden_size = 512
        rnn_num_layers = 1

        tanh_encoder_output = False
        num_costs = 9

        teacher_act = False
        imi_flag = True
      
    class runner( LeggedRobotCfgPPO.runner ):
        run_name = ''
        experiment_name = 'rough_go2_constraint'
        policy_class_name = 'ActorCriticRmaTrans'
        runner_class_name = 'OnConstraintPolicyRunner'
        algorithm_class_name = 'NP3O'
        max_iterations = 4000
        resume = True
        resume_path = 'model_4000.pt'
        
        

  
