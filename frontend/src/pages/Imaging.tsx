import { useNavigate } from "react-router-dom";
import Navigation from "@/components/Navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const Imaging = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8 animate-in fade-in-0 slide-in-from-bottom-2 duration-300">
        <Button
          variant="ghost"
          className="mb-6 px-0 text-primary hover:text-primary/80 hover:bg-transparent"
          onClick={() => navigate("/")}
        >
          ← Back to Model Selection
        </Button>

        <h1 className="mb-6 text-3xl font-bold text-foreground">
          Imaging Analysis Module (Ultrasound CNN)
        </h1>

        <Card className="shadow-lg">
          <CardHeader>
            <CardTitle>Imaging Module</CardTitle>
          </CardHeader>
          <CardContent className="text-muted-foreground">
            Ultrasound image upload and analysis coming soon
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Imaging;

