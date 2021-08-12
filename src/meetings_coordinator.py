#!/usr/bin/env python3

import argparse
import json
import logging
from argparse import Namespace
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s: %(message)s')
logger = logging.getLogger('meetings_coordinator')


class Meeting(BaseModel):
    start_time: datetime = Field(default_factory=datetime.fromisocalendar, alias='startTime')
    end_time: datetime = Field(default_factory=datetime.fromisocalendar, alias='endTime')
    subject: str

    def __lt__(self, other: "Meeting") -> bool:
        return self.start_time < other.start_time


class Calendar(BaseModel):
    name: str
    meetings: List[Meeting]


class TimeSlot(BaseModel):
    start_time: str = Field(alias='startTime')
    end_time: str = Field(alias='endTime')


def get_beginning_of_day(date: datetime) -> datetime:
    return date.replace(hour=0, minute=0, second=0, microsecond=0)


def get_end_of_day(date: datetime) -> datetime:
    return date.replace(hour=23, minute=59, second=59, microsecond=0)


def get_available_time_slots(calendars_list: list) -> list:
    time_slots = []
    calendars = [Calendar(**calendar_dict) for calendar_dict in calendars_list]
    logger.info("Sorting calenders by min start_time")
    meetings = sorted([m for c in calendars for m in c.meetings])

    if not meetings:
        raise Exception("No meetings were provided")

    min_meeting = meetings[0]
    max_end_time = min_meeting.end_time

    min_start_time = min_meeting.start_time
    if (beginning_of_day := get_beginning_of_day(min_start_time)) < min_start_time:
        logger.info("Adding beginning-of-day time slot")
        time_slots.append(TimeSlot(startTime=beginning_of_day.isoformat(), endTime=min_start_time.isoformat()))

    for meeting in meetings[1:]:

        if meeting.end_time > max_end_time:
            max_end_time = meeting.end_time

        if meeting.start_time > min_meeting.end_time:
            logger.info(f"Found new slot - start time: {min_meeting.end_time}, end time: {meeting.start_time}")
            time_slots.append(
                TimeSlot(startTime=min_meeting.end_time.isoformat(), endTime=meeting.start_time.isoformat())
            )

        if meeting.end_time > min_meeting.end_time:
            min_meeting = meeting

    if (end_of_day := get_end_of_day(max_end_time)) > max_end_time:
        logger.info("Adding end-of-day time slot")
        time_slots.append(TimeSlot(startTime=max_end_time.isoformat(), endTime=end_of_day.isoformat()))

    return [ts.dict(by_alias=True) for ts in time_slots]


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--calendars', type=json.loads, dest='calendars')
    parser.add_argument('-f', '--file', type=str, dest='file')
    args = parser.parse_args()
    if args.calendars and args.file:
        raise Exception('Only one of "--calenders" or "--file" can be used but not both')
    if args.file:
        with open(args.file, 'r') as f:
            args.calendars = json.load(f)
    return args


def main(args: Namespace) -> None:
    print(json.dumps(get_available_time_slots(calendars_list=args.calendars), indent=2, default=str))


if __name__ == '__main__':
    main(parse_arguments())
