$(document).ready(function () {
    // ko.options.deferUpdates = true;
    // var main = this;
    vm = new PayrollEntry(ko_data.emp_options);
    ko.applyBindings(vm);
    if (ko_data.ctx_data) {
        var mapping = {
            'entry_rows': {
                create: function (options) {
                    var entry_row = ko.mapping.fromJS(options.data, {copy: []}, new PaymentEntryRow(ko_data.emp_options.slice(0)));
                    // if (typeof(options.parent.paid_from_date_input()) == 'undefined') {
                    //     options.parent.paid_from_date_input(options.data.paid_from_date);
                    //     options.parent.paid_to_date_input(options.data.paid_to_date);
                    // }
                    return entry_row;
                }
            },
            // 'branch': {
            //     create: function(options){
            //         console.log(options.data)
            //         if(options.data == null){
            //             return 'ALL'
            //         }
            //         return options.data
            //     }
            // }
        };
        ko.mapping.fromJS(ko_data.ctx_data, mapping, vm);

    }
});

function has_no_common_emp(list1, list2){
    var has_no_commom = true;
    for (var i = 0; i < list1.length; i++){
        for(var j = 0; j < list2.length; j++){
            if (list1[i].id == list2[j].id){
                has_no_commom = false;
            }
        }
    }
    return has_no_commom;
}

// Subtract list not by type but by id
function diffByID(list1, list2, pdb) {
    if (list1.length >= list2.length) {
        var list1_ids = ko.utils.arrayMap(list1, function (obj) {
            return obj.id;
        });
        var list2_ids = ko.utils.arrayMap(list2, function (obj) {
            return obj.id;
        });
        var diff = $(list1_ids).not(list2_ids).get();

        var diff_obj_array = ko.utils.arrayFilter(list1, function (obj) {

            if ($.inArray(obj.id, diff) != -1) {
                return obj;
            }
        });

        if (pdb) {
            debugger;
        }
        return diff_obj_array;
    }

}

