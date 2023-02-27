$(document).ready(function() {
    console.log("Ready!");
    var origin = window.location.origin;

    // Manage edit-name-button text
    $('#edit-name').on('hide.bs.collapse', function() {
        $('a.edit-name-button').html("Edit");
    });
    $('#edit-name').on('show.bs.collapse', function() {
        $('a.edit-name-button').html("Close");
    });

    // Change the time period of Goals for the comparison data
    $(".select_period").on("change", function(){
        var value = this.value;
        var url_value = window.location.href.split("/");
        var goal_id = url_value[url_value.length - 1];
        $.ajax({
                url: origin + '/goals/get_goal_comparision',
                type: 'post',
                data: {"duration":value, "goal_id":goal_id},
                success: function(result){
                    $("#goal_returns").html("");
                    $("#nifty_returns").html("");
                    $("#goal_returns").text(parseInt(result.goal_returns).toLocaleString());
                    $("#nifty_returns").text(parseInt(result.nifty_returns).toLocaleString());
        }});
    });


    // Validate password
    $("#submit-button").click(function(event) {
        var pass = $("#pass").val();
        var confirmation = $("#confirmation").val();
        var regex = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,32}$/;
        if (!pass.match(regex)) {
            event.preventDefault();
            alert("Password must be 8-32 characters long and contain at least one number and one special character.");
        } else if (pass != confirmation) {
            event.preventDefault();
            alert("Password and confirmation do not match. Please re-enter them and try again.");
        }
    });


    // Resend validation email
    $("a.verify-button").click(function(event) {
        event.preventDefault();
        $(this).html("Sending email");
        $(this).css('pointer-events', 'none');
        $(this).addClass("text-muted");
        $.post("/verify", $("form.verify-form").serialize())
            .done(function(response) {
                console.log(response);
                $("a.verify-button").html("Email sent");
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Add note
    $("button.add-note-button").click(function() {
        $.post("/add_note", $("form.add-note-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Delete note
    $("button.delete-note-button").click(function() {
        $.post("/delete_note", $("form.delete-note-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Send message
    $("button.send-message-button").click(function() {
        $.post("/send_message", $("form.send-message-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Delete message
    $("button.delete-message-button").click(function() {
        $.post("/delete_message", $("form.delete-message-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Hide sent message
    $("button.hide-sent-message-button").click(function() {
        $.post("/hide_sent_message", $("form.hide-sent-message-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Change Name
    $("button.change-name-button").click(function() {
        $.post("/change_name", $("form.change-name-form").serialize())
            .done(function(response) {
                console.log(response);
                location.reload(true);
            })
            .fail(function(response) {
                console.log(response)
            });
    });


    // Delete account
    $("button.second-delete").click(function(event) {
        if (confirm("Are you sure you want to delete your account?")) {
            console.log("Deleting account");
            $.post("/delete_account", $("form.delete-account-form").serialize())
                .done(function(response) {
                    console.log(response);
                    location.href = "/";
                })
                .fail(function(response) {
                    console.log(response)
                });
        } else {
            event.preventDefault();
            $("div.delete-account").collapse("hide");
        }
    });


    // Toggle delete button
    $("div.delete-account").on('hide.bs.collapse', function() {
        $("div.account-card").removeClass("border-danger");
        $("div.account-card").addClass("border-secondary");
        $("p.delete-warning").removeClass("text-danger");
        $("button.first-delete").html("Delete account");
    });
    $("div.delete-account").on('show.bs.collapse', function() {
        $("div.account-card").removeClass("border-secondary");
        $("div.account-card").addClass("border-danger");
        $("p.delete-warning").addClass("text-danger");
        $("button.first-delete").html("Hide the red button!");
    });



////////////////////////////////////////////////////////
//var trace1 = {
//  x: "{{ month }}",
//  y: "{{ portfolio_value }}",
//  mode: 'lines',
//  name: 'Solid',
//  line: {
//    dash: 'solid',
//    width: 4
//  }
//};
//
//var trace2 = {
//  x: "{{ month }}",
//  y: "{{ predicted_value }}",
//  mode: 'lines',
//  name: 'dashdot',
//  line: {
//    dash: 'dashdot',
//    width: 4
//  }
//};
//
//var trace3 = {
//  x: "{{ month }}",
//  y: "{{ nifty_value }}",
//  mode: 'lines',
//  name: 'Solid',
//  line: {
//    dash: 'solid',
//    width: 4
//  }
//};
//
//var trace4 = {
//  x: [1, 2, 3, 4, 5],
//  y: [16, 18, 17, 18, 16],
//  mode: 'lines',
//  name: 'dot',
//  line: {
//    dash: 'dot',
//    width: 4
//  }
//};
//
//var data = [trace1, trace2, trace3, trace4];
//
//var layout = {
//  title: 'Custom Range',
//  xaxis: {
//    range: ['01-10-2020', '02-10-2023'],
//    type: 'date'
//  },
//  yaxis: {
//    autorange: true,
//    range: [0, 2000000],
//    type: 'linear'
//  }
//};
////
////var layout = {
////  title: 'Line Dash',
////  xaxis: {
////    range: "{{ month }}",
////    autorange: false
////  },
////  yaxis: {
////    range: [0, 2000000],
////    autorange: false
////  },
////  legend: {
////    y: 0.5,
////    traceorder: 'reversed',
////    font: {
////      size: 16
////    }
////  }
////};
//
//Plotly.newPlot('graph_performance', data, layout);

//var trace1 = {
//    x: "{{ month }}",
//    y: "{{ portfolio_value }}",mode: 'lines',
//    type: 'scatter'
//  };
//
//var trace2 = {
//    x: ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
//    y: [1, 2, 4],mode: 'lines',
//    type: 'scatter'
//};
//
//var data = [trace1, trace2];
//
//
//Plotly.newPlot('graph_performance', data);
});
///////////////////////////////////////////////////////////////


