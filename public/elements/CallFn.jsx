import { useEffect } from 'react';
import { useRecoilValue } from 'recoil';
import { callFnState } from '@chainlit/react-client';

export default function CallFnExample() {
    const callFn = useRecoilValue(callFnState);

    const card = {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.6",
        "msteams": { "width": "Full" },
        "body": [
          {
              "type": "TextBlock",
              "size": "Medium",
              "weight": "Bolder",
              "text": "Terms of Use"
          },
          {
              "type": "TextBlock",
              "text": "Before you can send a message to SIA, read and accept the terms of use. You can find them here: [SIA-Terms-of-Use](https://service4you.intranet.basf.com/esc?id=kb_article&sysparm_aricle=KB0072965)"
          }
        ],
        "actions": [
          {
            "type": "Action.Submit",
            "title": "Accept",
            "data": {
                "id": "terms_of_use",
                "action": "terms_of_use",
                "additionalAction": action
            }
          }
        ]
    
      }

    useEffect(() => {
        if (callFn?.name === "test") {
          // Replace the console log with your actual function
          console.log("Function called with", callFn.args.content)
          callFn.callback()
        }
      }, [callFn]);

      return null
}