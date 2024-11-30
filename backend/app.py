from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from pulp import *
import io
import json
from collections import defaultdict

app = Flask(__name__)
CORS(app)

# Global dictionaries for resource management
resource_availability = {
    'CPAP': 100,
    'Blood_Glucose_Monitors': 150,
    'Blood_Pressure_Monitors': 200,
    'Nebulizers': 80,
    'Rehabilitation_Equipment': 120,
    'Nursing_Staff': 50,
    'Mental_Health_Professionals': 30,
    'Physical_Therapists': 25,
    'Dermatological_Treatments': 40,
    'Endocrinologists': 20,
    'Air_Purifiers': 60,
    'Hydration_Equipment': 70,
    'Imaging_Equipment': 90,
    'Oncologists': 50,
    'Gastroenterologists': 30,
    'Pain_Management_Equipment': 40,
    'ENT_Specialists': 15,
    'Neurologists': 35,
    'Vaccination_Programs': 50,
    'Eye_Care_Equipment': 25,
    'Nephrologists': 20,
    'Pulmonologists': 15,
    'Cardiologists': 40,
    'Respiratory_Therapies': 30,
    'Critical_Care_Equipment': 50,
    'Behavioral_Therapists': 20,
    'Developmental_Therapists': 10,
    'Orthopedic_Surgeons': 15,
    'Hematologists': 20,
    'Gynecologists': 25,
    'Infectious_Disease_Specialists': 25,
    'Rheumatologists': 25
}

