# Copyright 2022 Michael Hu. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Evaluate the AlphaZero on free-style Gomoku game."""
from absl import app
from absl import flags
import timeit
import os
import torch

from alpha_zero.games.gomoku import GomokuEnv
from alpha_zero.network import AlphaZeroNet
from alpha_zero.pipeline_v1 import load_checkpoint
from alpha_zero.mcts_player import create_mcts_player


FLAGS = flags.FLAGS
flags.DEFINE_integer('board_size', 9, 'Board size for Gomoku.')
flags.DEFINE_integer('stack_history', 4, 'Stack previous states, the state is an image of N x 2 + 1 binary planes.')
flags.DEFINE_integer(
    'num_filters',
    32,
    'Number of filters for the conv2d layers in the neural network.',
)
flags.DEFINE_integer(
    'num_fc_units',
    64,
    'Number of hidden units in the linear layer of the neural network.',
)

flags.DEFINE_string('black_ckpt_file', 'checkpoints/gomoku_v2/train_steps_57000', 'Load the checkpoint file for black player.')
flags.DEFINE_string('white_ckpt_file', 'checkpoints/gomoku_v2/train_steps_57000', 'Load the checkpoint file for white player.')

flags.DEFINE_integer('num_simulations', 200, 'Number of iterations per MCTS search.')
flags.DEFINE_integer(
    'num_parallel',
    8,
    'Number of leaves to collect before using the neural network to evaluate the positions during MCTS search, 1 means no parallel search.',
)

flags.DEFINE_float('c_puct_base', 19652, 'Exploration constants balancing priors vs. search values.')
flags.DEFINE_float('c_puct_init', 1.25, 'Exploration constants balancing priors vs. search values.')

flags.DEFINE_float(
    'temperature',
    0.01,
    'Value of the temperature exploration rate after MCTS search to generate play policy.',
)

flags.DEFINE_integer('seed', 1, 'Seed the runtime.')


def main(argv):
    torch.manual_seed(FLAGS.seed)

    runtime_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    eval_env = GomokuEnv(board_size=FLAGS.board_size, stack_history=FLAGS.stack_history)

    input_shape = eval_env.observation_space.shape
    num_actions = eval_env.action_space.n

    def network_builder():
        return AlphaZeroNet(input_shape, num_actions, FLAGS.board_size, FLAGS.num_filters, FLAGS.num_fc_units)

    def load_checkpoint_for_net(network, ckpt_file):
        if ckpt_file and os.path.isfile(ckpt_file):
            loaded_state = load_checkpoint(ckpt_file, runtime_device)
            network.load_state_dict(loaded_state['network'])

    def mcts_player_builder(network):
        return create_mcts_player(
            network=network,
            device=runtime_device,
            num_simulations=FLAGS.num_simulations,
            num_parallel=FLAGS.num_parallel,
            root_noise=False,
            deterministic=True,
        )

    black_network = network_builder().to(device=runtime_device)
    white_network = network_builder().to(device=runtime_device)

    load_checkpoint_for_net(black_network, FLAGS.black_ckpt_file)
    load_checkpoint_for_net(white_network, FLAGS.white_ckpt_file)
    black_network.eval()
    white_network.eval()

    black_player = mcts_player_builder(black_network)
    white_player = mcts_player_builder(white_network)

    # Start to play game
    _ = eval_env.reset()

    start = timeit.default_timer()
    while True:
        if eval_env.current_player == eval_env.black_player:
            active_player = black_player
        else:
            active_player = white_player

        action, _, _ = active_player(eval_env, None, FLAGS.c_puct_base, FLAGS.c_puct_init, FLAGS.temperature)

        _, _, done, _ = eval_env.step(action)
        eval_env.render('human')

        if done:
            break
    
    duration = timeit.default_timer() - start
    eval_env.close()
    mean_search_time = duration / eval_env.steps
    print(f'Avg time per step: {mean_search_time:.2f}')


if __name__ == '__main__':
    app.run(main)
