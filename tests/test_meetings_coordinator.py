from unittest import TestCase

import pytest

from meetings_coordinator.meetings_coordinator import get_available_time_slots


@pytest.mark.parametrize('calendars,time_slots', [
    ([], []),
    (
        [
            {
                'name': 'Betty',
                'meetings': [
                    {
                        'startTime': '2021-03-10T08:55:39+00:00',
                        'endTime': '2021-03-10T09:15:39+00:00',
                        'subject': 'Meeting 1'
                    }
                ]
            }
        ],
        [
            {
                'startTime': '2021-03-10T00:00:00+00:00',
                'endTime': '2021-03-10T08:55:39+00:00'
            },
            {
                'startTime': '2021-03-10T09:15:39+00:00',
                'endTime': '2021-03-10T23:59:59+00:00'
            }
        ]
    ),
    (
        [
            {
                'name': 'Betty',
                'meetings': [
                    {
                        'startTime': '2021-03-10T08:55:39+00:00',
                        'endTime': '2021-03-10T09:15:39+00:00',
                        'subject': 'Meeting 1'
                    },
                    {
                        'startTime': '2021-03-10T09:55:39+00:00',
                        'endTime': '2021-03-10T10:15:39+00:00',
                        'subject': 'Meeting 2'
                    },
                    {
                        'startTime': '2021-03-10T11:55:39+00:00',
                        'endTime': '2021-03-10T12:15:39+00:00',
                        'subject': 'Meeting 3'
                    }
                ]
            },
            {
                'name': 'John',
                'meetings': [
                    {
                        'startTime': '2021-03-10T08:15:39+00:00',
                        'endTime': '2021-03-10T09:55:39+00:00',
                        'subject': 'Meeting a'
                    },
                    {
                        'startTime': '2021-03-10T10:15:39+00:00',
                        'endTime': '2021-03-10T10:55:39+00:00',
                        'subject': 'Meeting b'
                    },
                    {
                        'startTime': '2021-03-10T11:15:39+00:00',
                        'endTime': '2021-03-10T12:55:39+00:00',
                        'subject': 'Meeting c'
                    }
                ]
            }
        ],
        [
            {
                'startTime': '2021-03-10T00:00:00+00:00',
                'endTime': '2021-03-10T08:15:39+00:00'
            },
            {
                'startTime': '2021-03-10T10:55:39+00:00',
                'endTime': '2021-03-10T11:15:39+00:00'
            },
            {
                'startTime': '2021-03-10T12:55:39+00:00',
                'endTime': '2021-03-10T23:59:59+00:00'
            }
        ]
    ),
    (
        [
            {
                'name': 'Betty',
                'meetings': [
                    {
                        'startTime': '2021-03-10T00:00:00+00:00',
                        'endTime': '2021-03-10T12:00:00+00:00',
                        'subject': 'Meeting 1'
                    }
                ]
            },
            {
                'name': 'John',
                'meetings': [
                    {
                        'startTime': '2021-03-10T12:00:00+00:00',
                        'endTime': '2021-03-10T23:59:59+00:00',
                        'subject': 'Meeting a'
                    }
                ]
            }
        ],
        []
    ),
])
def test_meetings_coordinator(calendars: list, time_slots: list) -> None:
    results = get_available_time_slots(calendars_list=calendars)
    TestCase().assertListEqual(results, time_slots)
