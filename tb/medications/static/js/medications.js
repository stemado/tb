$(function() {
            $(".publish").click(function() {
                $("input[name='status']").val("P");
                $("form").submit();
            });

            $(".draft").click(function() {
                $("input[name='status']").val("D");
                $("form").submit();
            });

            $(".preview").click(function() {
                $.ajax({
                    url: '/medications/preview/',
                    data: $("form").serialize(),
                    cache: false,
                    type: 'post',
                    beforeSend: function() {
                        $("#preview .modal-body").html("<div style='text-align: center; padding-top: 1em'><img src='/static/img/loading.gif'></div>");
                    },
                    success: function(data) {
                        $("#preview .modal-body").html(data);
                    }
                });
            });

            //Start Custom JS for View Status Button
            $("#showStatusHistory").on('click', (function() {
                    $("#comment-list").toggle();
                });
                //End Custom JS For View Status Button
                $("#comment").focus(function() {
                    $(this).attr("rows", "3");
                    $("#comment-helper").fadeIn();
                });

                $("#comment").blur(function() {
                    $(this).attr("rows", "1");
                    $("#comment-helper").fadeOut();
                });

            });


            check_notifications_medication();
        });