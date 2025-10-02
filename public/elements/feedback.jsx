import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function feedback() {
  const restartSia = async () => {
    try {
      console.log("Restarting SIA");
      await callAction({ name: "restart_sia_action", payload: {} });
    } catch (error) {
      console.error("Failed to restart SIA:", error);
    }
  };

  const positiveFeedback = async () => {
    try {
      console.log("Positive feedback");
      await callAction({ name: "positive_feedback_action", payload: {} });
    } catch (error) {
      console.error("Failed to send positive feedback:", error);
    }
  };

  const negativeFeedback = async () => {
    try {
      console.log("Negative feedback");
      await callAction({ name: "negative_feedback_action", payload: {} });
    } catch (error) {
      console.error("Failed to send negative feedback:", error);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto shadow-md">
      <CardHeader className="pb-2 pt-3">
        <CardTitle className="text-sm font-medium text-gray-800 dark:text-gray-100">
          Responses are for informational purposes. Please verify important details.
        </CardTitle>
      </CardHeader>
      <CardContent className="flex items-center gap-2 pt-2">
        <Button id="restart_sia" variant="outline" onClick={restartSia} className="px-3 py-2 rounded-md" aria-label="Start a new SIA chat">
          🔄 New SIA chat
          {/* <span className="text-xs">New SIA chat</span> */}
        </Button>
        <Button
          id="positive_feedback"
          variant="outline"
          onClick={positiveFeedback}
          className="px-3 py-2 rounded-md"
          aria-label="Positive feedback"
        >
          👍
        </Button>
        <Button
          id="negative_feedback"
          variant="outline"
          onClick={negativeFeedback}
          className="px-3 py-2 rounded-md"
          aria-label="Negative feedback"
        >
          👎
        </Button>
      </CardContent>
    </Card>
  );
}
