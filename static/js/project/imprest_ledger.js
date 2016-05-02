$(document).ready(function () {
    vm = new ImprestVM(ko_data);
    ko.applyBindings(vm);
});


function ImprestVM(data) {
    var self = this;

    self.table_view = new TableViewModel({rows: data, argument: self}, ImprestTransaction);

    self.add_transaction = function (transaction_data) {
        if (!transaction_data['name']) {
            transaction_data['name'] = transaction_data['type'].toTitleCase();
        }
        var initial_deposit = new ImprestTransaction(transaction_data);
        self.table_view.rows.push(initial_deposit);
    }

    self.add_initial_deposit = function () {
        if (self.count_transaction_types('initial_deposit')()) {
            alert.error('There can only be one initial deposit!');
            return false;
        }
        self.add_transaction({'type': 'initial_deposit'})

    }

    self.count_transaction_types = function (type) {
        return ko.computed(function () {
            var transactions = ko.utils.arrayFilter(vm.table_view.rows(), function (row) {
                return row.type() == type;
            });
            return transactions.length;
        })
    }

    self.save = function () {
        var initial_deposits = self.count_transaction_types('initial_deposit')();
        if (initial_deposits < 1) {
            alert.error('Initial Deposit is required!');
            return false;
        } else if (initial_deposits > 1) {
            alert.error('There can only be one initial deposit!');
            return false;
        }
        //$.ajax({
        //    type: "POST",
        //    url: '/inventory/save/demand_forms/',
        //    data: ko.toJSON(self),
        //    success: function (msg) {
        //        if (typeof (msg.error_message) != 'undefined') {
        //            alert.error(msg.error_message);
        //        }
        //        else {
        //            alert.success('Saved!');
        //            self.status('Requested');
        //            if (msg.id)
        //                self.id(msg.id);
        //            $("#tbody > tr").each(function (i) {
        //                $($("#tbody > tr")[i]).addClass('invalid-row');
        //            });
        //            for (var i in msg.rows) {
        //                self.table_view.rows()[i].id = msg.rows[i];
        //                $($("#tbody > tr")[i]).removeClass('invalid-row');
        //            }
        //        }
        //    },
        //    error: function (XMLHttpRequest, textStatus, errorThrown) {
        //        alert.error(textStatus.toTitleCase() + ' - ' + errorThrown);
        //    }
        //});
    }
}

function ImprestTransaction(row, imprest_vm) {
    var self = this;
    self.name = ko.observable();
    self.wa_no = ko.observable();
    self.ref = ko.observable();
    self.date = ko.observable();
    self.description = ko.observable();
    self.exchange_rate = ko.observable();
    self.type = ko.observable();

    for (var k in row) {
        self[k] = ko.observable(row[k]);
    }
}