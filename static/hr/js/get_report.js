$(document).ready(function () {
    vm = new filterVM();
    ko.applyBindings(vm);
});

var filterVM = function () {
    var self = this;
    self.branch = ko.observable();
    self.employee_type = ko.observable();
    self.employee_options = ko.observableArray();

    self.get_emp_opts = ko.computed(function () {
        if (self.branch() && self.employee_type()) {
            var url = '/payroll/get_employee_options/';

            App.showProcessing();

            $.ajax({
                url: '/payroll/get_employee_options/',
                method: 'POST',
                dataType: 'json',
                // async: false,
                data: {
                    branch: self.branch(),
                    employee_type: self.employee_type()
                },
                success: function (response) {
                    App.hideProcessing();

                    self.employee_options(response.opt_data);

                },
                error: function (errorThrown) {
                    App.hideProcessing();
                    console.log(errorThrown);
                }
            });
        }
    });
};