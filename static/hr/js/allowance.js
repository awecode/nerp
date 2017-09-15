/**
 * Created by wrufesh on 10/17/16.
 */
/**
 * Created by wrufesh on 9/18/16.
 */

// TODO manage validity dates in bs

var allowance = {
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
        allowanceVm: function (employee_grade_id, data, validity_id, name_id) {
            var self = this;
            App.validationSettings();
            self.id = ko.observable();
            if (employee_grade_id) {
                self.employee_grade_id = ko.observable(employee_grade_id);
            } else {
                self.employee_grade_id = ko.observable();
            }
            // self.grade_name = ko.observable();
            // self.parent_grade_id = ko.observable();
            // self.parent_grade_name = ko.observable();
            if(name_id){
                self.name_id = ko.observable(name_id);
            }else{
                self.name_id = ko.observable();
            }
            self.sum_type = ko.observable();
            self.value = ko.observable();
            self.payment_cycle = ko.observable();


            self.year_payment_cycle_month = ko.observable();

            if (validity_id) {
                self.validity_id = ko.observable(validity_id);
            } else {
                self.validity_id = ko.observable();
            }
            if (data) {
                for (var k in data) {
                    self[k](data[k])
                }
            }
            self.ypcm_disable_edit = ko.observable(false);
            self.payment_cycle.subscribe(function () {
                // console.log(self.payment_cycle());
                if (self.payment_cycle() != 'Y') {
                    self.ypcm_disable_edit(true);
                } else {
                    self.ypcm_disable_edit(false);
                }
            });

            self.year_payment_cycle_month.extend({
                required: {
                    onlyIf: function () {
                        return typeof(self.sum_type()) != 'undefined' && typeof(self.value()) != 'undefined' && self.payment_cycle() == 'Y';
                    }
                }

            });
            self.errors = ko.validation.group({
                year_payment_cycle_month: self.year_payment_cycle_month
            })
        }
        ,

        vm: function (calender) {
            App.validationSettings();

            var self = this;
            // Grade scale Vality main observables
            self.validity_api_url = '/payroll/api/allowance-validity/';
            self.available_allowance_validities = ko.observableArray();
            self.selected_validity = ko.observable();
            self.selected_validity.extend({required: true});
            // End Grade scale Vality main observables

            // Grade scale Vality main observables
            self.allowance_name_api_url = '/payroll/api/allowance-name/';
            self.available_allowance_names = ko.observableArray();
            self.selected_allowance = ko.observable();
            self.selected_allowance.extend({required: true});
            // End Grade scale Vality main observables

            self.available_grade_groups = ko.observableArray();
            allowance.getList(
                '/payroll/api/grade-group/',
                function (res) {
                    ko.utils.arrayForEach(res, function (grade_group) {
                            ko.utils.arrayForEach(grade_group.employee_grades, function (grade) {
                                grade['allowance'] = ko.observable(new allowance.allowanceVm(grade.id));
                            });
                            grade_group['visibility'] = ko.observable(false);

                            grade_group['toggle_visibility'] = function () {
                                if (grade_group['visibility']() == false) {
                                    grade_group['visibility'](true);
                                } else {
                                    grade_group['visibility'](false);
                                }
                            };
                            //
                            // grade_group['save'] = function () {
                            //     console.log('Saving updated Value');
                            //     // TODO check whether the validity is selected or not(it needs to be selected)
                            // };

                        }
                    );
                    self.available_grade_groups(res);
                    App.hideProcessing();
                });


            var manage_list_response = function (res) {
                // Here res is all entered grade scale
                ko.utils.arrayForEach(self.available_grade_groups(), function (grade_group) {
                    ko.utils.arrayForEach(grade_group.employee_grades, function (grade) {
                        // console.log(grade['scale']().grade_rate(), grade['scale']().grade_number(), grade['scale']().salary_scale());
                        var matched_allowance = ko.utils.arrayFirst(res, function (allowance) {
                            if (allowance.employee_grade_id == grade.id) {
                                return allowance
                            }
                        });
                        if (matched_allowance) {
                            grade['allowance'](new allowance.allowanceVm(grade.id, matched_allowance, self.selected_validity().id(), self.selected_allowance().id()));
                        } else {
                            grade['allowance'](new allowance.allowanceVm(grade.id, null, self.selected_validity().id(), self.selected_allowance().id()));
                        }
                    });
                });
                App.hideProcessing();
                App.notifyUser('Success', 'success');
            };


            self.filtered_list = ko.computed(function () {
                if (self.selected_validity() && self.selected_allowance()) {
                    allowance.getList(
                        '/payroll/api/allowance/?validity_id=' + String(self.selected_validity().id()) + '&' + 'name_id=' + String(self.selected_allowance().id()),
                        manage_list_response
                    );
                } else {
                    ko.utils.arrayForEach(self.available_grade_groups(), function (grade_group) {
                        ko.utils.arrayForEach(grade_group.employee_grades, function (grade) {
                            grade['allowance'](new allowance.allowanceVm(grade.id));
                        });

                    });
                }
            });

            self.check_form_validity = function () {
                var is_valid = true;
                // console.log(self.errors().length);
                if(self.errors().length != 0){
                    self.errors.showAllMessages();
                    is_valid = false;
                }
                ko.utils.arrayForEach(self.available_grade_groups(), function (grade_groups) {
                    ko.utils.arrayForEach(grade_groups.employee_grades, function (grade) {
                        // console.log(grade.allowance().errors().length, grade.allowance().year_payment_cycle_month());
                        if(grade.allowance().errors().length != 0){
                            is_valid = false;
                            grade.allowance().errors.showAllMessages();
                        }
                    })
                });
              return is_valid;
            };

            self.save_update = function () {
                if (self.check_form_validity()) {
                    var payload = JSON.parse(ko.toJSON(self.available_grade_groups()));
                    allowance.postData(
                        '/payroll/api/allowance/',
                        payload,
                        manage_list_response
                    )
                }
            };

            // self.grade_scales = ko.observableArray();
            // gradeScale.getList(
            //     '/payroll/api/grade-scale/',
            //     function (res) {
            //         var items = ko.utils.arrayMap(res, function (item) {
            //             return new gradeScale.gradeScaleVm(item);
            //         });
            //         self.grade_scales([]);
            //         self.grade_scales(items);
            //     }
            // );
            // self.grades = ko.observableArray();
            // gradeScale.getList(
            //     '/payroll/api/employee-grade.',
            //     function (res) {
            //         var items = ko.utils.arrayMap(res, function (item) {
            //             return new gradeScale.gradeVm(item);
            //         });
            //         self.grades([]);
            //         self.grades(items);
            //     }
            // );
            self.months_options = ko.observable();
            self.bs_months = [
                {name: 'Baisakh', value: 1},
                {name: 'Jestha', value: 2},
                {name: 'Aashar', value: 3},
                {name: 'Shrawan', value: 4},
                {name: 'Bhadra', value: 5},
                {name: 'Asoj', value: 6},
                {name: 'Katik', value: 7},
                {name: 'Mansir', value: 8},
                {name: 'Poush', value: 9},
                {name: 'Magh', value: 10},
                {name: 'Falgun', value: 11},
                {name: 'Chaitra', value: 12},
            ];
            self.ad_months = [
                {name: 'January', value: 1},
                {name: 'February', value: 2},
                {name: 'March', value: 3},
                {name: 'April', value: 4},
                {name: 'May', value: 5},
                {name: 'June', value: 6},
                {name: 'July', value: 7},
                {name: 'August', value: 8},
                {name: 'September', value: 9},
                {name: 'October', value: 10},
                {name: 'November', value: 11},
                {name: 'December', value: 12}
            ];

            if (calender == 'AD') {
                self.months_options(self.ad_months);
            } else {
                self.months_options(self.bs_months);

            }

            self.errors = ko.validation.group({
                selected_validity: self.selected_validity,
                selected_allowance: self.selected_allowance
            })


        }
    }
    ;