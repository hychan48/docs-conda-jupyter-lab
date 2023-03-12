import yaml
from IPython.display import Markdown, display


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
