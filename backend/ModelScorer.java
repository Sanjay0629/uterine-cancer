// Minimal Java scorer that will be called from the FastAPI backend.
// NOTE: You MUST adapt the feature names and types to match your actual H2O model schema.

import java.util.HashMap;
import java.util.Map;

import hex.genmodel.MojoModel;
import hex.genmodel.easy.EasyPredictModelWrapper;
import hex.genmodel.easy.RowData;
import hex.genmodel.easy.exception.PredictException;
import hex.genmodel.easy.prediction.BinomialModelPrediction;

public class ModelScorer {

    // Path to the MOJO model file (relative to backend directory)
    private static final String MOJO_FILE = "models/GBM_grid_1_AutoML_1_20251122_200215_model_3.zip";

    public static void main(String[] args) {
        try {
            // Define feature names in the exact order expected by the H2O model
            String[] featureNames = new String[] {
                "Age",
                "BMI",
                "MenopauseStatus",
                "AbnormalBleeding",
                "PelvicPain",
                "ThickEndometrium",
                "Hypertension",
                "Diabetes",
                "FamilyHistoryCancer",
                "Smoking",
                "EstrogenTherapy",
                "CA125_Level",
                "HistologyType",
                "Parity",
                "Gravidity",
                "HormoneReceptorStatus",
                "VaginalDischarge",
                "UnexplainedWeightLoss"
            };

            if (args.length != featureNames.length) {
                System.err.println("Expected " + featureNames.length + " features, got " + args.length);
                System.exit(1);
            }

            MojoModel mojo = MojoModel.load(MOJO_FILE);
            EasyPredictModelWrapper model = new EasyPredictModelWrapper(mojo);

            RowData row = new RowData();
            for (int i = 0; i < featureNames.length; i++) {
                row.put(featureNames[i], args[i]);
            }

            // Assuming a binomial classification model (adjust if regression or multinomial)
            BinomialModelPrediction p = model.predictBinomial(row);

            // Print a single numeric value (probability of positive class) to stdout
            double positiveProb = p.classProbabilities[1];
            System.out.println(positiveProb);

        } catch (PredictException e) {
            e.printStackTrace();
            System.exit(1);
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}

