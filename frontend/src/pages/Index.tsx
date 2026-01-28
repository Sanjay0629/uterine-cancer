import { Link, useNavigate } from "react-router-dom";
import Navigation from "@/components/Navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu";
import { toast } from "@/components/ui/sonner";
import { Activity, Brain, ChevronDown, Shield, TrendingUp, Upload } from "lucide-react";

const Index = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-medical-blue-light to-background py-20">
        <div className="container mx-auto px-4">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-2 text-sm font-medium text-primary">
              <Activity className="h-4 w-4" />
              Powered by H2O.ai AutoML
            </div>
            <h1 className="mb-6 text-5xl font-bold leading-tight text-foreground md:text-6xl">
              Uterine Cancer Risk Predictor
            </h1>
            <p className="mb-8 text-lg text-muted-foreground md:text-xl">
              Advanced machine learning system for early detection and risk assessment
              of uterine cancer using comprehensive clinical data
            </p>
            <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
              <Button asChild size="lg" className="text-base">
                <Link to="/synthetic">Start Prediction</Link>
              </Button>
              <Button asChild variant="outline" size="lg" className="text-base">
                <Link to="/about">Learn More</Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <div className="mb-12 text-center">
            <h2 className="mb-3 text-3xl font-bold text-foreground">Key Features</h2>
            <p className="text-muted-foreground">
              Clinical-grade prediction system designed for healthcare professionals
            </p>
          </div>

          <div className="mx-auto grid max-w-5xl gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card className="transition-shadow hover:shadow-lg">
              <CardHeader>
                <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <Brain className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>AI-Powered Analysis</CardTitle>
                <CardDescription>
                  H2O.ai AutoML evaluates 19 clinical features for accurate risk assessment
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="transition-shadow hover:shadow-lg">
              <CardHeader>
                <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <TrendingUp className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>High Accuracy</CardTitle>
                <CardDescription>
                  Optimized using PR-AUC metric for superior performance on imbalanced medical data
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="transition-shadow hover:shadow-lg">
              <CardHeader>
                <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <Shield className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Clinical Grade</CardTitle>
                <CardDescription>
                  Built for healthcare professionals with focus on sensitivity and early detection
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="transition-shadow hover:shadow-lg">
              <CardHeader>
                <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <Activity className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Comprehensive Input</CardTitle>
                <CardDescription>
                  Analyzes demographics, symptoms, medical history, and biomarker data
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="transition-shadow hover:shadow-lg">
              <CardHeader>
                <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <Upload className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Model Upload</CardTitle>
                <CardDescription>
                  Support for custom H2O MOJO models (coming soon)
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="transition-shadow hover:shadow-lg">
              <CardHeader>
                <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10">
                  <TrendingUp className="h-6 w-6 text-primary" />
                </div>
                <CardTitle>Explainable AI</CardTitle>
                <CardDescription>
                  SHAP-based feature importance for transparent decision making
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="bg-muted/30 py-16">
        <div className="container mx-auto px-4">
          <div className="mb-12 text-center">
            <h2 className="mb-3 text-3xl font-bold text-foreground">How It Works</h2>
            <p className="text-muted-foreground">Simple three-step process</p>
          </div>

          <div className="mx-auto grid max-w-4xl gap-8 md:grid-cols-3">
            <div className="text-center">
              <div className="mb-4 flex justify-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
                  1
                </div>
              </div>
              <h3 className="mb-2 text-xl font-semibold text-foreground">Enter Patient Data</h3>
              <p className="text-sm text-muted-foreground">
                Input comprehensive clinical information including demographics, symptoms, and lab results
              </p>
            </div>

            <div className="text-center">
              <div className="mb-4 flex justify-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
                  2
                </div>
              </div>
              <h3 className="mb-2 text-xl font-semibold text-foreground">AI Analysis</h3>
              <p className="text-sm text-muted-foreground">
                H2O.ai AutoML processes the data using trained models optimized for cancer detection
              </p>
            </div>

            <div className="text-center">
              <div className="mb-4 flex justify-center">
                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
                  3
                </div>
              </div>
              <h3 className="mb-2 text-xl font-semibold text-foreground">Get Results</h3>
              <p className="text-sm text-muted-foreground">
                Receive risk assessment with color-coded severity and clinical recommendations
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section (Updated per your request) */}
      <section className="relative overflow-hidden bg-gradient-to-br from-medical-blue-light to-background py-20">
        <div className="container mx-auto px-4 animate-in fade-in-0 slide-in-from-bottom-2 duration-300">
          <Card className="mx-auto max-w-3xl border-primary/20 bg-gradient-to-br from-medical-blue-light to-background shadow-lg">
            <CardHeader className="text-center">
              <CardTitle className="text-4xl">Ready to Get Started?</CardTitle>
              <CardDescription className="text-base">
                Begin assessing uterine cancer risk with our advanced prediction system
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-4 sm:flex-row sm:justify-center">
              <Button size="lg" className="text-base" onClick={() => navigate("/synthetic")}>
                Start Prediction
              </Button>

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="lg" className="text-base">
                    <Upload className="mr-2 h-4 w-4" />
                    Select Decision Support Module
                    <ChevronDown className="ml-2 h-4 w-4" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="center" className="w-72 bg-popover">
                  <DropdownMenuItem
                    className="cursor-pointer"
                    onClick={() => navigate("/molecular")}
                  >
                    Molecular Prognostic Module (TCGA-UCEC)
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    className="cursor-pointer"
                    onClick={() => navigate("/imaging")}
                  >
                    Imaging Analysis Module (Ultrasound CNN)
                  </DropdownMenuItem>
                  <DropdownMenuItem
                    className="cursor-pointer"
                    onClick={() => toast("Coming Soon", { description: "Upload Custom Model is not available yet." })}
                  >
                    Upload Custom Model
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-muted/30 py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>
            Note: This is a design phase frontend. Backend integration with H2O.ai AutoML is planned for future releases.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;
