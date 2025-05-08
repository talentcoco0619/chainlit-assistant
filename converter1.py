import json
import os

# def convert_json_to_jsx(json_data):
#     # Initialize the JSX output with the imports and component setup
#     jsx_output = f"""
# import {{ Card, CardHeader, CardTitle, CardContent }} from "@/components/ui/card";
# import {{ Button }} from "@/components/ui/button";
# import {{ Checkbox }} from "@/components/ui/checkbox";
# import {{ Textarea }} from "@/components/ui/textarea";
# import React from 'react';

# export default function FeedbackComponent() {{
#   const [checkboxes, setCheckboxes] = React.useState({{
#     "bad-quality": false,
#     "technical-error": false,
#     "incorrect-response": false,
#     misunderstood: false,
#   }});
#   const [comment, setComment] = React.useState("");

#   const handleCheckboxChange = (id) => {{
#     setCheckboxes((prev) => ({{
#       ...prev,
#       [id]: !prev[id],
#     }}));
#   }};

#   const handleSubmit = () => {{
#     const commentText =
#       typeof comment === "object" ? comment.target.value : comment;

#     callAction({{
#       name: "feedback_comment_action",
#       payload: {{
#         feedback: checkboxes,
#         comment: commentText,
#       }},
#     }});
#   }};

#   return (
#     <Card className="max-w-md">
# """

#     # Process the JSON body
#     for item in json_data['body']:
#         if item['type'] == 'TextBlock':
#             if 'size' in item and item['size'] == 'Medium':
#                 jsx_output += f"""
#       <CardHeader>
#         <CardTitle>{item['text']}</CardTitle>
#       </CardHeader>
# """
#             else:
#                 jsx_output += f"""
#       <CardContent>
#         <div className="space-y-4">
#           <p>{item['text']}</p>
#         </div>
#       </CardContent>
# """
#         elif item['type'] == 'ColumnSet':
#             jsx_output += """
#       <CardContent>
#         <div className="grid grid-cols-2 gap-4">
# """
#             for column in item['columns']:
#                 for toggle in column['items']:
#                     jsx_output += f"""
#           <div className="flex items-center space-x-2">
#             <label htmlFor="{toggle['id']}">{toggle['title']}</label>
#           </div>
# """
#             jsx_output += """
#         </div>
#       </CardContent>
# """
#         elif item['type'] == 'ActionSet':
#             jsx_output += """
#       <CardContent>
#         <Button id="feedback_comment" variant="outline" className="w-24" onClick={handleSubmit}>
#           Submit
#         </Button>
#       </CardContent>
# """

#     # Close the component
#     jsx_output += """
#     </Card>
#   );
# }
# """

#     return jsx_output

def main():
    input_folder = 'input'
    output_folder = 'output'

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            with open(os.path.join(input_folder, filename), 'r') as f:
                json_data = json.load(f)

            jsx_content = convert_json_to_jsx(json_data)

            output_filename = os.path.splitext(filename)[0] + '.jsx'
            with open(os.path.join(output_folder, output_filename), 'w') as f:
                f.write(jsx_content)

if __name__ == "__main__":
    main()