import { Card, CardContent } from "@/components/ui/card";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function feedbackText() {
  const [showCards, setShowCards] = useState({});

  const toggleShowCard = (id) => {
    try {
      setShowCards((prev) => ({ ...prev, [id]: !prev[id] }));
    } catch (error) {
      console.error("Failed to toggle card:", error);
    }
  };

  return (
    <Card className="max-w-md">
      <CardContent className="pt-6">
        <div>
          <Button
            className="mt-2"
            variant="outline"
            onClick={() => toggleShowCard("action.showcard")}
          >
            Action.ShowCard
          </Button>
          {showCards["action.showcard"] && (
            <Card className="max-w-md mt-2">
              <CardContent className="pt-4">
                <p className="text-base font-bold mb-2">balabbal</p>
                <p className="text-sm font-normal text-wrap mb-2">balabala</p>
              </CardContent>
            </Card>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
