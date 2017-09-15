/**
 * Created by wrufesh on 11/24/16.
 */
// Dependencies:
//     <link rel="stylesheet" href="{% static 'hr/css/plugins/toastr/toastr.css' %}">
//     <script src="{% static 'hr/js/plugins/toastr/toastr.js' %}"></script>
var notifyUser = function (message, type, layout) {
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": true,
        "progressBar": true,
        "positionClass": "toast-bottom-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "300",
        "hideDuration": "1000",
        "timeOut": "20000",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };
    if (type == 'success') {
        toastr.success(message, 'Successful');
    }
    if (type == 'error') {
        toastr.error(message, 'Error');
    }
    if (type == 'warning') {
        toastr.warning(message, 'Warning');
    }
};
