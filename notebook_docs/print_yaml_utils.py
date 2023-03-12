import yaml
from IPython.display import Markdown, display

# ruamel.yaml package might be better. not a stable version... but for my purposes. probably plenty

def print_md(string):
    display(Markdown(string))


def print_yaml_md(yaml_dump_data):
    print_md(f"""
```yaml
{yaml_dump_data}
```
""")


def print_dict_as_yaml_md(data_dict):
    print_yaml_md(yaml.dump(data_dict, default_flow_style=None, sort_keys=False))  # maybe want to return as well..
    # print(yaml.dump(data[0]["apply"][0], default_flow_style=False)) # looks the same
    # print(yaml.dump(data[0]["apply"][0], default_flow_style=None )) # Compressed objects - recommended one
    # print(yaml.dump(data[0]["apply"][0], default_flow_style=True )) # very compressed. both list and obj

import pytest
import logging
def print_dict_as_yaml_md_opts(data_dict,default_flow_style=None,sort_keys=False, indent=4, **kwargs):
    # learning the struct
    kwargs["default_flow_style"] = default_flow_style
    kwargs["sort_keys"] = sort_keys
    kwargs["indent"] = indent
    data_dumped = yaml.safe_dump(data_dict, **kwargs)
    # logging.critical('crtical')
    logging.warning(type(data_dumped))
    logging.warning(f"""
```yaml
{data_dumped}
```
""")


    print_yaml_md(data_dumped)


def test_opts():
    s_yaml = """
    name: docs-conda-jupyter-lab
    channels:
      - defaults
    dependencies:
      - python=3.10
      - poetry
      - jupyterlab
    """
    d_yaml = yaml.safe_load(s_yaml)
    # print_dict_as_yaml_md_opts(d_yaml)
    print_dict_as_yaml_md_opts(d_yaml,default_flow_style=False)

