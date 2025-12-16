import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useCallback, useState } from "react";

// Action name constants for maintainability
const ACTIONS = {
  RESTART_SIA: "restart_sia_action",
  POSITIVE_FEEDBACK: "positive_feedback_action",
  NEGATIVE_FEEDBACK: "negative_feedback_action",
};

// Loading state keys
const LOADING_STATES = {
  RESTART: "restart",
  POSITIVE: "positive",
  NEGATIVE: "negative",
};

export default function feedback() {
  const [loadingStates, setLoadingStates] = useState({
    [LOADING_STATES.RESTART]: false,
    [LOADING_STATES.POSITIVE]: false,
    [LOADING_STATES.NEGATIVE]: false,
  });

  /**
   * Generic handler for async actions with loading state management
   * @param {string} actionName - The action name to call
   * @param {string} loadingKey - The key for the loading state
   * @param {string} actionLabel - Human-readable label for error messages
   */
  const handleAction = useCallback(
    async (actionName, loadingKey, actionLabel) => {
      // Prevent concurrent executions using functional update
      setLoadingStates((prev) => {
        if (prev[loadingKey]) {
          return prev; // Already loading, prevent duplicate execution
        }
        return { ...prev, [loadingKey]: true };
      });

      try {
        console.log(`Executing ${actionLabel}...`);
        
        await callAction({ name: actionName, payload: {} });
        
        console.log(`${actionLabel} completed successfully`);
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        console.error(`Failed to execute ${actionLabel}:`, {
          error: errorMessage,
          action: actionName,
          timestamp: new Date().toISOString(),
        });
        
        // Optionally show user-facing error notification
        // You could integrate with a toast/notification system here
      } finally {
        setLoadingStates((prev) => ({ ...prev, [loadingKey]: false }));
      }
    },
    [] // No dependencies needed - using functional updates
  );

  const restartSia = useCallback(() => {
    handleAction(ACTIONS.RESTART_SIA, LOADING_STATES.RESTART, "Restart SIA");
  }, [handleAction]);

  const positiveFeedback = useCallback(() => {
    handleAction(
      ACTIONS.POSITIVE_FEEDBACK,
      LOADING_STATES.POSITIVE,
      "Positive feedback"
    );
  }, [handleAction]);

  const negativeFeedback = useCallback(() => {
    handleAction(
      ACTIONS.NEGATIVE_FEEDBACK,
      LOADING_STATES.NEGATIVE,
      "Negative feedback"
    );
  }, [handleAction]);

  const isAnyLoading = Object.values(loadingStates).some(Boolean);

  return (
    <Card className="w-full max-w-md mx-auto shadow-md">
      <CardHeader className="pb-2 pt-3">
        <CardTitle className="text-sm font-medium text-gray-800 dark:text-gray-100">
          Responses are for informational purposes. Please verify important details.
        </CardTitle>
      </CardHeader>
      <CardContent className="flex items-center gap-2 pt-2">
        <Button
          id="restart_sia"
          variant="outline"
          onClick={restartSia}
          disabled={isAnyLoading || loadingStates[LOADING_STATES.RESTART]}
          className="px-3 py-2 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Start a new SIA chat"
        >
          🔄 New SIA chat
        </Button>
        <Button
          id="positive_feedback"
          variant="outline"
          onClick={positiveFeedback}
          disabled={isAnyLoading || loadingStates[LOADING_STATES.POSITIVE]}
          className="px-3 py-2 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Positive feedback"
        >
          👍
        </Button>
        <Button
          id="negative_feedback"
          variant="outline"
          onClick={negativeFeedback}
          disabled={isAnyLoading || loadingStates[LOADING_STATES.NEGATIVE]}
          className="px-3 py-2 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
          aria-label="Negative feedback"
        >
          👎
        </Button>
      </CardContent>
    </Card>
  );
}
