import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):

    month_to_index = {
        "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3,
        "May": 4, "June": 5, "Jul": 6, "Aug": 7,
        "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
    }

    evidence = []
    labels = []

    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        for row in reader:
            evidence.append([
                int(row[0]),                        # Administrative
                float(row[1]),                      # Administrative_Duration
                int(row[2]),                        # Informational
                float(row[3]),                      # Informational_Duration
                int(row[4]),                        # ProductRelated
                float(row[5]),                      # ProductRelated_Duration
                float(row[6]),                      # BounceRates
                float(row[7]),                      # ExitRates
                float(row[8]),                      # PageValues
                float(row[9]),                      # SpecialDay
                month_to_index.get(row[10], 0),     # Month
                int(row[11]),                       # OperatingSystems
                int(row[12]),                       # Browser
                int(row[13]),                       # Region
                int(row[14]),                       # TrafficType
                1 if row[15].strip() == "Returning_Visitor" else 0,  # VisitorType
                1 if row[16].strip().lower() == "true" else 0        # Weekend
            ])

            labels.append(1 if row[17].strip().lower() == "true" else 0)

    return (evidence, labels)



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_positives = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 1)
    true_negatives = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 0)

    total_positives = sum(1 for actual in labels if actual == 1)
    total_negatives = sum(1 for actual in labels if actual == 0)

    sensitivity = true_positives / total_positives if total_positives else 0
    specificity = true_negatives / total_negatives if total_negatives else 0

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
