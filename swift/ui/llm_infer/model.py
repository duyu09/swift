import os.path
from typing import Type

import gradio as gr
import json

from swift.llm import MODEL_MAPPING, TEMPLATE_MAPPING, ModelType
from swift.ui.base import BaseUI
from swift.ui.llm_infer.generate import Generate


class Model(BaseUI):

    llm_train = 'llm_infer'

    sub_ui = [Generate]

    locale_dict = {
        'checkpoint': {
            'value': {
                'zh': '训练后的模型',
                'en': 'Trained model'
            }
        },
        'model_type': {
            'label': {
                'zh': '选择模型',
                'en': 'Select Model'
            },
            'info': {
                'zh': 'SWIFT已支持的模型名称',
                'en': 'Base model supported by SWIFT'
            }
        },
        'load_checkpoint': {
            'value': {
                'zh': '加载模型',
                'en': 'Load model'
            }
        },
        'model_id_or_path': {
            'label': {
                'zh': '模型id或路径',
                'en': 'Model id or path'
            },
            'info': {
                'zh': '实际的模型id',
                'en': 'The actual model id or model path'
            }
        },
        'template_type': {
            'label': {
                'zh': '模型Prompt模板类型',
                'en': 'Prompt template type'
            },
            'info': {
                'zh': '选择匹配模型的Prompt模板',
                'en': 'Choose the template type of the model'
            }
        },
        'system': {
            'label': {
                'zh': 'system字段',
                'en': 'system'
            },
            'info': {
                'zh': '选择system字段的内容',
                'en': 'Choose the content of the system field'
            }
        },
        'more_params': {
            'label': {
                'zh': '更多参数',
                'en': 'More params'
            },
            'info': {
                'zh': '以json格式填入',
                'en': 'Fill in with json format'
            }
        }
    }

    @classmethod
    def do_build_ui(cls, base_tab: Type['BaseUI']):
        with gr.Row():
            model_type = gr.Dropdown(
                elem_id='model_type',
                choices=[base_tab.locale('checkpoint', cls.lang)['value']]
                + ModelType.get_model_name_list() + cls.get_custom_name_list(),
                value=base_tab.locale('checkpoint', cls.lang)['value'],
                scale=20)
            model_id_or_path = gr.Textbox(
                elem_id='model_id_or_path',
                lines=1,
                scale=20,
                interactive=True)
            template_type = gr.Dropdown(
                elem_id='template_type',
                choices=list(TEMPLATE_MAPPING.keys()) + ['AUTO'],
                scale=20)
        with gr.Row():
            system = gr.Textbox(elem_id='system', lines=1, scale=20)
        Generate.build_ui(base_tab)
        with gr.Row():
            gr.Textbox(elem_id='more_params', lines=1, scale=20)
            gr.Button(elem_id='load_checkpoint', scale=2, variant='primary')

        def update_input_model(choice):
            if choice == base_tab.locale('checkpoint', cls.lang)['value']:
                model_id_or_path = None
                default_system = None
                template = None
            else:
                model_id_or_path = MODEL_MAPPING[choice]['model_id_or_path']
                default_system = getattr(
                    TEMPLATE_MAPPING[MODEL_MAPPING[choice]['template']]
                    ['template'], 'default_system', None)
                template = MODEL_MAPPING[choice]['template']
            return model_id_or_path, default_system, template, gr.update(
                interactive=choice == base_tab.locale('checkpoint',
                                                      cls.lang)['value'])

        def update_model_id_or_path(model_type, path):
            if not path:
                return None, None, None
            local_path = os.path.join(path, 'sft_args.json')
            if not os.path.exists(local_path):
                default_system = getattr(
                    TEMPLATE_MAPPING[MODEL_MAPPING[model_type]['template']]
                    ['template'], 'default_system', None)
                template = MODEL_MAPPING[model_type]['template']
                return default_system, template

            with open(local_path, 'r') as f:
                sft_args = json.load(f)
            base_model_type = sft_args['model_type']
            system = getattr(
                TEMPLATE_MAPPING[MODEL_MAPPING[base_model_type]['template']]
                ['template'], 'default_system', None)
            return sft_args['system'] or system, sft_args['template_type']

        model_type.change(
            update_input_model,
            inputs=[model_type],
            outputs=[
                model_id_or_path, system, template_type, model_id_or_path
            ])

        model_id_or_path.change(
            update_model_id_or_path,
            inputs=[model_type, model_id_or_path],
            outputs=[system, template_type])
