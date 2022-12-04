"""Views for search results"""
import os
import json
import statistics
import requests

from django.shortcuts import render
from ..models import Subdepartment


def search(request):
    """Search results view."""

    # Set query
    query = request.GET.get('q', '')

    # Fetch Elasticsearch data
    courses = fetch_courses(query)
    instructors = fetch_instructors(query)

    courses_first = decide_order(query, courses, instructors)

    # Set arguments for template view
    args = set_arguments(query, courses, instructors, courses_first)
    context_vars = args

    # Load template view
    return render(request, 'search/search.html', context_vars)


def decide_order(query, courses, instructors):
    """Decides if courses or instructors should be displayed first.
    Returns True if courses should be prioritized, False if instructors should be prioritized """

    # Calculate z-score for courses
    courses_z = compute_zscore([x['score'] for x in courses['results']])

    # Calculate z-score for instructors
    instructors_z = compute_zscore([x['score'] for x in instructors['results']])

    # Likely an abbreviation if 4 letters or less
    if len(query) <= 4 and courses_z > 0:
        return True

    return courses_z >= instructors_z


def compute_zscore(scores):
    """Computes and returns the z_score from the list
     and gets the z-score of the highest z-score."""
    if len(scores) > 1:
        mean = statistics.mean(scores)

        stddev = statistics.stdev(scores, mean)

        if stddev == 0:
            stddev = 1
        z_score = scores[0] - mean
        z_score /= stddev

        return z_score
    # Returns 0 for only one item (can't compute z-score) or -1 if no items
    if len(scores) == 1:
        return 0

    return -1


def fetch_courses(query):
    """Gets Elasticsearch course data."""
    api_endpoint = os.environ['ELASTICSEARCH_ENDPOINT'] + 'tcf-courses/search'
    algorithm = rank_course(query)
    response = fetch_elasticsearch(api_endpoint, algorithm)
    return format_response(response)


def fetch_instructors(query):
    """Gets Elasticsearch instructor data."""
    api_endpoint = os.environ['ELASTICSEARCH_ENDPOINT'] + 'tcf-instructors/search'
    algorithm = rank_instructor(query)
    response = fetch_elasticsearch(api_endpoint, algorithm)
    return format_response(response)


def fetch_elasticsearch(api_endpoint, algorithm):
    """Requests a Document API using a specific search algorithm."""
    api_key = os.environ['ES_PUBLIC_API_KEY']
    https_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }
    try:
        response = requests.get(
            url=api_endpoint,
            headers=https_headers,
            params=algorithm,
            timeout=5
        )
        if response.status_code != 200:
            response = {
                "error": True,
                "message": "GET request failed w/ status code " +
                           str(response.status_code)
            }
        return response
    except requests.RequestException as error:
        response = {
            "error": True,
            "message": "GET request failed w/ error " + str(error)
        }
        return response


def rank_instructor(query):
    """Returns the instructors search algorithm."""
    algorithm = {
        "query": query
    }
    return algorithm  # improve algorithm later


def rank_course(query):
    """Returns the courses search algorithm."""
    #
    algorithm = {
        "query": query,
        # "page": {
        #     "current": 1,
        #     "size": 15
        # },
        # "search_fields": {
        #     "mnemonic": {
        #         "weight": 10
        #     },
        #     "title": {
        #         "weight": 8
        #     },
        #     "description": {
        #         "weight": 5
        #     }
        # },
        # "boosts": {
        #     "review_count": {
        #         "type": "functional",
        #         "function": "logarithmic",
        #         "operation": "multiply",
        #         "factor": 2
        #     }
        # }
    }
    return algorithm


def format_response(response):
    """Formats an Elastic search endpoint response."""
    formatted = {
        "error": False,
        "results": []
    }
    if "error" in response:
        formatted["error"] = True
        return formatted

    body = json.loads(response.text)
    engine = body.get("meta").get("engine").get("name")
    results = body.get("results")
    if engine == "tcf-courses":
        formatted["results"] = format_courses(results)
    elif engine == "tcf-instructors":
        formatted["results"] = format_instructors(results)
    else:
        formatted["error"] = True
        formatted["message"] = "Unknown engine, please verify engine exists"

    return formatted


def format_courses(results):
    """Formats courses engine results."""
    formatted = []
    for result in results:
        course = {
            "id": result.get("_meta").get("id"),
            "title": result.get("title").get("raw"),
            "number": result.get("number").get("raw"),
            "mnemonic": result.get("mnemonic").get("raw"),
            "description": result.get("description").get("raw"),
            "score": result.get("_meta").get("score"),
        }
        formatted.append(course)
    return formatted


def format_instructors(results):
    """Formats instructors engine results."""
    formatted = []
    for result in results:
        instructor = {
            "id": result.get("_meta").get("id"),
            "first_name": result.get("first_name").get("raw"),
            "last_name": result.get("last_name").get("raw"),
            "email": result.get("email").get("raw"),
            "website": result.get("website").get("raw"),
            "score": result.get("_meta").get("score"),
        }
        formatted.append(instructor)
    return formatted


def set_arguments(query, courses, instructors, courses_first):
    """Sets the search template arguments."""
    args = {
        "query": query
    }
    if not courses["error"]:
        args["courses"] = group_by_dept(courses['results'])
    if not instructors["error"]:
        args["instructors"] = instructors["results"]

    args["courses_first"] = courses_first

    args["displayed_query"] = query[:30] + "..." if len(query) > 30 else query
    return args


def group_by_dept(courses):
    """Groups courses by their department and adds relevant data."""
    grouped_courses = {}
    for course in courses:
        course_dept = course['mnemonic'][:course['mnemonic'].index(' ')]
        if course_dept not in grouped_courses:
            subdept = Subdepartment.objects.filter(mnemonic=course_dept)[0]
            # should only ever have one returned with that mnemonic
            grouped_courses[course_dept] = {
                "subdept_name": subdept.name,
                "dept_id": subdept.department_id,
                "courses": []
            }
        grouped_courses[course_dept]["courses"].append(course)

    return grouped_courses
