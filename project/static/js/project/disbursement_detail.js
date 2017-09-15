$(document).ready(function () {
    vm = new DisbursementDetailViewModel(ko_data);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function DisbursementDetailViewModel(data) {

    var self = this;
    self.id = ko.observable();
    self.aid = ko.observable();

    self.disbursement_methods = ko.observableArray([
		{id: 'reimbursement', name: 'Reimbursement'},
		{id: 'replenishment', name: 'Replenishment'},
		{id: 'liquidation', name: 'Liquidation'},
		{id: 'direct_payment', name: 'Direct Payment'},
	]);


    self.table_view = new TableViewModel({rows: data.rows}, DisbursementParticularRow);

    for (var k in data)
        self[k] = ko.observable(data[k]);

    self.save = function (item, event) {
        if (!self.aid()) {
            alert.error('Aid is required!');
            return false;
        }
        $.ajax({
            type: "POST",
            url: '/project/disbursement_detail/save/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (typeof (msg.error_message) != 'undefined') {
                    alert.error(msg.error_message);
                    self.status('errorlist');
                }
                else {
                    alert.success('Saved!');
                    self.table_view.deleted_rows([]);
                    if (msg.id)
                        self.id(msg.id);
                    $("#tbody > tr").each(function (i) {
                        $($("#tbody > tr")[i]).addClass('invalid-row');
                    });
                    for (var i in msg.rows) {
                        self.table_view.rows()[i].id = msg.rows[i];
                        $($("#tbody > tr")[i]).removeClass('invalid-row');
                    }
                }
            }
//            error: function(XMLHttpRequest, textStatus, errorThrown) {
//                $('#message').html(XMLHttpRequest.responseText.message);
//            }
        });
    }

    self.id.subscribe(function (id) {
        history.pushState(id, id, window.location.href + id + '/');
    });

}

function DisbursementParticularRow(row) {
    var self = this;
    self.id = ko.observable();
    self.expense_category_id = ko.observable();
    self.request_nrs = ko.observable();
    self.request_usd = ko.observable();
    self.request_sdr = ko.observable();
    self.response_nrs = ko.observable();
    self.response_usd = ko.observable();
    self.response_sdr = ko.observable();

    self.with_held_nrs = function() {
        return r2z(self.response_nrs() - self.request_nrs());
    };

    self.with_held_usd = function() {
        return r2z(self.response_usd() - self.request_usd());
    };

    self.with_held_sdr = function() {
        return r2z(self.response_sdr() - self.request_sdr());
    };

    for (var k in row) {
        if (ko.isObservable(self[k]))
            self[k](row[k]);
    }
}