# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime

from flask import Blueprint, jsonify, request

from cursor import get_kyruus_db_cursor
from util import safe_get
from version import VERSION

kyruus_api = Blueprint('kyruus_api', __name__, url_prefix='')


@kyruus_api.route('/', methods=['GET'])
def status():
    resp = {
        'name': 'doctor_service',
        'version': VERSION
    }

    return jsonify(resp), 200


@kyruus_api.route('/doctor/<str:doctor>', methods=['GET'])
def get_doctor_schedule(doctor):
    sql = """SELECT dl.name AS location_name, ds.day, ds.start_time, ds_end_time
             FROM doctor d
             JOIN doctor_location dl ON d.id = dl.doctor_id
             JOIN doctor_schedule ds ON d.id = ds.doctor_id AND dl.id = ds.location_id
             WHERE d.name = %(doctor)s"""

    with get_kyruus_db_cursor() as cur:
        cur.execute(sql, dict(doctor=doctor))
        result = cur.fetchall()
    resp = {
        'schedule': result
        }

    return jsonify(resp), 200


@kyruus_api.route('/appointment/book', methods=['POST'])
def book_appointment():
    data = request.get_json()
    doctor = data.get('doctor', '')
    location = data.get('location', '')
    day = data.get('day', '')
    start_time = data.get('start_time', datetime.now())
    end_time = data.get('end_time', datetime.now())
    conflict_sql = """SELECT dl.name AS location_name, ds.day, ds.start_time, ds_end_time
                      FROM doctor d
                      JOIN doctor_location dl ON d.id = dl.doctor_id
                      JOIN doctor_schedule ds ON d.id = ds.doctor_id AND dl.id = ds.location_id
                      WHERE d.name = %(doctor)s
                      AND   dl.location = %(location)s
                      AND   ds.day = %(day)s
                      AND   (%(start_time)s >= ds.start_time OR %(start_time)s <= ds.end_time
                             OR %(end_time)s >= ds.start_time OR %(end_time)s <= ds.end_time"""
    location_sql = """SELECT id FROM doctor_location WHERE name = %(location_name)s"""
    doctor_sql = """SELECT id FROM doctor WHERE name = %(doctor_name)s"""
    insert_sql = """INSERT INTO doctor_schedule (doctor_id, location_id, day, start_time, end_time)
                    VALUES (%(doctor_id)s, %(location_id)s, %(day)s, %(start_time)s, %(end_time)s)"""
    conflict_replacements = dict(doctor=doctor, location=location, day=day, start_time=start_time, end_time=end_time)
    location_replacements = dict(location_name=location)
    doctor_replacements = dict(doctor_name=doctor)
    conflict_message = 'conflicting appointment for doctor {doctor}, location {location}, between {start_time} {end_time}'
    location_message = 'location {location} does not exist'
    doctor_message = 'doctor {doctor} does not exist'
    with get_kyruus_db_cursor() as cur:
        safe_get(cur, conflict_sql, conflict_message, **conflict_replacements)
        safe_get(cur, location_sql, location_message, **location_replacements)
        safe_get(cur, doctor_sql, doctor_message, **doctor_replacements)
        cur.execute(insert_sql, conflict_replacements)
    return 200


@kyruus_api.route('/appointment/cancel', method=['POST'])
def cancel_appointment():
    data = request.get_json()
    doctor = data.get('doctor', '')
    location = data.get('location', '')
    day = data.get('day', '')
    start_time = data.get('start_time', '')
    end_time = data.get('end_time', '')
    sql = """DELETE FROM doctor_schedule
             USING doctor_schedule ds
             JOIN  doctor d ON ds.doctor_id
             JOIN  doctor dl ON d.id = dl.doctor_id AND ds.location_id = dl.id
             WHERE d.name = %(doctor)s AND dl.name = %(location)s
             AND   ds.day = %(day)s AND ds.start_time = %(start)s
             AND   ds.end_time = %(end)s"""
    with get_kyruus_db_cursor() as cur:
        cur.execute(sql, dict(doctor=doctor, location=location, day=day, start=start_time, end=end_time))
    return 200


@kyruus_api.route('/doctor/<int:doctorid>', methods=['GET'])
def get_doctor_details(doctorid):
    sql = """SELECT d.*
             FROM doctor d
             WHERE d.id = %(doctor_id)"""

    with get_kyruus_db_cursor() as cur:
        cur.execute(sql, dict(doctor_id=doctorid))
        result = cur.fetchall()
    resp = {
        'doctor': result
        }

    return jsonify(resp), 200