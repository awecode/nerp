$(document).ready(function () {
    vm = new ImprestJV(ko_data);
    ko.applyBindings(vm);
});


function ImprestJV(data) {
    var self = this;

    self.id = ko.observable();
    self.voucher_no = ko.observable();
    self.date = ko.observable();
    self.dr = ko.observable();
    self.cr = ko.observable();
    self.wa_no = ko.observable();
    self.amount_nrs = ko.observable();
    self.amount_usd = ko.observable();
    self.exchange_rate = ko.observable();

    self.dr_ledger = ko.observable();
    self.cr_ledger = ko.observable();

    self.dr_ledgers = ko.observableArray();
    self.cr_ledgers = ko.observableArray();

    for (var k in data.jv) {
        if (ko.isObservable(self[k]))
            self[k](data.jv[k]);
    }

    ko.utils.arrayForEach(data.dr_ledgers, function (obj) {
        self.dr_ledgers.push(obj);
    });

    ko.utils.arrayForEach(data.cr_ledgers, function (obj) {
        self.cr_ledgers.push(obj);
    });


    self.status = ko.observable('Loading...');

    self.save = function () {
        if (!self.date()) {
            alert.error('Date is required!');
            return false;
        }

        if (self.dr() == self.cr()) {
            alert.error('You can\'t debit and credit the same account.');
            return false;
        }
        return true;
    }

}