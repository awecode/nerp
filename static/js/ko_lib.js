var inject_binding = function (allBindings, key, value) {
    //https://github.com/knockout/knockout/pull/932#issuecomment-26547528
    return {
        has: function (bindingKey) {
            return (bindingKey == key) || allBindings.has(bindingKey);
        },
        get: function (bindingKey) {
            var binding = allBindings.get(bindingKey);
            if (bindingKey == key) {
                binding = binding ? [].concat(binding, value) : value;
            }
            return binding;
        }
    };
}

ko.bindingHandlers.foundation = {
    init: function () {
    },
    init: function () {
        $(document).foundation();
    }

}

ko.bindingHandlers.selectize = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
        if (!allBindingsAccessor.has('optionsText'))
            allBindingsAccessor = inject_binding(allBindingsAccessor, 'optionsText', 'name');
        if (!allBindingsAccessor.has('optionsValue'))
            allBindingsAccessor = inject_binding(allBindingsAccessor, 'optionsValue', 'id');
        if (typeof allBindingsAccessor.get('optionsCaption') == 'undefined')
            allBindingsAccessor = inject_binding(allBindingsAccessor, 'optionsCaption', 'Choose...');

        ko.bindingHandlers.options.update(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext);

        var options = {
            valueField: allBindingsAccessor.get('optionsValue'),
            labelField: allBindingsAccessor.get('optionsText'),
            searchField: allBindingsAccessor.get('optionsText')
        }

        if (allBindingsAccessor.has('options')) {
            var passed_options = allBindingsAccessor.get('options')
            for (var attr_name in passed_options) {
                options[attr_name] = passed_options[attr_name];
            }
        }

        var $select;

        var apply_selectize = function () {
            $select = $(element).selectize(options)[0].selectize;

            if (typeof allBindingsAccessor.get('value') == 'function') {
                $select.addItem(allBindingsAccessor.get('value')());
                allBindingsAccessor.get('value').subscribe(function (new_val) {
                    $select.addItem(new_val);
                })
            }

            if (typeof allBindingsAccessor.get('selectedOptions') == 'function') {
                allBindingsAccessor.get('selectedOptions').subscribe(function (new_val) {
                    // Removing items which are not in new value
                    var values = $select.getValue();
                    var items_to_remove = [];
                    for (var k in values) {
                        if (new_val.indexOf(values[k]) == -1) {
                            items_to_remove.push(values[k]);
                        }
                    }

                    for (var k in items_to_remove) {
                        $select.removeItem(items_to_remove[k]);
                    }

                    for (var k in new_val) {
                        $select.addItem(new_val[k]);
                    }

                });
                var selected = allBindingsAccessor.get('selectedOptions')();
                for (var k in selected) {
                    $select.addItem(selected[k]);
                }
            }


            if (typeof init_selectize == 'function') {
                init_selectize($select);
            }

            if (typeof valueAccessor().subscribe == 'function') {
                valueAccessor().subscribe(function (changes) {
                    // To avoid having duplicate keys, all delete operations will go first
                    var addedItems = new Array();
                    changes.forEach(function (change) {
                        switch (change.status) {
                            case 'added':
                                addedItems.push(change.value);
                                break;
                            case 'deleted':
                                var itemId = change.value[options.valueField];
                                if (itemId != null) $select.removeOption(itemId);
                        }
                    });
                    addedItems.forEach(function (item) {
                        $select.addOption(item);
                    });

                }, null, "arrayChange");
            }
        };

        apply_selectize();

        $(document).on('reload-selectize', function () {
            $select.destroy();
            apply_selectize();
        });


    },
    update: function (element, valueAccessor, allBindingsAccessor) {
        if (allBindingsAccessor.has('object')) {
            var optionsValue = allBindingsAccessor.get('optionsValue') || 'id';
            var value_accessor = valueAccessor();
            var selected_obj = $.grep(value_accessor(), function (i) {
                if (typeof i[optionsValue] == 'function')
                    var id = i[optionsValue]
                else
                    var id = i[optionsValue]
                return id == allBindingsAccessor.get('value')();
            })[0];

            if (selected_obj) {
                allBindingsAccessor.get('object')(selected_obj);
            }
        }
    }
}


ko.bindingHandlers.autosize = {
    init: function (element, valueAccessor, allBindingsAccessor) {
        $(element).autosizeInput();
        var min_width = valueAccessor();
        if (min_width != 0) {
            if (!isNaN(min_width)) {
                min_width = min_width + 'em';
            }
            $(element).css({
                "min-width": min_width
            });
        }
    },
    update: function (element, valueAccessor, allBindingsAccessor) {
        $(element).data(Plugins.AutosizeInput.instanceKey).update();
    }
}

