def recommend_skills(missing_skills):

    recommendations = {

        "python": [
            "pandas",
            "numpy"
        ],

        "machine learning": [
            "scikit-learn",
            "tensorflow"
        ],

        "sql": [
            "mysql",
            "postgresql"
        ],

        "aws": [
            "docker",
            "kubernetes"
        ]
    }

    result = []

    for skill in missing_skills:

        if skill in recommendations:

            result.extend(
                recommendations[skill]
            )

    return list(set(result))