function PaymentEntryRow(emp_options) {
    var self = this;
    self.id = ko.observable();
    self.emp_options = ko.observableArray(emp_options);
    // self.emp_options.extend({notify: 'always'});
    self.paid_employee = ko.observable();
    // self.employee_id = null;

    self.employee_grade = ko.observable();
    self.employee_designation = ko.observable();

    self.paid_from_date = ko.observable();
    self.paid_to_date = ko.observable();
    self.absent_days = ko.observable(0);
    self.allowance = ko.observable(0);
    self.incentive = ko.observable(0);
    self.deduced_amount = ko.observable(0);
    self.total_tax = ko.observable(0);
    self.pro_tempore_amount = ko.observable(0);
    self.salary = ko.observable(0);
    self.paid_amount = ko.observable(0);
    self.request_flag = ko.observable();
    self.row_errors = ko.observableArray();
    self.disable_input = ko.observable(false);


    self.incentive_details = ko.observableArray();
    self.allowance_details = ko.observableArray();
    self.deduction_details = ko.observableArray();
    self.pro_tempore_details = ko.observableArray();
    self.tax_details = ko.observableArray();

    self.amount_added_before_deduction = ko.observable(0);

    self.get_total_amount_added_before_deduction = ko.computed(function () {
        var total = 0;
        ko.utils.arrayForEach(self.deduction_details(), function (obj) {
            total += parseFloat(obj.amount_added_before_deduction());
        });
        self.amount_added_before_deduction(total);
    });

    self.deduction_details_total = ko.computed(function () {
        var total = 0;
        ko.utils.arrayForEach(self.deduction_details(), function (obj) {
            total += parseFloat(obj.amount());
        });
        self.deduced_amount(total);
    });

    self.allowance_details_total = ko.computed(function () {
        var total = 0;
        ko.utils.arrayForEach(self.allowance_details(), function (obj) {
            total += parseFloat(obj.amount());
        });
        self.allowance(total);
    });

    self.incentive_details_total = ko.computed(function () {
        var total = 0;
        ko.utils.arrayForEach(self.incentive_details(), function (obj) {
            total += parseFloat(obj.amount());
        });
        self.incentive(total);
    });

    self.pro_tempore_details_total = ko.computed(function () {
        var total = 0;
        ko.utils.arrayForEach(self.pro_tempore_details(), function (obj) {
            total += parseFloat(obj.amount());
        });
        self.pro_tempore_amount(total);
    });

    self.tax_details_total = ko.computed(function () {
        var total = 0;
        ko.utils.arrayForEach(self.tax_details(), function (obj) {
            total += parseFloat(obj.amount());
        });
        self.total_tax(total);
    });

    self.compute_paid_amount = ko.computed(function () {
        // console.log(self.salary() - self.deduced_amount() - self.income_tax() + self.incentive() + self.allowance());
        self.paid_amount(self.salary() + self.incentive() + self.allowance() + self.amount_added_before_deduction() - self.deduced_amount() - self.total_tax() + self.pro_tempore_amount());
    });

    self.row_salary_detail = ko.computed(function () {
        if (self.paid_employee() && self.paid_from_date() && self.paid_to_date()) {
            self.request_flag(self.paid_employee() + '-' + self.paid_from_date() + '-' + self.paid_to_date());
            console.log(self.request_flag());
        }
    });


    // Make here a observable function dat will set other parameters with employee id and date range
    self.request_flag.subscribe(function () {
        if (vm.payroll_type() == "INDIVIDUAL") {
            App.showProcessing();
            $.ajax({
                url: '/payroll/get_employee_account/',
                method: 'POST',
                dataType: 'json',
                data: {
                    paid_employee: self.paid_employee(),
                    paid_from_date: self.paid_from_date(),
                    paid_to_date: self.paid_to_date(),
                    is_monthly_payroll: vm.is_monthly_payroll(),
                    edit: vm.id()
                },
                // async: true,
                success: function (response) {
                    App.hideProcessing();
                    if (response.errors) {
                        vm.entry_rows([new PaymentEntryRow()]);
                        if (response.errors.paid_from_date) {
                            vm.paid_from_date_error(response.errors.paid_from_date);
                        } else {
                            vm.paid_from_date_error(null);
                        }

                        if (response.errors.paid_to_date) {
                            vm.paid_to_date_error(response.errors.paid_to_date);
                        } else {
                            vm.paid_to_date_error(null);
                        }
                        if (response.errors.global_errors) {
                            for (var k in response.errors.global_errors)
                                App.notifyUser(response.errors.global_errors[k], 'error');
                        }
                    } else {
                        vm.paid_from_date_error(null);
                        vm.paid_to_date_error(null);
                        // vm.invalid_date_range(null);
                        var mapping = {
                            'ignore': ["paid_employee", "emp_options"]
                        };
                        ko.mapping.fromJS(response.data, mapping, self);

                        if (typeof(response.data.row_errors) == 'undefined') {
                            self.row_errors([]);
                        }
                        // self.date_set_by_server(true);
                        // };
                    }

                },
                error: function (errorThrown) {
                    App.hideProcessing();
                    console.log(errorThrown);
                }
            });
            console.log('Hey soul sister');
        } else {
        }
        // self.request_flag(false);
    });
}

