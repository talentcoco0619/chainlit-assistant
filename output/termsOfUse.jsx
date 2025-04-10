import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function termsOfUse() {
  const handleSubmit = (data) => {
    console.log("Button clicked.");
    // Add your submit logic here
    callAction({ name: data, payload: {} });
  };

  return (
    <Card className="max-w-md">
      <br></br>{" "}
      <CardContent>
        <p className="text-base font-bold  mb-2">Terms Of Use</p>
        <p className="text-sm font-normal text-wrap mb-2">
          Before you can send a message to SIA, read and accept the terms of
          use. You can find them here:
          [SIA-Terms-of-Use](https://service4you.intranet.basf.com/esc?id=kb_article&sysparm_article=KB0072965)
        </p>
        <Button
          className="mt-2"
          variant="outline"
          id="terms_of_use"
          onClick={() => handleSubmit("terms_of_use_action")}
        >
          Accept
        </Button>
      </CardContent>
    </Card>
  );
}
