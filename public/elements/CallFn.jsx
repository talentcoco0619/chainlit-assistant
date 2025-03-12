import { useEffect } from 'react';
import { useRecoilValue } from 'recoil';
import { callFnState } from '@chainlit/react-client';

export default function CallFnExample() {
    const callFn = useRecoilValue(callFnState);

    useEffect(() => {
        if (callFn?.name === "test") {
          // Replace the console log with your actual function
          console.log("Function called with", callFn.args.content)
          callFn.callback()
        }
      }, [callFn]);

      return null
}