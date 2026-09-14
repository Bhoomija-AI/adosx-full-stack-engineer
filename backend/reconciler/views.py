from django.http import JsonResponse

from .services.comparator import compare_records


def discrepancies_view(request):
    org_id = request.GET.get("org_id")
    reason = request.GET.get("reason")

    if not org_id:
        return JsonResponse(
            {"error": "org_id is required"},
            status=400,
        )

    discrepancies = compare_records()

    results = []

    for item in discrepancies:
        if item.org_id != org_id:
            continue

        if reason and item.reason != reason:
            continue

        results.append(
            {
                "reason": item.reason,
                "record_id": item.record_id,
                "location_id": item.location_id,
                "org_id": item.org_id,
                "value_a": item.value_a,
                "value_b": item.value_b,
            }
        )

    return JsonResponse(
        {
            "count": len(results),
            "results": results,
        }
    )