# You'll need to define these dictionaries before using the function
disease_resource = {
    "common_cold": ["Nursing_Staff", "Thermometers"],
    "asthma": ["CPAP", "Nebulizers"],
    "depression": ["Mental_Health_Professionals"],
    "diabetes": ["Blood_Glucose_Monitors"],
    "heart_disease": ["Blood_Pressure_Monitors"],
    "arthritis": ["Rehabilitation_Equipment", "Physical_Therapists"],
    "influenza": ["Nursing_Staff", "Thermometers"],
    "eczema": ["Dermatological_Treatments"],
    "hyperthyroidism": ["Endocrinologists"],
    "allergic_rhinitis": ["Air_Purifiers"],
    "anxiety_disorders": ["Mental_Health_Professionals"],
    "gastroenteritis": ["Hydration_Equipment"],
    "pancreatitis": ["Imaging_Equipment"],
    "rheumatoid_arthritis": ["Rehabilitation_Equipment", "Physical_Therapists"],
    "liver_cancer": ["Oncologists", "Imaging_Equipment"],
    "stroke": ["Rehabilitation_Equipment", "Physical_Therapists"],
    "urinary_tract_infection": ["Hydration_Equipment"],
    "dengue_fever": ["Hydration_Equipment", "Nursing_Staff"],
    "hepatitis": ["Gastroenterologists"],
    "kidney_cancer": ["Oncologists", "Imaging_Equipment"],
    "migraine": ["Pain_Management_Equipment"],
    "muscular_dystrophy": ["Physical_Therapists"],
    "sinusitis": ["ENT_Specialists"],
    "ulcerative_colitis": ["Gastroenterologists"],
    "bipolar_disorder": ["Mental_Health_Professionals"],
    "bronchitis": ["Nebulizers", "CPAP"],
    "cerebral_palsy": ["Rehabilitation_Equipment", "Physical_Therapists"],
    "colorectal_cancer": ["Oncologists", "Imaging_Equipment"],
    "hypertensive_heart_disease": ["Blood_Pressure_Monitors"],
    "multiple_sclerosis": ["Neurologists", "Rehabilitation_Equipment"],
    "myocardial_infarction": ["Cardiologists", "CPAP"],
    "osteoporosis": ["Bone_Density_Scanners"],
    "atherosclerosis": ["Cardiologists"],
    "chronic_obstructive_pulmonary_disease": ["Nebulizers", "CPAP"],
    "epilepsy": ["Neurologists"],
    "hypertension": ["Blood_Pressure_Monitors"],
    "obsessive_compulsive_disorder": ["Mental_Health_Professionals"],
    "psoriasis": ["Dermatological_Treatments"],
    "rubella": ["Vaccination_Programs"],
    "cirrhosis": ["Gastroenterologists"],
    "conjunctivitis": ["Eye_Care_Equipment"],
    "kidney_disease": ["Nephrologists"],
    "osteoarthritis": ["Rehabilitation_Equipment", "Physical_Therapists"],
    "klinefelter_syndrome": ["Endocrinologists"],
    "acne": ["Dermatological_Treatments"],
    "brain_tumor": ["Oncologists", "Imaging_Equipment"],
    "cystic_fibrosis": ["Pulmonologists", "CPAP"],
    "glaucoma": ["Eye_Care_Equipment"],
    "rabies": ["Vaccination_Programs"],
    "chickenpox": ["Vaccination_Programs"],
    "coronary_artery_disease": ["Cardiologists", "Blood_Pressure_Monitors"],
    "eating_disorders": ["Mental_Health_Professionals"],
    "fibromyalgia": ["Pain_Management_Equipment"],
    "hemophilia": ["Hematologists"],
    "hypoglycemia": ["Blood_Glucose_Monitors"],
    "lymphoma": ["Oncologists"],
    "tuberculosis": ["Respiratory_Therapies"],
    "autism_spectrum_disorder": ["Behavioral_Therapists"],
    "crohns_disease": ["Gastroenterologists"],
    "hyperglycemia": ["Blood_Glucose_Monitors"],
    "melanoma": ["Dermatological_Treatments"],
    "ovarian_cancer": ["Oncologists", "Imaging_Equipment"],
    "turner_syndrome": ["Endocrinologists"],
    "zika_virus": ["Hydration_Equipment"],
    "cataracts": ["Eye_Care_Equipment"],
    "anemia": ["Hematologists"],
    "cholera": ["Hydration_Equipment"],
    "endometriosis": ["Gynecologists"],
    "sepsis": ["Critical_Care_Equipment"],
    "sleep_apnea": ["CPAP"],
    "down_syndrome": ["Developmental_Therapists"],
    "ebola_virus": ["Critical_Care_Equipment"],
    "lyme_disease": ["Infectious_Disease_Specialists"],
    "pancreatic_cancer": ["Oncologists", "Imaging_Equipment"],
    "pneumothorax": ["Respiratory_Therapies"],
    "esophageal_cancer": ["Oncologists", "Imaging_Equipment"],
    "hiv_aids": ["Infectious_Disease_Specialists"],
    "marfan_syndrome": ["Cardiologists"],
    "parkinsons_disease": ["Neurologists", "Rehabilitation_Equipment"],
    "polycystic_ovary_syndrome": ["Gynecologists"],
    "systemic_lupus_erythematosus": ["Rheumatologists"],
    "typhoid_fever": ["Infectious_Disease_Specialists"],
    "breast_cancer": ["Oncologists", "Imaging_Equipment"],
    "osteomyelitis": ["Orthopedic_Surgeons"],
    "polio": ["Rehabilitation_Equipment", "Physical_Therapists"],
    "chronic_kidney_disease": ["Nephrologists"],
    "hepatitis_b": ["Gastroenterologists"],
    "prader_willi_syndrome": ["Behavioral_Therapists"],
    "thyroid_cancer": ["Oncologists", "Imaging_Equipment"],
    "bladder_cancer": ["Oncologists", "Imaging_Equipment"],
    "otitis_media": ["ENT_Specialists"],
    "tourette_syndrome": ["Neurologists"],
    "alzheimers_disease": ["Neurologists", "Rehabilitation_Equipment"],
    "dementia": ["Neurologists", "Rehabilitation_Equipment"],
    "diverticulitis": ["Gastroenterologists"],
    "mumps": ["Vaccination_Programs"],
    "cholecystitis": ["Gastroenterologists"],
    "prostate_cancer": ["Oncologists", "Imaging_Equipment"],
    "schizophrenia": ["Mental_Health_Professionals"],
    "gout": ["Rheumatologists"],
    "testicular_cancer": ["Oncologists", "Imaging_Equipment"],
    "tonsillitis": ["ENT_Specialists"],
    "williams_syndrome": ["Behavioral_Therapists"]
}

