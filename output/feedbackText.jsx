import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Textarea } from "@/components/ui/textarea";

export default function feedbackText() {
  const [checkboxes, setCheckboxes] = React.useState({
    "bad-quality": false,
    "technical-error": false,
    "incorrect-response": false,
    misunderstood: false,
  });
  const [comment, setComment] = React.useState("");

  const handleCheckboxChange = (id) => {
    setCheckboxes((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const handleSubmit = () => {
    const commentText =
      typeof comment === "object" ? comment.target.value : comment;

    callAction({
      name: "feedback_comment_action",
      payload: {
        feedback: checkboxes,
        comment: commentText,
      },
    });
  };

  return (
    <Card className="max-w-md">
      <CardHeader>
        <CardTitle>Thanks for your feedback</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <p>
            Sorry to hear that. Help us to improve our service by giving us a
            comment.
          </p>

          <div className="space-y-2">
            <p className="font-medium">What went wrong?</p>

            <div className="grid grid-cols-2 gap-4">
              <div className="flex items-center space-x-2">
                <Checkbox
                  id="bad-quality"
                  checked={checkboxes["bad-quality"]}
                  onCheckedChange={() => handleCheckboxChange("bad-quality")}
                />
                <label htmlFor="bad-quality">Bad quality</label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="technical-error"
                  checked={checkboxes["technical-error"]}
                  onCheckedChange={() =>
                    handleCheckboxChange("technical-error")
                  }
                />
                <label htmlFor="technical-error">Technical error</label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="incorrect-response"
                  checked={checkboxes["incorrect-response"]}
                  onCheckedChange={() =>
                    handleCheckboxChange("incorrect-response")
                  }
                />
                <label htmlFor="incorrect-response">Incorrect response</label>
              </div>

              <div className="flex items-center space-x-2">
                <Checkbox
                  id="misunderstood"
                  checked={checkboxes["misunderstood"]}
                  onCheckedChange={() => handleCheckboxChange("misunderstood")}
                />
                <label htmlFor="misunderstood">Misunderstood</label>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <Textarea
              placeholder="Please describe more why the response was not good"
              className="min-h-[100px]"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
            />
          </div>

          <Button
            id="feedback_comment"
            variant="outline"
            className="w-24"
            onClick={handleSubmit}
          >
            Submit
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
