$(document).ready(function () {
    vm = new InspectionVM(ko_data, inspection_date);
    ko.applyBindings(vm);
    $('.change-on-ready').trigger('change');
});

function InspectionVM(data, date) {
    var self = this;
    self.report_no = ko.observable();
    self.id = ko.observable();
    self.date = ko.observable(date);

	self.table_view = new TableViewModel({rows: data}, InspectionRow);


    self.save = function (item, event) {
        $.ajax({
            type: "POST",
            url: '/inventory/save/inspection/',
            data: ko.toJSON(self),
            success: function (msg) {
                if (!self.report_no()) {
                    alert.error('Report No. is required!');
                    return false;
                }
                if (typeof (msg.error_message) != 'undefined') {
//                    $('#message').html(msg.error_message);
//                    self.msg();
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
}

function InspectionRow(row) {

    var self = this;
    // self.sn = ko.observable();
    self.id = ko.observable()
    self.total_dr_amount = ko.observable();
    self.rate = ko.observable();
    self.account_no =  ko.observable();
    self.inventory_classification_reference_no = ko.observable();
    self.item_name = ko.observable();
    self.unit = ko.observable();
    
    for (var k in row) {
        if (row[k] != null)
            self[k] = ko.observable(row[k]);
    }
    self.match_number = ko.observable();
    self.intialize = ko.observable(true);
    self.unmatch_number = ko.computed(function(){
        if ((self.total_dr_amount() - self.match_number()) != 0 && self.match_number() != ''){
            var unmatched = self.total_dr_amount() - self.match_number();
            if (unmatched < 0) {
                return unmatched * -1;
            }
            if (unmatched){
                return unmatched;
            } else {
                return '';
            };
        };
    });
    self.decrement = ko.computed(function(){
        if ((self.total_dr_amount() - self.match_number()) != 0 && self.match_number() != ''){
            var unmatched = self.total_dr_amount() - self.match_number();
            if (unmatched > 0){
                return unmatched;
            }
            return '';
        }
    });
    self.increment = ko.computed(function(){
        if ((self.total_dr_amount() - self.match_number()) != 0 && self.match_number() != ''){
            var unmatched = self.total_dr_amount() - self.match_number();
            if (unmatched < 0){
                return unmatched * -1;
            }
            return '';
        }
    });
    self.decrement_increment_price = ko.computed(function() {
        if (self.increment()) {
            return self.increment() * self.rate();
        }
        if (self.decrement()) {
            return self.decrement() * self.rate();
        }
    });
    self.good = ko.observable();
    self.bad = ko.observable();
    self.remarks = ko.observable();

    self.price = ko.computed(function() {
        return round2(self.total_dr_amount() * self.rate());
    });
}