resource_demand_factors = {
    "Nursing_Staff": 0.1,  # Assuming 1 nurse per 10 patients
    "Thermometers": 0.5,   # Assuming 1 thermometer per 2 patients
    "CPAP": 0.3,           # Assuming 1 CPAP machine per 3 patients
    "Nebulizers": 0.4,     # Assuming 1 nebulizer per 2.5 patients
    "Mental_Health_Professionals": 0.1,  # 1 professional per 10 patients
    "Blood_Glucose_Monitors": 0.3,       # 1 monitor per 3 patients
    "Blood_Pressure_Monitors": 0.2,      # 1 monitor per 5 patients
    "Rehabilitation_Equipment": 0.15,    # 1 set of equipment per ~7 patients
    "Dermatological_Treatments": 0.25,   # 1 treatment per 4 patients
    "Endocrinologists": 0.05,            # 1 endocrinologist per 20 patients
    "Air_Purifiers": 0.2,                # 1 air purifier per 5 patients
    "Hydration_Equipment": 0.3,          # 1 set of hydration equipment per 3 patients
    "Imaging_Equipment": 0.1,            # 1 imaging machine per 10 patients
    "Oncologists": 0.05,                 # 1 oncologist per 20 patients
    "Pain_Management_Equipment": 0.25,   # 1 set of equipment per 4 patients
    "ENT_Specialists": 0.05,             # 1 ENT specialist per 20 patients
    "Neurologists": 0.05,                # 1 neurologist per 20 patients
    "Vaccination_Programs": 0.4,         # 1 vaccination set per 2.5 patients
    "Eye_Care_Equipment": 0.15,          # 1 set of eye care equipment per 7 patients
    "Nephrologists": 0.05,               # 1 nephrologist per 20 patients
    "Pulmonologists": 0.05,              # 1 pulmonologist per 20 patients
    "Cardiologists": 0.05,               # 1 cardiologist per 20 patients
    "Respiratory_Therapies": 0.3,        # 1 therapy set per 3 patients
    "Critical_Care_Equipment": 0.2,      # 1 set of equipment per 5 patients
    "Behavioral_Therapists": 0.05,       # 1 therapist per 20 patients
    "Developmental_Therapists": 0.02,    # 1 therapist per 50 patients
    "Orthopedic_Surgeons": 0.05,         # 1 surgeon per 20 patients
    "Hematologists": 0.05,               # 1 hematologist per 20 patients
    "Gynecologists": 0.05,               # 1 gynecologist per 20 patients
    "Infectious_Disease_Specialists": 0.05,  # 1 specialist per 20 patients
    "Rheumatologists": 0.05              # 1 rheumatologist per 20 patients
}


def process_data(data):
    """Process uploaded data and perform initial preprocessing"""
    # Create disease_outcome column
    data['Disease_Outcome'] = data['Disease'] + '_' + data['Outcome Variable'].str.lower()

    # Define and process binary columns
    binary_columns = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']
    for col in binary_columns:
        data[col] = data[col].map({'Yes': 1, 'No': 0})

    # Encode categorical variables
    categorical_columns = ['Gender', 'Blood Pressure', 'Cholesterol Level']
    for col in categorical_columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])

    return data, binary_columns, categorical_columns


