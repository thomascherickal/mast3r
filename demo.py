#!/usr/bin/env python3
# Copyright (C) 2024-present Naver Corporation. All rights reserved.
# Licensed under CC BY-NC-SA 4.0 (non-commercial use only).
#
# --------------------------------------------------------
# gradio demo executable
# --------------------------------------------------------
import os
import torch
import tempfile

from mast3r.demo import get_args_parser, main_demo

from mast3r.model import AsymmetricMASt3R
from mast3r.utils.misc import hash_md5

import matplotlib.pyplot as pl
pl.ion()

torch.backends.cuda.matmul.allow_tf32 = True  # for gpu >= Ampere and pytorch >= 1.12

if __name__ == '__main__':
    parser = get_args_parser()
    args = parser.parse_args()

    if args.server_name is not None:
        server_name = args.server_name
    else:
        server_name = '0.0.0.0' if args.local_network else '127.0.0.1'

    if args.weights is not None:
        weights_path = args.weights
    else:
        weights_path = "naver/" + args.model_name

    model = AsymmetricMASt3R.from_pretrained(weights_path).to(args.device)
    chkpt_tag = hash_md5(weights_path)

    # mast3r will write the 3D model inside tmpdirname/chkpt_tag
    if args.tmp_dir is not None:
        tmpdirname = args.tmp_dir
        cache_path = os.path.join(tmpdirname, chkpt_tag)
        os.makedirs(cache_path, exist_ok=True)
        main_demo(cache_path, model, args.device, args.image_size, server_name, args.server_port, silent=args.silent,
                  share=args.share)
    else:
        with tempfile.TemporaryDirectory(suffix='_mast3r_gradio_demo') as tmpdirname:
            cache_path = os.path.join(tmpdirname, chkpt_tag)
            os.makedirs(cache_path, exist_ok=True)
            main_demo(tmpdirname, model, args.device, args.image_size,
                      server_name, args.server_port, silent=args.silent,
                      share=args.share)
