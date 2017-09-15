$(document).ready(function () {
    vm = new ReportHR(ko_data.obj_id);
    ko.applyBindings(vm);
    if (ko_data.ctx_data) {
        var mapping = {
            'report_tables': {
                create: function (options) {
                    var table_mapping = {
                        'table_details': {
                            create: function (options) {
                                var report_table_detail = ko.mapping.fromJS(options.data, {}, new ReportTableDetail());
                                return report_table_detail;
                            }
                        }
                    };
                    var report_table = ko.mapping.fromJS(options.data, table_mapping, new ReportTable());

                    return report_table;
                }
            }
        };
        ko.mapping.fromJS(ko_data.ctx_data, mapping, vm);

    }
});

function ReportTableDetail() {
    var self = this;
    self.id = ko.observable();
    self.field_name = ko.observable();
    self.field_description = ko.observable('');
    self.order = ko.observable();
    self.need_total = ko.observable();
}

function ReportTable(obj_id) {
    var self = this;
    self.id = ko.observable();
    self.title = ko.observable();
    self.table_details = ko.observableArray();
    self.to_remove = ko.observableArray();
    if (!obj_id) {
        self.table_details.push(new ReportTableDetail());
    }

    self.add_new_field = function () {
        self.table_details.push(new ReportTableDetail());
    };

    self.remove_field = function(field){
        self.table_details.remove(field);
        self.to_remove.push(field);
    };
}


function ReportHR(obj_id) {
    var self = this;
    self.id = ko.observable();
    self.name = ko.observable();
    self.code = ko.observable();
    self.template = ko.observable();
    self.for_employee_type = ko.observable();
    self.report_tables = ko.observableArray();
    self.to_remove = ko.observableArray();
    if (!obj_id) {
        self.report_tables.push(new ReportTable(obj_id));
    }

    self.add_new_table = function () {
        self.report_tables.push(new ReportTable(obj_id));
    };

    self.remove_table = function(table){
        self.report_tables.remove(table);
        self.to_remove.push(table);
        table.to_remove([]);
    };

    self.save_report = function () {
        var save_url = '/payroll/report-setting/';
        save_url = (obj_id ? save_url + 'edit/' + String(obj_id) + '/' : save_url + 'add/' );
        App.showProcessing();

        App.remotePost(save_url, ko.toJS(self), function (response) {
            App.hideProcessing();
            if(response.success){
                App.redirectTo('/payroll/report-setting/list/', 0);
            }else{
                App.notifyUser(response.message, 'error');
            }
        }, function () {
            App.hideProcessing();
            console.log(errorThrown);
        });
    };

}