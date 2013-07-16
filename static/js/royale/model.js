var Metric = Backbone.Model.extend({

	defaults: {
		id: null,
		metric: {},
		chart: {}
	}

});

var MetricList = Backbone.Collection.extend({
	model: Metric,
	url: '/metrics'
});

var MetricView = Backbone.View.extend({

	className: 'feed-element',

	initialize: function() {
		this.source = $('#feed-template').html();
		this.template = Handlebars.compile(this.source);
		this.listenTo(this.model, 'change', this.render);
	},

	render: function() {
		this.$el.html(this.template({
			id: this.model.get('id'),
			current: this.model.get('metric').current,
			compare: this.model.get('metric').compare,
			updated: moment(this.model.get('metric').updated).fromNow()
		}));

		var spec = this.model.get('chart').chart;

		vg.parse.spec(spec, function(chart) {
			chart({el: '.chart'})
				.width($('.feed-element').width() * 0.5)
				.height($('.feed-element').height() * 0.74)
				.update();
		});

		return this;
	}

});

var FeedView = Backbone.View.extend({

	el: $('#wrapper'),

	initialize: function() {
		this.collection = new MetricList();
		this.collection.bind('reset', _.bind(this.render, this));
		this.collection.fetch({reset: true});
	},

	render: function() {
		this.$el.empty();
		this.collection.each(function(metric) {
			var view = new MetricView({model: metric});
			this.$el.append(view.render().el);
		}, this);
		return this;
	}

});

$(function() {
	window.app = new FeedView;
});
