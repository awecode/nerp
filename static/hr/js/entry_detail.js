$(document).ready(function () {
    vm = new EntryDetail(ko_data);
    ko.applyBindings(vm);
    // $('.change-on-ready').trigger('change');
    // $('.dropdown-menu').click(function (event) {
    //     event.stopPropagation();
    // });
});

function EntryDetail(ed_data) {
    //debugger;
    var self = this;

    self.entry_id = ko.observable(ed_data.entry_id);
    self.entry_approved = ko.observable(ed_data.entry_approved);
    self.entry_transacted = ko.observable(ed_data.entry_transacted);

    self.approve_entry = function(){
        $.ajax({
                url: '/payroll/approve_entry/' + String(self.entry_id()),
                method: 'GET',
                dataType: 'json',
                // data: post_data,
                // async: true,
                success: function (response) {
                    console.log(response);
                    self.entry_approved(response.entry_approved);
                    
                },
                error: function(errorThrown){
                    console.log(errorThrown);
                    },
    //            self.budget_heads = ko.observableArray(data);
            });

    };
    self.transact = function(){
    	$.ajax({
                url: '/payroll/transact_entry/' + String(self.entry_id()),
                method: 'GET',
                dataType: 'json',
                // data: post_data,
                // async: true,
                success: function (response) {
                    console.log(response);
                    // self.entry_approved(response.entry_approved);
                    
                },
                error: function(errorThrown){
                    console.log(errorThrown);
                    },
    //            self.budget_heads = ko.observableArray(data);
        });

    };
};
