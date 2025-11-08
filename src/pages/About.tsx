import Navigation from "@/components/Navigation";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity, BarChart3, Target, TrendingUp } from "lucide-react";

const About = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8 text-center">
          <h1 className="mb-2 text-4xl font-bold text-foreground">About the System</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Advanced machine learning for uterine cancer risk assessment
          </p>
        </div>

        <div className="mx-auto max-w-4xl space-y-8">
          {/* Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5 text-primary" />
                System Overview
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-muted-foreground">
              <p>
                The Uterine Cancer Prediction System leverages state-of-the-art machine learning 
                to assess cancer risk based on comprehensive clinical and pathological features.
              </p>
              <p>
                This application represents the <strong>Design Phase frontend</strong>, built with 
                modern web technologies to provide an intuitive interface for healthcare professionals.
              </p>
              <p>
                Future versions will integrate <strong>H2O.ai AutoML</strong> for real-time predictions, 
                enabling accurate risk stratification and early intervention.
              </p>
            </CardContent>
          </Card>

          {/* Technology Stack */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                Technology Stack
              </CardTitle>
              <CardDescription>Current & Planned Technologies</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-6 md:grid-cols-2">
                <div>
                  <h3 className="font-semibold mb-2 text-foreground">Frontend (Current)</h3>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    <li>• React 18 with TypeScript</li>
                    <li>• Tailwind CSS for styling</li>
                    <li>• React Hook Form for validation</li>
                    <li>• shadcn/ui component library</li>
                    <li>• Responsive design</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold mb-2 text-foreground">Backend (Planned)</h3>
                  <ul className="space-y-1 text-sm text-muted-foreground">
                    <li>• H2O.ai AutoML engine</li>
                    <li>• FastAPI for REST endpoints</li>
                    <li>• MOJO model deployment</li>
                    <li>• SHAP for explainability</li>
                    <li>• PostgreSQL database</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Model Metrics */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5 text-primary" />
                Model Performance Metrics
              </CardTitle>
              <CardDescription>Evaluation criteria for H2O.ai AutoML models</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-4 md:grid-cols-2">
                <div className="p-4 bg-muted/50 rounded-lg">
                  <h4 className="font-semibold text-foreground mb-1">Primary Metric</h4>
                  <p className="text-2xl font-bold text-primary">PR-AUC</p>
                  <p className="text-xs text-muted-foreground mt-1">
                    Precision-Recall Area Under Curve - optimal for imbalanced datasets
                  </p>
                </div>
                <div className="p-4 bg-muted/50 rounded-lg">
                  <h4 className="font-semibold text-foreground mb-1">Secondary Metrics</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Sensitivity (Recall)</li>
                    <li>• Specificity</li>
                    <li>• ROC-AUC</li>
                    <li>• Accuracy</li>
                  </ul>
                </div>
              </div>

              <div className="border-t pt-4">
                <h4 className="font-semibold text-foreground mb-2">Why PR-AUC?</h4>
                <p className="text-sm text-muted-foreground">
                  PR-AUC is preferred over ROC-AUC for medical diagnostics with imbalanced classes. 
                  It focuses on the performance of positive predictions (cancer cases), making it 
                  more informative when the condition is rare but critical to detect.
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Model Explainability */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-primary" />
                Model Explainability
              </CardTitle>
              <CardDescription>Visualizations coming with backend integration</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-3">
                <div className="text-center p-4 bg-muted/30 rounded-lg">
                  <div className="h-32 flex items-center justify-center mb-2 bg-muted/50 rounded">
                    <BarChart3 className="h-12 w-12 text-muted-foreground" />
                  </div>
                  <h4 className="font-semibold text-sm">Feature Importance</h4>
                  <p className="text-xs text-muted-foreground mt-1">
                    SHAP values showing key predictive factors
                  </p>
                </div>
                <div className="text-center p-4 bg-muted/30 rounded-lg">
                  <div className="h-32 flex items-center justify-center mb-2 bg-muted/50 rounded">
                    <TrendingUp className="h-12 w-12 text-muted-foreground" />
                  </div>
                  <h4 className="font-semibold text-sm">ROC Curve</h4>
                  <p className="text-xs text-muted-foreground mt-1">
                    True vs false positive rate analysis
                  </p>
                </div>
                <div className="text-center p-4 bg-muted/30 rounded-lg">
                  <div className="h-32 flex items-center justify-center mb-2 bg-muted/50 rounded">
                    <Target className="h-12 w-12 text-muted-foreground" />
                  </div>
                  <h4 className="font-semibold text-sm">Confusion Matrix</h4>
                  <p className="text-xs text-muted-foreground mt-1">
                    Classification accuracy breakdown
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Clinical Features */}
          <Card>
            <CardHeader>
              <CardTitle>Input Features</CardTitle>
              <CardDescription>19 clinical and pathological variables</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2 text-sm">
                <div>
                  <h4 className="font-semibold mb-2 text-foreground">Demographics & Measurements</h4>
                  <ul className="space-y-1 text-muted-foreground">
                    <li>• Age, BMI</li>
                    <li>• Menopause Status</li>
                    <li>• Parity & Gravidity</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold mb-2 text-foreground">Clinical Symptoms</h4>
                  <ul className="space-y-1 text-muted-foreground">
                    <li>• Abnormal Bleeding</li>
                    <li>• Pelvic Pain</li>
                    <li>• Vaginal Discharge</li>
                    <li>• Weight Loss</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold mb-2 text-foreground">Medical History</h4>
                  <ul className="space-y-1 text-muted-foreground">
                    <li>• Hypertension, Diabetes</li>
                    <li>• Family History of Cancer</li>
                    <li>• Smoking, Estrogen Therapy</li>
                  </ul>
                </div>
                <div>
                  <h4 className="font-semibold mb-2 text-foreground">Pathology & Biomarkers</h4>
                  <ul className="space-y-1 text-muted-foreground">
                    <li>• Endometrium Thickness</li>
                    <li>• CA125 Level</li>
                    <li>• Histology Type</li>
                    <li>• Hormone Receptor Status</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Future Enhancements */}
          <Card className="border-primary/20 bg-medical-blue-light">
            <CardHeader>
              <CardTitle>Coming Soon</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>Real-time predictions via H2O.ai AutoML backend</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>Interactive model explainability dashboards</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>Model upload functionality (MOJO format)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>Downloadable clinical reports (PDF)</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-primary font-bold">•</span>
                  <span>Historical prediction tracking</span>
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default About;