function PayrollEntry(employee_options) {
    var self = this;

    self.id = ko.observable();
    self.entry_saved = ko.observable(false);
    self.approved = ko.observable(false);
    self.transacted = ko.observable(false);

    self.payroll_type = ko.observable();
    self.entry_rows = ko.observableArray([]);
    // self.id = ko.observable();
    self.paid_from_date_input = ko.observable();
    self.paid_to_date_input = ko.observable();

    self.paid_from_date_error = ko.observable();
    self.paid_to_date_error = ko.observable();

    self.is_monthly_payroll = ko.observable(true);

    self.paid_from_date = ko.computed(function () {
        var output = self.paid_from_date_input();
        if (self.paid_from_date_input()) {
            var splitted_date = output.split('-');
            if (splitted_date.length == 3) {
                if (self.is_monthly_payroll()) {
                    splitted_date[2] = zfill(String(1), 2);
                } else {
                    splitted_date[2] = zfill(splitted_date[2], 2);
                }
                splitted_date[1] = zfill(splitted_date[1], 2);
                output = splitted_date.join('-');
            }
        }
        return output;
    });
    self.paid_to_date = ko.computed(function () {
        var output = self.paid_to_date_input();
        if (self.paid_to_date_input()) {
            var splitted_date = output.split('-');
            if (splitted_date.length == 3) {
                if (ko_data.calendar == 'AD') {
                    var month_count = String(ad_month_days(parseInt(splitted_date[0]), parseInt(splitted_date[1])));
                    if (self.is_monthly_payroll() && month_count) {
                        splitted_date[2] = zfill(month_count, 2);
                    } else {
                        splitted_date[2] = zfill(splitted_date[2], 2);
                    }
                } else {
                    var month_count = String(bs_calendar.get_month_days(splitted_date[0], splitted_date[1]));
                    if (self.is_monthly_payroll() && month_count) {
                        splitted_date[2] = zfill(month_count, 2);
                    } else {
                        splitted_date[2] = zfill(splitted_date[2], 2);
                    }
                }
            }
            splitted_date[1] = zfill(splitted_date[1], 2);
            output = splitted_date.join('-');
        }
        return output;
    });

    self.entry_rows.subscribe(function () {
        console.log(self.entry_rows());

    });

    self.disable_main_input = ko.computed(function () {
        if (ko_data.ctx_data.computed_scenario == 'DETAIL-VIEW') {
            return true;
        } else {
            return false;
        }
    });

    self.branch = ko.observable();
    //
    // self.branch.subscribe(function () {
    //     if(self.branch()==2){
    //         console.log('this is branch', self.branch())
    //         debugger;
    //     }else{
    //         debugger;
    //     }
    // })

    self.employee_type = ko.observable();

    // self.messages = ko.observableArray();

    self.employee_options = ko.observableArray(employee_options);

    // self.id.subscribe(function(){
    //     if(self.id()){
    //         self.entry_saved(true);
    //     }
    // })

    self.approve_entry = function () {
        // debugger;
        App.showProcessing();
        $.ajax({
            url: '/payroll/approve_entry/' + String(self.id()),
            method: 'GET',
            dataType: 'json',
            // data: post_data,
            // async: true,
            success: function (response) {
                App.hideProcessing();
                self.approved(response.entry_approved);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
            //            self.budget_heads = ko.observableArray(data);
        });


    };
    self.transact = function () {
        App.showProcessing();
        $.ajax({
            url: '/payroll/transact_entry/' + String(self.id()),
            method: 'GET',
            dataType: 'json',
            success: function (response) {
                App.hideProcessing();
                self.transacted(true);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
    };
    // self.entry_delete = function(){
    //     $.ajax({
    //             url: 'delete_entry/' + String(self.id()),
    //             method: 'GET',
    //             dataType: 'json',
    //             // data: post_data,
    //             // async: true,
    //             success: function (response) {
    //                 console.log(response);


    //             },
    //             error: function(errorThrown){
    //                 console.log(errorThrown);
    //                 },
    // //            self.budget_heads = ko.observableArray(data);
    //         });
    // };


    self.switch_p_type = ko.computed(function () {
        if (self.payroll_type() == "INDIVIDUAL") {
            return true;
        } else {
            return false;
        }

    });

    // self.clear_row = ko.computed(function(){
    //     if(self.switch_p_type() == true){
    //         self.entry_rows([]);
    //         self.entry_rows.push(PaymentRowWitDeduction(pr_data));

    //     }else{
    //         self.entry_rows([]);
    //     };
    // });

    self.payroll_type.subscribe(function () {
        if (self.payroll_type() == 'INDIVIDUAL') {
            // debugger;
            if (!self.entry_rows().length) {
                self.entry_rows.push(new PaymentEntryRow(employee_options.slice(0)));
            }
        }
    });


    // Data Changing parameters when changed should reser self.save, approve,transact to default
    self.set_save_param_to_default = function () {
        self.id = ko.observable();
        self.entry_saved(false);
        self.approved(false);
        self.transacted(false);
    };


    self.saveAndAdd = function (formElement) {
        if (typeof(ko_data.ctx_data.id) != 'undefined') {
            var save_url = '/payroll/save_payroll_entry/' + String(ko_data.ctx_data.id) + '/';
        } else {
            var save_url = '/payroll/save_payroll_entry/';
        }
        var has_error = false;
        for (var row of self.entry_rows()) {
            if (row.row_errors().length > 0) {
                // here has true should be true 
                has_error = true;
                App.notifyUser('Remove rows with warnings to Save the entry', 'error');
            }
        }
        if (!has_error) {
            App.showProcessing();
            $.ajax({
                url: save_url,
                method: 'POST',
                dataType: 'json',
                data: ko.toJSON(self),
                // async: true,
                success: function (response) {
                    App.hideProcessing();
                    console.log(response);
                    // debugger;
                    self.id(response.entry_id);
                    self.entry_saved(response.entry_saved);
                    self.approved(response.entry_approved);
                    self.transacted(response.entry_transacted);

                },
                error: function (errorThrown) {
                    App.hideProcessing();
                    console.log(errorThrown);
                }
                //            self.budget_heads = ko.observableArray(data);
            });
        }
    };

    self.addRow = function (event) {
        self.entry_rows.push(new PaymentEntryRow(employee_options.slice(0)));
    };
    self.removeRow = function (row) {
        self.entry_rows.remove(row);
    };
    self.set_time_stamp = ko.computed(function () {
        // console.log('We are in timestamp function');
        if (self.payroll_type() != 'GROUP') {

            if (self.paid_from_date() && self.paid_to_date()) {
                for (var o of self.entry_rows()) {
                    o.paid_from_date(self.paid_from_date());
                    o.paid_to_date(self.paid_to_date());
                }
            }
        }
    });

    // self.request_flag = ko.computed(function () {
    //     // console.log("Group request flag IIN ");
    //     // console.log("Start");
    //     //console.log(self.branch() + self.paid_from_date() + "==" + self.paid_to_date());
    //     // console.log("End");
    //     // console.log(self.branch());
    //     // 
    //     if(){}
    //     return self.branch() + '-' + self.paid_from_date() + '-' + self.paid_to_date();
    // });
    self.request_flag = ko.observable();

    self.group_req_compute = ko.computed(function () {
        if (self.branch() && self.paid_from_date() && self.paid_to_date() && self.employee_type()) {
            self.request_flag(self.branch() + '-' + self.paid_from_date() + '-' + self.paid_to_date() + '-' + self.employee_type());
            console.log(self.request_flag());
            // console.log(self.request_flag());
        }
    });

    self.request_flag.subscribe(function () {
        if (self.payroll_type() == 'GROUP') {
            App.showProcessing();
            $.ajax({
                url: '/payroll/get_employees_account/',
                method: 'POST',
                dataType: 'json',
                data: {
                    branch: self.branch() ? self.branch() : 'ALL',
                    paid_from_date: self.paid_from_date(),
                    paid_to_date: self.paid_to_date(),
                    is_monthly_payroll: self.is_monthly_payroll(),
                    edit: ko_data.ctx_data.id,
                    employee_type: self.employee_type()
                },
                // async: true,
                success: function (response) {
                    App.hideProcessing();
                    if (response.errors) {
                        self.entry_rows([]);
                        if (response.errors.paid_from_date) {
                            self.paid_from_date_error(response.errors.paid_from_date);
                        } else {
                            self.paid_from_date_error(null);
                        }

                        if (response.errors.paid_to_date) {
                            self.paid_to_date_error(response.errors.paid_to_date);
                        } else {
                            self.paid_to_date_error(null);
                        }

                        if (response.errors.global_errors) {
                            for (var k in response.errors.global_errors)
                                App.notifyUser(response.errors.global_errors[k], 'error');
                        }


                    } else {
                        self.paid_from_date_error(null);
                        self.paid_to_date_error(null);

                        if (ko_data.ctx_data.computed_scenario == 'EDIT') {

                            ko.utils.arrayForEach(self.entry_rows(), function (row_vm) {
                                var row_res = ko.utils.arrayFirst(response.data, function (res_row) {
                                    return res_row.paid_employee == row_vm.paid_employee();
                                });

                                var mapping = {
                                    'ignore': ["emp_options"]
                                };
                                var row = ko.mapping.fromJS(row_res, mapping, row_vm);
                                if (typeof(row.row_errors) == 'undefined') {
                                    row.row_errors = ko.observableArray([]);
                                }

                            });
                            // FIXME check the usage of this block
                            ko.utils.arrayMap(response.data, function (data) {
                                var mapping = {
                                    'ignore': ["emp_options"]
                                };

                                var row = ko.mapping.fromJS(data, mapping, new PaymentEntryRow(employee_options.slice(0)));
                                if (typeof(row.row_errors) == 'undefined') {
                                    row.row_errors = ko.observableArray([]);
                                }
                                return row;
                            });
                        } else {
                            self.entry_rows([]);
                            self.entry_rows(ko.utils.arrayMap(response.data, function (data) {

                                var mapping = {
                                    'ignore': ["emp_options"]
                                };
                                var row = ko.mapping.fromJS(data, mapping, new PaymentEntryRow(employee_options.slice(0)));
                                // row.is_explicitly_added_row = false;
                                // row.request_flag(false);
                                if (typeof(row.row_errors) == 'undefined') {
                                    row.row_errors = ko.observableArray([]);
                                }
                                return row;
                            }));
                        }
                    }
                },
                error: function (errorThrown) {
                    App.hideProcessing();
                    App.notifyUser(errorThrown, 'error');
                }
            });
            // }

        }
    });

    // Set employee options
    self.update_employee_options = function () {
        App.showProcessing();
        $.ajax({
            url: '/payroll/get_employee_options/',
            method: 'POST',
            dataType: 'json',
            // async: false,
            data: {
                branch: self.branch() ? self.branch() : 'ALL',
                // branch: self.branch() ? self.branch() : 'ALL',
                // branch: 'ALL',
                employee_type: self.employee_type()
            },
            success: function (response) {
                App.hideProcessing();
                // self.employee_options(response.opt_data);
                // FIXME
                // dont delete just trim emp_options (ie either push or pop)(used when response is subset of existing employee_options)
                // debugger;
                if (!has_no_common_emp(self.employee_options(), response.opt_data)) {
                    if (self.employee_options().length > response.opt_data.length) {
                        // debugger;
                        self.employee_options.removeAll(diffByID(self.employee_options(), response.opt_data));
                    } else if (self.employee_options().length < response.opt_data.length) {
                        ko.utils.arrayPushAll(self.employee_options, diffByID(response.opt_data, self.employee_options()));
                    } else {
                        // self.employee_options(response.opt_data);
                        self.employee_options.removeAll(diffByID(self.employee_options(), response.opt_data));
                        ko.utils.arrayPushAll(self.employee_options, diffByID(response.opt_data, self.employee_options()));
                    }
                } else {
                    // console.log('hey');
                    self.employee_options(response.opt_data);
                }


                // below is used when response is totally different from existing employee options
                // self.employee_options(response.opt_data);

            },
            error: function (errorThrown) {
                App.hideProcessing();
                console.log(errorThrown);
            }
        });
    };
    // self.update_employee_options();

    self.this_on_ch_update_emp = ko.observable();
    self.branch_emp_type = ko.computed(function () {
        if (self.branch() && self.employee_type()) {
            self.this_on_ch_update_emp(self.branch() + '-' + self.employee_type());
        }
    });
    self.this_on_ch_update_emp.subscribe(function () {
        // console.log(self.this_on_ch_update_emp());
        self.update_employee_options();
    });

    self.employee_options.subscribe(function () {
        var branch_emp_ids = ko.utils.arrayMap(self.employee_options(), function (obj) {
            return obj.id;
        });
        var rows_to_remove = [];
        for (var roo of self.entry_rows()) {
            if ($.inArray(roo.paid_employee(), branch_emp_ids) == -1) {
                rows_to_remove.push(roo);
            }
        }
        self.entry_rows.removeAll(rows_to_remove);
    });

    self.selected_employees = ko.computed(function () {
        var sel_e = [];
        for (var row of self.entry_rows()) {
            if (typeof(row.paid_employee()) != 'undefined') {
                sel_e.push(row.paid_employee());
            }
        }
        return sel_e;
    });

    self.update_employees_options = ko.computed(function () {
        // debugger;
        for (var roow of self.entry_rows()) {

            // dont delete just trim emp_options (ie either push or pop)
            // if (self.employee_options().length > roow.emp_options().length) {
            //     // roow.emp_options.removeAll($(self.employee_options()).not(roow.emp_options()).get());
            //     ko.utils.arrayPushAll(roow.emp_options, diffByID(self.employee_options(), roow.emp_options()))
            // } else if (self.employee_options().length < roow.emp_options().length) {
            //     roow.emp_options.removeAll(diffByID(roow.emp_options(), self.employee_options()));
            // } else {
            //     roow.emp_options(self.employee_options().slice())
            // }
            roow.emp_options(self.employee_options().slice());

            var to_remove = [];
            for (var opt of roow.emp_options()) {

                if ($.inArray(opt.id, self.selected_employees()) != -1 && opt.id != roow.paid_employee()) {
                    to_remove.push(opt);
                }
            }

            // console.log('to remove diff')
            // console.log(roow.emp_options(), to_remove);
            // console.log(diffByID(roow.emp_options(), to_remove, true));

            // var diff = $(roow.emp_options()).not(to_remove).get();
            roow.emp_options(diffByID(roow.emp_options(), to_remove));

            // console.log(diff);
            // roow.emp_options.removeAll(diffByID(roow.emp_options(), to_remove));

            //  // dont delete just trim emp_options (ie either push or pop)
            // if(roow.emp_options().length > to_remove.length ){
            //    roow.emp_options.removeAll(to_remove);
            // }

            // // roow.paid_employee(roow.employee_id);
        }
    });

    // self.remove_alert = function (alert_msg) {
    //     self.messages.remove(alert_msg);
    // };
    // self.messages.subscribe(function(){
    //     if(self.messages()){
    //         for(var k in self.messages()){
    //             notifyUser(self.messages()[k], 'error')
    //         }
    //         self.messages([]);
    //     }
    // });
}


