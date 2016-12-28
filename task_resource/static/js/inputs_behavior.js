openerp.task_resource = function(instance) {

	var QWeb = openerp.web.qweb;
	    _t = instance.web._t;

	instance.web.FormView.include({
	    load_form: function(data) {
	        var self = this;
	        this.$el.find('#qty_to_request').on('click', function() {
	            console.log('Ya funcionó :D') // or $(this).val()
	            // here put your logic for validation field.
	        });
	        return self._super(data);
	    },
	});
};