/**
 * Created by wrufesh on 10/20/16.
 */
var deduction = {
    getList: function (url, success_callback) {
        App.showProcessing();
        App.remoteGet(
            url,
            {},
            success_callback,
            function (err) {
                var err_message = err.responseJSON.detail;
                var error = App.notifyUser(
                    err_message,
                    'error'
                );
                App.hideProcessing();
            }
        );
    },
    postData: function (url, payload, callback) {
        App.showProcessing();
        App.remotePost(
            url,
            payload,
            callback,
            function (err) {
                var err_message = err.responseJSON.detail;
                var error = App.notifyUser(
                    err_message,
                    'error'
                );
                App.hideProcessing();
            }
        );

    },
    deductionVm: function (name_id, data, validity_id) {
        var self = this;
        self.id = ko.observable();
        if(name_id){
            self.name_id = ko.observable(name_id);
        }else{
            self.name_id = ko.observable();
        }
        self.deduct_type = ko.observable();
        self.value = ko.observable();
        if (validity_id) {
            self.validity_id = ko.observable(validity_id)
        } else {
            self.validity_id = ko.observable()
        }
        if (data) {
            for (var k in data) {
                self[k](data[k]);
            }
        }

    },
    vm: function () {
        var self = this;
        App.validationSettings();

        // Grade scale Vality main observables
        self.validity_api_url = '/payroll/api/deduction-validity/';
        self.available_deduction_validities = ko.observableArray();
        self.selected_validity = ko.observable();
        // self.selected_validity.extend({required: true});
        // End Grade scale Vality main observables

        self.deductions = ko.observableArray();

        // Load Deduction Names
        deduction.getList('/payroll/api/deduction-name/', function (res) {
            ko.utils.arrayForEach(res, function (deduction_name) {
                deduction_name['deduction'] = ko.observable(new deduction.deductionVm(deduction_name.id));

            });
            self.deductions(res);
        });
        // End Load Deduction Names

        // Load deductions
        self.selected_validity.subscribe(function () {
            if (self.selected_validity()) {
                deduction.getList('/payroll/api/deduction/?validity_id=' + String(self.selected_validity().id()), function (res) {
                    console.log(self.deductions());
                    console.log(res);

                    ko.utils.arrayForEach(self.deductions(), function (deduction_name) {

                        var matched = ko.utils.arrayFirst(res, function (deduction) {
                            if(deduction_name.id == deduction.name_id){
                                return deduction;
                            }
                        });
                        console.log(matched);

                        if(matched){
                            deduction_name['deduction'](new deduction.deductionVm(deduction_name.id, matched, self.selected_validity().id()))
                        }else{
                            deduction_name['deduction'](new deduction.deductionVm(deduction_name.id, {}, self.selected_validity().id(), deduction_name.id))
                        }

                    });
                    App.hideProcessing();
                });
            }else{
                ko.utils.arrayForEach(self.deductions(), function(deduction_name){
                    deduction_name['deduction'](new deduction.deductionVm(deduction_name.id));
                })
            }
        });

        self.save = function () {
            var payload = JSON.parse(ko.toJSON(self.deductions()));
            deduction.postData(
                '/payroll/api/deduction/',
                payload,
                function (res) {
                    ko.utils.arrayForEach(self.deductions(), function (deduction_name) {

                        var matched = ko.utils.arrayFirst(res, function (deduction) {

                            if(deduction_name.id == deduction.name_id){
                                return deduction;
                            }
                        });

                        if(matched){
                            deduction_name['deduction'](new deduction.deductionVm(deduction_name.id, matched, self.selected_validity().id()));
                        }else{
                            deduction_name['deduction'](new deduction.deductionVm(deduction_name.id, {}, self.selected_validity().id(), deduction_name.id))
                        }

                    });
                    App.notifyUser('Successfully Saved', 'success');
                    App.hideProcessing();
                }
            )
        };

        // End Load deductions
    }
};