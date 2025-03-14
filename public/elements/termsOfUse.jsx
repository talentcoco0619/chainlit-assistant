import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function termsOfUse() {
  const handleAccept = () => {
    console.log("Button clicked");

    callAction({ name: "terms_of_use_action", payload: {} })
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg font-bold">
            Terms Of Use
          </CardTitle>
        </div>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        <div className="space-y-4">Before you can send a message to SIA, read and accept the terms of use. You can find them here: [SIA-Terms-Of-Use](https://test.com/test)</div>
        <Button id="terms_of_use" variant="outline" onClick={handleAccept}>
          Accept
        </Button>
      </CardContent>
    </Card>
  );
}
