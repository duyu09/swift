# Experimental environment: A100
# 2 * 45GB GPU memory
PYTHONPATH=../../.. \
CUDA_VISIBLE_DEVICES=0,1 \
python llm_infer.py \
    --ckpt_dir "output/mixtral-moe-7b-instruct/vx_xxx/checkpoint-xxx" \
    --load_dataset_config true \
    --max_length 2048 \
    --use_flash_attn true \
    --max_new_tokens 2048 \
    --temperature 0.5 \
    --top_p 0.7 \
    --repetition_penalty 1.05 \
    --do_sample true \
    --merge_lora_and_save false \
