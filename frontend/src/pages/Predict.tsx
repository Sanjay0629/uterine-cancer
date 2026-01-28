import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import Navigation from "@/components/Navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { AlertCircle, CheckCircle2, AlertTriangle, Loader2 } from "lucide-react";

interface PredictionFormData {
  patientId: string;
  age: number;
  bmi: number;
  menopauseStatus: string;
  abnormalBleeding: string;
  pelvicPain: string;
  thickEndometrium: number;
  hypertension: string;
  diabetes: string;
  familyHistoryCancer: string;
  smoking: string;
  estrogenTherapy: string;
  ca125Level: number;
  histologyType: string;
  parity: number;
  gravidity: number;
  hormoneReceptorStatus: string;
  vaginalDischarge: string;
  unexplainedWeightLoss: string;
}

const Predict = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [predictionResult, setPredictionResult] = useState<any>(null);
  const { register, handleSubmit, setValue, formState: { errors } } = useForm<PredictionFormData>();

  useEffect(() => {
    register("menopauseStatus", { required: true });
    register("abnormalBleeding", { required: true });
    register("pelvicPain", { required: true });
    register("vaginalDischarge", { required: true });
    register("unexplainedWeightLoss", { required: true });
    register("hypertension", { required: true });
    register("diabetes", { required: true });
    register("familyHistoryCancer", { required: true });
    register("smoking", { required: true });
    register("estrogenTherapy", { required: true });
    register("histologyType", { required: true });
    register("hormoneReceptorStatus", { required: true });
  }, [register]);

  const onSubmit = async (data: PredictionFormData) => {
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          Age: data.age,
          BMI: data.bmi,
          MenopauseStatus: data.menopauseStatus,
          AbnormalBleeding: data.abnormalBleeding,
          PelvicPain: data.pelvicPain,
          ThickEndometrium: data.thickEndometrium,
          Hypertension: data.hypertension,
          Diabetes: data.diabetes,
          FamilyHistoryCancer: data.familyHistoryCancer,
          Smoking: data.smoking,
          EstrogenTherapy: data.estrogenTherapy,
          CA125_Level: data.ca125Level,
          HistologyType: data.histologyType,
          Parity: data.parity,
          Gravidity: data.gravidity,
          HormoneReceptorStatus: data.hormoneReceptorStatus,
          VaginalDischarge: data.vaginalDischarge,
          UnexplainedWeightLoss: data.unexplainedWeightLoss
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error("Backend error response:", errorText);
        throw new Error(`Prediction failed: ${response.status} ${response.statusText}. ${errorText}`);
      }

      const result = await response.json();
      console.log("Prediction result:", result);
      setPredictionResult(result);
      setShowResults(true);

      // Scroll to results
      setTimeout(() => {
        document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage = error instanceof Error ? error.message : "Unknown error";
      alert(`Failed to get prediction: ${errorMessage}\n\nPlease ensure the backend is running on http://localhost:8000`);
    } finally {
      setIsLoading(false);
    }
  };

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
          <h1 className="mb-2 text-4xl font-bold text-foreground">
            Synthetic Uterine Cancer Prediction
          </h1>
          <p className="text-muted-foreground">
            Enter patient clinical data to assess uterine cancer risk
          </p>
        </div>

        <Card className="mx-auto max-w-4xl shadow-lg">
          <CardHeader>
            <CardTitle>Patient Information</CardTitle>
            <CardDescription>
              All fields are required for accurate risk prediction
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* Patient ID and Demographics */}
              <div className="grid gap-6 md:grid-cols-2">
                <div className="space-y-2">
                  <Label htmlFor="patientId">Patient ID</Label>
                  <Input
                    id="patientId"
                    placeholder="P001"
                    {...register("patientId", { required: true })}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="age">Age</Label>
                  <Input
                    id="age"
                    type="number"
                    placeholder="55"
                    {...register("age", { required: true, min: 0, max: 120, valueAsNumber: true })}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="bmi">BMI</Label>
                  <Input
                    id="bmi"
                    type="number"
                    step="0.1"
                    placeholder="26.8"
                    {...register("bmi", { required: true, min: 10, max: 60, valueAsNumber: true })}
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="menopauseStatus">Menopause Status</Label>
                  <Select onValueChange={(value) => setValue("menopauseStatus", value, { shouldValidate: true })}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select status" />
                    </SelectTrigger>
                    <SelectContent className="bg-popover">
                      <SelectItem value="Pre-menopausal">Pre-menopausal</SelectItem>
                      <SelectItem value="Post-menopausal">Post-menopausal</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Clinical Symptoms */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Clinical Symptoms</h3>
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="abnormalBleeding">Abnormal Bleeding</Label>
                    <Select onValueChange={(value) => setValue("abnormalBleeding", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="pelvicPain">Pelvic Pain</Label>
                    <Select onValueChange={(value) => setValue("pelvicPain", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="vaginalDischarge">Vaginal Discharge</Label>
                    <Select onValueChange={(value) => setValue("vaginalDischarge", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="unexplainedWeightLoss">Unexplained Weight Loss</Label>
                    <Select onValueChange={(value) => setValue("unexplainedWeightLoss", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              {/* Medical History */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Medical History</h3>
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="hypertension">Hypertension</Label>
                    <Select onValueChange={(value) => setValue("hypertension", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="diabetes">Diabetes</Label>
                    <Select onValueChange={(value) => setValue("diabetes", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="familyHistoryCancer">Family History of Cancer</Label>
                    <Select onValueChange={(value) => setValue("familyHistoryCancer", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="smoking">Smoking</Label>
                    <Select onValueChange={(value) => setValue("smoking", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="estrogenTherapy">Estrogen Therapy</Label>
                    <Select onValueChange={(value) => setValue("estrogenTherapy", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Yes">Yes</SelectItem>
                        <SelectItem value="No">No</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>
              </div>

              {/* Clinical Measurements */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Clinical Measurements</h3>
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="thickEndometrium">Endometrium Thickness (mm)</Label>
                    <Input
                      id="thickEndometrium"
                      type="number"
                      step="0.1"
                      placeholder="14.5"
                      {...register("thickEndometrium", { required: true, min: 0, valueAsNumber: true })}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="ca125Level">CA125 Level (U/mL)</Label>
                    <Input
                      id="ca125Level"
                      type="number"
                      step="0.1"
                      placeholder="38.2"
                      {...register("ca125Level", { required: true, min: 0, valueAsNumber: true })}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="parity">Parity</Label>
                    <Input
                      id="parity"
                      type="number"
                      placeholder="2"
                      {...register("parity", { required: true, min: 0, valueAsNumber: true })}
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="gravidity">Gravidity</Label>
                    <Input
                      id="gravidity"
                      type="number"
                      placeholder="3"
                      {...register("gravidity", { required: true, min: 0, valueAsNumber: true })}
                    />
                  </div>
                </div>
              </div>

              {/* Pathology */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">Pathology</h3>
                <div className="grid gap-6 md:grid-cols-2">
                  <div className="space-y-2">
                    <Label htmlFor="histologyType">Histology Type</Label>
                    <Select onValueChange={(value) => setValue("histologyType", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select type" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Endometrioid">Endometrioid</SelectItem>
                        <SelectItem value="Serous">Serous</SelectItem>
                        <SelectItem value="ClearCell">Clear Cell</SelectItem>
                        <SelectItem value="Other">Other</SelectItem>
                        <SelectItem value="None">None (Benign/Healthy)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="hormoneReceptorStatus">Hormone Receptor Status</Label>
                    <Select onValueChange={(value) => setValue("hormoneReceptorStatus", value, { shouldValidate: true })}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select status" />
                      </SelectTrigger>
                      <SelectContent className="bg-popover">
                        <SelectItem value="Positive">Positive</SelectItem>
                        <SelectItem value="Negative">Negative</SelectItem>
                        <SelectItem value="NotApplicable">Not Applicable</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
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
                    Analyzing...
                  </>
                ) : (
                  "Predict Cancer Risk"
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Results Section */}
        {showResults && predictionResult && (() => {
          // Extract probability of positive class (Cancer = 1)
          const p1 = parseFloat(predictionResult.p1) || 0;
          const riskProbability = p1 * 100; // Convert to percentage
          
          // Determine risk level based on thresholds
          const getRiskLevel = (prob: number): { level: string; color: string; bgColor: string } => {
            if (prob >= 0.71) {
              return { level: "High Risk", color: "text-red-600", bgColor: "bg-red-50 border-red-200" };
            } else if (prob >= 0.31) {
              return { level: "Moderate Risk", color: "text-orange-600", bgColor: "bg-orange-50 border-orange-200" };
            } else {
              return { level: "Low Risk", color: "text-green-600", bgColor: "bg-green-50 border-green-200" };
            }
          };
          
          const riskInfo = getRiskLevel(p1);
          const predictedClass = predictionResult.predict === "1" ? "Yes" : "No";
          
          return (
            <div id="results" className="mx-auto mt-8 max-w-4xl space-y-6">
              <h2 className="text-2xl font-bold text-center">Prediction Results</h2>

              <div className="grid gap-6 md:grid-cols-2">
                {/* Risk Probability */}
                <Card className={`${riskInfo.bgColor} border-2`}>
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-2">
                      <AlertCircle className={`h-5 w-5 ${riskInfo.color}`} />
                      <CardTitle className="text-sm">Risk Probability</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className={`text-4xl font-bold ${riskInfo.color}`}>
                      {riskProbability.toFixed(2)}%
                    </p>
                  </CardContent>
                </Card>

                {/* Risk Level */}
                <Card className={`${riskInfo.bgColor} border-2`}>
                  <CardHeader className="pb-3">
                    <div className="flex items-center gap-2">
                      <AlertTriangle className={`h-5 w-5 ${riskInfo.color}`} />
                      <CardTitle className="text-sm">Risk Level</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className={`text-4xl font-bold ${riskInfo.color}`}>
                      {riskInfo.level}
                    </p>
                  </CardContent>
                </Card>
              </div>

              {/* Clinical Recommendations - Dynamic based on risk level */}
              <Card className="bg-muted/30">
                <CardHeader>
                  <CardTitle className="text-base">Clinical Recommendations</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-sm">
                  {p1 >= 0.71 ? (
                    <>
                      <p className="font-semibold text-red-600">• Immediate referral to oncology specialist</p>
                      <p>• Comprehensive imaging and biopsy recommended</p>
                      <p>• Discuss treatment options including surgery and adjuvant therapy</p>
                      <p>• Schedule follow-up within 2 weeks</p>
                      <p>• Consider genetic counseling and family history assessment</p>
                    </>
                  ) : p1 >= 0.31 ? (
                    <>
                      <p className="font-semibold text-orange-600">• Schedule follow-up appointment within 1-2 months</p>
                      <p>• Consider additional diagnostic imaging</p>
                      <p>• Monitor symptoms and risk factors closely</p>
                      <p>• Discuss lifestyle modifications and preventive measures</p>
                      <p>• Regular screening recommended</p>
                    </>
                  ) : (
                    <>
                      <p className="font-semibold text-green-600">• Continue routine screening as recommended</p>
                      <p>• Maintain healthy lifestyle and regular check-ups</p>
                      <p>• Monitor any changes in symptoms</p>
                      <p>• Follow standard preventive care guidelines</p>
                    </>
                  )}
                </CardContent>
              </Card>

            </div>
          );
        })()}
      </div>
    </div>
  );
};


export default Predict;
