""" RESTful resource declarations """

import re
import json
from datetime import datetime

from flask import request
from flask.ext.restful import Resource, fields, marshal_with, abort

def serialize(obj):
    for k, v in obj.iteritems():
        if isinstance(v, dict):
            obj[k] = serialize(v)
        elif isinstance(v, datetime):
            obj[k] = v.isoformat()
    return obj

class MetricList(Resource):
    """ Aggregated data on all metrics, with related
    Charts and Series. """

    def get(self):

        extract_series = re.compile("\"\{\{(.*?)\}\}\"")
        metrics = []

        for metric in self.mongo.db.metric.find().sort('priority', 1):

            chart = self.mongo.db.chart.find_one(metric['_id'])

            if chart:
                chart_data = json.dumps(chart.get('chart', ''))
                found_series = set(re.findall(extract_series, chart_data))
                for series_name in found_series:
                    series = self.mongo.db.series.find_one(series_name)
                    if series:
                        chart_data = re.sub('\"{{%s}}\"' % series_name,
                                            json.dumps(series['values']),
                                            chart_data)

                chart['chart'] = json.loads(chart_data)

            metric_data = {'id': metric['_id'],
                           'metric': metric,
                           'chart': chart}
            metrics.append(serialize(metric_data))

        return metrics if metrics else None

class Metric(Resource):
    """ Defines a metric to show in the Royale dashboard.

    Each metric has an ID and 'current' and 'compare' values. """

    metric_fields = {'_id': fields.String,
                     'caption': fields.String,
                     'current': fields.String,
                     'current_caption': fields.String,
                     'compare': fields.String,
                     'compare_caption': fields.String,
                     'priority': fields.Integer}

    @marshal_with(metric_fields)
    def get(self, metric_id):
        return self.mongo.db.metric.find_one_or_404(metric_id)

    @marshal_with(metric_fields)
    def post(self, metric_id):
        obj = {'updated': datetime.utcnow()}
        for arg in ['caption', 'compare', 'current',
                    'current_caption', 'compare_caption',
                    'priority']:
            value = request.form.get(arg, None)
            if value:
                obj[arg] = value
        self.mongo.db.metric.update({'_id': metric_id},
                                    {'$set': obj},
                                    upsert=True)
        return self.mongo.db.metric.find_one(metric_id), 201

    @marshal_with(metric_fields)
    def put(self, metric_id):
        obj = {'_id': metric_id, 'updated': datetime.utcnow()}
        for arg in ['caption', 'compare', 'current',
                    'current_caption', 'compare_caption',
                    'priority']:
            value = request.form.get(arg, None)
            if value:
                obj[arg] = value
        self.mongo.db.metric.save(obj)
        return obj, 201

    def delete(self, metric_id):
        self.mongo.db.metric.remove(metric_id)
        return '', 204


class Chart(Resource):
    """ Chart structure JSON defined using Vega.

    Metrics will still be displayed if they don't have charts.

    The Vega JSON is stored as-is in Self.Mongo. Royale views can bind
    Charts to Series using the {{series_name}} construct in
    the Vega data field. """

    chart_fields = {'_id': fields.String,
                    'chart': fields.Raw}

    @marshal_with(chart_fields)
    def get(self, chart_id):
        return self.mongo.db.chart.find_one_or_404(chart_id)

    @marshal_with(chart_fields)
    def post(self, chart_id):
        obj = json.loads(request.form['chart'])
        self.mongo.db.chart.update({'_id': chart_id},
                              {'chart': {'$set': obj},
                               '$set': {'updated': datetime.utcnow()}},
                              upsert=True)
        return self.mongo.db.series.find_one(chart_id), 201

    @marshal_with(chart_fields)
    def put(self, chart_id):
        obj = {'_id': chart_id,
               'chart': json.loads(request.form['chart']),
               'updated': datetime.utcnow()}
        self.mongo.db.chart.save(obj)
        return obj, 201

    def delete(self, chart_id):
        self.mongo.db.chart.remove(chart_id)
        return '', 204


class Series(Resource):
    """ Series data structure stored as a list.

    Series IDs are not one-to-one with Metrics and only need to
    match up to any Series references within Chart objects. """

    series_fields = {'_id': fields.String,
                     'values': fields.Raw}

    @marshal_with(series_fields)
    def get(self, series_id):
        return self.mongo.db.series.find_one_or_404(series_id)

    @marshal_with(series_fields)
    def post(self, series_id):
        obj = json.loads(request.form['values'])
        self.mongo.db.series.update({'_id': series_id},
                               {'$push': {'values': obj},
                                '$set': {'updated': datetime.utcnow()}},
                               upsert=True)
        return self.mongo.db.series.find_one(series_id), 201

    @marshal_with(series_fields)
    def put(self, series_id):
        obj = {'_id': series_id,
               'values': json.loads(request.form['values']),
               'updated': datetime.utcnow()}
        if not isinstance(obj['values'], list):
            abort(400, error="values must be a list")
        self.mongo.db.series.save(obj)
        return obj, 201

    def delete(self, series_id):
        self.mongo.db.series.remove(series_id)
        return '', 204

def register_resources(api, mongo_instance):

    # We really dug too deep here with Flask blueprints and extensions.
    # Flask-Restful requires classes as arguments, but these needed
    # to also be dynamic. Maybe metaclasses would have been better?
    # For now, we have fake inheritance. And Balrogs.

    class MetricListCopy(MetricList): pass
    cls = MetricListCopy
    cls.mongo = mongo_instance
    api.add_resource(cls, '/metrics')

    class MetricCopy(Metric): pass
    cls = MetricCopy
    cls.mongo = mongo_instance
    api.add_resource(cls, '/metric/<string:metric_id>')

    class ChartCopy(Chart): pass
    cls = ChartCopy
    cls.mongo = mongo_instance
    api.add_resource(cls, '/chart/<string:chart_id>')

    class SeriesCopy(Series): pass
    cls = SeriesCopy
    cls.mongo = mongo_instance
    api.add_resource(cls, '/series/<string:series_id>')
