import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { CheckCircle, ExternalLink } from "lucide-react";

export default function termsOfUse() {
  const handleAccept = async () => {
    try {
      console.log("Button clicked");
      await callAction({ name: "terms_of_use_action", payload: {} });
    } catch (error) {
      console.error("Failed to accept terms of use:", error);
    }
  };

  return (
    <Card className="w-full max-w-lg mx-auto shadow-lg border-0 bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-900 dark:to-gray-800">
      <CardHeader className="pb-4 pt-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 dark:bg-blue-900 rounded-full">
            <CheckCircle className="h-6 w-6 text-blue-600 dark:text-blue-400" />
          </div>
          <CardTitle className="text-xl font-semibold text-gray-900 dark:text-white">
            Terms of Use Agreement
          </CardTitle>
        </div>
      </CardHeader>
      <CardContent className="px-6 pb-6">
        <div className="space-y-4">
          <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
            Before you can send a message to SIA, please read and accept our terms of use.
            This ensures a safe and compliant experience for all users.
          </p>
          <div className="flex items-center gap-2 p-3 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
            <ExternalLink className="h-4 w-4 text-blue-600 dark:text-blue-400 flex-shrink-0" />
            <a
              href="https://test.com/test"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium transition-colors duration-200"
            >
              View SIA Terms of Use
            </a>
          </div>
        </div>
        <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
          <Button
            id="terms_of_use"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5"
            onClick={handleAccept}
          >
            <CheckCircle className="h-5 w-5 mr-2" />
            Accept Terms of Use
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
