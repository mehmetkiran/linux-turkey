            var url = "{% url 'question:addFavorite' %}";
            var username = {{ request.user.id }};
            var questionID = {{ question.questionID }};
            $("#addFavorite").click(function () {
                $.ajax({
                    type: 'GET',
                    url: url,
                    data: {
                        'username': username,
                        'questionID': questionID
                    },
                    dataType: 'json',
                    success: function (data) {
                        if (data.status_) {
                            $('#favoriteQuestion').text(data.counter_);
                            $('#addFavorite').css({'background-color': '#dfaa63', 'color': 'white'});
                            toastr.success('Favori olarak eklendi.')
                        }
                        else {
                            $('#favoriteQuestion').text(data.counter_);
                            $('#addFavorite').css({'background-color': '#2f3239', 'color': 'white'});
                            toastr.success('Favorilerden kaldırıldı.')

                        }
                    }
                })
                ;
            })
        var yesVoteUrl = "{% url 'question:yesVote' %}";
        var username_ = {{ request.user.id }};
        var questionID_ = {{ question.questionID }};
        $("#upVote").click(function () {
            $.ajax({
                type: 'GET',
                url: yesVoteUrl,
                data: {
                    'username': username_,
                    'questionID_': questionID_
                },
                dataType: 'json',
                success: function (data) {
                    if (data.status_) {
                        $('#upVote').css({'background-color': '#338338', 'color': 'white'});

                    }
                }
            })
            ;
        })
