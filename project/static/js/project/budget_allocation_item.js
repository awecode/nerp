$(document).ready(function () {
    vm = new BudgetAllocationItem(ko_data);
    ko.applyBindings(vm);
    var total_col = $(".total").prev().children().length;
    $(".total td:first").first().attr('colspan', total_col - 2);
});

function BudgetAllocationItem(data) {
    var self = this;
    self.budget_heads = ko.observableArray([]);
    self.capital_expenditure = ko.observableArray([]);

    ko.utils.arrayForEach(data.budget_heads, function (obj) {
        if (obj.recurrent) {
            self.budget_heads.push(obj);
        } else {
            self.capital_expenditure.push(obj);
        }
    });

    self.aids = ko.observableArray();

    self.count = [];

    self.project_fy_id = ko.observable(data.project_fy_id);
    for (var k in data.aids) {
        if (data.aids[k].aid_name != null) {
            if (self.count.indexOf(data.aids[k].aid_name) == -1) {
                self.count.push(data.aids[k].aid_name);
                self.aids.push(data.aids[k].aid_name.split('-')[1]);
            }
        }
    }


    self.budget_head_values = [];
    self.capital_expenditure_values = [];
    self.value_count = [];
    for (var i in data.rows) {
        var val = data.rows[i].budget_head_id;
        if (data.rows[i].recurrent) {
            self.values = self.budget_head_values;
        } else {
            self.values = self.capital_expenditure_values;
        }
        if (self.value_count.indexOf(val) == -1) {
            self.value_count.push(val);
            self.values.push({
                'budget_head_id': val,
                'aid_amount': [{
                    'id': data.rows[i].id,
                    'aid_name': data.rows[i].aid_name,
                    'amount': data.rows[i].amount
                }]
            });

        } else {
            var obj = $.grep(self.values, function (e) {
                return e.budget_head_id == data.rows[i].budget_head_id;
            });
            obj[0].aid_amount.push({
                'id': data.rows[i].id,
                'aid_name': data.rows[i].aid_name,
                'amount': data.rows[i].amount
            });
        }
    }

    self.budget_head_view = new TableViewModel({rows: self.budget_head_values, argument: self}, RowVM);
    self.capital_expenditure_view = new TableViewModel({rows: self.capital_expenditure_values, argument: self}, RowVM);


    self.grand_total = function() {
        var total=0;
        self.budget_head_view.rows().forEach(function (i) {
            total = total + i.total();
        }) ;

        self.capital_expenditure_view.rows().forEach(function (i) {
            total += i.total();
        });
        return total;
    };

    self.available_budget_heads = ko.observableArray(data.budget_heads.diff([]));

    self.selected_budget_heads = ko.observableArray([]);


    //self.selected_budget_heads = ko.computed(function () {
    //    var heads = [];
    //    ko.utils.arrayForEach(self.table_view.rows(), function (row) {
    //        if (row.budget_head()) {
    //            heads.push(row.budget_head());
    //            //row.dummy.notifySubscribers();
    //        }
    //    });
    //    return heads;
    //});


    self.save = function () {
        $.ajax({
            type: "POST",
            url: '/project/budget_allocation/save/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                }
                else {
                    alert.success('Saved!');
                    for (var i in msg.rows.budget_head_view) {
                        for (var aid in msg.rows.budget_head_view[i]) {
                            self.budget_head_view.rows()[i][aid](msg.rows.budget_head_view[i][aid]);
                            if (self.budget_head_view.rows()[i].aid_amount().length != 0) {
                                self.budget_head_view.rows()[i].aid_amount().push({'id': msg.rows.budget_head_view[i][aid]});
                            }
                        }
                    }
                    for (var i in msg.rows.capital_expenditure_view) {
                        for (var aid in msg.rows.capital_expenditure_view[i]) {
                            self.capital_expenditure_view.rows()[i][aid](msg.rows.capital_expenditure_view[i][aid]);
                            if (self.capital_expenditure_view.rows()[i].aid_amount().length != 0) {
                                self.capital_expenditure_view.rows()[i].aid_amount().push({'id': msg.rows.capital_expenditure_view[i][aid]});
                            }
                        }
                    }
                    self.budget_head_view.deleted_rows([]);
                    self.capital_expenditure_view.deleted_rows([]);
                }
            }
            ,
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert.error(textStatus.toTitleCase() + ' - ' + errorThrown);
            }
        });
    }
}

function RowVM(row, vm) {
    var self = this;
    self.id = ko.observable();
    self.budget_head_id = ko.observable();
    self.goa_amount = ko.observable();
    self.goa_id = ko.observable();
    self.aid_amount = ko.observableArray();
    self.budget_head = ko.observable();
    //self.vm = ko.observable(vm);
    self.dummy = ko.observable();

    for (i in vm.count) {
        self[vm.count[i]] = ko.observable();
        self[vm.count[i] + "-id"] = ko.observable();
    }

    if (row) {
        for (i in row.aid_amount) {
            if (row.aid_amount[i].aid_name == null) {
                if (self.goa_amount() == undefined) {
                    self.goa_amount(row.aid_amount[i].amount);
                    self.goa_id(row.aid_amount[i].id);
                }
                //else {
                //self.goa_amount(self.goa_amount() + row.aid_amount[i].amount);
                //}
            }
            if (self[row.aid_amount[i].aid_name] != undefined) {
                self[row.aid_amount[i].aid_name](row.aid_amount[i].amount);
                self[row.aid_amount[i].aid_name + "-id"](row.aid_amount[i].id);

            }
        }
    }


    //self.available_budget_heads = ko.computed(function(){
    //    console.log('hey');
    //    var heads = self.vm().budget_heads().diff(self.vm().selected_budget_heads());
    //    
    //    return heads;
    //    
    //})

    //self.available_budget_heads = ko.observableArray(vm.budget_heads().diff([]));

    //self.available_budget_heads = ko.computed(function () {
    //    self.dummy();
    //    var heads = vm.budget_heads().diff(vm.selected_budget_heads())
    //    if (self.budget_head()) {
    //        heads.push(self.budget_head());
    //    }
    //    return heads;
    //});

    //self.available_budget_heads.subscribe(function () {
    //debugger;
    //$(document).trigger('reload-selectize');
    //});


    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }

    self.total = function () {
        var total = 0;
        if (self.goa_amount()) {
            total = parseInt(self.goa_amount());
        }
        for (i in vm.count) {
            if (typeof(self[vm.count[i]]()) != 'undefined') {
                if (self[vm.count[i]]() != null) {
                    total = total + empty_to_zero(self[vm.count[i]]());
                }
            }
        }
        return parseInt(total);
    }
}
