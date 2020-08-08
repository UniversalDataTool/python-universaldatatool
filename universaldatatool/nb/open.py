from .. import Dataset
from random import randint
from IPython.display import display, HTML

udt_counter = 0
udt_notebook_instances = {}


def get_udt_notebook_instance(i):
    global udt_notebook_instances
    return udt_notebook_instances[i]


def open(constructor_dict={}, **kwargs):
    global udt_counter
    dataset = None
    if isinstance(constructor_dict, Dataset):
        dataset = constructor_dict
    else:
        dataset = Dataset(constructor_dict, **kwargs)

    udt_counter += 1
    udt_id = "universal-data-tool-{}".format(udt_counter)
    udt_notebook_instances[udt_id] = dataset

    html_string = """
    <style>
    .output .output_area .udt img {{
        max-width: initial;
        margin-top: 0;
    }}
    .MuiButton-root {{
        font-size: 12px;
    }}
    .output .output_area .udt svg {{
        max-width: initial;
    }}
    .udt * {{
        box-sizing: initial;
    }}
    </style>
    <div style="display: flex;width: 100%;">
        <div style="width: 100%;" class="udt" id="{udt_id}"></div>
    </div>
    <script type="text/javascript" src="https://universaldatatool.com/vanilla.js"></script>
    <script type="text/javascript">
    (() => {{
    let run;
    let tries = 0;
    ;run = () => {{
        if (!window.UniversalDataTool) {{
            tries++;
            if (tries < 100) {{
                setTimeout(run, 250);
            }}
            return;
        }}
        window.UniversalDataTool.open({{
            container: "{udt_id}",
            height:700,
            udt: {udt_json},
            disableHotkeys: true,
            onSaveSample: (sample, index) => {{
                console.log(sample)
                console.log(`
                import universaldatatool as __udt
                __udt_last_changed = __udt.get_udt_notebook_instance("{udt_id}")
                __udt_last_changed.samples[${{ index }}].annotation = ${{JSON.stringify(sample.annotation)}}
                `.trim())
                Jupyter.notebook.kernel.execute(`
import universaldatatool as __udt
__udt_last_changed = __udt.get_udt_notebook_instance("{udt_id}")
__udt_last_changed.samples[${{ index }}].annotation = ${{JSON.stringify(sample.annotation)}}
                `.trim())
            }}
        }})
    }};
    run();
    }})();
    </script>""".format(
        udt_id=udt_id, udt_json=dataset.to_json_string(proxy_files=True)
    ).strip()

    display(HTML(html_string))
