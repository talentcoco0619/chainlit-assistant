import { Card, CardContent } from "@/components/ui/card";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function feedbackText() {
  const [showCards, setShowCards] = useState({});

  const toggleShowCard = (id) => {
    try {
      setShowCards((prev) => ({ ...prev, [id]: !prev[id] }));
    } catch (error) {
      console.error("Failed to toggle card visibility", error);
    }
  };

  return (
    <Card className="max-w-md">
      <br></br>{" "}
      <CardContent>
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
              <CardContent>
                {" "}
                <br></br>
                <p className="text-base font-bold  mb-2">Test message</p>
                <p className="text-sm font-normal text-wrap mb-2">
                  Test content
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
