import json
import os

def convert_textblock_to_jsx(data):
    # Determine additional classes based on properties
    classes = []
    if data.get('size') == 'Medium':
        classes.append('text-base')
    else:
        classes.append('text-sm')
    if data.get('weight') == 'Bolder':
        classes.append('font-bold')
    if data.get('wrap') == True:
        classes.append('text-wrap')

    # Join the additional classes into a single string
    classes_str = ' '.join(classes)

    # Return the JSX for the TextBlock
    return f'<p className="{classes_str}">{data["text"]}</p>'

def convert_input_to_jsx(data):
    if data['type'] == 'Input.Toggle':
        return f"""
              <Checkbox id="{data['id']}"/>
              <label htmlFor="{data['id']}">{data['title']}</label>
              """
    if data['type'] == 'Input.Text':
        if data.get('isMultiline') == True:
            return f"""
                  <Textarea
                    placeholder="{data['placeholder']}"
                    className="min-h-[100px]"
                    value="{data['value']}"
                    onChange=""
                    />
                """ 
        
def convert_action_to_jsx(data):
    if data['type'] == 'Action.Submit':
        return f"""
        <Button id="{data['data']['id']}" onClick={{{data['data']['action']}}}>{data['title']}</Button>
        """

    if data['type'] == 'Action.OpenUrl':
        return f"""
        <Button onClick={{() => {data['title']}({data['url']})}}>{data['title']}</Button>
        """

    if data['type'] == 'Action.ShowCard':
        function_name = data['title'].replace(" ", "_")
        return f"""
        <Button onClick={{{function_name}}}>{data['title']}</Button>
        """        

def convert_json_to_jsx(json_data, func_name):
    # Initialize the JSX output with the imports and component setup
    jsx_output = f"""
import {{ Card, CardHeader, CardTitle, CardContent }} from "@/components/ui/card";
import {{ Button }} from "@/components/ui/button";
import {{ Checkbox }} from "@/components/ui/checkbox";
import {{ Textarea }} from "@/components/ui/textarea";

export default function {func_name}() {{

  return (
    <Card className="max-w-md">
    """

    # Process the JSON body
    if json_data['body'] and json_data['body'][0]['type'] == 'TextBlock':
        
        first_textblock = json_data['body'].pop(0)
        # Determine additional classes based on properties
        classes = []
        if first_textblock.get('size') == 'Medium':
            classes.append('text-base')
        if first_textblock.get('weight') == 'Bolder':
            classes.append('font-bold')
        if first_textblock.get('wrap') == True:
            classes.append('text-wrap')
        
        # Join the additional classes into a single string
        classes_str = ' '.join(classes)
        
        jsx_output += f"""
                        <CardHeader className="pb-2">
                          <CardTitle className="{classes_str}">{first_textblock['text']}</CardTitle>
                        </CardHeader>
                  """
    

    jsx_output += f"""
                    <CardContent>
                    """


    for item in json_data['body']:
      if item['type'] == 'TextBlock':
        jsx_output += convert_textblock_to_jsx(item)
      else:
        jsx_output +=f""""""

    jsx_output += f"""
                  </CardContent>
                  </Card>
                  );
                  }}
                """

    return jsx_output



def main():
    input_folder = 'input'
    output_folder = 'output'

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            base_filename, _ = os.path.splitext(filename)
            with open(os.path.join(input_folder, filename), 'r') as f:
                json_data = json.load(f)

            jsx_content = convert_json_to_jsx(json_data, base_filename)

            # if jsx_content is not None:
            #     output_filename = f"{base_filename}.jsx"
            #     with open(os.path.join(output_folder, output_filename), 'w') as f:
            #         f.write(jsx_content)
            # else:
            #     print(f"Failed to convert {filename} to JSX.")

            # output_filename = os.path.splitext(filename)[0] + '.jsx'
            output_filename = 'test.jsx'
            with open(os.path.join(output_folder, output_filename), 'w') as f:
                f.write(jsx_content)

if __name__ == "__main__":
    main()