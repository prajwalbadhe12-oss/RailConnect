from app.data import TRAINS


def get_all_trains():
    return TRAINS


def get_train_by_id(train_id):
    for train in TRAINS:
        if train["id"] == train_id:
            return train

    return None


def search_trains(source, destination):
    source = source.strip().lower()
    destination = destination.strip().lower()

    results = []

    for train in TRAINS:
        if (
            train["source"].lower() == source
            and train["destination"].lower() == destination
        ):
            results.append(train)

    return results