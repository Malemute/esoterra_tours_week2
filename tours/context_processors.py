from tours.data import departures, description, subtitle, title


def depart(request) -> dict:
    return {
        'departures': departures,
        'description': description,
        'subtitle': subtitle,
        'title': title,
    }
