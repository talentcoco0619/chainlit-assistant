import json
import os

def detect_action_types(json_data):
    """Recursively detect the presence of specific action types in the JSON."""
    action_types = set()
    
    def traverse(data):
        if isinstance(data, dict):
            if data.get('type') in ['Action.Submit', 'Action.OpenUrl', 'Action.ShowCard']:
                action_types.add(data['type'])
            for value in data.values():
                traverse(value)
        elif isinstance(data, list):
            for item in data:
                traverse(item)
    
    traverse(json_data)
    return action_types

def detect_input_types(json_data):
    """Recursively detect the presence of specific input types in the JSON."""
    input_types = set()
    
    def traverse(data):
        if isinstance(data, dict):
            if data.get('type') in ['Input.Toggle', 'Input.Text']:
                input_types.add(data['type'])
            for value in data.values():
                traverse(value)
        elif isinstance(data, list):
            for item in data:
                traverse(item)
    
    traverse(json_data)
    return input_types

def convert_to_jsx(json_data, func_name, indent_level=0):
    # Collect all input IDs to manage their state
    input_ids = collect_input_ids(json_data)
    input_states = "\n".join([f"  const [{id.replace('.', '_')}, set_{id.replace('.', '_')}] = useState({json.dumps('' if 'Text' in id else False)});"
                            for id in input_ids])

    # Detect action and input types present in the JSON
    action_types = detect_action_types(json_data)
    input_types = detect_input_types(json_data)
    
    # Conditionally include imports and functions
    imports = ["import { Card, CardContent } from \"@/components/ui/card\";"]
    functions = []
    if input_ids or 'Action.ShowCard' in action_types:
        imports.append("import { useState } from \"react\";")
    imports.append("import { Button } from \"@/components/ui/button\";")
    if 'Input.Toggle' in input_types:
        imports.append("import { Checkbox } from \"@/components/ui/checkbox\";")
    if 'Input.Text' in input_types:
        if any(json_data.get('isMultiline', False) for item in json_data.get('body', []) if item.get('type') == 'Input.Text'):
            imports.append("import { Textarea } from \"@/components/ui/textarea\";")
        else:
            imports.append("import { Input } from \"@/components/ui/input\";")

    # Generate formData content based on whether there are inputs
    if input_ids and 'Action.Submit' in action_types:
        input_fields = ', '.join([f"'{id}': {id.replace('.', '_')}" for id in input_ids])
        data_content = f" name: data, payload: {{{input_fields}}}"
    else:
        data_content = " name: data, payload: {}" if 'Action.Submit' in action_types else ""

    # Add state for showCards only if Action.ShowCard exists
    state_declarations = "  const [showCards, setShowCards] = useState({});\n" if 'Action.ShowCard' in action_types else ""

    # Add handleSubmit only if Action.Submit exists
    if 'Action.Submit' in action_types:
        functions.append(f"""  const handleSubmit = (data) => {{
                         console.log("Button clicked.");
    // Add your submit logic here
                         callAction({{{data_content}}})
  }};""")

    # Add handleOpenUrl only if Action.OpenUrl exists
    if 'Action.OpenUrl' in action_types:
        functions.append("""  const handleOpenUrl = (url) => {
    window.open(url, '_blank');
    console.log("Opening URL:", url);
  };""")

    # Add toggleShowCard only if Action.ShowCard exists
    if 'Action.ShowCard' in action_types:
        functions.append("""  const toggleShowCard = (id) => {
    setShowCards(prev => ({ ...prev, [id]: !prev[id] }));
  };""")

    # Combine imports and function definitions
    header = "\n".join(imports) + f"\n\nexport default function {func_name}() {{\n{state_declarations}{input_states}\n" + "\n\n".join(functions) + "\n\n  return (\n    <Card className=\"max-w-md\">\n   <br></br>   <CardContent>\n"
    
    # Generate the main JSX content
    main_content = convert_adaptive_card_content(json_data, indent_level + 3)
    
    # Close the component with CardContent
    footer = f"""
      </CardContent>
    </Card>
  );
}}
"""
    
    return f"{header}{main_content}{footer}"

def collect_input_ids(json_data):
    """Recursively collect all input IDs from the JSON data."""
    input_ids = []
    
    def traverse(data):
        if isinstance(data, dict):
            if data.get('type') in ['Input.Toggle', 'Input.Text']:
                input_id = data.get('id', '')
                if input_id:
                    input_ids.append(input_id)
            for value in data.values():
                traverse(value)
        elif isinstance(data, list):
            for item in data:
                traverse(item)
    
    traverse(json_data)
    return input_ids

def convert_adaptive_card_content(json_data, indent_level=0):
    indent = "  " * indent_level
    
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    if not data or 'type' not in data:
        return f"{indent}<!-- Invalid or empty Adaptive Card -->"

    if data.get('type') == 'AdaptiveCard':
        body_content = ""
        actions_content = ""
        
        if 'body' in data:
            body_items = [convert_component(item, indent_level) for item in data['body']]
            body_content = "\n".join(item for item in body_items if item is not None)
        
        if 'actions' in data:
            action_items = [convert_action(action, indent_level) for action in data['actions']]
            actions_content = "\n".join(item for item in action_items if item is not None)
        
        if body_content or actions_content:
            return f"{body_content}\n{actions_content}".strip()
        return f"{indent}<!-- Empty Adaptive Card -->"
    
    return convert_component(data, indent_level)

