

https://github.com/huggingface/diffusers



模型很大 3.44G，小心使用 ... 



(env) cccimac@cccimacdeiMac 05-diffusers % python diffusers1.py
Cannot initialize model with low cpu memory usage because `accelerate` was not found in the environment. Defaulting to `low_cpu_mem_usage=False`. It is strongly recommended to install `accelerate` for faster and less memory-intense model loading. You can do so with: 
```
pip install accelerate
```
.
model_index.json: 100%|██████████████████████████████████████████| 541/541 [00:00<00:00, 828kB/s]
tokenizer/special_tokens_map.json: 100%|█████████████████████████| 472/472 [00:00<00:00, 829kB/s]
(…)ature_extractor/preprocessor_config.json: 100%|██████████████| 342/342 [00:00<00:00, 2.67MB/s]
scheduler/scheduler_config.json: 100%|██████████████████████████| 308/308 [00:00<00:00, 1.76MB/s]
safety_checker/config.json: 100%|███████████████████████████| 4.72k/4.72k [00:00<00:00, 7.92MB/s]
text_encoder/config.json: 100%|█████████████████████████████████| 617/617 [00:00<00:00, 2.72MB/s]
tokenizer/tokenizer_config.json: 100%|██████████████████████████| 806/806 [00:00<00:00, 4.38MB/s]
vae/config.json: 100%|██████████████████████████████████████████| 547/547 [00:00<00:00, 3.50MB/s]
tokenizer/merges.txt: 100%|████████████████████████████████████| 525k/525k [00:01<00:00, 517kB/s]
unet/config.json: 100%|█████████████████████████████████████████| 743/743 [00:00<00:00, 7.51MB/s]
tokenizer/vocab.json: 100%|██████████████████████████████████| 1.06M/1.06M [00:03<00:00, 333kB/s]
diffusion_pytorch_model.safetensors:   0%|                            | 0.00/335M [00:00<?, ?B/s^Fetching 15 files:  20%|████████▍                                 | 3/15 [00:22<01:31,  7.59s/it]
^CTraceback (most recent call last):                         | 10.5M/1.22G [00:20<39:29, 509kB/s]
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/tqdm/contrib/concurrent.py", line 51, in _executor_map
    return list(tqdm_class(ex.map(fn, *iterables, chunksize=chunksize), **kwargs))30:42, 630kB/s]
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/tqdm/std.py", line 1181, in __iter__
    for obj in iterable:
               ^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/concurrent/futures/_base.py", line 619, in result_iterator
    yield _result_or_cancel(fs.pop())
          ~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/concurrent/futures/_base.py", line 317, in _result_or_cancel
    return fut.result(timeout)
           ~~~~~~~~~~^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/concurrent/futures/_base.py", line 451, in result
    self._condition.wait(timeout)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/threading.py", line 359, in wait
    waiter.acquire()
    ~~~~~~~~~~~~~~^^
KeyboardInterrupt

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/cccimac/Desktop/ccc/course/algml/02-機器學習/02-使用套件/03-預訓練模型/05-diffusers/diffusers1.py", line 4, in <module>
    pipeline = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", torch_dtype=torch.float16)
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/huggingface_hub/utils/_validators.py", line 114, in _inner_fn
    return fn(*args, **kwargs)
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/diffusers/pipelines/pipeline_utils.py", line 732, in from_pretrained
    cached_folder = cls.download(
        pretrained_model_name_or_path,
    ...<13 lines>...
        **kwargs,
    )
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/huggingface_hub/utils/_validators.py", line 114, in _inner_fn
    return fn(*args, **kwargs)
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/diffusers/pipelines/pipeline_utils.py", line 1461, in download
    cached_folder = snapshot_download(
        pretrained_model_name,
    ...<7 lines>...
        user_agent=user_agent,
    )
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/huggingface_hub/utils/_validators.py", line 114, in _inner_fn
    return fn(*args, **kwargs)
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/huggingface_hub/_snapshot_download.py", line 296, in snapshot_download
    thread_map(
    ~~~~~~~~~~^
        _inner_hf_hub_download,
        ^^^^^^^^^^^^^^^^^^^^^^^
    ...<4 lines>...
        tqdm_class=tqdm_class or hf_tqdm,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/tqdm/contrib/concurrent.py", line 69, in thread_map
    return _executor_map(ThreadPoolExecutor, fn, *iterables, **tqdm_kwargs)
  File "/Users/cccimac/Desktop/env/lib/python3.13/site-packages/tqdm/contrib/concurrent.py", line 49, in _executor_map
    with PoolExecutor(max_workers=max_workers, initializer=tqdm_class.set_lock,
         ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                      initargs=(lk,)) as ex:
                      ^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/concurrent/futures/_base.py", line 647, in __exit__
    self.shutdown(wait=True)
    ~~~~~~~~~~~~~^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/concurrent/futures/thread.py", line 239, in shutdown
    t.join()
    ~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/lib/python3.13/threading.py", line 1092, in join
    self._handle.join(timeout)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^
KeyboardInterrupt

diffusion_pytorch_model.safetensors:   3%|▋                   | 10.5M/335M [00:26<13:37, 396kB/s]

model.safetensors:   4%|█▌                                    | 21.0M/492M [00:28<10:41, 735kB/s]

diffusion_pytorch_model.safetensors:   0%|                 | 10.5M/3.44G [00:28<1:30:42, 630kB/s]