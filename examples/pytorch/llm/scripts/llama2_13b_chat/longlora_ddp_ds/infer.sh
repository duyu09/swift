# Experimental environment: A100
PYTHONPATH=../../.. \
CUDA_VISIBLE_DEVICES=0 \
python llm_infer.py \
    --ckpt_dir "output/llama2-13b-chat/vx_xxx/checkpoint-xxx" \
    --load_dataset_config true \
    --max_length 4096 \
    --max_new_tokens 2048 \
    --temperature 0.1 \
    --top_p 0.7 \
    --repetition_penalty 1.05 \
    --do_sample true \
    --merge_lora_and_save false \
