# 导入必要的库和模块
import os
import time
import random
import argparse

import torch

from tokenizers import Tokenizer
from models.progen.modeling_progen import ProGenForCausalLM

# 实用工具定义区域
########################################################################

# 一个用于测量和打印代码块执行时间的上下文管理器类
class print_time:
    def __init__(self, desc):
        self.desc = desc  # 描述性文字

    def __enter__(self):
        print(self.desc)
        self.t = time.time()  # 记录开始时间

    def __exit__(self, type, value, traceback):
        # 计算并打印执行时间
        print(f'{self.desc} took {time.time()-self.t:.02f}s')

# 设置环境变量来禁用tokenizers库的并行处理
def set_env():
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# 设置随机种子以确保结果的可复现性
def set_seed(seed, deterministic=True):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        # 如果要求确定性，则禁用某些优化
        torch.backends.cudnn.deterministic = deterministic
        torch.backends.cudnn.benchmark = not deterministic

# 模型定义区域
########################################################################

# 创建模型的函数，支持半精度（FP16）
def create_model(ckpt, fp16=True):
    if fp16:
        # 加载模型，设置为float16以节省内存和提高计算速度
        return ProGenForCausalLM.from_pretrained(ckpt, revision='float16', torch_dtype=torch.float16, low_cpu_mem_usage=True)
    else:
        # 不使用半精度
        return ProGenForCausalLM.from_pretrained(ckpt)

# 创建自定义分词器的函数
def create_tokenizer_custom(file):
    with open(file, 'r') as f:
        # 从给定文件加载分词器配置
        return Tokenizer.from_str(f.read())

# 采样相关函数定义区域
########################################################################

# 使用模型生成序列的函数
def sample(device, model, tokenizer, context, max_length, num_return_sequences, top_p, temp, pad_token_id):
    with torch.no_grad():  # 不计算梯度以加速生成过程
        # 编码输入上下文，并将其传输到指定的设备上
        input_ids = torch.tensor(tokenizer.encode(context).ids).view([1, -1]).to(device)
        # 生成序列
        tokens_batch = model.generate(input_ids, do_sample=True, temperature=temp, max_length=max_length, top_p=top_p, num_return_sequences=num_return_sequences, pad_token_id=pad_token_id)
        # 将生成的序列从tensor转换为列表
        as_lists = lambda batch: [batch[i, ...].detach().cpu().numpy().tolist() for i in range(batch.shape[0])]
        # 使用分词器解码生成的序列
        return tokenizer.decode_batch(as_lists(tokens_batch))

# 截断序列的函数
def truncate(sample, terminals):
    pos = []
    # 查找终止符的位置
    for terminal in terminals:
        find_pos = sample.find(terminal, 1)
        if find_pos != -1:
            pos.append(find_pos)
    if len(pos) > 0:
        # 根据找到的最早的终止符位置截断序列
        return sample[:(min(pos)+1)]
    else:
        return sample

# 计算交叉熵损失的函数
def cross_entropy(logits, target, reduction='mean'):
    return torch.nn.functional.cross_entropy(input=logits, target=target, weight=None, size_average=None, reduce=None, reduction=reduction)

# 主函数定义区域
########################################################################

def main():
    # 定义一些常量和参数
    models_151M = [ 'progen2-small' ]
    models_754M = [ 'progen2-medium', 'progen2-oas', 'progen2-base' ]
    models_2B = [ 'progen2-large', '
