// Dependencies
// App.js and its dependencies and knockout js
// App.js
// End Dependencies

// TODO loading initial query

var optionVM = function (options, selected, order, main_vm) {
    var self = this;
    self.options = ko.observableArray(options);
    self.selected = ko.observable(selected);
    self.order = ko.observable(order);

    self.remove_forward_opt_vm = function () {
        var to_remove = [];
        ko.utils.arrayForEach(main_vm.option_vms(), function (option_vm) {
            if(option_vm.order() > self.order()){
                to_remove.push(option_vm);
            }
        });
        main_vm.option_vms.removeAll(to_remove);
        main_vm.option_vm_count(self.order());
    };
    
    self.selected.subscribe(function () {
        console.log(self.selected());
        self.remove_forward_opt_vm();
        main_vm.compute_query();
        
    })
};


var mainVM = function (params) {
    var self = this;
    // if params.query populate optionvm
    self.option_vms = ko.observableArray();
    self.option_vm_count = ko.observable(0);
    self.query = params.value_obs;

    self.get_child_options = function () {
        var url = '/payroll/get-report-field/';
        App.showProcessing();

        App.remotePost(url, {'query': self.query()}, function (response) {
            App.hideProcessing();
            self.option_vm_count(self.option_vm_count() + 1);
            self.option_vms.push(new optionVM(response.options, null, self.option_vm_count(), self));
            console.log('success');
        }, function () {
            App.hideProcessing();
            console.log(errorThrown);
        });
    };

    self.load_selected_options = function () {
        var url = '/payroll/get-selected-options/';
        App.showProcessing();

        App.remotePost(url, {'query': self.query()}, function (response) {
            App.hideProcessing();
            if(response.selected_options){
                var selected_options_to_load = [];
                response.selected_options.forEach(function (selected_options, index) {
                    self.option_vm_count(self.option_vm_count() + 1);
                    selected_options_to_load.push(new optionVM(selected_options.options, selected_options.selected, self.option_vm_count(), self));
                });
                self.option_vms(selected_options_to_load);
            }
        }, function () {
            App.hideProcessing();
            console.log(errorThrown);
        });
    };
    self.compute_query = function(){
        var total_qry = '';
        ko.utils.arrayForEach(self.option_vms(), function (option_vm) {
            total_qry += option_vm.selected();
        });
        self.query(total_qry);
    };

    if (!self.query()){
        self.get_child_options();
    }else{
        self.load_selected_options();
    }

    self.query.subscribe(function () {
        // debugger;
        if (self.query().slice(-3) == '___' || self.query().slice(-2) == '__') {
            self.get_child_options()

        }
    });
};

ko.components.register('report-field-chooser', {
    viewModel: mainVM,
    template: '<div class="">'

    + '<!-- ko foreach: option_vms -->'
    + '<select data-bind="options: options, optionsText: function(item){return item[1];}, optionsValue: function(item){ return item[0];}, optionsCaption: \'Choose...\', value: selected">'
    + '<select>'
    + '<!-- /ko -->'
    + '</div>'
});

