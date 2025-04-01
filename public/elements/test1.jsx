import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function feedbackText() {
  const [showCards, setShowCards] = useState({});

  const toggleShowCard = (id) => {
    setShowCards(prev => ({ ...prev, [id]: !prev[id] }));
  };

  return (
    <Card className="max-w-md">
   <br></br>   <CardContent>
<div>
      <Button className="mt-2" onClick={() => toggleShowCard('action.showcard')}>Action.ShowCard</Button>
      {showCards['action.showcard'] && (
        <Card className="max-w-md mt-2">
          <CardContent> <br></br>
<p className="text-base font-bold whitespace-nowrap mb-2">balabbal</p>
        <p className="text-sm font-normal whitespace-pre-wrap mb-2">balabala</p>
          </CardContent>
        </Card>
      )}
      </div>
      </CardContent>
    </Card>
  );
}