ko.bindingHandlers.localize = {
    init: function (element, valueAccessor, allBindingsAccessor) {

    },
    update: function (element, valueAccessor, allBindingsAccessor) {

        var lang_code = window.lang;

        if (allBindingsAccessor().editableText)
            var accessor = allBindingsAccessor().editableText;
        else if (allBindingsAccessor().value)
            var accessor = allBindingsAccessor().value;
        else if (allBindingsAccessor().text) {
            var original_text = allBindingsAccessor().text;
        }

        if (typeof accessor == 'function') {
            if (accessor() == null || typeof accessor() == 'undefined')
                return;
            var original_text = accessor();
        }

        var value = localize(original_text, lang_code, true);

        if (typeof accessor == 'function') {
            if (isAN(value)) {
                accessor(parseFloat(value));
            } else {
                accessor(value);
            }
        }

        var txt = localize(original_text, lang_code);

        $(element).html(txt);
        $(element).val(txt);

    }
}


ko.bindingHandlers.flash = {
    init: function (element) {
        $(element).hide().fadeIn('slow');
    }
};

ko.bindingHandlers.focus = {
    init: function (element, valueAccessor) {
        $(element).on('focus', valueAccessor());
    }
};

ko.bindingHandlers.max = {
    init: function (element, valueAccessor) {
        //$(element).attr('max', valueAccessor());
    },
    update: function (element, valueAccessor, allBindingsAccessor) {

        $(element).on('change', function (e) {
            if (allBindingsAccessor().hasOwnProperty('localize')) {
                var val = localize($(element).val(), window.lang, true)
            } else {
                val = $(element).val()
            }
            if (val > valueAccessor()) {
                $(element).val(null);
            }
        });
    }
};


ko.bindingHandlers.editableText = {
    init: function (element, valueAccessor) {
        $(element).attr('contenteditable', true);
        $(element).on('blur', function () {
            var observable = valueAccessor();
            if (typeof (observable) == 'function') {
                observable($(this).text());
            }
        });
    },
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        $(element).text(value);
    }
};

ko.bindingHandlers.numeric = {
    init: function (element, valueAccessor) {
        $(element).on('keydown', function (event) {

            // Allow: backspace, delete, tab, escape, and enter
            if (event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
                    // Allow: Ctrl combinations
                (event.ctrlKey === true) ||
                    //Allow decimal symbol (.)
                (event.keyCode === 190) ||
                    // Allow: home, end, left, right
                (event.keyCode >= 35 && event.keyCode <= 39)) {
                // let it happen, don't do anything
                return;
            }
            else {
                // Ensure that it is a number and stop the keypress
                if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                    event.preventDefault();
                }
            }
        });
    },
    update: function (element, valueAccessor) {
    }
};

//Custom Observable Extensions
ko.extenders.numeric = function (target, precision) {
    //create a writeable computed observable to intercept writes to our observable
    var result = ko.computed({
        read: target,  //always return the original observables value
        write: function (newValue) {
            var current = target(),
                roundingMultiplier = Math.pow(10, precision),
                newValueAsNum = isNaN(newValue) ? current : parseFloat(+newValue),
                valueToWrite = Math.round(newValueAsNum * roundingMultiplier) / roundingMultiplier;

            //only write if it changed
            if (valueToWrite !== current) {
                target(valueToWrite);
            } else {
                //if the rounded value is the same, but a different value was written, force a notification for the current field
                if (newValue !== current) {
                    target.notifySubscribers(valueToWrite);
                }
            }
        }
    });

    //initialize with current value to make sure it is rounded appropriately
    result(target());

    //return the new computed observable
    return result;
};

//Other useful KO-related functions
function setBinding(id, value) {
    var el = document.getElementById(id);
    if (el) {
        el.setAttribute('data-bind', value);
    }
}

ko.bindingHandlers.disable_content_editable = {
    init: function (element, valueAccessor, allBindingsAccessor, viewModel) {
    },
    update: function (element, valueAccessor, allBindingsAccessor, viewModel) {
        if (valueAccessor()) {
//            $(element).text('');
            $(element).removeAttr('contenteditable');
        }
        else {
            $(element).attr('contenteditable', true);
        }
    }
}

ko.bindingHandlers.readOnly = {
    update: function (element, valueAccessor) {
        var value = ko.utils.unwrapObservable(valueAccessor());
        if (value) {
            element.setAttribute("readOnly", true);
        } else {
            element.removeAttribute("readOnly");
        }
    }
}

ko.bindingHandlers.toggle = {
    init: function (element, valueAccessor) {
        ko.utils.registerEventHandler(element, 'click', function (event) {
            var toggleValue = valueAccessor();
            toggleValue(!toggleValue());
            if (event.preventDefault)
                event.preventDefault();
            event.returnValue = false;
        });
    },
    update: function (element, valueAccessor) {
    }
};