def convert_component(data, indent_level=0):
    indent = "  " * indent_level
    
    if not data or 'type' not in data:
        return None

    type_handlers = {
        'TextBlock': convert_text_block,
        'ColumnSet': convert_column_set,
        'Column': convert_column,
        'Input.Toggle': convert_toggle_input,
        'Input.Text': convert_text_input,
        'ActionSet': convert_action_set
    }
    
    handler = type_handlers.get(data['type'])
    if handler:
        return handler(data, indent_level)
    
    return f"{indent}<!-- Unsupported type: {data['type']} -->"

def convert_text_block(data, indent_level):
    indent = "  " * indent_level
    size_classes = {
        'small': 'text-sm',
        'medium': 'text-base',
        'large': 'text-lg',
        'extraLarge': 'text-xl'
    }
    weight_classes = {
        'bolder': 'font-bold',
        'normal': 'font-normal'
    }
    
    size = size_classes.get(data.get('size', 'small').lower(), 'text-sm')
    weight = weight_classes.get(data.get('weight', 'normal').lower(), 'font-normal')
    wrap = 'text-wrap' if data.get('wrap', False) else ''
    
    return f'{indent}<p className="{size} {weight} {wrap} mb-2">{data.get("text", "")}</p>'

def convert_column_set(data, indent_level):
    indent = "  " * indent_level
    columns = [convert_component(col, indent_level + 1) for col in data.get('columns', [])]
    valid_columns = [col for col in columns if col is not None]
    
    if not valid_columns:
        return None
        
    joined_columns = "\n".join(valid_columns)
    return f"{indent}<div className=\"flex flex-row gap-4\">\n{joined_columns}\n{indent}</div>"

def convert_column(data, indent_level):
    indent = "  " * indent_level
    items = [convert_component(item, indent_level + 1) for item in data.get('items', [])]
    valid_items = [item for item in items if item is not None]
    
    if not valid_items:
        return None
        
    joined_items = "\n".join(valid_items)
    return f"{indent}<div className=\"flex-1\">\n{joined_items}\n{indent}</div>"

def convert_toggle_input(data, indent_level):
    indent = "  " * indent_level
    inner_indent = "  " * (indent_level + 1)
    id = data.get('id', '')
    state_var = id.replace('.', '_')
    # Use onCheckedChange instead of onChange for Shadcn/UI Checkbox
    return f"{indent}<div className=\"flex items-center mb-2\">\n{inner_indent}<Checkbox id=\"{id}\" checked={{{state_var}}} onCheckedChange={{(checked) => set_{state_var}(checked)}} />\n{inner_indent}<label htmlFor=\"{id}\" className=\"ml-2\">{data.get('title', '')}</label>\n{indent}</div>"

def convert_text_input(data, indent_level):
    indent = "  " * indent_level
    inner_indent = "  " * (indent_level + 1)
    multiline = data.get('isMultiline', False)
    component = 'Textarea' if multiline else 'Input'
    id = data.get('id', '')
    state_var = id.replace('.', '_')
    return f"{indent}<{component}\n{inner_indent}id=\"{id}\"\n{inner_indent}placeholder=\"{data.get('placeholder', '')}\"\n{inner_indent}maxLength={data.get('maxLength', '') or 'undefined'}\n{inner_indent}value={{{state_var}}}\n{inner_indent}onChange={{(e) => set_{state_var}(e.target.value)}}\n{inner_indent}className=\"mb-2\"\n{indent}/>"

def convert_action(action, indent_level):
    indent = "  " * indent_level
    inner_indent = "  " * (indent_level + 1)
    
    action_id = action.get('id', action.get('title', action.get('type', 'action')).replace(' ', '_').lower())
    
    if action.get('type') == 'Action.Submit':
        data = action.get('data', {})
        data_id = data.get('id', '')
        data_action = data.get('action', '')
        return f'{indent}<Button className="mt-2" variant="outline" id="{data_id}" onClick={{() => handleSubmit("{data_action}_action")}}>{action.get("title", "")}</Button>'
    
    elif action.get('type') == 'Action.OpenUrl':
        url = action.get('url', '')
        return f'{indent}<Button className="mt-2" variant="outline"  onClick={{() => handleOpenUrl("{url}")}}>{action.get("title", "")}</Button>'
    
    elif action.get('type') == 'Action.ShowCard':
        card_content = convert_adaptive_card_content(action['card'], indent_level + 1)
        if card_content is None:
            return None
        return f"{indent}<div>\n{indent}<Button className=\"mt-2\" variant=\"outline\" onClick={{() => toggleShowCard('{action_id}')}}>{action.get('title', '')}</Button>\n{indent}{{showCards['{action_id}'] && (\n{inner_indent}<Card className=\"max-w-md mt-2\">\n{inner_indent}  <CardContent> <br></br>\n{card_content}\n{inner_indent}  </CardContent>\n{inner_indent}</Card>\n{indent})}}\n{indent}</div>"
    
    return f"{indent}<!-- Unsupported action type: {action.get('type')} -->"

def convert_action_set(data, indent_level):
    indent = "  " * indent_level
    actions = [convert_action(action, indent_level + 1) for action in data.get('actions', [])]
    valid_actions = [action for action in actions if action is not None]
    
    if not valid_actions:
        return None
    return "\n".join(valid_actions)

def main():
    input_folder = 'input'
    output_folder = 'output'

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            base_filename, _ = os.path.splitext(filename)
            with open(os.path.join(input_folder, filename), 'r') as f:
                json_data = json.load(f)

            jsx_content = convert_to_jsx(json_data, base_filename)
            output_filename = base_filename + '.jsx'
            with open(os.path.join(output_folder, output_filename), 'w') as f:
                f.write(jsx_content)

if __name__ == "__main__":
    main()