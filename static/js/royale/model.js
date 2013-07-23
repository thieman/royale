var slideDelay = 600;
var app = null;
var cycleInterval = null;
var refreshInterval = null;

var Metric = Backbone.Model.extend({

	defaults: {
		id: null,
		caption: "",
		metric: {},
		chart: {}
	}

});

var MetricList = Backbone.Collection.extend({
	model: Metric,
	url: $SCRIPT_ROOT + '/metrics'
});

var CycleControl = Backbone.Model.extend({

	defaults: {
		prefix: 'static/img/',
		cycle: true
	},

	src: function() {
		return $SCRIPT_ROOT + this.get('prefix') + (this.get('cycle') ? 'pause.png' : 'play.png');
	}

});

var CycleControlView = Backbone.View.extend({

	el: $('#control-wrapper'),
	className: 'cycle-control',

	initialize: function() {
		this.source = $('#cycle-control-template').html();
		this.template = Handlebars.compile(this.source);
		this.listenTo(this.model, 'change', this.render);
	},

	render: function() {
		this.$el.html(this.template({
			src: this.model.src()
		}));
		return this;
	},

	events: {
		'click': 'controlClick'
	},

	controlClick: function() {
		this.model.set('cycle', !(this.model.get('cycle')));
	}

});

var MetricView = Backbone.View.extend({

	className: 'feed-element',

	initialize: function() {
		this.guid = guid();
		this.source = $('#feed-template').html();
		this.template = Handlebars.compile(this.source);
		this.listenTo(this.model, 'remove', this.slideOut);
	},

	render: function() {

		this.$el.html(this.template({
			id: this.model.id,
			caption: this.model.get('metric').caption,
			current: this.model.get('metric').current,
			compare: this.model.get('metric').compare,
			updated: moment(this.model.get('metric').updated).fromNow(),
			guid: this.guid
		}));

		if (this.model.has('chart')) {
			var spec = this.model.get('chart').chart;

			(function (renderId, thisGuid) {
				vg.parse.spec(spec, function(chart) {
					chart({el: '#chart-' + thisGuid})
						.width($('.feed-element').width() * 0.5)
						.height($('.feed-element').height() * 0.74)
						.update();
				});
			})(this.model.id, this.guid);
		}

		return this;
	},

	slideOut: function() {
		(function(view) {
			view.$el.animate({height: 0}, slideDelay, function() { view.remove(); });
		})(this);
	}

});

var FeedView = Backbone.View.extend({

	el: $('#wrapper'),

	initialize: function() {
		this.views = [];

		this.control = new CycleControlView({model: new CycleControl()});
		this.control.render();

		this.collection = new MetricList();
		this.listenTo(this.collection, 'add', this.addOne);
		this.listenTo(this.collection, 'remove', this.removeOne);
		this.collection.fetch();
	},

	addOne: function(model, collection, options) {
		var newView = new MetricView({model: model});
		this.views.push(newView);
		this.$el.append(newView.render().el);
	},

	removeOne: function(model, collection, options) {
		this.views = _.filter(this.views, function(view) {
			return (view.model !== this);
		}, model);
	},

	render: function(reverse) {

		_.each(this.collection, function(model) {
			_.each(this.views, function(view) {
				var app = this[0];
				var coll = this[1];
				if (view.model === model) {
					app.$el.append(view.render().el);
				}
			}, [this, model]);
		}, this);

		return this;
	},

	cycle: function() {
		if (this.control.model.get('cycle') && this.collection.length !== 0) {
			var first = this.collection.shift();
			setTimeout(function() { app.collection.push(first); }, 1000);
		}
	}

});

$(document).ready(function() {
	app = new FeedView;
	cycleInterval = setInterval(function() { app.cycle(); }, 5000);
	refreshInterval = setInterval(function() { app.collection.fetch(); },
								  5000);
});