def perform_clustering(data, features):
    """Perform clustering on the processed data"""
    X = data[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Find optimal number of clusters
    silhouette_scores = []
    K = range(2, 10)
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        score = silhouette_score(X_scaled, kmeans.labels_)
        silhouette_scores.append(score)

    optimal_k = K[np.argmax(silhouette_scores)]
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    return clusters, optimal_k, X_scaled


def assess_cluster_risk(cluster_data, binary_columns):
    """Assess risk level for a cluster"""
    risk_factors = {
        'high_symptoms': cluster_data[binary_columns].mean().mean(),
        'age_factor': cluster_data['Age'].mean() / 100,
        'difficulty_breathing': cluster_data['Difficulty Breathing'].mean(),
        'blood_pressure': cluster_data['Blood Pressure'].mean() / 2
    }

    risk_score = (
            risk_factors['high_symptoms'] * 0.3 +
            risk_factors['age_factor'] * 0.3 +
            risk_factors['difficulty_breathing'] * 0.2 +
            risk_factors['blood_pressure'] * 0.2
    )

    if risk_score > 0.7:
        return "High Risk"
    elif risk_score > 0.4:
        return "Medium Risk"
    else:
        return "Low Risk"


def create_lp_model(cluster_demands, risk_levels, resource_availability):
    """Create and solve the linear programming model"""
    prob = LpProblem("Healthcare_Resource_Allocation", LpMaximize)

    # Decision variables
    x = LpVariable.dicts("allocation",
                         ((i, j) for i in cluster_demands.keys()
                          for j in resource_availability.keys()),
                         lowBound=0,
                         cat='Continuous')

    # Risk weights
    risk_weights = {
        "High Risk": 3,
        "Medium Risk": 2,
        "Low Risk": 1
    }

    # Objective function
    prob += lpSum([risk_weights[risk_levels[i]] * x[i, j]
                   for i in cluster_demands.keys()
                   for j in resource_availability.keys()])

    # Constraints
    for j in resource_availability:
        prob += lpSum(x[i, j] for i in cluster_demands.keys()) <= resource_availability[j]

    for i in cluster_demands:
        for j in resource_availability:
            if j in cluster_demands[i]:
                prob += x[i, j] <= cluster_demands[i][j]

    return prob, x


@app.route('/api/upload', methods=['POST'])
def upload_data():
    """Handle data upload and initial processing"""
    try:
        file = request.files['file']
        if not file:
            return jsonify({'error': 'No file uploaded'}), 400

        # Read CSV file
        data = pd.read_csv(io.StringIO(file.stream.read().decode("UTF8")))

        # Process data
        processed_data, binary_columns, categorical_columns = process_data(data)

        # Perform clustering
        features = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing',
                    'Age', 'Gender', 'Blood Pressure', 'Cholesterol Level']
        clusters, optimal_k, X_scaled = perform_clustering(processed_data, features)

        # Add clusters to data
        processed_data['Cluster'] = clusters

        # Assess risk levels
        cluster_risks = {}
        for cluster in range(optimal_k):
            cluster_data = processed_data[processed_data['Cluster'] == cluster]
            cluster_risks[cluster] = assess_cluster_risk(cluster_data, binary_columns)

        # Store processed data in session or database here if needed

        return jsonify({
            'message': 'Data processed successfully',
            'clusters': optimal_k,
            'cluster_risks': cluster_risks
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/parameters', methods=['GET', 'PUT'])
def handle_parameters():
    """Get or update resource parameters"""
    global resource_availability

    if request.method == 'GET':
        return jsonify(resource_availability)

    elif request.method == 'PUT':
        try:
            new_params = request.json
            resource_availability.update(new_params)
            return jsonify({
                'message': 'Parameters updated successfully',
                'parameters': resource_availability
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/allocate', methods=['POST'])
def allocate_resources():
    """Perform resource allocation optimization"""
    try:
        # Get cluster data from request
        cluster_data = request.json.get('cluster_data')
        risk_levels = request.json.get('risk_levels')

        # Create and solve LP model
        prob, x = create_lp_model(cluster_data, risk_levels, resource_availability)
        prob.solve()

        # Process results
        if prob.status == 1:  # Optimal solution found
            allocation_results = {}
            for i in cluster_data.keys():
                allocation_results[i] = {
                    'risk_level': risk_levels[i],
                    'allocations': {
                        j: value(x[i, j])
                        for j in resource_availability.keys()
                        if value(x[i, j]) > 0
                    }
                }

            return jsonify({
                'status': 'optimal',
                'objective_value': value(prob.objective),
                'allocations': allocation_results
            })
        else:
            return jsonify({
                'status': 'not optimal',
                'message': 'No optimal solution found'
            }), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    """Get analysis of the current allocation state"""
    try:
        # Implementation would depend on how you're storing state
        # This is a placeholder that returns sample analysis
        analysis = {
            'total_resources_allocated': sum(resource_availability.values()),
            'resource_utilization': {
                resource: {
                    'available': amount,
                    'utilized': amount * 0.8  # Sample utilization
                }
                for resource, amount in resource_availability.items()
            },
            'cluster_statistics': {
                'high_risk_clusters': 2,
                'medium_risk_clusters': 3,
                'low_risk_clusters': 1
            }
        }
        return jsonify(analysis)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
