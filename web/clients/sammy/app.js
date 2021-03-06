(function($) {

    var app = $.sammy('#main', function() {
        this.debug = true;

        this.get('#/', function(context) {

            this.load('/persons')
                .then(function(items) {
                    persons = JSON.parse(items)
                    $.each(persons, function(i, person) {
                        context.log(person.firstname, '-', person.lastname);
                    });
                });
        });

        this.post('#/persons', function (context) {

            var person = {
                firstname : $("#firstname").val(),
                lastname : $("#lastname").val(),
                gender: $('input:radio[name=gender]:checked').val() || "",
                phone: $("#phone").val()
            };

            DeleteErrors(['firstname', 'lastname', 'gender']);

            $.ajax({
                type: "POST",
                url: "/persons",
                data: JSON.stringify(person),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(resp){

                    if (resp.result == 'error') {
                        $("#server-message").text(resp.result);
                        $("#server-message").parent().addClass("alert-error");
                        ShowErrors(resp.message);
                    } else {
                        $("#server-message").text(JSON.stringify(resp.message));
                        $("#server-message").parent().addClass("alert-success");
                        ResetFields(['firstname', 'lastname', 'gender', 'phone']);
                    }
                },
                error: function(errMsg) {
                    $("#server-message").html(JSON.stringify(errMsg).replace(/\\n/g, ''));
                    $("#server-message").parent().addClass("alert-error");
                }
            });
            this.app.swap();
            this.redirect('#/');
        });

        var ShowErrors = function(msg) {
            for (var field in msg) {
                $("#" + field).parent().parent().addClass("error");
                $("#" + field).parent().parent().find("span.help-inline").text(msg[field]);

                if (field == 'gender') {
                    $('input:radio[name=gender]').parent().parent().addClass("error");
                    $('input:radio[name=gender]').parent().parent().find("span.help-inline").text(msg[field]);
                }
            }
        }

        var DeleteErrors = function(fields) {
            $("#server-message").text("");
            for (var field in fields) {
                $("#" + fields[field]).parent().parent().removeClass("error");
                $("#" + fields[field]).parent().parent().find("span.help-inline").text("");

                if (fields[field] == 'gender') {
                    $('input:radio[name=gender]').parent().parent().removeClass("error");
                    $('input:radio[name=gender]').parent().parent().find("span.help-inline").text("");
                }
            }
        }

        var ResetFields = function(fields) {
            for (var field in fields) {
                $("#" + fields[field]).val("");

                if (fields[field] == 'gender') {
                    $('input:radio[name=gender]').checked = false;
                }
            }
            $("#server-message").parent().removeClass("alert-error");
        }

    });

    $(function() {
        app.run('#/');
    });

})(jQuery);