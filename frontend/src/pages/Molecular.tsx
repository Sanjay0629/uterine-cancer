import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import Navigation from "@/components/Navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { AlertCircle, CheckCircle2, AlertTriangle, Loader2, Dna, Activity, TrendingUp, Info } from "lucide-react";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";

interface MolecularFormData {
  diagnosisAge: number;
  mutationCount: number;
  msiMantisScore: number;
  tmbNonsynonymous: number;
  fractionGenomeAltered: number;
  aneuploidyScore: number;
}

const Molecular = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [predictionResult, setPredictionResult] = useState<any>(null);
  const { register, handleSubmit, formState: { errors } } = useForm<MolecularFormData>();

  const onSubmit = async (data: MolecularFormData) => {
    setIsLoading(true);
    setShowResults(false);
    
    // Simulate API call with mock data
    setTimeout(() => {
      const mockResponse = {
        molecular_subtype: {
          predicted_class: "CN_HIGH",
          confidence: 0.92
        },
        survival: {
          prediction: "Living",
          survival_probability: 0.85,
          risk_category: "Low Risk"
        }
      };
      
      setPredictionResult(mockResponse);
      setShowResults(true);
      setIsLoading(false);
      
      // Scroll to results
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }, 1500);
  };

  const getSubtypeColor = (subtype: string) => {
    switch (subtype) {
      case "POLE":
        return { color: "text-green-600", bgColor: "bg-green-50 border-green-200", icon: CheckCircle2 };
      case "MSI":
        return { color: "text-yellow-600", bgColor: "bg-yellow-50 border-yellow-200", icon: AlertTriangle };
      case "CN_LOW":
        return { color: "text-orange-600", bgColor: "bg-orange-50 border-orange-200", icon: AlertCircle };
      case "CN_HIGH":
        return { color: "text-red-600", bgColor: "bg-red-50 border-red-200", icon: AlertCircle };
      default:
        return { color: "text-gray-600", bgColor: "bg-gray-50 border-gray-200", icon: AlertCircle };
    }
  };

  const getRiskColor = (risk: string) => {
    if (risk.includes("Low")) {
      return { color: "text-green-600", bgColor: "bg-green-50 border-green-200" };
    } else if (risk.includes("Medium")) {
      return { color: "text-orange-600", bgColor: "bg-orange-50 border-orange-200" };
    } else {
      return { color: "text-red-600", bgColor: "bg-red-50 border-red-200" };
    }
  };

  const subtypeInfo = predictionResult?.molecular_subtype 
    ? getSubtypeColor(predictionResult.molecular_subtype.predicted_class)
    : null;
  const riskInfo = predictionResult?.survival?.risk_category
    ? getRiskColor(predictionResult.survival.risk_category)
    : null;

  return (
    <div className="min-h-screen bg-background">
      <Navigation />

      <div className="container mx-auto px-4 py-8">
        <Button
          variant="ghost"
          className="mb-6 px-0 text-primary hover:text-primary/80 hover:bg-transparent"
          onClick={() => navigate("/")}
        >
          ← Back to Model Selection
        </Button>

        <div className="mb-8 text-center">
          <h1 className="mb-2 text-4xl font-bold text-foreground">TCGA Uterine Cancer Molecular Prognostic Module</h1>
          <p className="text-muted-foreground">
            Analyze molecular biomarkers to predict subtype and survival outcomes
          </p>
        </div>

        <Card className="mx-auto max-w-4xl shadow-lg">
          <CardHeader className="bg-gradient-to-r from-primary/10 to-primary/5">
            <CardTitle className="flex items-center gap-2">
              <Dna className="h-6 w-6 text-primary" />
              Molecular Biomarker Input
            </CardTitle>
            <CardDescription>
              Enter patient molecular data for prognostic analysis
            </CardDescription>
          </CardHeader>
          <CardContent className="pt-6">
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              <div className="grid gap-6 md:grid-cols-2">
                {/* Diagnosis Age */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Label htmlFor="diagnosisAge">Diagnosis Age</Label>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <Info className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Patient age at time of diagnosis (years)</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </div>
                  <Input
                    id="diagnosisAge"
                    type="number"
                    placeholder="65"
                    {...register("diagnosisAge", {
                      required: "Diagnosis age is required",
                      min: { value: 25, message: "Minimum age is 25 years" },
                      max: { value: 90, message: "Maximum age is 90 years" },
                      valueAsNumber: true
                    })}
                    className={errors.diagnosisAge ? "border-red-500" : ""}
                  />
                  {errors.diagnosisAge && (
                    <p className="text-sm text-red-500">{errors.diagnosisAge.message}</p>
                  )}
                </div>

                {/* Mutation Count */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Label htmlFor="mutationCount">Mutation Count</Label>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <Info className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Total number of somatic mutations detected</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </div>
                  <Input
                    id="mutationCount"
                    type="number"
                    placeholder="1250"
                    {...register("mutationCount", {
                      required: "Mutation count is required",
                      min: { value: 0, message: "Minimum is 0" },
                      max: { value: 5000, message: "Maximum is 5000" },
                      valueAsNumber: true
                    })}
                    className={errors.mutationCount ? "border-red-500" : ""}
                  />
                  {errors.mutationCount && (
                    <p className="text-sm text-red-500">{errors.mutationCount.message}</p>
                  )}
                </div>

                {/* MSI MANTIS Score */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Label htmlFor="msiMantisScore">MSI MANTIS Score</Label>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <Info className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Microsatellite Instability score (0.0-1.0)</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </div>
                  <Input
                    id="msiMantisScore"
                    type="number"
                    step="0.01"
                    placeholder="0.45"
                    {...register("msiMantisScore", {
                      required: "MSI MANTIS score is required",
                      min: { value: 0.0, message: "Minimum is 0.0" },
                      max: { value: 1.0, message: "Maximum is 1.0" },
                      valueAsNumber: true
                    })}
                    className={errors.msiMantisScore ? "border-red-500" : ""}
                  />
                  {errors.msiMantisScore && (
                    <p className="text-sm text-red-500">{errors.msiMantisScore.message}</p>
                  )}
                </div>

                {/* TMB Nonsynonymous */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Label htmlFor="tmbNonsynonymous">TMB Nonsynonymous</Label>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <Info className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Tumor Mutational Burden - nonsynonymous mutations per MB</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </div>
                  <Input
                    id="tmbNonsynonymous"
                    type="number"
                    step="0.1"
                    placeholder="12.5"
                    {...register("tmbNonsynonymous", {
                      required: "TMB Nonsynonymous is required",
                      min: { value: 0.0, message: "Minimum is 0.0" },
                      max: { value: 100.0, message: "Maximum is 100.0" },
                      valueAsNumber: true
                    })}
                    className={errors.tmbNonsynonymous ? "border-red-500" : ""}
                  />
                  {errors.tmbNonsynonymous && (
                    <p className="text-sm text-red-500">{errors.tmbNonsynonymous.message}</p>
                  )}
                </div>

                {/* Fraction Genome Altered */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Label htmlFor="fractionGenomeAltered">Fraction Genome Altered</Label>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <Info className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Proportion of genome with copy number alterations (0.0-1.0)</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </div>
                  <Input
                    id="fractionGenomeAltered"
                    type="number"
                    step="0.01"
                    placeholder="0.35"
                    {...register("fractionGenomeAltered", {
                      required: "Fraction Genome Altered is required",
                      min: { value: 0.0, message: "Minimum is 0.0" },
                      max: { value: 1.0, message: "Maximum is 1.0" },
                      valueAsNumber: true
                    })}
                    className={errors.fractionGenomeAltered ? "border-red-500" : ""}
                  />
                  {errors.fractionGenomeAltered && (
                    <p className="text-sm text-red-500">{errors.fractionGenomeAltered.message}</p>
                  )}
                </div>

                {/* Aneuploidy Score */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Label htmlFor="aneuploidyScore">Aneuploidy Score</Label>
                    <TooltipProvider>
                      <Tooltip>
                        <TooltipTrigger>
                          <Info className="h-4 w-4 text-muted-foreground" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p>Measure of chromosomal instability (0.0-30.0)</p>
                        </TooltipContent>
                      </Tooltip>
                    </TooltipProvider>
                  </div>
                  <Input
                    id="aneuploidyScore"
                    type="number"
                    step="0.1"
                    placeholder="8.5"
                    {...register("aneuploidyScore", {
                      required: "Aneuploidy Score is required",
                      min: { value: 0.0, message: "Minimum is 0.0" },
                      max: { value: 30.0, message: "Maximum is 30.0" },
                      valueAsNumber: true
                    })}
                    className={errors.aneuploidyScore ? "border-red-500" : ""}
                  />
                  {errors.aneuploidyScore && (
                    <p className="text-sm text-red-500">{errors.aneuploidyScore.message}</p>
                  )}
                </div>
              </div>

              <Button
                type="submit"
                className="w-full"
                size="lg"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Analyzing Molecular Data...
                  </>
                ) : (
                  <>
                    <Activity className="mr-2 h-4 w-4" />
                    Analyze Prognosis
                  </>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Results Section */}
        {showResults && predictionResult && (
          <div id="results" className="mx-auto mt-8 max-w-4xl space-y-6 animate-in fade-in-0 slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-bold text-center">Prognostic Analysis Results</h2>

            <div className="grid gap-6 md:grid-cols-2">
              {/* Molecular Subtype Prediction */}
              {subtypeInfo && (
                <Card className={`${subtypeInfo.bgColor} border-2 shadow-lg`}>
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-2">
                      <subtypeInfo.icon className={`h-5 w-5 ${subtypeInfo.color}`} />
                      <CardTitle className="text-sm">Molecular Subtype</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className={`text-4xl font-bold ${subtypeInfo.color} mb-2`}>
                      {predictionResult.molecular_subtype.predicted_class}
                    </p>
                    <p className="text-sm text-muted-foreground mb-4">
                      Confidence: {(predictionResult.molecular_subtype.confidence * 100).toFixed(1)}%
                    </p>
                    <div className="mt-4">
                      <Progress 
                        value={predictionResult.molecular_subtype.confidence * 100} 
                        className="h-2"
                      />
                    </div>
                    <div className="mt-4 text-xs text-muted-foreground">
                      {predictionResult.molecular_subtype.predicted_class === "POLE" && "Best prognosis - POLE-mutated tumors"}
                      {predictionResult.molecular_subtype.predicted_class === "MSI" && "Good prognosis - Microsatellite unstable"}
                      {predictionResult.molecular_subtype.predicted_class === "CN_LOW" && "Moderate prognosis - Copy number low"}
                      {predictionResult.molecular_subtype.predicted_class === "CN_HIGH" && "Poor prognosis - Copy number high"}
                    </div>
                  </CardContent>
                </Card>
              )}

              {/* Survival Prediction */}
              {riskInfo && predictionResult.survival && (
                <Card className={`${riskInfo.bgColor} border-2 shadow-lg`}>
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-2">
                      <TrendingUp className={`h-5 w-5 ${riskInfo.color}`} />
                      <CardTitle className="text-sm">Survival Prediction</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className={`text-3xl font-bold ${riskInfo.color} mb-2`}>
                      {predictionResult.survival.prediction}
                    </p>
                    <p className={`text-2xl font-semibold ${riskInfo.color} mb-2`}>
                      {predictionResult.survival.risk_category}
                    </p>
                    <p className="text-sm text-muted-foreground mb-4">
                      Survival Probability: {(predictionResult.survival.survival_probability * 100).toFixed(1)}%
                    </p>
                    <div className="mt-4">
                      <Progress 
                        value={predictionResult.survival.survival_probability * 100} 
                        className="h-2"
                      />
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Clinical Interpretation */}
            <Card className="bg-gradient-to-br from-muted/30 to-muted/10 shadow-lg">
              <CardHeader>
                <CardTitle className="text-base flex items-center gap-2">
                  <Dna className="h-5 w-5 text-primary" />
                  Clinical Interpretation
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm">
                {predictionResult.molecular_subtype.predicted_class === "CN_HIGH" && (
                  <>
                    <p className="font-semibold text-red-600">• Copy Number High (CN-High) subtype detected</p>
                    <p>• Associated with aggressive disease and poorer outcomes</p>
                    <p>• Consider intensive treatment protocols and close monitoring</p>
                    <p>• Regular follow-up and surveillance recommended</p>
                  </>
                )}
                {predictionResult.molecular_subtype.predicted_class === "CN_LOW" && (
                  <>
                    <p className="font-semibold text-orange-600">• Copy Number Low (CN-Low) subtype detected</p>
                    <p>• Moderate prognosis with standard treatment approaches</p>
                    <p>• Follow standard treatment guidelines</p>
                    <p>• Regular monitoring recommended</p>
                  </>
                )}
                {predictionResult.molecular_subtype.predicted_class === "MSI" && (
                  <>
                    <p className="font-semibold text-yellow-600">• Microsatellite Instable (MSI) subtype detected</p>
                    <p>• Generally favorable prognosis</p>
                    <p>• May benefit from immunotherapy approaches</p>
                    <p>• Standard surveillance protocols recommended</p>
                  </>
                )}
                {predictionResult.molecular_subtype.predicted_class === "POLE" && (
                  <>
                    <p className="font-semibold text-green-600">• POLE-mutated subtype detected</p>
                    <p>• Excellent prognosis with favorable outcomes</p>
                    <p>• May benefit from less aggressive treatment</p>
                    <p>• Standard follow-up protocols sufficient</p>
                  </>
                )}
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default Molecular;
