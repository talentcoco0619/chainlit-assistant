import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Textarea } from "@/components/ui/textarea";

export default function feedbackText() {
  return (
    <Card className="max-w-md">
      <CardHeader className="pb-2">
        <CardTitle className="text-base font-bold">
          Thanks for your feedback.
        </CardTitle>
      </CardHeader>

      <CardContent>
        <p className="text-sm text-wrap">
          Sorry to hear that. Help us to improve our service by giving us a
          comment.
        </p>
        <p className="text-sm font-bold text-wrap">What went wrong?</p>
      </CardContent>
    </Card>
  );
}
